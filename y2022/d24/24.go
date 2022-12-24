package d24

import (
	"fmt"
	"runtime"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

const NB = 2687

type Blizzard struct {
	Pos, Dir lib.GridPoint[int]
}

type Blizzards [NB]Blizzard

func (bl Blizzards) Step(h, w, a int) Blizzards {
	newBlizzards := Blizzards{}
	for i, b := range bl[:a] {
		newBlizzards[i].Dir = b.Dir

		newR := b.Pos.R + b.Dir.R
		if newR == 0 {
			newR = h - 2
		} else if newR == h-1 {
			newR = 1
		}

		newC := b.Pos.C + b.Dir.C
		if newC == 0 {
			newC = w - 2
		} else if newC == w-1 {
			newC = 1
		}

		newBlizzards[i].Pos = lib.NewGridPoint(newR, newC)
	}
	return newBlizzards
}

func (bl Blizzards) Snowy(a int) ds.Set[lib.GridPoint[int]] {
	snowy := ds.Set[lib.GridPoint[int]]{}
	for _, b := range bl[:a] {
		snowy.Add(b.Pos)
	}
	return snowy
}

func (bl Blizzards) Print(h, w, a int, pos lib.GridPoint[int]) {
	for r := 0; r < h; r++ {
		for c := 0; c < w; c++ {
			actives := []Blizzard{}
			for _, b := range bl[:a] {
				if b.Pos == lib.NewGridPoint(r, c) {
					actives = append(actives, b)
				}
			}
			if len(actives) > 1 {
				fmt.Printf("%d", len(actives))
			} else if len(actives) == 1 {
				switch actives[0].Dir {
				case lib.NewGridPoint(0, 1):
					fmt.Printf(">")
				case lib.NewGridPoint(0, -1):
					fmt.Printf("<")
				case lib.NewGridPoint(1, 0):
					fmt.Printf("v")
				case lib.NewGridPoint(-1, 0):
					fmt.Printf("^")
				}
			} else {
				if pos == lib.NewGridPoint(r, c) {
					fmt.Printf("E")
				} else if r == 0 || c == 0 || r == h-1 || c == w-1 {
					fmt.Printf("#")
				} else {
					fmt.Printf(".")
				}
			}
		}
		fmt.Printf("\n")
	}
}

type Minute struct {
	Time int
	Pos  lib.GridPoint[int]
}

func (m Minute) StepTo(to lib.GridPoint[int]) Minute {
	return Minute{Time: m.Time + 1, Pos: to}
}

type Day24 struct {
	BlizzardStart Blizzards
	Open          ds.Set[lib.GridPoint[int]]
	Start, End    lib.GridPoint[int]
	Active        int
	H, W          int
}

func (d *Day24) LoadInput(lines []string) error {
	i := 0
	d.H = len(lines)
	d.W = len(lines[0])
	d.Open = ds.Set[lib.GridPoint[int]]{}
	for r, line := range lines {
		for c, char := range line {
			switch char {
			case '.':
				if r == 0 {
					d.Start = lib.NewGridPoint(r, c)
				} else if r == len(lines)-1 {
					d.End = lib.NewGridPoint(r, c)
				}
				d.Open.Add(lib.NewGridPoint(r, c))
			case '>':
				d.BlizzardStart[i] = Blizzard{lib.NewGridPoint(r, c), lib.NewGridPoint(0, 1)}
				i++
				d.Open.Add(lib.NewGridPoint(r, c))
			case '<':
				d.BlizzardStart[i] = Blizzard{lib.NewGridPoint(r, c), lib.NewGridPoint(0, -1)}
				i++
				d.Open.Add(lib.NewGridPoint(r, c))
			case 'v':
				d.BlizzardStart[i] = Blizzard{lib.NewGridPoint(r, c), lib.NewGridPoint(1, 0)}
				i++
				d.Open.Add(lib.NewGridPoint(r, c))
			case '^':
				d.BlizzardStart[i] = Blizzard{lib.NewGridPoint(r, c), lib.NewGridPoint(-1, 0)}
				i++
				d.Open.Add(lib.NewGridPoint(r, c))
			}
		}
	}
	d.Active = i
	return nil
}

func (d *Day24) Part1(isTest bool) int {
	forTime := []Blizzards{}
	cur := d.BlizzardStart
	for i := 0; i < 200; i++ {
		forTime = append(forTime, cur)
		cur = cur.Step(d.H, d.W, d.Active)
	}

	return lib.ShortestPath(
		func(m Minute) ds.Set[Minute] {
			snowy := forTime[m.Time+1].Snowy(d.Active)
			opts := ds.Set[Minute]{}

			// Stay
			stay := lib.NewGridPoint(m.Pos.R, m.Pos.C)
			if !snowy.Contains(stay) {
				opts.Add(m.StepTo(stay))
			}

			// Up
			up := lib.NewGridPoint(m.Pos.R-1, m.Pos.C)
			if !snowy.Contains(up) && d.Open.Contains(up) {
				opts.Add(m.StepTo(up))
			}

			// Down
			down := lib.NewGridPoint(m.Pos.R+1, m.Pos.C)
			if !snowy.Contains(down) && d.Open.Contains(down) {
				opts.Add(m.StepTo(down))
			}

			// Left
			left := lib.NewGridPoint(m.Pos.R, m.Pos.C-1)
			if !snowy.Contains(left) && d.Open.Contains(left) {
				opts.Add(m.StepTo(left))
			}

			// Right
			right := lib.NewGridPoint(m.Pos.R, m.Pos.C+1)
			if !snowy.Contains(right) && d.Open.Contains(right) {
				opts.Add(m.StepTo(right))
			}

			return opts
		},
		Minute{Time: 0, Pos: d.Start},
		func(m Minute) bool {
			return m.Pos == d.End
		},
	)
}

func (d *Day24) Part2(isTest bool) int {
	forTime := []Blizzards{}
	cur := d.BlizzardStart
	for i := 0; i < 5000; i++ {
		forTime = append(forTime, cur)
		cur = cur.Step(d.H, d.W, d.Active)
	}

	nextStates := func(m Minute) ds.Set[Minute] {
		snowy := forTime[m.Time+1].Snowy(d.Active)
		opts := ds.Set[Minute]{}

		// Stay
		stay := lib.NewGridPoint(m.Pos.R, m.Pos.C)
		if !snowy.Contains(stay) {
			opts.Add(m.StepTo(stay))
		}

		// Up
		up := lib.NewGridPoint(m.Pos.R-1, m.Pos.C)
		if !snowy.Contains(up) && d.Open.Contains(up) {
			opts.Add(m.StepTo(up))
		}

		// Down
		down := lib.NewGridPoint(m.Pos.R+1, m.Pos.C)
		if !snowy.Contains(down) && d.Open.Contains(down) {
			opts.Add(m.StepTo(down))
		}

		// Left
		left := lib.NewGridPoint(m.Pos.R, m.Pos.C-1)
		if !snowy.Contains(left) && d.Open.Contains(left) {
			opts.Add(m.StepTo(left))
		}

		// Right
		right := lib.NewGridPoint(m.Pos.R, m.Pos.C+1)
		if !snowy.Contains(right) && d.Open.Contains(right) {
			opts.Add(m.StepTo(right))
		}

		return opts
	}

	end := lib.ShortestPath(
		nextStates,
		Minute{Time: 0, Pos: d.Start},
		func(m Minute) bool {
			return m.Pos == d.End
		},
	)
	runtime.GC()
	back := lib.ShortestPath(
		nextStates,
		Minute{Time: end, Pos: d.End},
		func(m Minute) bool {
			return m.Pos == d.Start
		},
	)
	runtime.GC()
	goalagain := lib.ShortestPath(
		nextStates,
		Minute{Time: end + back, Pos: d.Start},
		func(m Minute) bool {
			return m.Pos == d.End
		},
	)
	return end + back + goalagain
}
