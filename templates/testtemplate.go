package d%DAYNUM%_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y%YEARNUM%/d%DAYNUM%"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day%DAYNUM%(t *testing.T) {
	_, samples, actual := lib.SetupTest(t, inputs, "%DAYNUM%")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []int64{
					-1,
				}

				for i, sample := range samples {
					if i >= len(EXPECTED) {
						break
					}

					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day%DAYNUM% := &d%DAYNUM%.Day%DAYNUM%{}
						err := day%DAYNUM%.LoadInput(sample)
						assert.NoError(t, err)
						output := day%DAYNUM%.Part1()

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
			day%DAYNUM% := &d%DAYNUM%.Day%DAYNUM%{}
			err := day%DAYNUM%.LoadInput(actual)
			assert.NoError(t, err)
			output := day%DAYNUM%.Part1()
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			require.NotEqualValues(t, 0, output)

			assert.EqualValues(t, -1, output)

			require.True(t, false)
			lib.Submit(t, %YEARNUM%, %DAYNUM, 1, output)
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
						day%DAYNUM% := &d%DAYNUM%.Day%DAYNUM%{}
						err := day%DAYNUM%.LoadInput(sample)
						assert.NoError(t, err)
						output := day%DAYNUM%.Part2()

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
			day%DAYNUM% := &d%DAYNUM%.Day%DAYNUM%{}
			err := day%DAYNUM%.LoadInput(actual)
			assert.NoError(t, err)
			output := day%DAYNUM%.Part2()
			fmt.Print("=================================\n\n")
			fmt.Print("ACTUAL INPUT\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			require.NotEqualValues(t, 0, output)

			assert.EqualValues(t, -1, output)

			require.True(t, false)
			lib.Submit(t, %YEARNUM%, %DAYNUM, 2, output)
		})
	})
}
