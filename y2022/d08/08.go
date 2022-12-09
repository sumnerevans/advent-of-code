package d08

import (
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day08 struct {
	Grid [][]int
}

func (d *Day08) LoadInput(lines []string) error {
	for _, line := range lines {
		row := []int{}
		for _, c := range line {
			row = append(row, lib.ToInt(string(c)))
		}
		d.Grid = append(d.Grid, row)
	}
	return nil
}

func (d *Day08) Part1() int {
	visibleTrees := ds.Set[lib.Point[int]]{}

	for r, row := range d.Grid {
		curhi := -1
		for c, t := range row {
			if t > curhi {
				visibleTrees.Add(lib.Point[int]{Y: r, X: c})
				curhi = t
			}
		}
		curhi = -1
		for i := len(row) - 1; i > -1; i-- {
			if row[i] > curhi {
				visibleTrees.Add(lib.Point[int]{Y: r, X: i})
				curhi = row[i]
			}
		}
	}

	for r, row := range lib.Columns(d.Grid) {
		curhi := -1
		for c, t := range row {
			if t > curhi {
				visibleTrees.Add(lib.Point[int]{Y: c, X: r})
				curhi = t
			}
		}
		curhi = -1
		for i := len(row) - 1; i > -1; i-- {
			if row[i] > curhi {
				visibleTrees.Add(lib.Point[int]{Y: i, X: r})
				curhi = row[i]
			}
		}
	}

	return len(visibleTrees)
}

func (d *Day08) Part2() int {
	var ans int

	for r := 1; r < len(d.Grid)-1; r++ {
		for c := 1; c < len(d.Grid[0])-1; c++ {
			height := d.Grid[r][c]
			up := 0
			for cr := r - 1; cr >= 0; cr-- {
				up++
				if d.Grid[cr][c] >= height {
					break
				}
			}

			down := 0
			for cr := r + 1; cr < len(d.Grid); cr++ {
				down++
				if d.Grid[cr][c] >= height {
					break
				}
			}

			left := 0
			for cc := c - 1; cc >= 0; cc-- {
				left++
				if d.Grid[r][cc] >= height {
					break
				}
			}

			right := 0
			for cc := c + 1; cc < len(d.Grid[0]); cc++ {
				right++
				if d.Grid[r][cc] >= height {
					break
				}
			}

			ans = lib.Max(ans, up*down*left*right)
		}
	}

	return ans
}
