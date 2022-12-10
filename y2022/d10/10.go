package d10

import (
	"fmt"
	"strings"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
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
	clock := 1
	pc := 0

	for {
		// fmt.Printf("%d %d\n", clock, x)
		if clock > 0 && clock%20 == 0 {
			if clock == 20 || (clock-20)%40 == 0 {
				ans += x * clock
			}
		}
		op := d.Ops[pc]

		if op.Type == TypeNoOp {
		} else {
			clock++
			// fmt.Printf("%d %d\n", clock, x)
			if clock == 20 || (clock-20)%40 == 0 {
				ans += x * clock
			}
			x += op.Val
		}

		pc++
		clock++
		// fmt.Printf("%d %d\n", clock, x)
		if len(d.Ops) <= pc {
			break
		}
	}

	return ans
}

func (d *Day10) Part2() string {
	// If the sprite is positioned such that one of its three pixels is the
	// pixel currently being drawn, the screen produces a lit pixel (#);
	// otherwise, the screen leaves the pixel dark (.).

	sprite := 1
	clock := 0
	pc := 0

	crt := make([]rune, 6*40)
	for i := 0; i < len(crt); i++ {
		crt[i] = '.'
	}

	for {
		// fmt.Printf("%d %d\n", clock, x)
		fmt.Printf("%d %d\n", sprite, clock)
		if sprite == clock%40 || sprite-1 == clock%40 || sprite+1 == clock%40 {
			crt[clock] = '#'
		}
		op := d.Ops[pc]

		if op.Type == TypeNoOp {
		} else {
			clock++
			// fmt.Printf("%d %d\n", clock, x)
			if sprite == clock%40 || sprite-1 == clock%40 || sprite+1 == clock%40 {
				crt[clock] = '#'
			}
			sprite += op.Val
		}

		pc++
		clock++
		// fmt.Printf("%d %d\n", clock, x)
		if len(d.Ops) <= pc {
			break
		}
	}

	fmt.Printf("%v\n", crt)
	for r := 0; r < 6; r++ {
		for c := 0; c < 40; c++ {
			fmt.Printf("%c", crt[r*40+c])
		}
		fmt.Printf("\n")
	}

	return string(crt)
}
