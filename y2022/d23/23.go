package d23

import (
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day23 struct {
	Map ds.Set[lib.GridPoint[int]]
}

func (d *Day23) LoadInput(lines []string) error {
	d.Map = ds.Set[lib.GridPoint[int]]{}
	for r, line := range lines {
		for c, char := range line {
			if char == '#' {
				d.Map.Add(lib.NewGridPoint(r, c))
			}
		}
	}
	return nil
}

func (d *Day23) Round(i int, poses ds.Set[lib.GridPoint[int]]) ds.Set[lib.GridPoint[int]] {
	// The Elves follow a time-consuming process to figure out where they
	// should each go; you can speed up this process considerably. The process
	// consists of some number of rounds during which Elves alternate between
	// considering where to move and actually moving.

	// During the first half of each round, each Elf considers the eight
	// positions adjacent to themself.
	proposals := map[lib.GridPoint[int]]lib.GridPoint[int]{}

	// Otherwise, the Elf looks in each of four directions in the following
	// order and proposes moving one step in the first valid direction:
	newPoses := ds.Set[lib.GridPoint[int]]{}
	for pose := range poses {
		// If no other Elves are in one of those eight positions, the Elf does not
		// do anything during this round.
		surrounds := false
		for dr := -1; dr <= 1; dr++ {
			for dc := -1; dc <= 1; dc++ {
				if dr == 0 && dc == 0 {
					continue
				}
				if poses.Contains(lib.NewGridPoint(pose.R+dr, pose.C+dc)) {
					surrounds = true
					break
				}
			}
		}
		if !surrounds {
			// Nobody in either four directions.
			newPoses.Add(pose)
			continue
		}

		// Finally, at the end of the round, the first direction the Elves
		// considered is moved to the end of the list of directions. For
		// example, during the second round, the Elves would try proposing a
		// move to the south first, then west, then east, then north. On the
		// third round, the Elves would first consider west, then east, then
		// north, then south.
		considers := []struct {
			dr  []int
			dc  []int
			dir lib.GridPoint[int]
		}{
			{[]int{-1}, []int{-1, 0, 1}, lib.NewGridPoint(-1, 0)}, // North
			{[]int{1}, []int{-1, 0, 1}, lib.NewGridPoint(1, 0)},   // South
			{[]int{-1, 0, 1}, []int{-1}, lib.NewGridPoint(0, -1)}, // West
			{[]int{-1, 0, 1}, []int{1}, lib.NewGridPoint(0, 1)},   // East
		}

		proposed := false
		for j := 0; j < 4; j++ {
			consider := considers[(j+i)%4]
			open := true
			for _, dr := range consider.dr {
				for _, dc := range consider.dc {
					if poses.Contains(lib.NewGridPoint(pose.R+dr, pose.C+dc)) {
						open = false
						break
					}
				}
			}
			if open {
				proposals[pose] = lib.NewGridPoint(pose.R+consider.dir.R, pose.C+consider.dir.C)
				proposed = true
				break
			}
		}
		if !proposed {
			newPoses.Add(pose)
		}
	}

	// After each Elf has had a chance to propose a move, the second half of
	// the round can begin. Simultaneously, each Elf moves to their proposed
	// destination tile if they were the only Elf to propose moving to that
	// position. If two or more Elves propose moving to the same position, none
	// of those Elves move.
	overlaps := map[lib.GridPoint[int]]int{}
	for _, proposal := range proposals {
		overlaps[proposal]++
	}
	for elf, proposal := range proposals {
		if overlaps[proposal] == 1 {
			newPoses.Add(proposal)
		} else {
			newPoses.Add(elf)
		}
	}
	return newPoses
}

func (d *Day23) Part1(isTest bool) int {
	var ans int

	poses := d.Map

	// Simulate the Elves' process and find the smallest rectangle that
	// contains the Elves after 10 rounds.
	for i := 0; i < 10; i++ {
		newPoses := d.Round(i, poses)
		if poses.Equal(newPoses) {
			break
		}
		poses = newPoses
	}

	// How many empty ground tiles does that rectangle contain?
	minR, maxR := lib.MinMaxListFn(poses.List(), func(p lib.GridPoint[int]) int { return p.R })
	minC, maxC := lib.MinMaxListFn(poses.List(), func(p lib.GridPoint[int]) int { return p.C })
	for r := minR; r <= maxR; r++ {
		for c := minC; c <= maxC; c++ {
			if !poses.Contains(lib.NewGridPoint(r, c)) {
				ans++
			}
		}
	}

	return ans
}

func (d *Day23) Part2(isTest bool) int {
	poses := d.Map

	// Find the round where the elves stop moving.
	for i := 0; ; i++ {
		newPoses := d.Round(i, poses)
		if poses.Equal(newPoses) {
			return i + 1
		}
		poses = newPoses
	}
}
