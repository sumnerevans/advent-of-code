package d01_test

import (
	"embed"
	"fmt"
	"os"
	"testing"
	"time"

	"github.com/rs/zerolog"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/sumnerevans/advent-of-code/util"
	"github.com/sumnerevans/advent-of-code/y2021/d01"
)

//go:embed *.txt
var inputs embed.FS

func SetupTest(t *testing.T) (log *zerolog.Logger, sample []string, actual []string) {
	output := zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.RFC3339}
	logger := zerolog.New(output).With().Timestamp().Logger()
	log = &logger

	if testFile, err := inputs.ReadFile("01.test.txt"); err != nil {
		log.Warn().Msg("No test file found")
	} else {
		sample = util.Lines(string(testFile))
	}

	if actualInput, err := inputs.ReadFile("01.txt"); err != nil {
		t.Fatalf("Unable to open input file")
	} else {
		actual = util.Lines(string(actualInput))
	}
	return
}

func Test_Part1(t *testing.T) {
	log, sample, actual := SetupTest(t)

	if len(sample) > 0 {
		ok := t.Run("Test case", func(t *testing.T) {
			day01 := &d01.Day01{}
			err := day01.LoadInput(log, sample)
			assert.NoError(t, err)
			output := day01.Part1(log)

			assert.EqualValues(t, 7, output)
		})
		require.True(t, ok)
	}

	t.Run("Actual input", func(t *testing.T) {
		day01 := &d01.Day01{}
		err := day01.LoadInput(log, actual)
		assert.NoError(t, err)
		output := day01.Part1(log)
		fmt.Printf("\nPart 1:\n%d\n", output)

		assert.EqualValues(t, 1502, output)
	})
}

func Test_Part2(t *testing.T) {
	log, sample, actual := SetupTest(t)

	if len(sample) > 0 {
		ok := t.Run("Test case", func(t *testing.T) {
			day01 := &d01.Day01{}
			err := day01.LoadInput(log, sample)
			assert.NoError(t, err)
			output := day01.Part2(log)

			assert.EqualValues(t, 5, output)
		})
		require.True(t, ok)
	}

	t.Run("Actual input", func(t *testing.T) {
		day01 := &d01.Day01{}
		err := day01.LoadInput(log, actual)
		assert.NoError(t, err)
		output := day01.Part2(log)
		fmt.Printf("\nPart 2:\n%d\n", output)

		assert.EqualValues(t, 1538, output)
	})
}
