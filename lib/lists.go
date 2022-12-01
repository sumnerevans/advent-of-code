package lib

import (
	"sort"

	"golang.org/x/exp/constraints"
)

// Columns returns the columnar version of a grid array.
func Columns[T any](input [][]T) (columns [][]T) {
	if len(input) == 0 {
		return
	}

	columns = make([][]T, len(input[0]))
	for _, row := range input {
		for col, val := range row {
			columns[col] = append(columns[col], val)
		}
	}
	return
}

func Sort[T constraints.Ordered](input []T) {
	sort.Slice(input, func(i, j int) bool { return input[i] < input[j] })
}

func TopN[T constraints.Ordered](input []T, n int) []T {
	cp := make([]T, len(input))
	for i, val := range input {
		cp[i] = val
	}
	sort.Slice(cp, func(i, j int) bool { return cp[i] > cp[j] })
	return cp[:n]
}

func BottomN[T constraints.Ordered](input []T, n int) []T {
	cp := make([]T, len(input))
	for i, val := range input {
		cp[i] = val
	}
	sort.Slice(cp, func(i, j int) bool { return cp[i] < cp[j] })
	return cp[:n]
}
