package linq

import (
	"math"

	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type LinqList[T any] struct {
	underlying []T
}

func List[T any](values ...T) *LinqList[T] {
	return &LinqList[T]{underlying: values}
}

func ListFromIter[T any](it ds.Iterator[T]) *LinqList[T] {
	underlying := []T{}
	for val := range it {
		underlying = append(underlying, val)
	}
	return &LinqList[T]{underlying: underlying}
}

func (l *LinqList[T]) Count() int {
	return len(l.underlying)
}

func (l *LinqList[T]) MinMax(fn func(v T) int) (int, int) {
	min, max := math.MaxInt, math.MinInt
	for _, v := range l.underlying {
		value := fn(v)
		if value < min {
			min = value
		}
		if value > max {
			max = value
		}
	}
	return min, max
}

func (l *LinqList[T]) MinMax64(fn func(v T) int64) (int64, int64) {
	var min, max int64 = math.MaxInt64, math.MinInt64
	for _, v := range l.underlying {
		value := fn(v)
		if value < min {
			min = value
		}
		if value > max {
			max = value
		}
	}
	return min, max
}

func (l *LinqList[T]) Min(fn func(v T) int) (min int) {
	min, _ = l.MinMax(fn)
	return
}

func (l *LinqList[T]) Max(fn func(v T) int) (max int) {
	_, max = l.MinMax(fn)
	return
}
