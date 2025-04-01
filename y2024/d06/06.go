package d06

import (
	"sync"
	"sync/atomic"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Day06 struct {
	grid  [][]byte
	start lib.GridPoint[int]
}

func (d *Day06) LoadInput(lines []string) error {
	for r, line := range lines {
		for c, ch := range line {
			if ch == '^' {
				d.start.R = r
				d.start.C = c
			}
		}
		d.grid = append(d.grid, []byte(line))
	}
	return nil
}

func (d *Day06) Part1(isTest bool) int {
	dr := -1
	dc := 0
	cur := d.start
	visited := map[lib.GridPoint[int]]struct{}{}
	for {
		visited[cur] = struct{}{}
		if cur.R+dr >= 0 && cur.R+dr < len(d.grid) && cur.C+dc >= 0 && cur.C+dc < len(d.grid[0]) {
			if d.grid[cur.R+dr][cur.C+dc] == '#' {
				dr, dc = dc, -dr
			}
		} else {
			break
		}
		cur.R, cur.C = cur.R+dr, cur.C+dc
	}

	return len(visited)
}

func (d *Day06) hasLoopWith(addR, addC int) bool {
	dr := -1
	dc := 0
	cur := d.start
	visited := map[lib.GridPoint[int]]map[lib.GridPoint[int]]struct{}{}
	for {
		if _, ok := visited[cur]; !ok {
			visited[cur] = map[lib.GridPoint[int]]struct{}{}
		}
		if _, ok := visited[cur][lib.GridPoint[int]{dr, dc}]; ok {
			return true
		}
		visited[cur][lib.GridPoint[int]{dr, dc}] = struct{}{}

		if cur.R+dr >= 0 && cur.R+dr < len(d.grid) && cur.C+dc >= 0 && cur.C+dc < len(d.grid[0]) {
			if d.grid[cur.R+dr][cur.C+dc] == '#' || (addR == cur.R+dr && addC == cur.C+dc) {
				dr, dc = dc, -dr
			}
		} else {
			return false
		}
		cur.R, cur.C = cur.R+dr, cur.C+dc
	}
}

func (d *Day06) Part2(isTest bool) int {
	var ans int32

	var wg sync.WaitGroup
	for r := range len(d.grid) {
		for c := range len(d.grid[0]) {
			wg.Add(1)
			go func() {
				defer wg.Done()
				if d.hasLoopWith(r, c) {
					atomic.AddInt32(&ans, 1)
				}
			}()
		}
	}

	wg.Wait()

	return int(ans)
}
