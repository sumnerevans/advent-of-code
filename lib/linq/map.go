package linq

import (
	"math"

	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type LinqMap[T comparable, U any] struct {
	underlying map[T]U
}

func Map[T comparable, U any](input map[T]U) *LinqMap[T, U] {
	return &LinqMap[T, U]{underlying: input}
}

type KeyValuePair[K comparable, V any] struct {
	Key   K
	Value V
}

func (lm *LinqMap[T, U]) Where(f func(T, U) bool) ds.Iterator[KeyValuePair[T, U]] {
	it := make(chan KeyValuePair[T, U])
	go func() {
		defer close(it)
		for k, v := range lm.underlying {
			if f(k, v) {
				it <- KeyValuePair[T, U]{Key: k, Value: v}
			}
		}
	}()
	return it
}

func (lm *LinqMap[T, U]) Count() int {
	return len(lm.underlying)
}

func (lm *LinqMap[T, U]) MinMax(fn func(k T, v U) int) (int, int) {
	min, max := math.MaxInt, math.MinInt
	for k, v := range lm.underlying {
		value := fn(k, v)
		if value < min {
			min = value
		}
		if value > max {
			max = value
		}
	}
	return min, max
}

func (lm *LinqMap[T, U]) Min(fn func(k T, v U) int) (min int) {
	min, _ = lm.MinMax(fn)
	return
}

func (lm *LinqMap[T, U]) Max(fn func(k T, v U) int) (max int) {
	_, max = lm.MinMax(fn)
	return
}
