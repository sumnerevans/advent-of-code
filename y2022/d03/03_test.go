package d03_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y2022/d03"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day03(t *testing.T) {
	log, samples, actual := lib.SetupTest(t, inputs, "03")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []int64{
					157,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i), func(t *testing.T) {
						day03 := &d03.Day03{}
						err := day03.LoadInput(log, sample)
						assert.NoError(t, err)
						output := day03.Part1(log)

						assert.EqualValues(t, EXPECTED[i], output)
					})
				}
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day03 := &d03.Day03{}
			err := day03.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day03.Part1(log)
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.NotEqualValues(t, 0, output)

			assert.EqualValues(t, 8153, output)
		})
	})
	if !ok {
		t.FailNow()
		return
	}

	t.Run("Part 2", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []int64{
					70,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i), func(t *testing.T) {
						day03 := &d03.Day03{}
						err := day03.LoadInput(log, sample)
						assert.NoError(t, err)
						output := day03.Part2(log)

						assert.EqualValues(t, EXPECTED[i], output)
					})
				}
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day03 := &d03.Day03{}
			err := day03.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day03.Part2(log)
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.NotEqualValues(t, 0, output)

			assert.EqualValues(t, 2342, output)
		})
	})
}
