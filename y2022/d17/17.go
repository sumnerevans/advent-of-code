package d17

import (
	"fmt"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

// shapes
// ####

// .#.
// ###
// .#.

// ..#
// ..#
// ###

// #
// #
// #
// #

// ##
// ##

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

func (d *Day17) Part1(isTest bool) int64 {
	return d.Solve(2022)
	seq := []Shape{Line, Cross, Ell, Bar, Square}

	chamber := ds.Set[lib.GridPoint[int64]]{}

	// The tall, vertical chamber is exactly seven units wide. Each rock
	// appears so that its left edge is two units away from the left wall and
	// its bottom edge is three units above the highest rock in the room (or
	// the floor, if there isn't one).

	var top int64
	x := 0
	for i := 0; i < 2022; i++ {
		shape := seq[i%len(seq)]
		shapeBottomLeftPos := lib.GridPoint[int64]{R: top + 3, C: 2}
		for {
			// fmt.Printf("x %d\n", x)
			// PrintChamberWithShape(chamber, shape, shapeBottomLeftPos)
			// Direction
			var newPos lib.GridPoint[int64]
			switch d.Dirs[x%len(d.Dirs)] {
			case Left:
				// fmt.Printf("L\n")
				newPos = lib.GridPoint[int64]{R: shapeBottomLeftPos.R, C: shapeBottomLeftPos.C - 1}
			case Right:
				// fmt.Printf("R\n")
				newPos = lib.GridPoint[int64]{R: shapeBottomLeftPos.R, C: shapeBottomLeftPos.C + 1}
			default:
				panic("fail")
			}
			// fmt.Printf("DIR %v\n", shapeBottomLeftPos)
			// fmt.Printf("%v %v %v\n", !shape.Intersects(newPos, chamber), newPos.C >= 0, newPos.C+len(shape[0]) <= 7)
			if !shape.Intersects(newPos, chamber) && newPos.C >= 0 && newPos.C+int64(len(shape[0])) <= 7 {
				// fmt.Printf("Rock moves %d horizontally\n", int(d.Dirs[x%len(d.Dirs)]))
				// fmt.Printf("--> %v\n", newPos)
				shapeBottomLeftPos = newPos
			} else {
				// fmt.Printf("Rock doesn't move horizontally\n")
			}
			x++
			// PrintChamberWithShape(chamber, shape, shapeBottomLeftPos)

			// fmt.Printf("Rock falls one unit\n")
			// Down
			newPos = lib.GridPoint[int64]{R: shapeBottomLeftPos.R - 1, C: shapeBottomLeftPos.C}
			if shape.Intersects(newPos, chamber) || newPos.R < 0 {
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
		top = lib.MaxListFn(chamber.List(), func(gp lib.GridPoint[int64]) int64 {
			return gp.R + 1
		})
	}

	return top
}

type FloorShape struct {
	Space1 int64
	Space2 int64
	Space3 int64
	Space4 int64
	Space5 int64
	Space6 int64
	Space7 int64
}

func (fs FloorShape) Print() {
	var i int64
	for ; i < lib.MaxList([]int64{fs.Space1, fs.Space2, fs.Space3, fs.Space4, fs.Space5, fs.Space6, fs.Space7})+1; i++ {
		if fs.Space1 < i {
			fmt.Printf("#")
		} else {
			fmt.Printf(" ")
		}
		if fs.Space2 < i {
			fmt.Printf("#")
		} else {
			fmt.Printf(" ")
		}
		if fs.Space3 < i {
			fmt.Printf("#")
		} else {
			fmt.Printf(" ")
		}
		if fs.Space4 < i {
			fmt.Printf("#")
		} else {
			fmt.Printf(" ")
		}
		if fs.Space5 < i {
			fmt.Printf("#")
		} else {
			fmt.Printf(" ")
		}
		if fs.Space6 < i {
			fmt.Printf("#")
		} else {
			fmt.Printf(" ")
		}
		if fs.Space7 < i {
			fmt.Printf("#")
		} else {
			fmt.Printf(" ")
		}
		fmt.Printf("\n")
	}
}

type FloorShapeDelta struct {
	FloorShape FloorShape
	DR         int64
	SeqIdx     int
	DI         int64
}

func (d *Day17) Solve(iters int64) int64 {
	seq := []Shape{Line, Cross, Ell, Bar, Square}

	// The tall, vertical chamber is exactly seven units wide. Each rock
	// appears so that its left edge is two units away from the left wall and
	// its bottom edge is three units above the highest rock in the room (or
	// the floor, if there isn't one).

	var top int64
	var curDirIdx int

	var hits, misses int64

	floorShapePerIdx := map[FloorShape]map[int]map[int]FloorShapeDelta{}

	currentFloorShape := FloorShape{1, 1, 1, 1, 1, 1, 1}
	curSeqIdx := 0
	var i int64
	for ; i < iters; i++ {
		if i%10000 == 0 {
			fmt.Printf("i=%d\n", i)
			fmt.Printf("   hits %d, misses %d\n", hits, misses)
		}
		// if perSeqID, ok := floorShapePerIdx[currentFloorShape]; ok {
		// 	if perDir, ok := perSeqID[curSeqIdx]; ok {
		// 		if next, ok := perDir[dirIdx]; ok {
		// 			// fmt.Printf("hit %v, %d -> %v\n", currentFloorShape, curSeqIdx, next)
		// 			// currentFloorShape.Print()
		// 			// next.FloorShape.Print()

		// 			i += next.DI
		// 			hits++
		// 			top += next.DR
		// 			currentFloorShape = next.FloorShape
		// 			curSeqIdx = next.SeqIdx

		// 			// break
		// 			continue
		// 		}
		// 	}
		// }

		// fmt.Printf("Unknown combination of floor shape and sequence index\n")
		misses++

		shape := seq[curSeqIdx]

		// fmt.Printf("cfs %v\n", currentFloorShape)
		chamber := ds.Set[lib.GridPoint[int64]]{}
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space1, C: 0})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space2, C: 1})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space3, C: 2})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space4, C: 3})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space5, C: 4})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space6, C: 5})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space7, C: 6})

		shapeBottomLeftPos := lib.GridPoint[int64]{R: top + 3, C: 2}
		newDirIdx := curDirIdx
		for {
			// fmt.Printf("x %d\n", shape)
			// fmt.Printf("START\n")
			// PrintChamberWithShape(chamber, shape, shapeBottomLeftPos)
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
			if shape.Intersects(newPos, chamber) || newPos.R < 0 {
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
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 0}) {
				newFloorShape.Space1 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 1}) {
				newFloorShape.Space2 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 2}) {
				newFloorShape.Space3 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 3}) {
				newFloorShape.Space4 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 4}) {
				newFloorShape.Space5 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 5}) {
				newFloorShape.Space6 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 6}) {
				newFloorShape.Space7 = int64(dr)
				break
			}
		}
		// fmt.Printf("%v\n", newFloorShape)
		if _, ok := floorShapePerIdx[currentFloorShape]; !ok {
			floorShapePerIdx[currentFloorShape] = map[int]map[int]FloorShapeDelta{}
		}
		if _, ok := floorShapePerIdx[currentFloorShape][curSeqIdx]; !ok {
			floorShapePerIdx[currentFloorShape][curSeqIdx] = map[int]FloorShapeDelta{}
		}

		fsd := FloorShapeDelta{
			FloorShape: newFloorShape,
			DR:         newTop - top,
			DI:         0,
			SeqIdx:     (curSeqIdx + 1) % 5,
		}
		// for {
		// 	if fsm, ok1 := floorShapePerIdx[fsd.FloorShape]; ok1 {
		// 		if delta, ok2 := fsm[(curSeqIdx+1)%5]; ok2 {
		// 			fsd.FloorShape = delta.FloorShape
		// 			fsd.DR += delta.DR
		// 			fsd.DI = delta.DI + 1
		// 			fsd.SeqIdx = delta.SeqIdx
		// 		} else {
		// 			break
		// 		}
		// 	} else {
		// 		break
		// 	}
		// }

		floorShapePerIdx[currentFloorShape][curSeqIdx][curDirIdx] = fsd
		currentFloorShape = newFloorShape
		curSeqIdx = (curSeqIdx + 1) % 5
		curDirIdx = newDirIdx
		top = newTop

		// fmt.Printf("%v\n", floorShapePerIdx)
		// if i >= 2 {
		// 	break
		// }
	}
	fmt.Printf("Hits: %d\n", hits)
	fmt.Printf("Misses: %d\n", misses)

	return top
}
func (d *Day17) Part2(isTest bool) int64 {
	return d.Solve(1000000000000)
	seq := []Shape{Line, Cross, Ell, Bar, Square}

	// The tall, vertical chamber is exactly seven units wide. Each rock
	// appears so that its left edge is two units away from the left wall and
	// its bottom edge is three units above the highest rock in the room (or
	// the floor, if there isn't one).

	var top int64
	var dirIdx int

	var hits, misses int64

	floorShapePerIdx := map[FloorShape]map[int]FloorShapeDelta{}

	currentFloorShape := FloorShape{1, 1, 1, 1, 1, 1, 1}
	curSeqIdx := 0
	var i int64
	for ; i < 1000000000000; i++ {
		if i%100000000 == 0 {
			fmt.Printf("i=%d\n", i)
			fmt.Printf("   hits %d, misses %d\n", hits, misses)
		}
		if perSeqID, ok := floorShapePerIdx[currentFloorShape]; ok {
			if next, ok := perSeqID[curSeqIdx]; ok {
				i += next.DI
				hits++
				top += next.DR
				currentFloorShape = next.FloorShape
				curSeqIdx = next.SeqIdx
				continue
			}
		}

		// fmt.Printf("Unknown combination of floor shape and sequence index\n")
		misses++

		shape := seq[curSeqIdx]

		// fmt.Printf("cfs %v\n", currentFloorShape)
		chamber := ds.Set[lib.GridPoint[int64]]{}
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space1, C: 0})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space2, C: 1})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space3, C: 2})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space4, C: 3})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space5, C: 4})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space6, C: 5})
		chamber.Add(lib.GridPoint[int64]{R: top - currentFloorShape.Space7, C: 6})

		shapeBottomLeftPos := lib.GridPoint[int64]{R: top + 3, C: 2}
		for {
			// fmt.Printf("x %d\n", shape)
			// fmt.Printf("START\n")
			// PrintChamberWithShape(chamber, shape, shapeBottomLeftPos)
			// Direction
			var newPos lib.GridPoint[int64]
			switch d.Dirs[dirIdx] {
			case Left:
				// fmt.Printf("L\n")
				newPos = lib.GridPoint[int64]{R: shapeBottomLeftPos.R, C: shapeBottomLeftPos.C - 1}
			case Right:
				// fmt.Printf("R\n")
				newPos = lib.GridPoint[int64]{R: shapeBottomLeftPos.R, C: shapeBottomLeftPos.C + 1}
			default:
				panic("fail")
			}
			// fmt.Printf("DIR %v\n", shapeBottomLeftPos)
			// fmt.Printf("%v %v %v\n", !shape.Intersects(newPos, chamber), newPos.C >= 0, newPos.C+len(shape[0]) <= 7)
			if !shape.Intersects(newPos, chamber) && newPos.C >= 0 && newPos.C+int64(len(shape[0])) <= 7 {
				// fmt.Printf("Rock moves %d horizontally\n", int(d.Dirs[x%len(d.Dirs)]))
				// fmt.Printf("--> %v\n", newPos)
				shapeBottomLeftPos = newPos
			} else {
				// fmt.Printf("Rock doesn't move horizontally\n")
			}
			dirIdx = (dirIdx + 1) % len(d.Dirs)
			// PrintChamberWithShape(chamber, shape, shapeBottomLeftPos)

			// fmt.Printf("Rock falls one unit\n")
			// Down
			newPos = lib.GridPoint[int64]{R: shapeBottomLeftPos.R - 1, C: shapeBottomLeftPos.C}
			if shape.Intersects(newPos, chamber) || newPos.R < 0 {
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
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 0}) {
				newFloorShape.Space1 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 1}) {
				newFloorShape.Space2 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 2}) {
				newFloorShape.Space3 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 3}) {
				newFloorShape.Space4 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 4}) {
				newFloorShape.Space5 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 5}) {
				newFloorShape.Space6 = int64(dr)
				break
			}
		}
		for dr := 0; ; dr++ {
			if chamber.Contains(lib.GridPoint[int64]{R: newTop - int64(dr), C: 6}) {
				newFloorShape.Space7 = int64(dr)
				break
			}
		}
		// fmt.Printf("%v\n", newFloorShape)
		if _, ok := floorShapePerIdx[currentFloorShape]; !ok {
			floorShapePerIdx[currentFloorShape] = map[int]FloorShapeDelta{}
		}

		fsd := FloorShapeDelta{
			FloorShape: newFloorShape,
			DR:         newTop - top,
			DI:         0,
			SeqIdx:     (curSeqIdx + 1) % 5,
		}
		for {
			if fsm, ok1 := floorShapePerIdx[fsd.FloorShape]; ok1 {
				if delta, ok2 := fsm[(curSeqIdx+1)%5]; ok2 {
					fsd.FloorShape = delta.FloorShape
					fsd.DR += delta.DR
					fsd.DI = delta.DI + 1
					fsd.SeqIdx = delta.SeqIdx
				} else {
					break
				}
			} else {
				break
			}
		}

		floorShapePerIdx[currentFloorShape][curSeqIdx] = fsd
		curSeqIdx = (curSeqIdx + 1) % 5
		currentFloorShape = newFloorShape
		top = newTop

		// if i >= 0 {
		// 	break
		// }
	}
	fmt.Printf("Hits: %d\n", hits)
	fmt.Printf("Misses: %d\n", misses)

	return top
}
