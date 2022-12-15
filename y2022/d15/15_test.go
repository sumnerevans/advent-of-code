package d15_test

import (
	"embed"
	"fmt"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y2022/d15"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day15(t *testing.T) {
	t.Log(lib.ColorString("============================================", lib.ColorGreen))
	t.Log(lib.ColorString("=                START TEST                =", lib.ColorGreen))
	t.Log(lib.ColorString("============================================", lib.ColorGreen))

	_, samples, actual := lib.SetupTest(t, inputs, "15")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []int64{
					// Test cases
					26,
				}

				for i, sample := range samples {
					if i >= len(EXPECTED) {
						break
					}

					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day15 := &d15.Day15{}
						err := day15.LoadInput(sample)
						require.NoError(t, err)
						output := day15.Part1(true)

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
			day15 := &d15.Day15{}
			err := day15.LoadInput(actual)
			require.NoError(t, err)
			output := day15.Part1(false)
			t.Log("=================================")
			t.Log("")
			t.Log("ACTUAL INPUT")
			t.Log("")
			t.Log(lib.ColorString("Part 1:", lib.ColorBlue))
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

				result, answerText := lib.Submit(t, 2022, 15, 1, output)
				switch result {
				case lib.SubmissionCorrect:
					os.WriteFile("output.1.txt", []byte(lib.AsJSON(output)), 0644)
					os.WriteFile("answertext.1.txt", []byte(answerText), 0644)
				case lib.SubmissionIncorrect:
					require.NoError(t, lib.WriteIncorrect(1, lib.AsJSON(output)))
				case lib.SubmissionTooSoon:
					t.Fatal(lib.ColorString("Submission was too recent.", lib.ColorRed))
				}
			} else if existingOutput == lib.AsJSON(output) {
				t.Log(lib.ColorString("Answer already ACCEPTED", lib.ColorGreen))
				if answerText, err := os.ReadFile("answertext.1.txt"); err == nil {
					t.Log("")
					t.Log("Original server response:")
					t.Log("")
					for _, s := range lib.WrapString(string(answerText), 60) {
						t.Log(lib.ColorString(s, lib.ColorGreen))
					}
				}
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
					56000011,
				}

				for i, sample := range samples {
					if i >= len(EXPECTED) {
						break
					}

					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day15 := &d15.Day15{}
						err := day15.LoadInput(sample)
						require.NoError(t, err)
						output := day15.Part2(true)

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
			day15 := &d15.Day15{}
			err := day15.LoadInput(actual)
			require.NoError(t, err)
			output := day15.Part2(false)
			t.Log("=================================")
			t.Log("")
			t.Log("ACTUAL INPUT")
			t.Log("")
			t.Log(lib.ColorString("Part 2:", lib.ColorYellow))
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

				result, answerText := lib.Submit(t, 2022, 15, 2, output)
				switch result {
				case lib.SubmissionCorrect:
					os.WriteFile("output.2.txt", []byte(lib.AsJSON(output)), 0644)
					os.WriteFile("answertext.2.txt", []byte(answerText), 0644)
				case lib.SubmissionIncorrect:
					require.NoError(t, lib.WriteIncorrect(2, lib.AsJSON(output)))
				case lib.SubmissionTooSoon:
					t.Fatal(lib.ColorString("Submission was too recent.", lib.ColorRed))
				}
			} else if existingOutput == lib.AsJSON(output) {
				t.Log(lib.ColorString("Answer already ACCEPTED", lib.ColorGreen))
				if answerText, err := os.ReadFile("answertext.2.txt"); err == nil {
					t.Log("")
					t.Log("Original server response:")
					t.Log("")
					for _, s := range lib.WrapString(string(answerText), 60) {
						t.Log(lib.ColorString(s, lib.ColorGreen))
					}
				}
			} else {
				t.Fatal(lib.ColorString("Answer is not equal to accepted output", lib.ColorRed))
			}

			t.Log("")
			t.Log("=================================")
		})
	})
}
