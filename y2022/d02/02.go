package d02

import (
	"strings"

	"github.com/rs/zerolog"
)

type Play int

const (
	Rock Play = iota
	Paper
	Scisors
)

func (p Play) Score() int {
	return int(p) + 1
}

func (p Play) Beats(other Play) bool {
	return int(p) == (int(other)+1)%3
}

func PlayFromStr(play string) Play {
	switch play {
	case "X", "A":
		return Rock
	case "Y", "B":
		return Paper
	case "Z", "C":
		return Scisors
	default:
		panic(play)
	}
}

type Round struct {
	You Play
	Me  Play
}

type Day02 struct {
	Rounds []Round
}

func (d *Day02) LoadInput(log *zerolog.Logger, lines []string) error {
	for _, line := range lines {
		k := strings.Split(line, " ")
		d.Rounds = append(d.Rounds, Round{PlayFromStr(k[0]), PlayFromStr(k[1])})
	}
	return nil
}

func (d *Day02) Part1(log *zerolog.Logger) int {
	var ans int

	for _, r := range d.Rounds {
		ans += r.Me.Score()
		if r.Me == r.You {
			ans += 3
		} else if r.Me.Beats(r.You) {
			ans += 6
		}
	}

	return ans
}

func (d *Day02) Part2(log *zerolog.Logger) int {
	var ans int

	for _, p := range d.Rounds {
		switch p.Me {
		case Rock: // Lose
			ans += 0
			switch p.You {
			case Rock:
				ans += Scisors.Score()
			case Paper:
				ans += Rock.Score()
			case Scisors:
				ans += Paper.Score()
			}
		case Paper: // Draw
			ans += 3 + p.You.Score()
		case Scisors: // Win
			ans += 6
			switch p.You {
			case Rock:
				ans += Paper.Score()
			case Paper:
				ans += Scisors.Score()
			case Scisors:
				ans += Rock.Score()
			}
		}
	}

	return ans
}
