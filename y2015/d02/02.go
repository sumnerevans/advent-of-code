package d02

import (
	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Dimension struct {
	L, W, H int
}

type Day02 struct {
	Presents []Dimension
}

func (d *Day02) LoadInput(lines []string) error {
	for _, line := range lines {
		dims := lib.AllInts(line)
		d.Presents = append(d.Presents, Dimension{dims[0], dims[1], dims[2]})
	}
	return nil
}

func (d *Day02) Part1() int {
	var ans int

	for _, p := range d.Presents {
		s1 := p.L * p.W
		s2 := p.W * p.H
		s3 := p.H * p.L
		ans += 2*s1 + 2*s2 + 2*s3
		ans += lib.Min(s1, lib.Min(s2, s3))
	}

	return ans
}

func (d *Day02) Part2() int {
	var ans int

	for _, p := range d.Presents {
		f1 := 2*p.L + 2*p.W
		f2 := 2*p.W + 2*p.H
		f3 := 2*p.H + 2*p.L
		ans += p.L * p.W * p.H
		ans += lib.Min(f1, lib.Min(f2, f3))
	}

	return ans
}
