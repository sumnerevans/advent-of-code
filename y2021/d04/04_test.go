package d04_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib/testutil"
	"github.com/sumnerevans/advent-of-code/y2021/d04"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day04(t *testing.T) {
	log, sample, actual := testutil.SetupTest(t, inputs, "04")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day04 := &d04.Day04{}
				err := day04.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day04.Part1(log)

				assert.EqualValues(t, 4512, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day04 := &d04.Day04{}
			err := day04.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day04.Part1(log)
			fmt.Print("=================================\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 60368, output)
		})
	})
	if !ok {
		t.FailNow()
		return
	}

	t.Run("Part 2", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day04 := &d04.Day04{}
				err := day04.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day04.Part2(log)

				assert.EqualValues(t, 1924, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day04 := &d04.Day04{}
			err := day04.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day04.Part2(log)
			fmt.Print("=================================\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 17435, output)
		})
	})
}
