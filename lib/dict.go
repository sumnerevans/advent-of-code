package lib

import "golang.org/x/exp/constraints"

func Keys[T comparable, U any](m map[T]U) []T {
	keys := make([]T, 0, len(m))
	for k := range m {
		keys = append(keys, k)
	}
	return keys
}

func Values[T comparable, U any](m map[T]U) []U {
	values := make([]U, 0, len(m))
	for _, v := range m {
		values = append(values, v)
	}
	return values
}

func MinMaxMap[T comparable, U any, V constraints.Ordered](m map[T]U, f func(T, U) V) (min, max V) {
	if len(m) == 0 {
		panic("cannot find min-max of empty map")
	}
	i := 0
	for k, v := range m {
		out := f(k, v)
		if i == 0 {
			min = out
			max = out
			i++
		} else {
			min = Min(min, out)
			max = Max(max, out)
		}
	}
	return
}
