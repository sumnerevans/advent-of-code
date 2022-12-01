package lib

import (
	"golang.org/x/exp/constraints"
)

func Reduce[T any, U any](f func(U, T) U) func(init U) func([]T) U {
	return func(initial U) func([]T) U {
		return func(input []T) U {
			init := initial
			for _, x := range input {
				init = f(init, x)
			}
			return init
		}
	}
}

func Sum[T constraints.Integer | constraints.Float](input []T) T {
	return Reduce(func(acc, next T) T { return acc + next })(T(0))(input)
}
