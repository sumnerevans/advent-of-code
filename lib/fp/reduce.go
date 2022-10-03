package fp

import "github.com/sumnerevans/advent-of-code/lib/ds"

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
var Sum = Reduce(func(acc, next int64) int64 { return acc + next })(0)
