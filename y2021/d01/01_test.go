package d01_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/sumnerevans/advent-of-code/util"
	"github.com/sumnerevans/advent-of-code/y2021/d01"
)

//go:embed *.txt
var inputs embed.FS

func Test_Part1(t *testing.T) {
	log, sample, actual := util.SetupTest(t, inputs, "01")

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
	log, sample, actual := util.SetupTest(t, inputs, "01")

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
