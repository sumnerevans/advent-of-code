package math

import (
	"fmt"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
	"github.com/sumnerevans/advent-of-code/lib/fp"
	"golang.org/x/exp/constraints"
)

type Point[T constraints.Signed] struct {
	X, Y T
}

func (p Point[T]) String() string {
	return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

// IntPointsBetween return an iterator of all of the integer points between two
// given points. Note that you are *not* guaranteed that the points will be
// given from `start` to `end`, but all points will be included.
func IntPointsBetween[T constraints.Signed](start Point[T], end Point[T]) ds.Iterator[Point[T]] {
	if start.X == end.X {
		return fp.IMap(func(y T) Point[T] { return Point[T]{X: start.X, Y: y} })(lib.IRange(start.Y, end.Y))
	} else if start.Y == end.Y {
		return fp.IMap(func(x T) Point[T] { return Point[T]{X: x, Y: start.Y} })(lib.IRange(start.X, end.X))
	} else {
		// If the start X > end X, that means that "start" is to the right of
		// "end", so we need to switch the points around so iteration always
		// goes in the positive "x" direction
		if start.X > end.X {
			start.X, start.Y, end.X, end.Y = end.X, end.Y, start.X, start.Y
		}

		dy := end.Y - start.Y
		dx := end.X - start.X
		common := GCD(dy, dx)
		dy /= common
		dx /= common
		it := make(chan Point[T])
		go func() {
			defer close(it)
			x := start.X
			y := start.Y
			for x <= end.X {
				it <- Point[T]{X: x, Y: y}
				x += dx
				y += dy
			}
		}()
		return it
	}
}
