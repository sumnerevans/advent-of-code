package d%DAYNUM%_test

import (
	"embed"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/util"
	"github.com/sumnerevans/advent-of-code/y%YEARNUM%/d%DAYNUM%"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day%DAYNUM%(t *testing.T) {
	log, sample, actual := util.SetupTest(t, inputs, "%DAYNUM%")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day%DAYNUM% := &d%DAYNUM%.Day%DAYNUM%{}
				err := day%DAYNUM%.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day%DAYNUM%.Part1(log)

				assert.EqualValues(t, -1, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day%DAYNUM% := &d%DAYNUM%.Day%DAYNUM%{}
			err := day%DAYNUM%.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day%DAYNUM%.Part1(log)
			fmt.Print("=================================\n\n")
			fmt.Printf("Part 1:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, -1, output)
		})
	})
	if !ok {
		t.FailNow()
		return
	}

	t.Run("Part 2", func(t *testing.T) {
		if len(sample) > 0 {
			ok := t.Run("1 Test case", func(t *testing.T) {
				day%DAYNUM% := &d%DAYNUM%.Day%DAYNUM%{}
				err := day%DAYNUM%.LoadInput(log, sample)
				assert.NoError(t, err)
				output := day%DAYNUM%.Part2(log)

				assert.EqualValues(t, -1, output)
			})
			if !ok {
				t.FailNow()
				return
			}
		}

		t.Run("2 Actual input", func(t *testing.T) {
			day%DAYNUM% := &d%DAYNUM%.Day%DAYNUM%{}
			err := day%DAYNUM%.LoadInput(log, actual)
			assert.NoError(t, err)
			output := day%DAYNUM%.Part2(log)
			fmt.Print("=================================\n\n")
			fmt.Printf("Part 2:\n%d", output)
			fmt.Print("\n\n=================================\n")

			assert.EqualValues(t, -1, output)
		})
	})
}
