package fp

import (
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

func Map[T any, U any](f func(T) U) func([]T) ds.Iterator[U] {
	return func(input []T) ds.Iterator[U] {
		it := make(chan U)
		go func() {
			defer close(it)
			for _, v := range input {
				it <- f(v)
			}
		}()
		return it
	}
}

func IMap[T any, U any](f func(T) U) func(ds.Iterator[T]) ds.Iterator[U] {
	return func(input ds.Iterator[T]) ds.Iterator[U] {
		it := make(chan U)
		go func() {
			defer close(it)
			for v := range input {
				it <- f(v)
			}
		}()
		return it
	}
}

func MapStrInt(input []string) ds.Iterator[int] {
	return Map(lib.ToInt)(input)
}

func MapStrInt64(input []string) ds.Iterator[int64] {
	return Map(lib.ToInt64)(input)
}
