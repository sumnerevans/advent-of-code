package d01

import (
	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day01 struct {
	Seq string
}

func (d *Day01) LoadInput(lines []string) error {
	d.Seq = lines[0]
	return nil
}

func (d *Day01) Part1() int {
	var ans int

	for _, c := range d.Seq {
		if c == '(' {
			ans++
		} else {
			ans--
		}
	}

	return ans
}

func (d *Day01) Part2() int {
	var level int

	for i, c := range d.Seq {
		if c == '(' {
			level++
		} else {
			level--
		}
		if level == -1 {
			return i + 1
		}
	}

	return level
}
