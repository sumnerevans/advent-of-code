package d07_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y2022/d07"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day07(t *testing.T) {
	_, samples, actual := lib.SetupTest(t, inputs, "07")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []int64{
					95437,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day07 := &d07.Day07{}
						err := day07.LoadInput(sample)
						assert.NoError(t, err)
						output := day07.Part1()

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
			day07 := &d07.Day07{}
			err := day07.LoadInput(actual)
			assert.NoError(t, err)
			output := day07.Part1()
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.NotEqualValues(t, 0, output)

			assert.EqualValues(t, 1989474, output)
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
					24933642,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day07 := &d07.Day07{}
						err := day07.LoadInput(sample)
						assert.NoError(t, err)
						output := day07.Part2()

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
			day07 := &d07.Day07{}
			err := day07.LoadInput(actual)
			assert.NoError(t, err)
			output := day07.Part2()
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.NotEqualValues(t, 0, output)

			assert.EqualValues(t, 1111607, output)
		})
	})
}
