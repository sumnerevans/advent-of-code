package math

import "golang.org/x/exp/constraints"

func GCD[T constraints.Integer](x, y T) T {
	for y != T(0) {
		x, y = y, x%y
	}
	return x
}

func AbsInt[T constraints.Integer](x T) T {
	if x < 0 {
		return -x
	}
	return x
}

func Max[T constraints.Ordered](a, b T) T {
	if a >= b {
		return a
	} else {
		return b
	}
}

func Min[T constraints.Ordered](a, b T) T {
	if a <= b {
		return a
	} else {
		return b
	}
}
