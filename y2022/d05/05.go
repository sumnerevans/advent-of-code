package d05

import (
	"regexp"
	"strings"

	"github.com/rs/zerolog"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Move struct {
	Count, From, To int
}

type Day05 struct {
	Stacks [][]string
	Moves  []Move
}

func (d *Day05) LoadInput(log *zerolog.Logger, lines []string) error {
	re := regexp.MustCompile(`(?:\[(\w)\] ?|    )`)

	rows := [][]string{}
	moves := false
	for _, line := range lines {
		if line == "" {
			moves = true
			continue
		}

		if !moves {
			rows = append(rows, []string{})
			for _, y := range re.FindAllStringSubmatch(line, -1) {
				rows[len(rows)-1] = append(rows[len(rows)-1], y[1])
			}
		} else {
			m := lib.AllInts(line)
			d.Moves = append(d.Moves, Move{m[0], m[1] - 1, m[2] - 1})
		}
	}

	for i := 0; i < lib.MaxListFn(rows, func(r []string) int { return len(r) }); i++ {
		d.Stacks = append(d.Stacks, []string{})
		for _, r := range rows {
			if i < len(r) && r[i] != "" {
				d.Stacks[i] = append(d.Stacks[i], r[i])
			}
		}
	}

	return nil
}

func (d *Day05) Part1(log *zerolog.Logger) string {
	for _, m := range d.Moves {
		for i := 0; i < m.Count; i++ {
			move := []string{d.Stacks[m.From][0]}
			d.Stacks[m.From] = d.Stacks[m.From][1:]
			d.Stacks[m.To] = append(move, d.Stacks[m.To]...)
		}
	}

	return strings.Join(lib.Map(func(s []string) string { return s[0] })(d.Stacks), "")
}

func (d *Day05) Part2(log *zerolog.Logger) string {
	for _, m := range d.Moves {
		topN := lib.CopySlice(d.Stacks[m.From][:m.Count])
		d.Stacks[m.From] = d.Stacks[m.From][m.Count:]
		d.Stacks[m.To] = append(topN, d.Stacks[m.To]...)
	}

	return strings.Join(lib.Map(func(s []string) string { return s[0] })(d.Stacks), "")
}
