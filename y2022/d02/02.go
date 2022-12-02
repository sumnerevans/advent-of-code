package d02

import (
	"strings"

	"github.com/rs/zerolog"

	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Pair struct {
	You string
	Me  string
}

type Day02 struct {
	Pairs []Pair
}

func (d *Day02) LoadInput(log *zerolog.Logger, lines []string) error {
	for _, line := range lines {
		k := strings.Split(line, " ")
		d.Pairs = append(d.Pairs, Pair{k[0], k[1]})
	}
	return nil
}

func (d *Day02) Part1(log *zerolog.Logger) int64 {
	var ans int64

	for _, p := range d.Pairs {
		val := 0
		switch p.Me {
		case "X": // R
			val = 1
		case "Y": // paper
			val = 2
		case "Z": // sci
			val = 3
		}

		switch p.You {
		case "A": // R
			if val == 1 {
				val += 3
			} else if val == 2 {
				val += 6
			}
		case "B": // paper
			if val == 2 {
				val += 3
			} else if val == 3 {
				val += 6
			}
		case "C": // sci
			if val == 3 {
				val += 3
			} else if val == 1 {
				val += 6
			}
		}
		ans += int64(val)
	}

	return ans
}

func (d *Day02) SkipFirst() bool {
	return false
}

func (d *Day02) Part2(log *zerolog.Logger) int64 {
	var ans int64

	for _, p := range d.Pairs {
		val := 0
		switch p.Me {
		case "X": // R
			val = 0
		case "Y": // paper
			val = 3
		case "Z": // sci
			val = 6
		}

		if val == 0 {
			switch p.You {
			case "A": //R
				val += 3
			case "B": //p
				val += 1
			case "C": //s
				val += 2
			}
		} else if val == 3 {
			switch p.You {
			case "A": //R
				val += 1
			case "B": //p
				val += 2
			case "C": //s
				val += 3
			}
		} else if val == 6 {
			switch p.You {
			case "A": //R
				val += 2
			case "B": //p
				val += 3
			case "C": //s
				val += 1
			}
		}
		ans += int64(val)
	}

	return ans
}
