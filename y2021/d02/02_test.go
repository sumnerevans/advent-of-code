package d02_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/sumnerevans/advent-of-code/util"
	"github.com/sumnerevans/advent-of-code/y2021/d02"
)

//go:embed *.txt
var inputs embed.FS

func Test_Part1(t *testing.T) {
	log, sample, actual := util.SetupTest(t, inputs, "02")

	if len(sample) > 0 {
		ok := t.Run("Test case", func(t *testing.T) {
			day02 := &d02.Day02{}
			err := day02.LoadInput(log, sample)
			assert.NoError(t, err)
			output := day02.Part1(log)

			assert.EqualValues(t, 150, output)
		})
		require.True(t, ok)
	}

	t.Run("Actual input", func(t *testing.T) {
		day02 := &d02.Day02{}
		err := day02.LoadInput(log, actual)
		assert.NoError(t, err)
		output := day02.Part1(log)
		fmt.Printf("\nPart 1:\n%d\n", output)

		assert.EqualValues(t, 2073315, output)
	})
}

func Test_Part2(t *testing.T) {
	log, sample, actual := util.SetupTest(t, inputs, "02")

	if len(sample) > 0 {
		ok := t.Run("Test case", func(t *testing.T) {
			day02 := &d02.Day02{}
			err := day02.LoadInput(log, sample)
			assert.NoError(t, err)
			output := day02.Part2(log)

			assert.EqualValues(t, 900, output)
		})
		require.True(t, ok)
	}

	t.Run("Actual input", func(t *testing.T) {
		day02 := &d02.Day02{}
		err := day02.LoadInput(log, actual)
		assert.NoError(t, err)
		output := day02.Part2(log)
		fmt.Printf("\nPart 2:\n%d\n", output)

		assert.EqualValues(t, 1840311528, output)
	})
}
