package d06

import (
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day06 struct {
	Signal []rune
}

func (d *Day06) LoadInput(lines []string) error {
	d.Signal = []rune(lines[0])
	return nil
}

func (d *Day06) Solve(n int) int {
	for i, w := range lib.SlidingWindowsSlices(d.Signal, n) {
		if len(ds.NewSet(w).List()) == n {
			return i + n
		}
	}
	panic("failed to find message start")
}

func (d *Day06) Part1() int {
	return d.Solve(4)
}

func (d *Day06) Part2() int {
	return d.Solve(14)
}
