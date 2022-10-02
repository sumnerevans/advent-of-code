package d02

import (
	"strings"

	"github.com/rs/zerolog"
	"github.com/sumnerevans/advent-of-code/util"
)

type Direction string

const (
	Forward Direction = "forward"
	Down              = "down"
	Up                = "up"
)

type Instruction struct {
	Dir  Direction
	Amnt int64
}

type Day02 struct {
	Instr []Instruction
}

func (d *Day02) LoadInput(log *zerolog.Logger, lines []string) error {
	for _, line := range lines {
		l := strings.Split(line, " ")
		d.Instr = append(d.Instr, Instruction{
			Dir:  Direction(l[0]),
			Amnt: util.ToIntUnsafe(l[1]),
		})
	}
	return nil
}

func (d *Day02) Part1(log *zerolog.Logger) int64 {
	var x, dep int64
	for _, instr := range d.Instr {
		switch instr.Dir {
		case Forward:
			x += instr.Amnt
		case Down:
			dep += instr.Amnt
		case Up:
			dep -= instr.Amnt
		}
	}
	return x * dep
}

func (d *Day02) Part2(log *zerolog.Logger) int64 {
	var a, x, dep int64
	for _, instr := range d.Instr {
		switch instr.Dir {
		case Forward:
			x += instr.Amnt
			dep += a * instr.Amnt
		case Down:
			a += instr.Amnt
		case Up:
			a -= instr.Amnt
		}
	}
	return x * dep
}
