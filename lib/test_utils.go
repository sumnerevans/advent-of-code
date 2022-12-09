package lib

import (
	"bytes"
	"embed"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"strconv"
	"strings"
	"testing"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/rs/zerolog"
	"github.com/stretchr/testify/require"
)

var sampleFileRegex = regexp.MustCompile(`^\d+\.test\.\d+\.txt$`)

func SetupTest(t *testing.T, inputs embed.FS, dayNum string) (log *zerolog.Logger, samples [][]string, actual []string) {
	output := zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.RFC3339}
	logger := zerolog.New(output).With().Timestamp().Logger()
	log = &logger

	xs, err := inputs.ReadDir(".")
	if err != nil {
		t.Fatal(err)
	}
	for _, x := range xs {
		if !sampleFileRegex.MatchString(x.Name()) {
			continue
		}

		if testFile, err := inputs.ReadFile(x.Name()); err != nil {
			log.Warn().Msg("No test file found")
		} else if len(testFile) > 0 {
			samples = append(samples, Lines(string(testFile)))
		}
	}

	if actualInput, err := inputs.ReadFile(fmt.Sprintf("%s.txt", dayNum)); err != nil {
		t.Error("Unable to open input file")
	} else {
		actual = Lines(string(actualInput))
	}
	return
}

type Color string

const (
	ColorReset Color = "\033[0m"

	ColorRed    Color = "\033[31m"
	ColorGreen  Color = "\033[32m"
	ColorYellow Color = "\033[33m"
)

func ColorString(msg string, color Color) string {
	return fmt.Sprintf("%s%s%s", color, msg, ColorReset)
}

func ReadOutput(level int) (string, error) {
	outputFile, err := os.OpenFile(fmt.Sprintf("output.%d.txt", level), os.O_RDONLY, 0644)
	if err != nil {
		return "", err
	}
	defer outputFile.Close()

	existingOutput, err := io.ReadAll(outputFile)
	if err != nil {
		return "", err
	}

	if len(existingOutput) == 0 {
		return "", fmt.Errorf("No data in output file")
	}
	return string(bytes.TrimSpace(existingOutput)), nil
}

type IncorrectSubmissions struct {
	Previous []string `json:"previous"`
}

func ReadIncorrect(level int) ([]string, error) {
	incorrectsJSON, err := os.ReadFile(fmt.Sprintf("incorrect.%d.txt", level))
	if err != nil {
		return nil, nil
	}

	incorrectSubmissions := IncorrectSubmissions{}
	err = json.Unmarshal(incorrectsJSON, &incorrectSubmissions)
	if err != nil {
		return nil, err
	}
	return incorrectSubmissions.Previous, nil
}

func WriteIncorrect(level int, output string) error {
	incorrectSubmissions, err := ReadIncorrect(level)
	if err != nil {
		return err
	}

	incorrectSubmissions = append(incorrectSubmissions, output)

	return os.WriteFile(
		fmt.Sprintf("incorrect.%d.txt", level),
		[]byte(AsJSON(IncorrectSubmissions{Previous: incorrectSubmissions})),
		0644)
}

type SubmissionResult int

const (
	SubmissionIncorrect SubmissionResult = iota
	SubmissionTooSoon
	SubmissionAlreadyComplete
	SubmissionCorrect
)

func Submit(t *testing.T, year, day, part int, answer any) (result SubmissionResult) {
	projectRoot, found := os.LookupEnv("PROJECT_ROOT")
	require.True(t, found)
	sessionTokenBytes, err := ioutil.ReadFile(projectRoot + "/.session_token")
	require.NoError(t, err)
	sessionToken := strings.TrimSpace(string(sessionTokenBytes))

	var answerBytes []byte
	if str, ok := answer.(string); ok {
		answerBytes = []byte(str)
	} else {
		answerBytes, err = json.Marshal(answer)
		require.NoError(t, err)
	}

	uri := fmt.Sprintf("https://adventofcode.com/%d/day/%d/answer", year, day)

	form := url.Values{}
	form.Add("level", strconv.Itoa(part))
	form.Add("answer", string(answerBytes))

	req, err := http.NewRequest("POST", uri, strings.NewReader(form.Encode()))
	require.NoError(t, err)
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
	req.AddCookie(&http.Cookie{Name: "session", Value: sessionToken})

	resp, err := http.DefaultClient.Do(req)
	require.NoError(t, err)
	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromResponse(resp)
	require.NoError(t, err)

	answerText := doc.Find("article").Text()
	var wrappedAnswer strings.Builder
	lineLen := 0
	for _, word := range strings.Fields(strings.TrimSpace(answerText)) {
		if lineLen+len(word) > 80 {
			lineLen = 0
			wrappedAnswer.WriteString("\n")
		}

		if lineLen > 0 {
			wrappedAnswer.WriteString(" ")
		}

		wrappedAnswer.WriteString(word)
		lineLen += len(word)
	}

	result = SubmissionIncorrect
	switch {
	case strings.Contains(answerText, "That's not the right answer"):
		t.Log(ColorString(wrappedAnswer.String(), ColorRed))
		return SubmissionIncorrect

	case strings.Contains(answerText, "You gave an answer too recently"):
		t.Log(ColorString(wrappedAnswer.String(), ColorRed))
		return SubmissionTooSoon

	case strings.Contains(answerText, "Did you already complete it"):
		t.Log(ColorString(wrappedAnswer.String(), ColorYellow))
		return SubmissionAlreadyComplete

	case strings.Contains(answerText, "That's the right answer"):
		t.Log(ColorString(wrappedAnswer.String(), ColorGreen))
		return SubmissionCorrect
	default:
		t.Log(ColorString(wrappedAnswer.String(), ColorRed))
		panic("no idea what the output means")
	}
}
