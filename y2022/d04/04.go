package d04

import (
	"github.com/rs/zerolog"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Section struct {
	Start, End int
}

func (s Section) Contains(other Section) bool {
	return s.Start <= other.Start && other.End <= s.End
}

func (s Section) Intersects(other Section) bool {
	return lib.Max(s.Start, other.Start) <= lib.Min(s.End, other.End)
}

type Pair struct {
	Section1, Section2 Section
}

type Day04 struct {
	Pairs []Pair
}

func (d *Day04) LoadInput(log *zerolog.Logger, lines []string) error {
	for _, line := range lines {
		ints := lib.MapStrInt(lib.ReGroups(`(\d+?)-(\d+?),(\d+?)-(\d+)`, line))
		d.Pairs = append(d.Pairs, Pair{
			Section1: Section{Start: ints[0], End: ints[1]},
			Section2: Section{Start: ints[2], End: ints[3]},
		})
	}
	return nil
}

func (d *Day04) Part1(log *zerolog.Logger) int {
	var ans int

	for _, p := range d.Pairs {
		if p.Section1.Contains(p.Section2) || p.Section2.Contains(p.Section1) {
			ans++
		}
	}

	return ans
}

func (d *Day04) Part2(log *zerolog.Logger) int {
	var ans int
	for _, p := range d.Pairs {
		if p.Section1.Intersects(p.Section2) {
			ans += 1
		}
	}
	return ans
}
