package d03

import (
	"github.com/rs/zerolog"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day03 struct {
	Sacks [][]rune
}

func (d *Day03) LoadInput(log *zerolog.Logger, lines []string) error {
	for _, line := range lines {
		d.Sacks = append(d.Sacks, []rune(line))
	}
	return nil
}

func score(c rune) int {
	if c >= 'a' && c <= 'z' {
		return int(c-'a') + 1
	}
	if c >= 'A' && c <= 'Z' {
		return int(c-'A') + 27
	}
	panic("impossible")
}

func (d *Day03) Part1(log *zerolog.Logger) int {
	var ans int

	for _, s := range d.Sacks {
		half := len(s) / 2
		ans += score(ds.NewSet(s[:half]).Intersection(ds.NewSet(s[half:])).List()[0])
	}

	return ans
}

func (d *Day03) Part2(log *zerolog.Logger) int {
	var ans int

	for _, w := range lib.Windowed(d.Sacks, 3) {
		ans += score(ds.NewSet(w[0]).Intersection(ds.NewSet(w[1])).Intersection(ds.NewSet(w[2])).List()[0])
	}

	return ans
}
