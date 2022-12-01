package d07

import (
	"math"
	"strings"

	"github.com/rs/zerolog"
	"github.com/sumnerevans/advent-of-code/lib"
)

type Day07 struct {
	Poses []int64
}

func (d *Day07) LoadInput(log *zerolog.Logger, lines []string) error {
	d.Poses = lib.MapStrInt64(strings.Split(lines[0], ","))
	return nil
}

func (d *Day07) Solve(log *zerolog.Logger, cost func(a, b int64) int64) int64 {
	var ans int64 = math.MaxInt64

	min, max := lib.MinMaxListFn(d.Poses, func(v int64) int64 { return v })
	for i := min; i <= max; i++ {
		var total int64
		for _, p := range d.Poses {
			total += cost(i, p)
		}
		ans = lib.Min(total, ans)
	}

	return ans
}

func (d *Day07) Part1(log *zerolog.Logger) int64 {
	return d.Solve(log, func(a, b int64) int64 {
		return lib.AbsInt(a - b)
	})
}

func (d *Day07) Part2(log *zerolog.Logger) int64 {
	return d.Solve(log, func(a, b int64) int64 {
		abs := lib.AbsInt(a - b)
		return abs * (abs + 1) / 2
	})
}
