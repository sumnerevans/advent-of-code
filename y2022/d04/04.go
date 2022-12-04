package d04

import (
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type S struct {
	Start, End int
}

func (s S) Contains(other S) bool {
	return s.Start <= other.Start && other.End <= s.End
}

func (s S) InterCard(other S) int {
	st := lib.Max(s.Start, other.Start)
	e := lib.Min(s.End, other.End)
	log.Info().Int("st", st).Int("e", e).Msg("I")
	if st <= e {
		return e - st + 1
	}
	return 0
}

type P struct {
	S1, S2 S
}

type Day04 struct {
	Pairs []P
}

func (d *Day04) LoadInput(log *zerolog.Logger, lines []string) error {
	for _, line := range lines {
		log.Info().Msg(line)
		x := lib.AllInts(line)
		d.Pairs = append(d.Pairs, P{S1: S{Start: x[0], End: x[1]}, S2: S{Start: x[2], End: x[3]}})
	}
	return nil
}

func (d *Day04) Part1(log *zerolog.Logger) int {
	var ans int

	for _, p := range d.Pairs {
		if p.S1.Contains(p.S2) || p.S2.Contains(p.S1) {
			ans++
		}
	}

	return ans
}

func (d *Day04) Part2(log *zerolog.Logger) int {
	var ans int
	for _, p := range d.Pairs {
		log.Info().Interface("p", p).Int("x", p.S1.InterCard(p.S2)).Msg("ohea")
		if p.S1.InterCard(p.S2) > 0 {
			ans += 1
		}
	}
	return ans
}
