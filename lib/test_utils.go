package lib

import (
	"embed"
	"encoding/json"
	"fmt"
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
	"github.com/stretchr/testify/assert"
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

const (
	ColorReset string = "\033[0m"

	ColorRed    string = "\033[31m"
	ColorGreen  string = "\033[32m"
	ColorYellow string = "\033[33m"
)

func Submit(t *testing.T, year, day, part int, answer any) (accepted bool) {
	projectRoot, found := os.LookupEnv("PROJECT_ROOT")
	assert.True(t, found)
	sessionTokenBytes, err := ioutil.ReadFile(projectRoot + "/.session_token")
	assert.NoError(t, err)
	sessionToken := strings.TrimSpace(string(sessionTokenBytes))

	var answerBytes []byte
	if str, ok := answer.(string); ok {
		answerBytes = []byte(str)
	} else {
		answerBytes, err = json.Marshal(answer)
		assert.NoError(t, err)
	}

	uri := fmt.Sprintf("https://adventofcode.com/%d/day/%d/answer", year, day)

	form := url.Values{}
	form.Add("level", strconv.Itoa(part))
	form.Add("answer", string(answerBytes))

	req, err := http.NewRequest("POST", uri, strings.NewReader(form.Encode()))
	assert.NoError(t, err)
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
	req.AddCookie(&http.Cookie{Name: "session", Value: sessionToken})

	resp, err := http.DefaultClient.Do(req)
	assert.NoError(t, err)
	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromResponse(resp)
	assert.NoError(t, err)

	answerText := doc.Find("article").Text()
	if strings.Contains(answerText, "That's not the right answer") || strings.Contains(answerText, "You gave an answer too recently") {
		fmt.Print(ColorRed)
	} else if strings.Contains(answerText, "Did you already complete it") {
		fmt.Print(ColorYellow)
	} else if strings.Contains(answerText, "That's the right answer") {
		fmt.Print(ColorGreen)
		accepted = true
	}
	lineLen := 0
	for _, word := range strings.Fields(strings.TrimSpace(answerText)) {
		if lineLen+len(word) > 80 {
			lineLen = 0
			fmt.Print("\n")
		}

		if lineLen > 0 {
			fmt.Print(" ")
		}

		fmt.Print(word)
		lineLen += len(word)
	}
	fmt.Printf("%s\n", ColorReset)
	return
}
