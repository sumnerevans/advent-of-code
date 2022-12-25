package d25_test

import (
	"embed"
	"fmt"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/y2022/d25"
)

//go:embed *.txt
var inputs embed.FS

func Test_Day25(t *testing.T) {
	t.Log(lib.ColorString("============================================", lib.ColorGreen))
	t.Log(lib.ColorString("=                START TEST                =", lib.ColorGreen))
	t.Log(lib.ColorString("============================================", lib.ColorGreen))

	_, samples, actual := lib.SetupTest(t, inputs, "25")

	ok := t.Run("Part 1", func(t *testing.T) {
		if len(samples) > 0 {
			ok := t.Run("1 Test cases", func(t *testing.T) {
				EXPECTED := []string{
					// Test cases
					"1=",
					"1-",
					"2=-1=0",
				}

				for i, sample := range samples {
					if i >= len(EXPECTED) {
						break
					}

					t.Run(fmt.Sprintf("Test %d", i+1), func(t *testing.T) {
						day25 := &d25.Day25{}
						err := day25.LoadInput(sample)
						require.NoError(t, err)
						output := day25.Part1(true)

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
			day25 := &d25.Day25{}
			err := day25.LoadInput(actual)
			require.NoError(t, err)
			output := day25.Part1(false)
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

				result, answerText := lib.Submit(t, 2022, 25, 1, output)
				switch result {
				case lib.SubmissionCorrect:
					os.WriteFile("output.1.txt", []byte(lib.AsJSON(output)), 0644)
					os.WriteFile("answertext.1.txt", []byte(answerText), 0644)

					t.Log("=================================")
					t.Log("")
					t.Log(lib.ColorString("AUTOSUBMITTING PART 2 BECAUSE IT'S DAY 25", lib.ColorYellow))
					t.Log("")

					_, err := lib.ReadOutput(2)
					if err != nil {
						result, answerText := lib.Submit(t, 2022, 25, 2, "done")
						switch result {
						case lib.SubmissionCorrect:
							os.WriteFile("output.2.txt", []byte(lib.AsJSON("done")), 0644)
							os.WriteFile("answertext.2.txt", []byte(answerText), 0644)
						default:
							t.Fatal("Something bad happened with the autosubmission on part 2")
						}
					} else {
						t.Log(lib.ColorString("Auto-submission already complete", lib.ColorGreen))
						if answerText, err := os.ReadFile("answertext.2.txt"); err == nil {
							t.Log("")
							t.Log("Original server response:")
							t.Log("")
							for _, s := range lib.WrapString(string(answerText), 60) {
								t.Log(lib.ColorString(s, lib.ColorGreen))
							}
						}
					}
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
				t.Error(lib.ColorString("Answer is not equal to accepted output", lib.ColorRed))
				t.Fatalf("Expected %v", existingOutput)
			}

			t.Log("")
			t.Log("=================================")
		})
	})
	if !ok {
		t.FailNow()
		return
	}
}
