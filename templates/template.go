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

func (d *Day%DAYNUM%) Part1(log *zerolog.Logger) int64 {
	var ans int64
	return ans
}

func (d *Day01) SkipFirst() bool {
	return false
}

func (d *Day%DAYNUM%) Part2(log *zerolog.Logger) int64 {
	var ans int64
	return ans
}
