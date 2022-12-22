package d22

import (
	"fmt"
	"math"
	"regexp"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Turn string

const (
	Left  Turn = "L"
	Right Turn = "R"
)

type Instr struct {
	Magnitude int
	Turn      Turn
}

type Day22 struct {
	Map     map[lib.GridPoint[int]]bool
	TopLeft lib.GridPoint[int]
	MaxC    int
	MaxR    int
	Instrs  []Instr
}

func (d *Day22) LoadInput(lines []string) error {
	d.Map = map[lib.GridPoint[int]]bool{}
	for r, line := range lines {
		if line == "" {
			re := regexp.MustCompile(`(?:(\d+)|(L|R))`)
			submatches := re.FindAllStringSubmatch(lines[r+1], -1)
			for _, s := range submatches {
				if s[1] != "" {
					d.Instrs = append(d.Instrs, Instr{
						Magnitude: lib.ToInt(s[1]),
					})
				} else {
					d.Instrs = append(d.Instrs, Instr{
						Turn: Turn(s[2]),
					})
				}
			}
			break
		} else {
			found := false
			for c, char := range line {
				switch char {
				case '.':
					d.Map[lib.GridPoint[int]{R: r, C: c}] = false
					if r == 0 && !found {
						d.TopLeft = lib.GridPoint[int]{R: r, C: c}
					}
					found = true
				case '#':
					d.Map[lib.GridPoint[int]{R: r, C: c}] = true
				}
				d.MaxC = lib.Max(d.MaxC, c)
			}
			d.MaxR = lib.Max(d.MaxR, r)
		}
	}
	return nil
}

func (d *Day22) Part1(isTest bool) int {
	// You begin the path in the leftmost open tile of the top row of tiles.
	pos := d.TopLeft

	// Initially, you are facing to the right (from the perspective of how the
	// map is drawn).
	dir := lib.GridPoint[int]{R: 0, C: 1}

	// The second half is a description of the path you must follow. It consists of alternating numbers and letters:

	// * A number indicates the number of tiles to move in the direction you are
	//   facing. If you run into a wall, you stop moving forward and continue with
	//   the next instruction.
	// * A letter indicates whether to turn 90 degrees clockwise (R) or
	//   counterclockwise (L). Turning happens in-place; it does not change your
	//   current tile.

	for _, instr := range d.Instrs {
		if instr.Turn == "" {
			// num
			for x := 0; x < instr.Magnitude; x++ {
				newPos := lib.GridPoint[int]{
					R: pos.R + dir.R,
					C: pos.C + dir.C,
				}
				if _, exists := d.Map[newPos]; !exists {
					// wrap
					if dir.C == 1 { // right
						for c := 0; ; c++ {
							if _, exists := d.Map[lib.GridPoint[int]{R: newPos.R, C: c}]; exists {
								newPos = lib.GridPoint[int]{R: newPos.R, C: c}
								break
							}
						}
					} else if dir.C == -1 { // left
						for c := d.MaxC; ; c-- {
							if _, exists := d.Map[lib.GridPoint[int]{R: newPos.R, C: c}]; exists {
								newPos = lib.GridPoint[int]{R: newPos.R, C: c}
								break
							}
						}
					} else if dir.R == 1 { // down
						for r := 0; ; r++ {
							if _, exists := d.Map[lib.GridPoint[int]{R: r, C: newPos.C}]; exists {
								newPos = lib.GridPoint[int]{R: r, C: newPos.C}
								break
							}
						}
					} else if dir.R == -1 { // up
						for r := d.MaxR; ; r-- {
							if _, exists := d.Map[lib.GridPoint[int]{R: r, C: newPos.C}]; exists {
								newPos = lib.GridPoint[int]{R: r, C: newPos.C}
								break
							}
						}
					}
				}

				if wall, exists := d.Map[newPos]; exists && wall {
					break
				} else {
					pos = newPos
				}
			}
		} else if instr.Turn == Right {
			dir = lib.GridPoint[int]{
				R: dir.C,
				C: -dir.R,
			}
		} else if instr.Turn == Left {
			dir = lib.GridPoint[int]{
				R: -dir.C,
				C: dir.R,
			}
		} else {
			panic("ohe")
		}
	}

	// Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
	facingNum := 0
	if dir.C == 1 {
		facingNum = 0
	} else if dir.C == -1 {
		facingNum = 2
	} else if dir.R == 1 {
		facingNum = 1
	} else {
		facingNum = 3
	}

	// The final password is the sum of 1000 times the row, 4 times the column, and the facing.
	return (pos.R+1)*1000 + (pos.C+1)*4 + facingNum
}

func (d *Day22) Part2(isTest bool) int {
	var ans int

	sidelen := int(math.Sqrt(float64(len(d.Map) / 6)))
	fmt.Printf("sidelen %d\n", sidelen)

	// Form the groups
	// sides := map[lib.GridPoint[int]](func(pos, dir lib.GridPoint[int]) (lib.GridPoint[int], lib.GridPoint[int])){}
	// for rowgroup := 0; rowgroup < d.MaxR; rowgroup += sidelen {
	// 	for colgroup := 0; colgroup < d.MaxC; colgroup += sidelen {
	// 		if _, exists := d.Map[lib.GridPoint[int]{rowgroup, colgroup}]; exists {
	// 			side := map[lib.GridPoint[int]]bool{}
	// 			for r := rowgroup; r < rowgroup+sidelen; r++ {
	// 				for c := colgroup; c < colgroup+sidelen; c++ {
	// 					side[lib.GridPoint[int]{r, c}] = d.Map[lib.GridPoint[int]{r, c}]
	// 				}
	// 			}
	// 			sides[lib.GridPoint[int]{rowgroup / sidelen, colgroup / sidelen}] = Side{Data: side}
	// 		}
	// 	}
	// }

	DirUp := lib.GridPoint[int]{R: -1, C: 0}
	DirDown := lib.GridPoint[int]{R: 1, C: 0}
	DirLeft := lib.GridPoint[int]{R: 0, C: -1}
	DirRight := lib.GridPoint[int]{R: 0, C: 1}

	nextPosDir := func(pos, dir lib.GridPoint[int]) (lib.GridPoint[int], lib.GridPoint[int]) {
		// fmt.Printf("%v %v -> ", pos, dir)
		newPos := lib.GridPoint[int]{
			R: pos.R + dir.R,
			C: pos.C + dir.C,
		}
		newDir := dir
		if _, exists := d.Map[newPos]; !exists {
			if isTest {
				panic("test")
			} else {
				// Hard coding the map
				//
				//   1 2
				//   3
				// 4 5
				// 6

				switch dir.C {
				case 1: // right
					switch newPos.R / sidelen {
					case 0:
						// @2 going right
						// Go to right of 5, going left
						newPos = lib.GridPoint[int]{R: sidelen*2 + (sidelen - 1 - newPos.R), C: sidelen*2 - 1}
						newDir = DirLeft
					case 1:
						// @3 going right
						// Go to bottom of 2, going up
						newPos = lib.GridPoint[int]{R: sidelen - 1, C: newPos.R + sidelen}
						newDir = DirUp
					case 2:
						// @5 going right
						// Go to right of 2, going left
						newPos = lib.GridPoint[int]{R: sidelen*3 - 1 - newPos.R, C: sidelen*3 - 1}
						newDir = DirLeft
					case 3:
						// @6 going right
						// Go to bottom of 5, going up
						newPos = lib.GridPoint[int]{R: 3*sidelen - 1, C: newPos.R - 2*sidelen}
						newDir = DirUp
					}
				case -1: // left
					switch newPos.R / sidelen {
					case 0:
						// @1 going left
						// Go to right of 4, going right
						newPos = lib.GridPoint[int]{R: 3*sidelen - 1 - newPos.R, C: 0}
						newDir = DirRight
					case 1:
						// @3 going left
						// Go to top of 4, going down
						newPos = lib.GridPoint[int]{R: 2 * sidelen, C: newPos.R - sidelen}
						newDir = DirDown
					case 2:
						// @4 going left
						// Go to left of 1, going right
						newPos = lib.GridPoint[int]{R: 3*sidelen - 1 - newPos.R, C: sidelen}
						newDir = DirRight
					case 3:
						// @6 going left
						// Go to top of 1, going down
						newPos = lib.GridPoint[int]{R: 0, C: newPos.R - sidelen*2}
						newDir = DirDown
					}
				}
				switch dir.R {
				case 1: // down
					switch newPos.C / sidelen {
					case 0:
						// @6 going down
						// Go to 2 going down
						newPos = lib.GridPoint[int]{R: 0, C: newPos.C + sidelen*2}
						newDir = DirDown
					case 1:
						// @5 going down
						// Go to 6 going left
						newPos = lib.GridPoint[int]{R: newPos.C + 2*sidelen, C: sidelen - 1}
						newDir = DirLeft
					case 2:
						// @2 going down
						// Go to right of 3 going left
						newPos = lib.GridPoint[int]{R: newPos.C - sidelen, C: sidelen*2 - 1}
						newDir = DirLeft
					}
				case -1: // up
					switch newPos.C / sidelen {
					case 0:
						// @4 going up
						// Go to left of 3 going right
						newPos = lib.GridPoint[int]{R: newPos.C + sidelen, C: sidelen}
						newDir = DirRight
					case 1:
						// @1 going up
						// Go to left of 6 going right
						newPos = lib.GridPoint[int]{R: newPos.C + 2*sidelen, C: 0}
						newDir = DirRight
					case 2:
						// @2 going up
						// Go to bottom of 6 going up
						newPos = lib.GridPoint[int]{R: sidelen*4 - 1, C: newPos.C - 2*sidelen}
						newDir = DirUp
					}
				}
				// fmt.Printf(">>>>>>>>>>%v %v\n", pos, dir)
				// fmt.Printf(">>>>>>>>>>%v %v\n", pos.R/sidelen, pos.C/sidelen)
				// panic("fail!")
			}
		}
		if val, exists := d.Map[newPos]; !exists {
			panic("shouldn't happen")
		} else if val {
			fmt.Printf("%v %v\n", pos, dir)
			fmt.Printf("blocked\n")
			return pos, dir
		} else {
			fmt.Printf("%v %v\n", pos, dir)
			return newPos, newDir
		}
	}

	// 	sideq := []lib.GridPoint[int]{lib.GridPoint[int]{0, 0}}
	// 	positioned := ds.Set[lib.GridPoint[int]]{}
	// 	for len(sideq) > 0 {
	// 		cur := sideq[0]
	// 		sideq = sideq[1:]
	// 		fmt.Printf("cur %v\n", cur)

	// 	}

	// for sidePos, sideDat := range sides {
	// 	newSideDat := sideDat
	// 	// calculate right
	// 	if _, exists := sides[lib.GridPoint[int]{sidePos.R, sidePos.C + 1}]; exists {
	// 		// has right
	// 		sideDat.Right = SideAdj{
	// 			SidePos:        lib.GridPoint[int]{sidePos.R, sidePos.C + 1},
	// 			NewDir:         lib.GridPoint[int]{0, 1}, // keep going right
	// 			PointTransform: func(p lib.GridPoint[int]) lib.GridPoint[int] { return p },
	// 		}
	// 	}

	// 	fmt.Printf("%v %v\n", sidePos, sideDat)
	// 	// for r := rowgroup; r < rowgroup+sidelen; r++ {
	// 	// 	for c := colgroup; c < colgroup+sidelen; c++ {
	// 	// 		if val, exists := d.Map[lib.GridPoint[int]{r, c}]; !exists {
	// 	// 			fmt.Printf(" ")
	// 	// 		} else if val {
	// 	// 			fmt.Printf("#")
	// 	// 		} else {
	// 	// 			fmt.Printf(".")
	// 	// 		}
	// 	// 	}
	// 	// 	fmt.Printf("\n")
	// 	// }
	// 	// fmt.Printf("====\n")
	// }

	// You begin the path in the leftmost open tile of the top row of tiles.
	pos := d.TopLeft

	// Initially, you are facing to the right (from the perspective of how the
	// map is drawn).
	dir := lib.GridPoint[int]{R: 0, C: 1}

	for i, instr := range d.Instrs {
		fmt.Printf(">>>>>>>>>>%d %v<<<<<<<<\n", i, instr)
		// for r := 0; r < d.MaxR; r++ {
		// 	for c := 0; c < d.MaxC; c++ {
		// 		if pos.R == r && pos.C == c {
		// 			switch dir.C {
		// 			case -1:
		// 				fmt.Printf(lib.ColorString("<", lib.ColorRed))
		// 			case 1:
		// 				fmt.Printf(lib.ColorString(">", lib.ColorRed))
		// 			default:
		// 				switch dir.R {
		// 				case -1:
		// 					fmt.Printf(lib.ColorString("^", lib.ColorRed))
		// 				case 1:
		// 					fmt.Printf(lib.ColorString("v", lib.ColorRed))
		// 				}
		// 			}
		// 		} else if val, exists := d.Map[lib.GridPoint[int]{r, c}]; !exists {
		// 			fmt.Printf(" ")
		// 		} else if val {
		// 			fmt.Printf("#")
		// 		} else {
		// 			fmt.Printf(".")
		// 		}
		// 	}
		// 	fmt.Printf("\n")
		// }
		if instr.Turn == "" {
			fmt.Printf(">>>>>>>>>>\n")
			// num
			for x := 0; x < instr.Magnitude; x++ {
				newPos, newDir := nextPosDir(pos, dir)
				if newPos == pos {
					break
				} else {
					pos = newPos
					dir = newDir
				}
			}
		} else if instr.Turn == Right {
			fmt.Printf("TURN RIGHT\n")
			dir = lib.GridPoint[int]{
				R: dir.C,
				C: -dir.R,
			}
		} else if instr.Turn == Left {
			fmt.Printf("TURN LEFT\n")
			dir = lib.GridPoint[int]{
				R: -dir.C,
				C: dir.R,
			}
		} else {
			panic("ohe")
		}
		// for r := 0; r < d.MaxR; r++ {
		// 	for c := 0; c < d.MaxC; c++ {
		// 		if pos.R == r && pos.C == c {
		// 			switch dir.C {
		// 			case -1:
		// 				fmt.Printf(lib.ColorString("<", lib.ColorRed))
		// 			case 1:
		// 				fmt.Printf(lib.ColorString(">", lib.ColorRed))
		// 			default:
		// 				switch dir.R {
		// 				case -1:
		// 					fmt.Printf(lib.ColorString("^", lib.ColorRed))
		// 				case 1:
		// 					fmt.Printf(lib.ColorString("v", lib.ColorRed))
		// 				}
		// 			}
		// 		} else if val, exists := d.Map[lib.GridPoint[int]{r, c}]; !exists {
		// 			fmt.Printf(" ")
		// 		} else if val {
		// 			fmt.Printf("#")
		// 		} else {
		// 			fmt.Printf(".")
		// 		}
		// 	}
		// 	fmt.Printf("\n")
		// }
		// if i == 10 {
		// 	break
		// }
	}

	// Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
	facingNum := 0
	if dir.C == 1 {
		facingNum = 0
	} else if dir.C == -1 {
		facingNum = 2
	} else if dir.R == 1 {
		facingNum = 1
	} else {
		facingNum = 3
	}

	// The final password is the sum of 1000 times the row, 4 times the column, and the facing.
	fmt.Printf("ANS:%d\n", (pos.R+1)*1000+(pos.C+1)*4+facingNum)
	return (pos.R+1)*1000 + (pos.C+1)*4 + facingNum

	return ans
}

// The first half of the monkeys' notes is a map of the board. It is comprised
// of a set of open tiles (on which you can move, drawn .) and solid walls
// (tiles which you cannot enter, drawn #).

// So, a path like 10R5 means "go forward 10 tiles, then turn clockwise 90 degrees, then go forward 5 tiles".
