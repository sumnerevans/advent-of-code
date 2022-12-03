package d03

import (
	"unicode"

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
	if unicode.IsLower(c) {
		return int(c - 'a' + 1)
	} else {
		return int(c - 'A' + 27)
	}
}

func (d *Day03) Part1(log *zerolog.Logger) int {
	var ans int

	for _, s := range d.Sacks {
		fst, snd := lib.SplitAt(s, len(s)/2)
		ans += score(ds.NewSet(fst).Intersection(ds.NewSet(snd)).List()[0])
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
