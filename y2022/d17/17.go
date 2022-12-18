package d17

import (
	"fmt"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Shape [][]bool

var (
	Line  = [][]bool{{true, true, true, true}}
	Cross = [][]bool{
		{false, true, false},
		{true, true, true},
		{false, true, false},
	}
	Ell = [][]bool{
		{false, false, true},
		{false, false, true},
		{true, true, true},
	}
	Bar = [][]bool{
		{true},
		{true},
		{true},
		{true},
	}
	Square = [][]bool{
		{true, true},
		{true, true},
	}
)

func (s Shape) Intersects(bottomLeftPos lib.GridPoint[int64], covered ds.Set[lib.GridPoint[int64]]) bool {
	for r := 0; r < len(s); r++ {
		for c := 0; c < len(s[0]); c++ {
			point := lib.GridPoint[int64]{
				R: bottomLeftPos.R + int64(len(s)-r-1),
				C: bottomLeftPos.C + int64(c),
			}

			if s[r][c] && covered.Contains(point) {
				return true
			}
		}
	}
	return false
}

type Direction int

const (
	Left  Direction = -1
	Right Direction = 1
)

type Day17 struct {
	Dirs []Direction
}

func (d *Day17) LoadInput(lines []string) error {
	for _, c := range lines[0] {
		switch c {
		case '<':
			d.Dirs = append(d.Dirs, Left)
		case '>':
			d.Dirs = append(d.Dirs, Right)
		}
	}

	return nil
}

func PrintChamberWithShape(chamber ds.Set[lib.GridPoint[int64]], shape Shape, shapeBottomLeftPos lib.GridPoint[int64]) {
	shapePoints := ds.Set[lib.GridPoint[int64]]{}
	for r := 0; r < len(shape); r++ {
		for c := 0; c < len(shape[0]); c++ {
			if shape[r][c] {
				shapePoints.Add(lib.GridPoint[int64]{
					R: shapeBottomLeftPos.R + int64(len(shape)-r-1),
					C: shapeBottomLeftPos.C + int64(c),
				})
			}
		}
	}

	chamberTop := lib.MaxListFn(shapePoints.List(), func(gp lib.GridPoint[int64]) int64 {
		return gp.R
	})
	for r := chamberTop; r >= 0; r-- {
		fmt.Printf("|")
		for c := 0; c < 7; c++ {
			if shapePoints.Contains(lib.GridPoint[int64]{R: r, C: int64(c)}) {
				fmt.Printf("@")
			} else if chamber.Contains(lib.GridPoint[int64]{R: r, C: int64(c)}) {
				fmt.Printf("#")
			} else {
				fmt.Printf(".")
			}
		}
		fmt.Printf("|\n")
	}
	fmt.Printf("---------\n")
}

const ROWS int = 200

type FloorShape [ROWS][7]bool

func (fs FloorShape) Print() {
	for r := 0; r < ROWS; r++ {
		for c := 0; c < 7; c++ {
			if fs[r][c] {
				fmt.Printf("#")
			} else {
				fmt.Printf(" ")
			}
		}
		fmt.Printf("\n")
	}
}

func NewFloorShape() FloorShape {
	fs := FloorShape{}
	for c := 0; c < 7; c++ {
		fs[1][c] = true
	}
	return fs
}

type ShapeHeight struct {
	Idx int64
	Top int64
}

func (d *Day17) Solve(iters int64) int64 {
	shapes := []Shape{Line, Cross, Ell, Bar, Square}

	// The tall, vertical chamber is exactly seven units wide. Each rock
	// appears so that its left edge is two units away from the left wall and
	// its bottom edge is three units above the highest rock in the room (or
	// the floor, if there isn't one).

	var top int64
	var curDirIdx, curShapeIdx int

	floorShapePerIdx := map[FloorShape]map[int]map[int]ShapeHeight{}

	currentFloorShape := NewFloorShape()
	var i int64
	foundCycle := false
	for ; i < iters; i++ {
		if !foundCycle {
			if perShape, ok := floorShapePerIdx[currentFloorShape]; ok {
				if perDir, ok := perShape[curShapeIdx]; ok {
					if prevIdx, ok := perDir[curDirIdx]; ok {
						di := i - prevIdx.Idx
						if i+di < iters {
							cycleCount := (iters - i) / di
							top += cycleCount * (top - prevIdx.Top)
							i += cycleCount*di - 1 // the -1 here is because we re-add it in the for-loop
							foundCycle = true
							continue
						}
					}
				}
			}
		}

		shape := shapes[curShapeIdx]

		chamber := ds.Set[lib.GridPoint[int64]]{}
		for dr := 0; dr < ROWS; dr++ {
			for c := 0; c < 7; c++ {
				if currentFloorShape[dr][c] {
					chamber.Add(lib.GridPoint[int64]{R: top - int64(dr), C: int64(c)})
				}
			}
		}

		shapeBottomLeftPos := lib.GridPoint[int64]{R: top + 3, C: 2}
		newDirIdx := curDirIdx
		for {
			// Direction
			var newPos lib.GridPoint[int64]
			switch d.Dirs[newDirIdx] {
			case Left:
				newPos = lib.GridPoint[int64]{R: shapeBottomLeftPos.R, C: shapeBottomLeftPos.C - 1}
			case Right:
				newPos = lib.GridPoint[int64]{R: shapeBottomLeftPos.R, C: shapeBottomLeftPos.C + 1}
			default:
				panic("fail")
			}
			newDirIdx = (newDirIdx + 1) % len(d.Dirs)
			if !shape.Intersects(newPos, chamber) && newPos.C >= 0 && newPos.C+int64(len(shape[0])) <= 7 {
				shapeBottomLeftPos = newPos
			}

			// Down
			newPos = lib.GridPoint[int64]{R: shapeBottomLeftPos.R - 1, C: shapeBottomLeftPos.C}
			if shape.Intersects(newPos, chamber) {
				break
			} else {
				shapeBottomLeftPos = newPos
			}
		}

		for r := 0; r < len(shape); r++ {
			for c := 0; c < len(shape[0]); c++ {
				if shape[r][c] {
					chamber.Add(lib.GridPoint[int64]{
						R: shapeBottomLeftPos.R + int64(len(shape)-r-1),
						C: shapeBottomLeftPos.C + int64(c),
					})
				}
			}
		}

		newTop := lib.MaxListFn(chamber.List(), func(gp lib.GridPoint[int64]) int64 {
			return gp.R + 1
		})

		newFloorShape := FloorShape{}
		for dr := 0; dr < ROWS; dr++ {
			for c := 0; c < 7; c++ {
				if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: int64(c)}) {
					newFloorShape[dr][c] = true
				}
			}
		}
		if _, ok := floorShapePerIdx[currentFloorShape]; !ok {
			floorShapePerIdx[currentFloorShape] = map[int]map[int]ShapeHeight{}
		}
		if _, ok := floorShapePerIdx[currentFloorShape][curShapeIdx]; !ok {
			floorShapePerIdx[currentFloorShape][curShapeIdx] = map[int]ShapeHeight{}
		}

		floorShapePerIdx[currentFloorShape][curShapeIdx][curDirIdx] = ShapeHeight{Idx: i, Top: newTop}
		currentFloorShape = newFloorShape
		curShapeIdx = (curShapeIdx + 1) % 5
		curDirIdx = newDirIdx
		top = newTop
	}

	return top
}

func (d *Day17) Part1(isTest bool) int64 {
	return d.Solve(2022)
}

func (d *Day17) Part2(isTest bool) int64 {
	return d.Solve(1000000000000)
}
