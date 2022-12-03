package d02_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y2021/d02"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day02(t *testing.T) {
	log, samples, actual := lib.SetupTest(t, inputs, "02")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []int64{
					150,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day02 := &d02.Day02{}
						err := day02.LoadInput(log, sample)
						assert.NoError(t, err)
						output := day02.Part1(log)

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
			day02 := &d02.Day02{}
			err := day02.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day02.Part1(log)
			fmt.Print("=================================\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 2073315, output)
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
					900,
				}

				for i, sample := range samples {
					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day02 := &d02.Day02{}
						err := day02.LoadInput(log, sample)
						assert.NoError(t, err)
						output := day02.Part2(log)

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
			day02 := &d02.Day02{}
			err := day02.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day02.Part2(log)
			fmt.Print("=================================\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, 1840311528, output)
		})
	})
}
