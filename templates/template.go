package d%DAYNUM%

import (
	"github.com/rs/zerolog"

	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day%DAYNUM% struct {
}

func (d *Day%DAYNUM%) LoadInput(log *zerolog.Logger, lines []string) error {
	for _, line := range lines {
		log.Info().Msg(line)
	}
	return nil
}

func (d *Day%DAYNUM%) Part1(log *zerolog.Logger) int {
	var ans int
	return ans
}

func (d *Day%DAYNUM%) SkipFirst() bool {
	return false
}

func (d *Day%DAYNUM%) Part2(log *zerolog.Logger) int {
	var ans int
	return ans
}
