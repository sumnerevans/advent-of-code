package d14

import (
	"strings"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day14 struct {
	Rock ds.Set[lib.GridPoint[int]]
	MaxY int
}

func (d *Day14) LoadInput(lines []string) error {
	d.Rock = ds.Set[lib.GridPoint[int]]{}
	for _, line := range lines {
		points := strings.Split(line, " -> ")
		for i := 0; i < len(points)-1; i++ {
			s := lib.AllInts(points[i])
			start := lib.GridPoint[int]{R: s[1], C: s[0]}
			e := lib.AllInts(points[i+1])
			end := lib.GridPoint[int]{R: e[1], C: e[0]}
			for _, p := range lib.GridPointsBetween(start, end) {
				d.Rock.Add(p)
			}

			d.MaxY = lib.Max(d.MaxY, s[1])
			d.MaxY = lib.Max(d.MaxY, e[1])
		}

	}
	return nil
}

func (d *Day14) Part1() int {
	var ans int

	hasThing := ds.NewSetFromValues(d.Rock.List()...)

	for ; ; ans++ {
		sandPos := lib.GridPoint[int]{R: 0, C: 500}
		for {
			if !hasThing.Contains(lib.GridPoint[int]{R: sandPos.R + 1, C: sandPos.C}) {
				sandPos.R++
			} else if !hasThing.Contains(lib.GridPoint[int]{R: sandPos.R + 1, C: sandPos.C - 1}) {
				sandPos.C--
				sandPos.R++
			} else if !hasThing.Contains(lib.GridPoint[int]{R: sandPos.R + 1, C: sandPos.C + 1}) {
				sandPos.C++
				sandPos.R++
			} else {
				hasThing.Add(sandPos)
				break
			}

			if sandPos.R > d.MaxY {
				return ans
			}
		}
	}
}

func (d *Day14) Part2() int {
	var ans int

	hasThing := ds.NewSetFromValues(d.Rock.List()...)

	// "infinite" floor
	for i := -1000; i < 1000; i++ {
		hasThing.Add(lib.GridPoint[int]{R: d.MaxY + 2, C: i})
	}

	for ; ; ans++ {
		sandPos := lib.GridPoint[int]{R: 0, C: 500}
		for {
			if !hasThing.Contains(lib.GridPoint[int]{R: sandPos.R + 1, C: sandPos.C}) {
				sandPos.R++
			} else if !hasThing.Contains(lib.GridPoint[int]{R: sandPos.R + 1, C: sandPos.C - 1}) {
				sandPos.C--
				sandPos.R++
			} else if !hasThing.Contains(lib.GridPoint[int]{R: sandPos.R + 1, C: sandPos.C + 1}) {
				sandPos.C++
				sandPos.R++
			} else {
				hasThing.Add(sandPos)
				break
			}
		}

		if hasThing.Contains(lib.GridPoint[int]{R: 0, C: 500}) {
			return ans + 1
		}
	}
}
