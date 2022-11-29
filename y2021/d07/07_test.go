package d07_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib/testutil"
	"github.com/sumnerevans/advent-of-code/y2021/d07"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day07(t *testing.T) {
	log, sample, actual := testutil.SetupTest(t, inputs, "07")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day07 := &d07.Day07{}
				err := day07.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day07.Part1(log)

				assert.EqualValues(t, 37, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day07 := &d07.Day07{}
			err := day07.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day07.Part1(log)
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 345035, output)
		})
	})
	if !ok {
		t.FailNow()
		return
	}

	t.Run("Part 2", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day07 := &d07.Day07{}
				err := day07.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day07.Part2(log)

				assert.EqualValues(t, 168, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day07 := &d07.Day07{}
			err := day07.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day07.Part2(log)
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 97038163, output)
		})
	})
}
