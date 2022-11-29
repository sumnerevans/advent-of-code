package testutil

import (
	"embed"
	"fmt"
	"os"
	"testing"
	"time"

	"github.com/rs/zerolog"

	"github.com/sumnerevans/advent-of-code/lib/strs"
)

func SetupTest(t *testing.T, inputs embed.FS, dayNum string) (log *zerolog.Logger, sample []string, actual []string) {
	output := zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.RFC3339}
	logger := zerolog.New(output).With().Timestamp().Logger()
	log = &logger

	if testFile, err := inputs.ReadFile(fmt.Sprintf("%s.test.txt", dayNum)); err != nil {
		log.Warn().Msg("No test file found")
	} else if len(testFile) > 0 {
		sample = strs.Lines(string(testFile))
	}

	if actualInput, err := inputs.ReadFile(fmt.Sprintf("%s.txt", dayNum)); err != nil {
		t.Fatalf("Unable to open input file")
	} else {
		actual = strs.Lines(string(actualInput))
	}
	return
}