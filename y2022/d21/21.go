package d21

import (
	"strconv"
	"strings"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Op string

const (
	Plus  Op = "+"
	Minus Op = "-"
	Div   Op = "/"
	Mul   Op = "*"
)

type Monkey struct {
	Name        string
	Op          Op
	Left, Right string
	Val         int64
}

type Day21 struct {
	Monkeys map[string]Monkey
}

func (d *Day21) LoadInput(lines []string) error {
	d.Monkeys = map[string]Monkey{}
	for _, line := range lines {
		x := strings.Split(line, ": ")
		m := Monkey{Name: x[0]}

		val, err := strconv.Atoi(x[1])
		if err == nil {
			m.Val = int64(val)
		} else {
			y := lib.ReGroups(`(\w+) (.) (\w+)`, x[1])
			m.Left = y[0]
			m.Op = Op(y[1])
			m.Right = y[2]
		}
		d.Monkeys[x[0]] = m
	}
	return nil
}

func (d *Day21) Solve(m Monkey) int64 {
	if m.Val > 0 {
		return m.Val
	}

	l := d.Solve(d.Monkeys[m.Left])
	r := d.Solve(d.Monkeys[m.Right])
	switch m.Op {
	case Plus:
		return l + r
	case Minus:
		return l - r
	case Div:
		return l / r
	case Mul:
		return l * r
	default:
		panic("f")
	}
}

func (d *Day21) Part1(isTest bool) int64 {
	return d.Solve(d.Monkeys["root"])
}

func (m Monkey) ClosedFormForLHS(closed string) Monkey {
	switch m.Op {
	case Plus:
		// l + r = c => l = c - r
		return Monkey{Op: Minus, Left: closed, Right: m.Right}
	case Minus:
		// l - r = c => l = c + r
		return Monkey{Op: Plus, Left: closed, Right: m.Right}
	case Div:
		// l / r = c => l = c * r
		return Monkey{Op: Mul, Left: closed, Right: m.Right}
	case Mul:
		// l * r = c => l = c / r
		return Monkey{Op: Div, Left: closed, Right: m.Right}
	default:
		panic("il")
	}
}

func (m Monkey) ClosedFormForRHS(closed string) Monkey {
	switch m.Op {
	case Plus:
		// l + r = c => r = c - l
		return Monkey{Op: Minus, Left: closed, Right: m.Left}
	case Minus:
		// l - r = c => r = l - c
		return Monkey{Op: Minus, Left: m.Left, Right: closed}
	case Div:
		// l / r = c => r = l / c
		return Monkey{Op: Div, Left: m.Left, Right: closed}
	case Mul:
		// l * r = c => r = c / l
		return Monkey{Op: Div, Left: closed, Right: m.Left}
	default:
		panic("ir")
	}
}

func (d *Day21) DependsOnHuman(ms string) bool {
	if ms == "humn" {
		return true
	}
	m := d.Monkeys[ms]
	if m.Op == "" {
		return false
	}
	return d.DependsOnHuman(m.Left) || d.DependsOnHuman(m.Right)
}

func (d *Day21) Part2(isTest bool) int64 {
	var open, closed string

	// Find which side of the root depends on the human. (It is only one side.)
	if d.DependsOnHuman(d.Monkeys["root"].Left) {
		open = d.Monkeys["root"].Left
		closed = d.Monkeys["root"].Right
	} else {
		open = d.Monkeys["root"].Right
		closed = d.Monkeys["root"].Left
	}

	// At this point, "open" contains the equation (monkey name) which depends
	// on the human while "closed" contains an equation that will have an
	// entirely closed-form since it's not dependent on the human.

	// Find a closed form for the human by stripping of the side that isn't
	// dependent on the human from the open side until it's just "humn" on one
	// side of the equation.
	for open != "humn" {
		m := d.Monkeys[open]
		if d.DependsOnHuman(m.Left) {
			newName := lib.RandomString(10)
			d.Monkeys[newName] = m.ClosedFormForLHS(closed)
			closed = newName
			open = m.Left
		} else {
			newName := lib.RandomString(10)
			d.Monkeys[newName] = m.ClosedFormForRHS(closed)
			closed = newName
			open = m.Right
		}
	}

	// The "closed" equation is entirely non-dependent on humn, so whatever its
	// solution is will be the value that humn needs to be for the equation to
	// be satisfied.
	return d.Solve(d.Monkeys[closed])
}
