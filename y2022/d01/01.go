package d01

import (
	"github.com/rs/zerolog"
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/fp"
	"github.com/sumnerevans/advent-of-code/lib/input"
)

type Day01 struct {
	GroupSums []int64
}

func (d *Day01) LoadInput(log *zerolog.Logger, lines []string) (err error) {
	d.GroupSums = input.ParseGroups(lines, func(ls []string) int64 {
		return fp.Sum(lib.LoadInt64s(ls))
	})
	return nil
}

func (d *Day01) Part1(log *zerolog.Logger) int64 {
	return fp.Sum(lib.TopN(d.GroupSums, 1))
}

func (d *Day01) SkipFirst() bool {
	return false
}

func (d *Day01) Part2(log *zerolog.Logger) int64 {
	return fp.Sum(lib.TopN(d.GroupSums, 3))
}
