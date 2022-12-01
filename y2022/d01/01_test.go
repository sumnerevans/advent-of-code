package d01_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib/testutil"
	"github.com/sumnerevans/advent-of-code/y2022/d01"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day01(t *testing.T) {
	log, sample, actual := testutil.SetupTest(t, inputs, "01")

	ok := t.Run("Part 1", func(t *testing.T) {
		day01 := &d01.Day01{}
		if day01.SkipFirst() {
			return
		}

		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day01 := &d01.Day01{}
				err := day01.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day01.Part1(log)

				assert.EqualValues(t, 24000, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day01 := &d01.Day01{}
			err := day01.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day01.Part1(log)
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 66616, output)
		})
	})
	if !ok {
		t.FailNow()
		return
	}

	t.Run("Part 2", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day01 := &d01.Day01{}
				err := day01.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day01.Part2(log)

				assert.EqualValues(t, 45000, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day01 := &d01.Day01{}
			err := day01.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day01.Part2(log)
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 199172, output)
		})
	})
}
