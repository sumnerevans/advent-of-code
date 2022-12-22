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

	// You begin the path in the leftmost open tile of the top row of tiles.
	pos := d.TopLeft

	// Initially, you are facing to the right (from the perspective of how the
	// map is drawn).
	dir := lib.GridPoint[int]{R: 0, C: 1}

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

	nextPosDir := func(pos, dir lib.GridPoint[int]) (lib.GridPoint[int], lib.GridPoint[int]) {
		fmt.Printf("%v %v -> ", pos, dir)
		newPos := lib.GridPoint[int]{
			R: pos.R + dir.R,
			C: pos.C + dir.C,
		}
		if val, exists := d.Map[newPos]; !exists {
			if isTest {
				fmt.Printf("%v %v\n", newPos, dir)
				panic("test")
			} else {
				panic("not done")
			}
		} else if val {
			return pos, dir
		} else {
			return newPos, dir
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

	for _, instr := range d.Instrs {
		if instr.Turn == "" {
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

	return ans
}

// The first half of the monkeys' notes is a map of the board. It is comprised
// of a set of open tiles (on which you can move, drawn .) and solid walls
// (tiles which you cannot enter, drawn #).

// So, a path like 10R5 means "go forward 10 tiles, then turn clockwise 90 degrees, then go forward 5 tiles".
