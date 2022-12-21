package d21

import (
	"fmt"
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

func (m Monkey) InverseL(closed string) Monkey {
	switch m.Op {
	case Plus:
		return Monkey{
			Op:    Minus,
			Left:  closed,
			Right: m.Right,
		}
	case Minus:
		return Monkey{
			Op:    Plus,
			Left:  closed,
			Right: m.Right,
		}
	case Div:
		return Monkey{
			Op:    Mul,
			Left:  closed,
			Right: m.Right,
		}
	case Mul:
		return Monkey{
			Op:    Div,
			Left:  closed,
			Right: m.Right,
		}
	default:
		panic("il")
	}
}

func (m Monkey) InverseR(closed string) Monkey {
	switch m.Op {
	case Plus:
		return Monkey{
			Op:    Minus,
			Left:  closed,
			Right: m.Left,
		}
	case Minus:
		return Monkey{
			Op:    Minus,
			Left:  m.Left,
			Right: closed,
		}
	case Div:
		return Monkey{
			Op:    Div,
			Left:  m.Left,
			Right: closed,
		}
	case Mul:
		return Monkey{
			Op:    Div,
			Left:  closed,
			Right: m.Left,
		}
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
	if m.Left == "humn" || m.Right == "humn" {
		return true
	}
	return d.DependsOnHuman(m.Left) || d.DependsOnHuman(m.Right)
}

func (d *Day21) Part2(isTest bool) int64 {
	var open, closed string
	if d.DependsOnHuman(d.Monkeys["root"].Left) {
		open = d.Monkeys["root"].Left
		closed = d.Monkeys["root"].Right
	} else {
		open = d.Monkeys["root"].Right
		closed = d.Monkeys["root"].Left
	}
	fmt.Printf("open %v\n", open)
	fmt.Printf("closed %v\n", closed)

	i := 0
	for open != "humn" {
		fmt.Printf("\n")
		fmt.Printf("\n")
		fmt.Printf("\n")
		fmt.Printf("\n")
		fmt.Printf("%v\n", d.Monkeys)
		m := d.Monkeys[open]
		if d.DependsOnHuman(m.Left) {
			newName := lib.RandomString(10)
			if _, ok := d.Monkeys[newName]; ok {
				panic("dup")
			}
			d.Monkeys[newName] = m.InverseL(closed)
			closed = newName
			open = m.Left
		} else {
			newName := lib.RandomString(10)
			if _, ok := d.Monkeys[newName]; ok {
				panic("dup")
			}
			d.Monkeys[newName] = m.InverseR(closed)
			closed = newName
			open = m.Right
		}
		fmt.Printf("open %v\n", open)
		fmt.Printf("closed %v\n", closed)
		fmt.Printf("%v\n", d.Monkeys)
		if i > 1 {
			// break
		}
		i++
	}

	return d.Solve(d.Monkeys[closed])
}
