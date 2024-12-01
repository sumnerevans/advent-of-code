package d01

import (
	"sort"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Day01 struct {
	l []int
	r []int
}

func (d *Day01) LoadInput(lines []string) error {
	for _, line := range lines {
		xs := lib.AllInts(line)
		d.l = append(d.l, xs[0])
		d.r = append(d.r, xs[1])
	}
	return nil
}

func (d *Day01) Part1(isTest bool) int {
	var ans int

	sort.Ints(d.l)
	sort.Ints(d.r)

	for i, l := range d.l {
		ans += lib.AbsInt(l - d.r[i])
	}

	return ans
}

func (d *Day01) Part2(isTest bool) int {
	var ans int

	freq := map[int]int{}
	for _, v := range d.r {
		if _, ok := freq[v]; !ok {
			freq[v] = 0
		}
		freq[v]++
	}

	for _, v := range d.l {
		ans += v * freq[v]
	}

	return ans
}
