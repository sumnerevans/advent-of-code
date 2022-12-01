package d05

import (
	"fmt"

	"github.com/rs/zerolog"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Cell struct {
	X, Y int
}

type Line struct {
	X1, Y1 int
	X2, Y2 int
}

func (l Line) String() string {
	return fmt.Sprintf("%d, %d -> %d, %d", l.X1, l.Y1, l.X2, l.Y2)
}

type Day05 struct {
	Lines []*Line
}

func (d *Day05) LoadInput(log *zerolog.Logger, lines []string) error {
	for _, line := range lines {
		ints := lib.AllInts(line)
		d.Lines = append(d.Lines, &Line{X1: ints[0], Y1: ints[1], X2: ints[2], Y2: ints[3]})
	}
	return nil
}

func (d *Day05) Part1(log *zerolog.Logger) int {
	covered := map[Cell]int{}
	for _, line := range d.Lines {
		if line.X1 == line.X2 || line.Y1 == line.Y2 {
			for _, p := range lib.IntPointsBetween(lib.Point[int]{X: line.X1, Y: line.Y1}, lib.Point[int]{X: line.X2, Y: line.Y2}) {
				covered[Cell{p.X, p.Y}] += 1
			}
		}
	}
	return len(lib.FilterMap(covered, func(_ Cell, v int) bool { return v >= 2 }))
}

func printGrid(points map[Cell]int) {
	minX, maxX := lib.MinMaxMap(points, func(c Cell, _ int) int { return c.X })
	minY, maxY := lib.MinMaxMap(points, func(c Cell, _ int) int { return c.Y })
	fmt.Printf("minX: %d, maxX: %d, minY: %d, maxY: %d\n", minX, maxX, minY, maxY)

	for y := range lib.IRange(minY, maxY) {
		for x := range lib.IRange(minX, maxX) {
			if v, ok := points[Cell{x, y}]; ok {
				fmt.Printf("%d", v)
			} else {
				fmt.Print(".")
			}
		}
		fmt.Print("\n")
	}
}

func (d *Day05) Part2(log *zerolog.Logger) int {
	covered := map[Cell]int{}
	for _, line := range d.Lines {
		for _, p := range lib.IntPointsBetween(lib.Point[int]{X: line.X1, Y: line.Y1}, lib.Point[int]{X: line.X2, Y: line.Y2}) {
			covered[Cell{p.X, p.Y}] += 1
		}
	}
	return len(lib.FilterMap(covered, func(_ Cell, v int) bool { return v >= 2 }))
}
