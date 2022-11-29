package lib

import (
	"fmt"

	"github.com/sumnerevans/advent-of-code/lib/ds"
	"golang.org/x/exp/constraints"
)

// ERange generates a Range that iterates over the integers in the range
// [start, end).
func ERange(rangearg1 int, rangeargs ...int) ds.Iterator[int] {
	if len(rangeargs) == 0 {
		return IRange(rangearg1 - 1)
	}
	args := []int{}
	if rangearg1 == rangeargs[0] {
		r := make(chan int)
		go func() {
			close(r)
		}()
		return r
	} else if rangearg1 < rangeargs[0] {
		args = append(args, rangeargs[0]-1)
	} else {
		args = append(args, rangeargs[0]+1)
	}
	args = append(args, rangeargs[1:]...)
	return IRange(rangearg1, args...)
}

// IRange generates a Range using the same rules as the Python range function.
func IRange[T constraints.Signed](rangearg1 T, rangeargs ...T) ds.Iterator[T] {
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

	r := make(chan T)
	go func() {
		defer close(r)
		if start == end {
			r <- start
			return
		} else if start < end {
			for i := start; i <= end; i += step {
				r <- i
			}
		} else {
			for i := start; i >= end; i -= step {
				r <- i
			}
		}
	}()
	return r
}
