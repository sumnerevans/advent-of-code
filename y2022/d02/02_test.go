package d02_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y2022/d02"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day02(t *testing.T) {
	log, sample, actual := lib.SetupTest(t, inputs, "02")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day02 := &d02.Day02{}
				err := day02.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day02.Part1(log)

				assert.EqualValues(t, 15, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day02 := &d02.Day02{}
			err := day02.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day02.Part1(log)
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.NotEqualValues(t, 9872, output)
			assert.EqualValues(t, 14531, output)
		})
	})
	if !ok {
		t.FailNow()
		return
	}

	t.Run("Part 2", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day02 := &d02.Day02{}
				err := day02.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day02.Part2(log)

				assert.EqualValues(t, 12, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day02 := &d02.Day02{}
			err := day02.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day02.Part2(log)
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 11258, output)
		})
	})
}
