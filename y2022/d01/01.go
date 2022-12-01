package d01

import (
	"sort"

	"github.com/rs/zerolog"
	"github.com/sumnerevans/advent-of-code/lib"
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
	return err
}

func (d *Day01) Part1(log *zerolog.Logger) int64 {
	var ans int64

	for i, n := range d.G {
		log.Debug().Int("i", i).Interface("n", n).Msg("num")
		var sum int64
		for _, x := range n {
			sum += x
		}
		if sum > ans {
			ans = sum
		}
	}

	return ans
}

func (d *Day01) SkipFirst() bool {
	return false
}

func (d *Day01) Part2(log *zerolog.Logger) int {
	var ans []int

	for i, n := range d.G {
		log.Debug().Int("i", i).Interface("n", n).Msg("num")
		var sum int
		for _, x := range n {
			sum += int(x)
		}
		ans = append(ans, sum)
	}

	sort.Ints(ans)

	return ans[len(ans)-1] + ans[len(ans)-2] + ans[len(ans)-3]

}
