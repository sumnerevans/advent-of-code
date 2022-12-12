package d03

import (
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day03 struct {
	Dirs []rune
}

func (d *Day03) LoadInput(lines []string) error {
	d.Dirs = []rune(lines[0])
	return nil
}

func (d *Day03) Part1() int {
	visited := ds.Set[lib.Point[int]]{}

	curPos := lib.Point[int]{X: 0, Y: 0}
	for _, d := range d.Dirs {
		visited.Add(curPos)
		switch d {
		case '^':
			curPos.Y++
		case '<':
			curPos.X--
		case '>':
			curPos.X++
		case 'v':
			curPos.Y--
		}
	}
	visited.Add(curPos)

	return len(visited)
}

func (d *Day03) Part2() int {
	visited := ds.Set[lib.Point[int]]{}

	curPos := lib.Point[int]{X: 0, Y: 0}
	roboCurPos := lib.Point[int]{X: 0, Y: 0}
	for i, d := range d.Dirs {
		visited.Add(curPos)
		visited.Add(roboCurPos)
		if i%2 == 0 {
			switch d {
			case '^':
				curPos.Y++
			case '<':
				curPos.X--
			case '>':
				curPos.X++
			case 'v':
				curPos.Y--
			}
		} else {
			switch d {
			case '^':
				roboCurPos.Y++
			case '<':
				roboCurPos.X--
			case '>':
				roboCurPos.X++
			case 'v':
				roboCurPos.Y--
			}
		}
	}
	visited.Add(curPos)
	visited.Add(roboCurPos)

	return len(visited)
}
