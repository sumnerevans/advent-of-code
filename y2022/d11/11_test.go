package d11_test

import (
	"embed"
	"fmt"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y2022/d11"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day11(t *testing.T) {
	t.Log(lib.ColorString("============================================", lib.ColorGreen))
	t.Log(lib.ColorString("=                START TEST                =", lib.ColorGreen))
	t.Log(lib.ColorString("============================================", lib.ColorGreen))

	_, samples, actual := lib.SetupTest(t, inputs, "11")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []int64{
					// Test cases
					10605,
				}

				for i, sample := range samples {
					if i >= len(EXPECTED) {
						break
					}

					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day11 := &d11.Day11{}
						err := day11.LoadInput(sample)
						require.NoError(t, err)
						output := day11.Part1()

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
			day11 := &d11.Day11{}
			err := day11.LoadInput(actual)
			require.NoError(t, err)
			output := day11.Part1()
			t.Log("=================================")
			t.Log("")
			t.Log("ACTUAL INPUT")
			t.Log("")
			t.Log("Part 1:")
			t.Log("")
			t.Logf("%v", output)
			t.Log("")

			require.NotEqualValues(t, 0, output)

			existingOutput, err := lib.ReadOutput(1)
			if err != nil {
				previousIncorrects, err := lib.ReadIncorrect(1)
				require.NoError(t, err)
				for _, prev := range previousIncorrects {
					if prev == lib.AsJSON(output) {
						t.Fatal(lib.ColorString("You already submitted that and it was incorrect\n", lib.ColorRed))
					}
				}

				// require.True(t, false, "AUTOSUBMISSION GATE")

				switch result, _ := lib.Submit(t, 2022, 11, 1, output); result {
				case lib.SubmissionCorrect:
					os.WriteFile("output.1.txt", []byte(lib.AsJSON(output)), 0644)
				case lib.SubmissionIncorrect:
					require.NoError(t, lib.WriteIncorrect(1, lib.AsJSON(output)))
				case lib.SubmissionTooSoon:
					t.Fatal(lib.ColorString("Submission was too recent.", lib.ColorRed))
				}
			} else if existingOutput == lib.AsJSON(output) {
				t.Log(lib.ColorString("Answer already ACCEPTED", lib.ColorGreen))
			} else {
				t.Fatal(lib.ColorString("Answer is not equal to accepted output", lib.ColorRed))
			}

			t.Log("")
			t.Log("=================================")
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
					// Test cases
					2713310158,
				}

				for i, sample := range samples {
					if i >= len(EXPECTED) {
						break
					}

					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day11 := &d11.Day11{}
						err := day11.LoadInput(sample)
						require.NoError(t, err)
						output := day11.Part2()

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
			day11 := &d11.Day11{}
			err := day11.LoadInput(actual)
			require.NoError(t, err)
			output := day11.Part2()
			t.Log("=================================")
			t.Log("")
			t.Log("ACTUAL INPUT")
			t.Log("")
			t.Log("Part 2:")
			t.Log("")
			t.Logf("%v", output)
			t.Log("")

			require.NotEqualValues(t, 0, output)

			existingOutput, err := lib.ReadOutput(2)
			if err != nil {
				previousIncorrects, err := lib.ReadIncorrect(2)
				require.NoError(t, err)
				for _, prev := range previousIncorrects {
					if prev == lib.AsJSON(output) {
						t.Fatal(lib.ColorString("You already submitted that and it was incorrect\n", lib.ColorRed))
					}
				}

				// require.True(t, false, "AUTOSUBMISSION GATE")

				switch result, _ := lib.Submit(t, 2022, 11, 2, output); result {
				case lib.SubmissionCorrect:
					os.WriteFile("output.2.txt", []byte(lib.AsJSON(output)), 0644)
				case lib.SubmissionIncorrect:
					require.NoError(t, lib.WriteIncorrect(2, lib.AsJSON(output)))
				case lib.SubmissionTooSoon:
					t.Fatal(lib.ColorString("Submission was too recent.", lib.ColorRed))
				}
			} else if existingOutput == lib.AsJSON(output) {
				t.Log(lib.ColorString("Answer already ACCEPTED", lib.ColorGreen))
			} else {
				t.Fatal(lib.ColorString("Answer is not equal to accepted output", lib.ColorRed))
			}

			t.Log("")
			t.Log("=================================")
		})
	})
}
