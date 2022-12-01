package d01

import (
	"github.com/rs/zerolog"
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/fp"
)

type Day01 struct {
	GroupSums []int64
}

func (d *Day01) LoadInput(log *zerolog.Logger, lines []string) (err error) {
	var sum int64
	for _, line := range lines {
		if line == "" {
			d.GroupSums = append(d.GroupSums, sum)
			sum = 0
		} else {
			x, _ := lib.ToInt64(line)
			sum += x
		}
	}
	d.GroupSums = append(d.GroupSums, sum)
	return err
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
