package d14

import (
	"fmt"
	"strings"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day14 struct {
	Rock ds.Set[lib.Point[int]]
	MaxY int
}

func (d *Day14) LoadInput(lines []string) error {
	d.Rock = ds.Set[lib.Point[int]]{}
	for _, line := range lines {
		points := strings.Split(line, " -> ")
		for i := 0; i < len(points)-1; i++ {
			s := lib.AllInts(points[i])
			start := lib.Point[int]{X: s[0], Y: s[1]}
			e := lib.AllInts(points[i+1])
			end := lib.Point[int]{X: e[0], Y: e[1]}
			p := lib.IntPointsBetween(start, end)
			for _, p := range p {
				d.Rock.Add(p)
			}

			d.MaxY = lib.Max(d.MaxY, s[1])
			d.MaxY = lib.Max(d.MaxY, e[1])
		}
		fmt.Printf("%s\n", line)

	}
	return nil
}

func (d *Day14) Part1() int {
	var ans int

	hasThing := ds.Set[lib.Point[int]]{}
	for k := range d.Rock {
		hasThing.Add(k)
	}

	for ; ; ans++ {
		sandPos := lib.Point[int]{500, 0}
		for {
			fmt.Printf("sand pos %v\n", sandPos)
			if !hasThing.Contains(lib.Point[int]{sandPos.X, sandPos.Y + 1}) {
				sandPos.Y++
			} else if !hasThing.Contains(lib.Point[int]{sandPos.X - 1, sandPos.Y + 1}) {
				sandPos.X--
				sandPos.Y++
			} else if !hasThing.Contains(lib.Point[int]{sandPos.X + 1, sandPos.Y + 1}) {
				sandPos.X++
				sandPos.Y++
			} else {
				hasThing.Add(sandPos)
				break
			}

			if sandPos.Y > d.MaxY {
				return ans
			}
		}
	}
}

func (d *Day14) Part2() int {
	var ans int

	hasThing := ds.Set[lib.Point[int]]{}
	for k := range d.Rock {
		hasThing.Add(k)
	}
	for i := -1000; i < 1000; i++ {
		hasThing.Add(lib.Point[int]{X: i, Y: d.MaxY + 2})
	}

	for ; ; ans++ {
		sandPos := lib.Point[int]{500, 0}
		for {
			if !hasThing.Contains(lib.Point[int]{sandPos.X, sandPos.Y + 1}) {
				sandPos.Y++
			} else if !hasThing.Contains(lib.Point[int]{sandPos.X - 1, sandPos.Y + 1}) {
				sandPos.X--
				sandPos.Y++
			} else if !hasThing.Contains(lib.Point[int]{sandPos.X + 1, sandPos.Y + 1}) {
				sandPos.X++
				sandPos.Y++
			} else {
				hasThing.Add(sandPos)
				break
			}
		}

		if hasThing.Contains(lib.Point[int]{500, 0}) {
			return ans + 1
		}
	}
}
