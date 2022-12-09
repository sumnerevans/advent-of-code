package d09

import (
	"fmt"
	"strings"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Command struct {
	Dir       lib.Point[int]
	Magnitude int
}

type Day09 struct {
	Commands []Command
}

func (d *Day09) LoadInput(lines []string) error {
	for _, line := range lines {
		fs := strings.Fields(line)
		var dir lib.Point[int]
		switch fs[0] {
		case "U":
			dir = lib.Point[int]{0, 1}
		case "R":
			dir = lib.Point[int]{1, 0}
		case "L":
			dir = lib.Point[int]{-1, 0}
		case "D":
			dir = lib.Point[int]{0, -1}
		}
		d.Commands = append(d.Commands, Command{dir, lib.ToInt(fs[1])})
	}
	return nil
}

var Quads = map[int]lib.Point[int]{
	1: lib.Point[int]{1, 1},
	2: lib.Point[int]{-1, 1},
	3: lib.Point[int]{-1, -1},
	4: lib.Point[int]{1, -1},
}

func PrintGrid(head, tail lib.Point[int]) {
	maxX := lib.Max(head.X, tail.X)
	maxY := lib.Max(head.Y, tail.Y)
	for y := maxY; y >= 0; y-- {
		for x := 0; x <= maxX; x++ {
			if head.X == x && head.Y == y {
				fmt.Print("H")
			} else if tail.X == x && tail.Y == y {
				fmt.Print("T")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Printf("\n")
	}
}

func (d *Day09) Part1() int {
	visited := ds.Set[lib.Point[int]]{}
	var head, tail lib.Point[int]
	visited.Add(tail)

	for _, c := range d.Commands {
		for i := 0; i < c.Magnitude; i++ {
			head.X += c.Dir.X
			head.Y += c.Dir.Y

			if tail.Y == head.Y {
				if tail.X < head.X-1 {
					tail.X++
				} else if head.X+1 < tail.X {
					tail.X--
				}
			} else if tail.X == head.X {
				if tail.Y < head.Y-1 {
					tail.Y++
				} else if head.Y+1 < tail.Y {
					tail.Y--
				}
			} else {
				if lib.AbsInt(head.X-tail.X)+lib.AbsInt(head.Y-tail.Y) <= 2 {
					continue
				}

				if head.X > tail.X && head.Y > tail.Y {
					// 1st quad
					tail.X += Quads[1].X
					tail.Y += Quads[1].Y
				}
				if head.X < tail.X && head.Y > tail.Y {
					// 2st quad
					tail.X += Quads[2].X
					tail.Y += Quads[2].Y
				}
				if head.X < tail.X && head.Y < tail.Y {
					// 3rd quad
					tail.X += Quads[3].X
					tail.Y += Quads[3].Y
				}
				if head.X > tail.X && head.Y < tail.Y {
					// 1st quad
					tail.X += Quads[4].X
					tail.Y += Quads[4].Y
				}
			}

			visited.Add(tail)
		}
	}
	return len(visited)
}

func (d *Day09) Part2() int {
	var ans int

	visited := ds.Set[lib.Point[int]]{}
	rope := []lib.Point[int]{
		{0, 0},
		{0, 0},
		{0, 0},
		{0, 0},
		{0, 0},
		{0, 0},
		{0, 0},
		{0, 0},
		{0, 0},
		{0, 0},
	}
	visited.Add(lib.Point[int]{0, 0})

	for _, c := range d.Commands {
		for i := 0; i < c.Magnitude; i++ {
			rope[0].X += c.Dir.X
			rope[0].Y += c.Dir.Y
			for seg := 0; seg < 9; seg++ {
				leader := rope[seg]
				follower := rope[seg+1]

				if follower.Y == leader.Y {
					if follower.X < leader.X-1 {
						follower.X++
					} else if leader.X+1 < follower.X {
						follower.X--
					}
				} else if follower.X == leader.X {
					if follower.Y < leader.Y-1 {
						follower.Y++
					} else if leader.Y+1 < follower.Y {
						follower.Y--
					}
				} else {
					if lib.AbsInt(leader.X-follower.X)+lib.AbsInt(leader.Y-follower.Y) <= 2 {
						continue
					}

					if leader.X > follower.X && leader.Y > follower.Y {
						// 1st quad
						follower.X += Quads[1].X
						follower.Y += Quads[1].Y
					}
					if leader.X < follower.X && leader.Y > follower.Y {
						// 2st quad
						follower.X += Quads[2].X
						follower.Y += Quads[2].Y
					}
					if leader.X < follower.X && leader.Y < follower.Y {
						// 3rd quad
						follower.X += Quads[3].X
						follower.Y += Quads[3].Y
					}
					if leader.X > follower.X && leader.Y < follower.Y {
						// 1st quad
						follower.X += Quads[4].X
						follower.Y += Quads[4].Y
					}
				}
				rope[seg].X = leader.X
				rope[seg].Y = leader.Y
				rope[seg+1].X = follower.X
				rope[seg+1].Y = follower.Y
			}

			visited.Add(rope[len(rope)-1])
		}
	}
	return len(visited)

	return ans
}
