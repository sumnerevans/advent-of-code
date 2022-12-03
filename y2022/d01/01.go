package d01

import (
	"github.com/rs/zerolog"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Day01 struct {
	GroupSums []int64
}

func (d *Day01) LoadInput(log *zerolog.Logger, lines []string) (err error) {
	d.GroupSums = lib.ParseGroups(lines, func(ls []string) int64 {
		return lib.Sum(lib.LoadInt64s(ls))
	})
	return nil
}

func (d *Day01) Part1(log *zerolog.Logger) int64 {
	return lib.Sum(lib.TopN(d.GroupSums, 1))
}

func (d *Day01) Part2(log *zerolog.Logger) int64 {
	return lib.Sum(lib.TopN(d.GroupSums, 3))
}
