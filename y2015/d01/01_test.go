package d01_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y2015/d01"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day01(t *testing.T) {
	_, samples, actual := lib.SetupTest(t, inputs, "01")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []int64{
					0,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day01 := &d01.Day01{}
						err := day01.LoadInput(sample)
						assert.NoError(t, err)
						output := day01.Part1()

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
			day01 := &d01.Day01{}
			err := day01.LoadInput(actual)
			assert.NoError(t, err)
			output := day01.Part1()
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 1:\n%v\n\n", output)

			fmt.Print("\n\n=================================\n")

			require.NotEqualValues(t, 0, output)
			assert.EqualValues(t, 138, output)

			lib.Submit(t, 2015, 1, 1, output)
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
					-1,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day01 := &d01.Day01{}
						err := day01.LoadInput(sample)
						assert.NoError(t, err)
						output := day01.Part2()

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
			day01 := &d01.Day01{}
			err := day01.LoadInput(actual)
			assert.NoError(t, err)
			output := day01.Part2()
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.NotEqualValues(t, 0, output)

			assert.EqualValues(t, -1, output)
		})
	})
}
