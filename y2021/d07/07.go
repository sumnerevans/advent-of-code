package d07

import (
	"math"
	"strings"

	"github.com/rs/zerolog"
	"github.com/sumnerevans/advent-of-code/lib/fp"
	"github.com/sumnerevans/advent-of-code/lib/linq"
	lmath "github.com/sumnerevans/advent-of-code/lib/math"
)

type Day07 struct {
	Poses []int64
}

func (d *Day07) LoadInput(log *zerolog.Logger, lines []string) error {
	d.Poses = fp.MapStrInt64(strings.Split(lines[0], ",")).List()
	return nil
}

func (d *Day07) Solve(log *zerolog.Logger, cost func(a, b int64) int64) int64 {
	var ans int64 = math.MaxInt64

	min, max := linq.List(d.Poses...).MinMax64(func(v int64) int64 { return v })
	for i := min; i <= max; i++ {
		var total int64
		for _, p := range d.Poses {
			total += cost(i, p)
		}
		ans = lmath.Min(total, ans)
	}

	return ans
}

func (d *Day07) Part1(log *zerolog.Logger) int64 {
	return d.Solve(log, func(a, b int64) int64 {
		return lmath.AbsInt(a - b)
	})
}

func (d *Day07) Part2(log *zerolog.Logger) int64 {
	return d.Solve(log, func(a, b int64) int64 {
		var c int64
		var i int64
		for ; i < lmath.AbsInt(a-b); i++ {
			c += i + 1
		}
		return c
	})
}
