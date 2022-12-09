package d09

import (
	"strings"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
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
			dir = lib.Point[int]{X: 0, Y: 1}
		case "R":
			dir = lib.Point[int]{X: 1, Y: 0}
		case "L":
			dir = lib.Point[int]{X: -1, Y: 0}
		case "D":
			dir = lib.Point[int]{X: 0, Y: -1}
		}
		d.Commands = append(d.Commands, Command{dir, lib.ToInt(fs[1])})
	}
	return nil
}

func (d *Day09) Follow(numFollowers int) int {
	visited := ds.Set[lib.Point[int]]{}
	rope := []lib.Point[int]{}
	for i := 0; i < numFollowers+1; i++ {
		rope = append(rope, lib.Point[int]{X: 0, Y: 0})
	}

	for _, c := range d.Commands {
		for i := 0; i < c.Magnitude; i++ {
			rope[0].X += c.Dir.X
			rope[0].Y += c.Dir.Y
			for seg := 0; seg < len(rope)-1; seg++ {
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
				} else if lib.AbsInt(leader.X-follower.X)+lib.AbsInt(leader.Y-follower.Y) > 2 {
					if leader.X > follower.X {
						follower.X++
					}
					if leader.Y > follower.Y {
						follower.Y++
					}
					if leader.X < follower.X {
						follower.X--
					}
					if leader.Y < follower.Y {
						follower.Y--
					}
				}
				rope[seg] = leader
				rope[seg+1] = follower
			}

			visited.Add(rope[len(rope)-1])
		}
	}

	return len(visited)
}

func (d *Day09) Part1() int {
	return d.Follow(1)
}

func (d *Day09) Part2() int {
	return d.Follow(9)
}
