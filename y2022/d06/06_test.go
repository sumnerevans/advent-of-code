package d06_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y2022/d06"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day06(t *testing.T) {
	_, samples, actual := lib.SetupTest(t, inputs, "06")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []int64{
					7,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day06 := &d06.Day06{}
						err := day06.LoadInput(sample)
						assert.NoError(t, err)
						output := day06.Part1()

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
			day06 := &d06.Day06{}
			err := day06.LoadInput(actual)
			assert.NoError(t, err)
			output := day06.Part1()
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.NotEqualValues(t, 0, output)

			assert.EqualValues(t, 1275, output)
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
					19,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day06 := &d06.Day06{}
						err := day06.LoadInput(sample)
						assert.NoError(t, err)
						output := day06.Part2()

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
			day06 := &d06.Day06{}
			err := day06.LoadInput(actual)
			assert.NoError(t, err)
			output := day06.Part2()
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.NotEqualValues(t, 0, output)

			assert.EqualValues(t, 3605, output)
		})
	})
}
