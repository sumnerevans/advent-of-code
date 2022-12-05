package d05

import (
	"regexp"

	"github.com/rs/zerolog"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Move struct {
	Count, From, To int
}

type Day05 struct {
	S [][]string
	M []Move
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
			x := re.FindAllStringSubmatch(line, -1)
			rows = append(rows, []string{})
			for _, y := range x {
				if y[0] == "    " {
					rows[len(rows)-1] = append(rows[len(rows)-1], "")
				} else {
					rows[len(rows)-1] = append(rows[len(rows)-1], y[1])
				}
			}
		} else {
			m := lib.AllInts(line)
			log.Info().Interface("m", m).Msg(line)
			d.M = append(d.M, Move{m[0], m[1] - 1, m[2] - 1})
		}
	}
	log.Info().Interface("rows", rows).Msg("")

	maxlen := 0
	for _, r := range rows {
		maxlen = lib.Max(maxlen, len(r))
	}

	for i := 0; i < maxlen; i++ {
		d.S = append(d.S, []string{})
		for _, r := range rows {
			if i < len(r) && r[i] != "" {
				d.S[i] = append(d.S[i], r[i])
				log.Info().Msgf("%v", r)
			}
		}
	}

	log.Info().Msgf("%v", d)
	return nil
}

func (d *Day05) Part1(log *zerolog.Logger) string {
	// After the rearrangement procedure completes, what crate ends up on top
	// of each stack?

	for _, m := range d.M {
		for i := 0; i < m.Count; i++ {
			move := []string{d.S[m.From][0]}
			d.S[m.From] = d.S[m.From][1:]
			d.S[m.To] = append(move, d.S[m.To]...)
		}
	}

	ans := ""
	for i := 0; i < len(d.S); i++ {
		ans += d.S[i][0]
	}

	return ans
}

func (d *Day05) Part2(log *zerolog.Logger) string {
	for i, m := range d.M {
		log.Info().Interface("d", d.S).Int("i", i).Msg("move before")
		topN := []string{}
		topN = append(topN, d.S[m.From][:m.Count]...)
		d.S[m.From] = d.S[m.From][m.Count:]
		d.S[m.To] = append(topN, d.S[m.To]...)

		log.Info().Interface("d", d.S).Int("i", i).Msg("after")
	}

	ans := ""
	for i := 0; i < len(d.S); i++ {
		ans += d.S[i][0]
	}
	return ans
}
