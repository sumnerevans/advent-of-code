package d03

import (
	"github.com/rs/zerolog"

	_ "github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day03 struct {
	Sacks [][]rune
}

func (d *Day03) LoadInput(log *zerolog.Logger, lines []string) error {
	for _, line := range lines {
		d.Sacks = append(d.Sacks, []rune{})
		for _, c := range line {
			d.Sacks[len(d.Sacks)-1] = append(d.Sacks[len(d.Sacks)-1], c)
		}
	}
	return nil
}

func (d *Day03) Part1(log *zerolog.Logger) int {
	var ans int

	for _, s := range d.Sacks {
		half := len(s) / 2
		first, second := s[:half], s[half:]

		log.Info().Interface("f", first).Interface("s", second).Msg("f")

		f := ds.NewSet(first)
		s := ds.NewSet(second)
		x := f.Intersection(s)
		i := 0
		for c := range x {
			if i == 1 {
				panic("fail")
			}

			log.Info().Str("c", string(c)).Msg("ohea")

			if c >= 'a' && c <= 'z' {
				ans += int(c-'a') + 1
			}
			if c >= 'A' && c <= 'Z' {
				ans += int(c-'A') + 27
			}

			i++
		}
	}

	return ans
}

func (d *Day03) Part2(log *zerolog.Logger) int {
	var ans int

	cur := [][]rune{}
	log.Info().Msgf("aohea %v", d.Sacks)

	for _, s := range d.Sacks {
		if len(cur) == 3 {
			for c := range ds.NewSet(cur[0]).Intersection(ds.NewSet(cur[1])).Intersection(ds.NewSet(cur[2])) {

				log.Info().Msgf("%v", c)

				if c >= 'a' && c <= 'z' {
					ans += int(c-'a') + 1
				}
				if c >= 'A' && c <= 'Z' {
					ans += int(c-'A') + 27
				}
			}

			cur = [][]rune{}
			cur = append(cur, s)
		} else {
			cur = append(cur, s)
		}
	}

	for c := range ds.NewSet(cur[0]).Intersection(ds.NewSet(cur[1])).Intersection(ds.NewSet(cur[2])) {
		log.Info().Msgf("%v", c)

		if c >= 'a' && c <= 'z' {
			ans += int(c-'a') + 1
		}
		if c >= 'A' && c <= 'Z' {
			ans += int(c-'A') + 27
		}
	}

	return ans
}
