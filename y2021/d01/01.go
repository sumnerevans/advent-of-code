package d01

import (
	"github.com/rs/zerolog"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Day01 struct {
	Nums []int64
}

func (d *Day01) LoadInput(log *zerolog.Logger, lines []string) (err error) {
	d.Nums = lib.LoadInt64s(lines)
	return
}

func (d *Day01) Part1(log *zerolog.Logger) int64 {
	var a int64 = 0
	for i := 0; i < len(d.Nums)-1; i++ {
		if d.Nums[i] < d.Nums[i+1] {
			a++
		}
	}
	return a
}

func (d *Day01) Part2(log *zerolog.Logger) int64 {
	var b int64 = 0
	for i := 0; i < len(d.Nums)-3; i++ {
		if d.Nums[i]+d.Nums[i+1]+d.Nums[i+2] < d.Nums[i+1]+d.Nums[i+2]+d.Nums[i+3] {
			b++
		}
	}
	return b
}
