package d04

import (
	"bytes"
	"fmt"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Day04 struct {
	grid [][]byte
	cols [][]byte
}

func (d *Day04) LoadInput(lines []string) error {
	for _, line := range lines {
		fmt.Printf("%s\n", line)
		d.grid = append(d.grid, []byte(line))
	}
	d.cols = lib.Columns(d.grid)
	return nil
}

func (d *Day04) Part1(isTest bool) int {
	var ans int

	for r := range d.grid {
		for c := range d.grid[0] {
			if c+3 < len(d.grid[0]) {
				var word []byte
				for _, p := range lib.GridPointsBetween(lib.GridPoint[int]{r, c}, lib.GridPoint[int]{r, c + 3}) {
					word = append(word, d.grid[p.R][p.C])
				}
				if bytes.Equal(word, []byte("XMAS")) || bytes.Equal(word, []byte("SAMX")) {
					ans++
				}
			}

			if r+3 < len(d.grid[0]) {
				var word []byte
				for _, p := range lib.GridPointsBetween(lib.GridPoint[int]{r, c}, lib.GridPoint[int]{r + 3, c}) {
					word = append(word, d.grid[p.R][p.C])
				}
				if bytes.Equal(word, []byte("XMAS")) || bytes.Equal(word, []byte("SAMX")) {
					ans++
				}
			}

			if r-3 >= 0 && c+3 < len(d.grid[0]) {
				var word []byte
				for _, p := range lib.GridPointsBetween(lib.GridPoint[int]{r, c}, lib.GridPoint[int]{r - 3, c + 3}) {
					word = append(word, d.grid[p.R][p.C])
				}
				if bytes.Equal(word, []byte("XMAS")) || bytes.Equal(word, []byte("SAMX")) {
					ans++
				}
			}
			if r-3 >= 0 && c-3 >= 0 {
				var word []byte
				for _, p := range lib.GridPointsBetween(lib.GridPoint[int]{r - 3, c - 3}, lib.GridPoint[int]{r, c}) {
					word = append(word, d.grid[p.R][p.C])
				}
				if bytes.Equal(word, []byte("XMAS")) || bytes.Equal(word, []byte("SAMX")) {
					ans++
				}
			}
		}
	}

	return ans
}

func (d *Day04) Part2(isTest bool) int {
	var ans int

	for r := range d.grid {
		for c := range d.grid[0] {
			if r+2 < len(d.grid) && c+2 < len(d.grid[0]) {
				var tlbr []byte
				for _, p := range lib.GridPointsBetween(lib.GridPoint[int]{r, c}, lib.GridPoint[int]{r + 2, c + 2}) {
					tlbr = append(tlbr, d.grid[p.R][p.C])
				}
				if bytes.Equal(tlbr, []byte("MAS")) || bytes.Equal(tlbr, []byte("SAM")) {
					var bltr []byte
					for _, p := range lib.GridPointsBetween(lib.GridPoint[int]{r + 2, c}, lib.GridPoint[int]{r, c + 2}) {
						bltr = append(bltr, d.grid[p.R][p.C])
					}
					if bytes.Equal(bltr, []byte("MAS")) || bytes.Equal(bltr, []byte("SAM")) {
						fmt.Printf("%d %d\n", r, c)
						ans++
					}
				}
			}
		}
	}

	return ans
}
