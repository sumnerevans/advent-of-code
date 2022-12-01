package fp

import (
	"github.com/sumnerevans/advent-of-code/lib/ds"
	"golang.org/x/exp/constraints"
)

func IReduce[T any, U any](f func(U, T) U) func(init U) func(ds.Iterator[T]) U {
	return func(initial U) func(ds.Iterator[T]) U {
		return func(input ds.Iterator[T]) U {
			init := initial
			for x := range input {
				init = f(init, x)
			}
			return init
		}
	}
}

func Reduce[T any, U any](f func(U, T) U) func(init U) func([]T) U {
	return func(initial U) func([]T) U {
		return func(input []T) U {
			return IReduce(f)(initial)(ds.NewIterator(input))
		}
	}
}

var ISum = IReduce(func(acc, next int64) int64 { return acc + next })(0)

func Sum[T constraints.Integer | constraints.Float](input []T) T {
	return Reduce(func(acc, next T) T { return acc + next })(T(0))(input)
}
