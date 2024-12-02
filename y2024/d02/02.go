package d02

import (
	"github.com/sumnerevans/advent-of-code/lib"
)

type Day02 struct {
	reports [][]int
}

func (d *Day02) LoadInput(lines []string) error {
	for _, line := range lines {
		d.reports = append(d.reports, lib.AllInts(line))
	}
	return nil
}

func (d *Day02) safe(levels []int) bool {
	increasing := levels[0] < levels[1]
	trailing := levels[0]
	for _, level := range levels[1:] {
		diff := lib.AbsInt(trailing - level)
		if diff < 1 || diff > 3 || (increasing && level < trailing) || (!increasing && level > trailing) {
			return false
		}
		trailing = level
	}
	return true
}

func (d *Day02) Part1(isTest bool) int {
	var ans int

	for _, levels := range d.reports {
		if d.safe(levels) {
			ans++
		}
	}

	return ans
}

func (d *Day02) Part2(isTest bool) int {
	var ans int

	for _, levels := range d.reports {
		if d.safe(levels) {
			ans++
			continue
		}

		for i := range levels {
			newLevels := make([]int, len(levels)-1)
			copy(newLevels[0:i], levels[0:i])
			copy(newLevels[i:], levels[i+1:])
			if d.safe(newLevels) {
				ans++
				break
			}
		}
	}

	return ans
}
