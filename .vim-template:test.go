package dDAYNUM_test

import (
	"os"
	"testing"
	"time"

	"github.com/rs/zerolog"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/sumnerevans/advent-of-code/util"
	"github.com/sumnerevans/advent-of-code/y2021/dDAYNUM"
)

const TestInput = `

`

func SetupTest(t *testing.T) (*dDAYNUM.DayDAYNUM, *zerolog.Logger) {
	output := zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.RFC3339}
	log := zerolog.New(output).With().Timestamp().Logger()

	dayDAYNUM := dDAYNUM.DayDAYNUM{}
	err := dayDAYNUM.LoadInput(&log, util.Lines(TestInput))
	require.NoError(t, err)
	return &dayDAYNUM, &log
}

func Test_Part1(t *testing.T) {
	dayDAYNUM, log := SetupTest(t)
	require.EqualValues(t, 7, dayDAYNUM.Part1(log))
}

func Test_Part2(t *testing.T) {
	dayDAYNUM, log := SetupTest(t)
	require.EqualValues(t, 5, dayDAYNUM.Part2(log))
}
