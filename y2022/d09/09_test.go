package d09_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y2022/d09"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day09(t *testing.T) {
	_, samples, actual := lib.SetupTest(t, inputs, "09")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []int64{
					13,
				}

				for i, sample := range samples {
					if i >= len(EXPECTED) {
						break
					}

					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day09 := &d09.Day09{}
						err := day09.LoadInput(sample)
						assert.NoError(t, err)
						output := day09.Part1()

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
			day09 := &d09.Day09{}
			err := day09.LoadInput(actual)
			assert.NoError(t, err)
			output := day09.Part1()
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			require.NotEqualValues(t, 0, output)

			assert.EqualValues(t, 5735, output)

			// lib.Submit(t, 2022, 9, 1, output)
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
					1,
					36,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day09 := &d09.Day09{}
						err := day09.LoadInput(sample)
						assert.NoError(t, err)
						output := day09.Part2()

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
			day09 := &d09.Day09{}
			err := day09.LoadInput(actual)
			assert.NoError(t, err)
			output := day09.Part2()
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			require.NotEqualValues(t, 0, output)

			assert.EqualValues(t, 2478, output)

			// lib.Submit(t, 2022, 9, 2, output)
		})
	})
}
