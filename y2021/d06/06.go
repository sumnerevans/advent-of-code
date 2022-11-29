package d06

import (
	"strings"

	"github.com/rs/zerolog"
	"github.com/sumnerevans/advent-of-code/lib/fp"
)

type Day06 struct {
	Fishes []int
}

func (d *Day06) LoadInput(log *zerolog.Logger, lines []string) error {
	d.Fishes = fp.MapStrInt(strings.Split(lines[0], ",")).List()
	return nil
}

func (d *Day06) Solve(log *zerolog.Logger, iterations int) int64 {
	countGen := map[int]int64{}
	for _, fish := range d.Fishes {
		countGen[fish] += 1
	}
	for i := 0; i < iterations; i++ {
		newCountGen := map[int]int64{}
		for k, v := range countGen {
			if k == 0 {
				newCountGen[6] += v
				newCountGen[8] += v
			} else {
				newCountGen[k-1] += v
			}
		}
		countGen = newCountGen
	}
	var ans int64
	for _, v := range countGen {
		ans += v
	}
	return ans

}

func (d *Day06) Part1(log *zerolog.Logger) int64 {
	return d.Solve(log, 80)
}

func (d *Day06) Part2(log *zerolog.Logger) int64 {
	return d.Solve(log, 256)
}
