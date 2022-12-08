package d08

import (
	"fmt"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
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

	vis := ds.Set[lib.Point[int]]{}

	for r, row := range d.Grid {
		curhi := -1
		for c, t := range row {
			if t > curhi {
				vis.Add(lib.Point[int]{Y: r, X: c})
				curhi = t
			}
		}
		curhi = -1
		for i := len(row) - 1; i > -1; i-- {
			if row[i] > curhi {
				vis.Add(lib.Point[int]{Y: r, X: i})
				curhi = row[i]
			}
		}
	}

	for r, row := range lib.Columns(d.Grid) {
		curhi := -1
		for c, t := range row {
			if t > curhi {
				vis.Add(lib.Point[int]{Y: c, X: r})
				curhi = t
			}
		}
		curhi = -1
		for i := len(row) - 1; i > -1; i-- {
			if row[i] > curhi {
				vis.Add(lib.Point[int]{Y: i, X: r})
				curhi = row[i]
			}
		}
	}

	return len(vis.List())
}

func (d *Day08) Part2() int {
	var ans int

	for r, row := range d.Grid {
		for c, height := range row {
			fmt.Printf("EVAL (%d, %d) %d\n", r, c, height)

			up := 0
			for cr := r - 1; cr >= 0; cr-- {
				fmt.Printf("up (%d, %d)\n", cr, c)
				up++
				if d.Grid[cr][c] >= height {
					break
				}
			}
			fmt.Printf("up %d\n", up)

			down := 0
			for cr := r + 1; cr < len(d.Grid); cr++ {
				fmt.Printf("down (%d, %d)\n", cr, c)
				down++
				if d.Grid[cr][c] >= height {
					break
				}
			}
			fmt.Printf("down %d\n", down)

			left := 0
			for cc := c - 1; cc >= 0; cc-- {
				fmt.Printf("left (%d, %d)\n", r, cc)
				left++
				if d.Grid[r][cc] >= height {
					break
				}
			}
			fmt.Printf("left %d\n", left)

			right := 0
			for cc := c + 1; cc < len(d.Grid[0]); cc++ {
				fmt.Printf("right (%d, %d)\n", r, cc)
				right++
				if d.Grid[r][cc] >= height {
					break
				}
			}
			fmt.Printf("right %d\n", right)

			fmt.Printf("ANS FOR (%d, %d) = %d\n", r, c, up*down*left*right)
			ans = lib.Max(ans, up*down*left*right)
		}
	}

	return ans

	// What is the highest scenic score possible for any tree?
	for r, row := range d.Grid {
		for c, height := range row {
			if r == 0 || c == 0 || r == len(d.Grid)-1 || c == len(d.Grid[0])-1 {
				continue
			}
			fmt.Printf("RC %d %d\n", r, c)
			score := 1
			// Up: TODO
			up := 0
			for curR := r - 1; curR >= 0; curR-- {
				fmt.Printf("=%d %d %d\n", curR, c, d.Grid[curR][c])
				if d.Grid[curR][c] < height {
					up++
				} else {
					break
				}
			}
			fmt.Printf("up %d\n", up)
			score *= up
			// down:
			down := 1
			for curR := r + 1; curR < len(d.Grid); curR++ {
				if d.Grid[curR][c] < height {
					down++
				} else {
					break
				}
			}
			fmt.Printf("d %d\n", down)
			score *= down
			// Left:
			left := 1
			for curC := c - 1; curC > 0; curC-- {
				if d.Grid[r][curC] < height {
					up++
				} else {
					break
				}
			}
			fmt.Printf("l %d\n", left)
			score *= left
			// Right: TODO
			right := 0
			for curC := c + 1; curC < len(d.Grid[0]); curC++ {
				if d.Grid[r][curC] < height {
					right++
				} else {
					break
				}
			}
			fmt.Printf("r %d\n", right)
			score *= right

			fmt.Printf("SCORE (%d, %d) %d\n", r, c, score)
			ans = lib.Max(ans, score)
		}
	}

	return ans
}
