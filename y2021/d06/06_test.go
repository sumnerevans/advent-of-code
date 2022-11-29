package d06_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib/testutil"
	"github.com/sumnerevans/advent-of-code/y2021/d06"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day06(t *testing.T) {
	log, sample, actual := testutil.SetupTest(t, inputs, "06")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day06 := &d06.Day06{}
				err := day06.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day06.Part1(log)

				assert.EqualValues(t, 5934, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day06 := &d06.Day06{}
			err := day06.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day06.Part1(log)
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 372984, output)
		})
	})
	if !ok {
		t.FailNow()
		return
	}

	t.Run("Part 2", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day06 := &d06.Day06{}
				err := day06.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day06.Part2(log)

				assert.EqualValues(t, 26984457539, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day06 := &d06.Day06{}
			err := day06.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day06.Part2(log)
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 1681503251694, output)
		})
	})
}
