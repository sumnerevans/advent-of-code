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
						fmt.Printf("GOT HERE %d %d\n", prevIdx, i)
						fmt.Printf("%v\n", currentFloorShape)
						fmt.Printf("%v\n", shapes[curShapeIdx])
						fmt.Printf("%v\n", d.Dirs[curDirIdx])
						fmt.Printf("curtop %d\n", top)
						fmt.Printf("prvtop %d\n", prevIdx.Top)
						fmt.Printf("curidx %d\n", i)
						fmt.Printf("prvidx %d\n", prevIdx.Idx)

						di := i - prevIdx.Idx
						fmt.Printf("di %d\n", di)
						fmt.Printf("i+di %d %d\n", i+di, iters)
						if i+di < iters {
							cycleCount := (iters - i) / di
							fmt.Printf("cycles %d\n", cycleCount)
							fmt.Printf("dt %d\n", top-prevIdx.Top)
							top += cycleCount * (top - prevIdx.Top)
							i += cycleCount*di - 1 // the -1 here is because we re-add it in the for-loop
							fmt.Printf("NEW i=%d\n", i)
							foundCycle = true
							continue
						}
					}
				}
			}
		}

		// fmt.Printf("Unknown combination of floor shape and sequence index\n")

		shape := shapes[curShapeIdx]

		// fmt.Printf("cfs %v\n", currentFloorShape)
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
			// fmt.Printf("x %d\n", shape)
			// fmt.Printf("START\n")
			// fmt.Printf("\n")
			if shapeBottomLeftPos.R < top-int64(ROWS) {
				PrintChamberWithShape(chamber, shape, shapeBottomLeftPos)
				panic("falling!")
			}

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
			// fmt.Printf("DIR %v\n", shapeBottomLeftPos)
			// fmt.Printf("%v %v %v\n", !shape.Intersects(newPos, chamber), newPos.C >= 0, newPos.C+len(shape[0]) <= 7)
			if !shape.Intersects(newPos, chamber) && newPos.C >= 0 && newPos.C+int64(len(shape[0])) <= 7 {
				// fmt.Printf("Rock moves %d horizontally\n", int(d.Dirs[x%len(d.Dirs)]))
				// fmt.Printf("--> %v\n", newPos)
				shapeBottomLeftPos = newPos
			} else {
				// fmt.Printf("Rock doesn't move horizontally\n")
			}
			// PrintChamberWithShape(chamber, shape, shapeBottomLeftPos)

			// fmt.Printf("Rock falls one unit\n")
			// Down
			newPos = lib.GridPoint[int64]{R: shapeBottomLeftPos.R - 1, C: shapeBottomLeftPos.C}
			// fmt.Printf("%v %v\n", chamber, newPos)
			// if newPos.R < -10{panic("ohea")}
			if shape.Intersects(newPos, chamber) {
				// fmt.Printf("... and comes to rest\n")
				break
			} else {
				// fmt.Printf("-> %v\n", newPos)
				shapeBottomLeftPos = newPos
			}
			// PrintChamberWithShape(chamber, shape, shapeBottomLeftPos)
		}

		// fmt.Printf("PLACE %v\n", shapeBottomLeftPos)
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

		// fmt.Printf("chamber %v\n", chamber)
		// for r := top; r >= 0; r-- {
		// 	fmt.Printf("|")
		// 	for c := 0; c < 7; c++ {
		// 		if chamber.Contains(lib.GridPoint[int]{R: r, C: c}) {
		// 			fmt.Printf("#")
		// 		} else {
		// 			fmt.Printf(".")
		// 		}
		// 	}
		// 	fmt.Printf("|\n")
		// }

		newFloorShape := FloorShape{}
		for dr := 0; dr < ROWS; dr++ {
			for c := 0; c < 7; c++ {
				if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: int64(c)}) {
					newFloorShape[dr][c] = true
				}
			}
		}
		// if newFloorShape.Space1.Cmp(big.NewInt(0)) == 0 || newFloorShape.Space2.Cmp(big.NewInt(0)) == 0 || newFloorShape.Space3.Cmp(big.NewInt(0)) == 0 || newFloorShape.Space4.Cmp(big.NewInt(0)) == 0 || newFloorShape.Space5.Cmp(big.NewInt(0)) == 0 || newFloorShape.Space6.Cmp(big.NewInt(0)) == 0 || newFloorShape.Space7.Cmp(big.NewInt(0)) == 0 {
		// 	fmt.Printf("%v\n", newFloorShape)
		// 	panic("something bad happened!")
		// }
		// fmt.Printf("%v\n", newFloorShape)
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

		// fmt.Printf("%v\n", floorShapePerIdx)
		// if i >= 2 {
		// 	break
		// }
	}

	return top
}

func (d *Day17) Part1(isTest bool) int64 {
	return d.Solve(2022)
}

func (d *Day17) Part2(isTest bool) int64 {
	return d.Solve(1000000000000)
}
