package d06

import (
	_ "github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day06 struct {
	S []rune
}

func (d *Day06) LoadInput(lines []string) error {
	d.S = []rune(lines[0])
	return nil
}

func (d *Day06) Part1() int {
	var ans int

	// How many characters need to be processed before the first start-of-packet marker is detected?
	win := []rune{}
	for i := 0; i < len(d.S); i++ {
		win = append(win, d.S[i])
		if len(win) == 4 {
			s := ds.SetFromValues(win...)
			if len(s.List()) == 4 {
				return i + 1
			}
			win = win[1:]
		}
	}

	return ans
}

func (d *Day06) Part2() int {
	var ans int

	// How many characters need to be processed before the first start-of-packet marker is detected?
	win := []rune{}
	for i := 0; i < len(d.S); i++ {
		win = append(win, d.S[i])
		if len(win) == 14 {
			s := ds.SetFromValues(win...)
			if len(s.List()) == 14 {
				return i + 1
			}
			win = win[1:]
		}
	}

	return ans
}
