package d10

import (
	"strings"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Type int

const (
	TypeNoOp Type = iota
	TypeAddX
)

type Op struct {
	Type Type
	Val  int
}

type Day10 struct {
	Ops []Op
}

func (d *Day10) LoadInput(lines []string) error {
	for _, line := range lines {
		f := strings.Fields(line)
		switch f[0] {
		case "noop":
			d.Ops = append(d.Ops, Op{TypeNoOp, 0})
		default:
			d.Ops = append(d.Ops, Op{TypeAddX, lib.ToInt(f[1])})
		}
	}
	return nil
}

func (d *Day10) Part1() int {
	var ans int

	x := 1
	pc := 0
	midAdd := false

	for clock := 1; pc < len(d.Ops); clock++ {
		if clock > 0 && clock%20 == 0 {
			if clock == 20 || (clock-20)%40 == 0 {
				ans += x * clock
			}
		}
		if !midAdd {
			switch d.Ops[pc].Type {
			case TypeNoOp:
				pc++
			case TypeAddX:
				midAdd = true
			}
		} else {
			midAdd = false
			x += d.Ops[pc].Val
			pc++
		}
	}

	return ans
}

type CRT []rune

func (crt CRT) String() string {
	var builder strings.Builder
	for r := 0; r < 6; r++ {
		for c := 0; c < 40; c++ {
			builder.WriteRune(crt[r*40+c])
		}
		if r != 5 {
			builder.WriteRune('\n')
		}
	}
	return builder.String()
}

func (d *Day10) Part2() string {
	// If the sprite is positioned such that one of its three pixels is the
	// pixel currently being drawn, the screen produces a lit pixel (#);
	// otherwise, the screen leaves the pixel dark (.).

	sprite := 1
	pc := 0
	midAdd := false

	crt := make(CRT, 6*40)
	for i := 0; i < len(crt); i++ {
		crt[i] = '.'
	}

	for clock := 0; pc < len(d.Ops); clock++ {
		if sprite == clock%40 || sprite-1 == clock%40 || sprite+1 == clock%40 {
			crt[clock] = '#'
		}
		if !midAdd {
			switch d.Ops[pc].Type {
			case TypeNoOp:
				pc++
			case TypeAddX:
				midAdd = true
			}
		} else {
			midAdd = false
			sprite += d.Ops[pc].Val
			pc++
		}
	}

	return crt.String()
}
