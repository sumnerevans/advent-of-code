package d%DAYNUM%

import (
	"github.com/rs/zerolog"

	math "github.com/sumnerevans/advent-of-code/lib/math"
)

type Day%DAYNUM% struct {
}

func (d *Day%DAYNUM%) LoadInput(log *zerolog.Logger, lines []string) error {
	math.Min(1, 2)
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
