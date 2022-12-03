package lib

import (
	"embed"
	"fmt"
	"os"
	"regexp"
	"testing"
	"time"

	"github.com/rs/zerolog"
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
