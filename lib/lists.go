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

func CopySlice[T any](input []T) []T {
	output := make([]T, len(input))
	copy(output, input)
	return output
}

func Sort[T constraints.Ordered](input []T) {
	sort.Slice(input, func(i, j int) bool { return input[i] < input[j] })
}

func Reverse[T any](input []T) (output []T) {
	for i := len(input) - 1; i >= 0; i-- {
		output = append(output, input[i])
	}
	return
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

func MaxList[T constraints.Ordered](l []T) T {
	_, max := MinMaxList(l)
	return max
}

func MaxListFn[T any, U constraints.Ordered](l []T, f func(T) U) U {
	_, max := MinMaxListFn(l, f)
	return max
}

func MinList[T constraints.Ordered](l []T) T {
	min, _ := MinMaxList(l)
	return min
}

func MinListFn[T, U constraints.Ordered](l []T, f func(T) U) U {
	min, _ := MinMaxListFn(l, f)
	return min
}

func MinMaxList[T constraints.Ordered](l []T) (min, max T) {
	return MinMaxListFn(l, func(x T) T { return x })
}

func MinMaxListFn[T any, U constraints.Ordered](l []T, f func(T) U) (min, max U) {
	if len(l) == 0 {
		panic("cannot find min/max of empty list")
	}
	min = f(l[0])
	max = min
	for _, val := range l {
		v := f(val)
		min = Min(min, v)
		max = Max(max, v)
	}
	return
}

func Windowed[T any](l []T, n int) (windows [][]T) {
	if n <= 0 {
		panic("invalid window size")
	}
	cur := []T{}
	for i := 0; i < len(l); i++ {
		if i > 0 && i%n == 0 {
			windows = append(windows, cur)
			cur = []T{}
		}

		cur = append(cur, l[i])
	}
	windows = append(windows, cur)
	return windows
}

// SlidingWindowsSlices gives the sliding n-sized windows of l as an array of
// slices of the original list. It is recommended that you only use this for
// read-only use-cases, and copy out the elements if needed to put into a
// different data structure.
func SlidingWindowsSlices[T any](l []T, n int) (windows [][]T) {
	if n <= 0 {
		panic("invalid sliding window size")
	}
	for i := 0; i < len(l)-n; i++ {
		windows = append(windows, l[i:i+n])
	}
	return
}

func SplitAt[T any](l []T, n int) ([]T, []T) {
	return l[:n], l[n:]
}
