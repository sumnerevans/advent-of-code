package lib

import (
	"fmt"

	"golang.org/x/exp/constraints"
)

// ERange generates a Range that iterates over the integers in the range
// [start, end).
func ERange(rangearg1 int, rangeargs ...int) []int {
	if len(rangeargs) == 0 {
		return IRange(rangearg1 - 1)
	}
	args := []int{}
	if rangearg1 == rangeargs[0] {
		return []int{}
	} else if rangearg1 < rangeargs[0] {
		args = append(args, rangeargs[0]-1)
	} else {
		args = append(args, rangeargs[0]+1)
	}
	args = append(args, rangeargs[1:]...)
	return IRange(rangearg1, args...)
}

// IRange generates a Range using the same rules as the Python range function.
func IRange[T constraints.Signed](rangearg1 T, rangeargs ...T) (output []T) {
	if len(rangeargs) > 2 {
		panic(fmt.Sprintf("Invalid rangeargs %+v", rangeargs))
	}
	var start T = rangearg1
	var end T = 0
	var step T = 1
	if len(rangeargs) == 0 {
		start, end = 0, rangearg1
	} else {
		end = rangeargs[0]
	}

	if len(rangeargs) > 1 {
		step = rangeargs[1]
	}

	if step == 0 {
		panic("Step cannot be 0")
	} else if step < 0 {
		start, end = end, start
		step *= -1
	}

	if start == end {
		return []T{start}
	} else if start < end {
		for i := start; i <= end; i += step {
			output = append(output, i)
		}
	} else {
		for i := start; i >= end; i -= step {
			output = append(output, i)
		}
	}
	return output
}
