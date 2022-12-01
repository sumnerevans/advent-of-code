package d01

import (
	"github.com/rs/zerolog"
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/fp"
	math "github.com/sumnerevans/advent-of-code/lib/math"
)

type Day01 struct {
	G [][]int64
}

func (d *Day01) LoadInput(log *zerolog.Logger, lines []string) (err error) {
	cur := []int64{}
	for _, line := range lines {
		if line == "" {
			d.G = append(d.G, cur)
			cur = []int64{}
		} else {
			x, _ := lib.ToInt64(line)
			cur = append(cur, x)
		}
	}
	d.G = append(d.G, cur)
	return err
}

func (d *Day01) Part1(log *zerolog.Logger) int64 {
	var ans int64

	for _, nums := range d.G {
		ans = math.Max(fp.Sum(nums), ans)
	}

	return ans
}

func (d *Day01) SkipFirst() bool {
	return false
}

func (d *Day01) Part2(log *zerolog.Logger) int64 {
	var groupSums []int64

	for _, nums := range d.G {
		groupSums = append(groupSums, fp.Sum(nums))
	}

	return fp.Sum(lib.TopN(groupSums, 3))
}
