package lib

import (
	"fmt"

	"golang.org/x/exp/constraints"
)

type GridPoint[T constraints.Signed] struct {
	R, C T
}

func NewGridPoint[T constraints.Signed](r, c T) GridPoint[T] {
	return GridPoint[T]{R: r, C: c}
}

func (g GridPoint[T]) String() string {
	return fmt.Sprintf("(%d, %d)", g.R, g.C)
}

func (g GridPoint[T]) ToPoint() Point[T] {
	return Point[T]{X: g.C, Y: g.R}
}
