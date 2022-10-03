package d04

import (
	"fmt"
	"strings"

	"github.com/rs/zerolog"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/fp"
	"github.com/sumnerevans/advent-of-code/lib/strs"
)

type Board [][]int64

func (b Board) String() string {
	s := ""
	for _, row := range b {
		s += fmt.Sprintf("%v\n", row)
	}
	return s
}

func (b Board) Mark(num int64) {
	for i, row := range b {
		for j, cell := range row {
			if cell == num {
				b[i][j] = 0
			}
		}
	}
}

func (b Board) Won() bool {
	for _, row := range b {
		if fp.Sum(row) == 0 {
			return true
		}
	}
	for _, col := range lib.Columns(b) {
		if fp.Sum(col) == 0 {
			return true
		}
	}
	return false
}

func (b Board) Sum() int64 {
	return fp.ISum(fp.Map(fp.Sum)(b))
}

type Day04 struct {
	Nums   []int64
	Boards []Board
}

func (d *Day04) LoadInput(log *zerolog.Logger, lines []string) error {
	d.Nums = strs.AllInts(lines[0]).List()

	d.Boards = []Board{}
	board := Board{}
	for _, line := range lines[2:] {
		if line == "" {
			d.Boards = append(d.Boards, board)
			board = Board{}
		} else {
			board = append(board, fp.MapStrInt(strings.Fields(line)).List())
		}
	}
	d.Boards = append(d.Boards, board)

	return nil
}

func (d *Day04) Part1(log *zerolog.Logger) int64 {
	for _, n := range d.Nums {
		for _, b := range d.Boards {
			b.Mark(n)
			if b.Won() {
				return n * b.Sum()
			}
		}
	}
	panic("Nobody won!")
}

func (d *Day04) Part2(log *zerolog.Logger) int64 {
	wons := map[int]struct{}{}
	for _, n := range d.Nums {
		for boardID, b := range d.Boards {
			b.Mark(n)
			if b.Won() {
				wons[boardID] = struct{}{}
				if len(wons) == len(d.Boards) {
					return n * b.Sum()
				}
			}
		}
	}
	panic("Nobody won!")
}
