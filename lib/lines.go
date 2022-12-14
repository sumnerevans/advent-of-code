package lib

import (
	"fmt"

	"golang.org/x/exp/constraints"
)

type Point[T constraints.Signed] struct {
	X, Y T
}

func (p Point[T]) String() string {
	return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

func (p Point[T]) ToGridIdx() GridPoint[T] {
	return GridPoint[T]{R: p.Y, C: p.X}
}

var Quadrants = map[int]Point[int]{
	1: {1, 1},
	2: {-1, 1},
	3: {-1, -1},
	4: {1, -1},
}

// IntPointsBetween return an iterator of all of the integer points between two
// given points. Note that you are *not* guaranteed that the points will be
// given from `start` to `end`, but all points will be included.
func IntPointsBetween[T constraints.Signed](start Point[T], end Point[T]) (points []Point[T]) {
	if start.X == end.X {
		return Map(func(y T) Point[T] { return Point[T]{X: start.X, Y: y} })(IRange(start.Y, end.Y))
	} else if start.Y == end.Y {
		return Map(func(x T) Point[T] { return Point[T]{X: x, Y: start.Y} })(IRange(start.X, end.X))
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

		x := start.X
		y := start.Y
		for x <= end.X {
			points = append(points, Point[T]{X: x, Y: y})
			x += dx
			y += dy
		}
		return
	}
}

// IntPointsBetween return an iterator of all of the integer points between two
// given points. Note that you are *not* guaranteed that the points will be
// given from `start` to `end`, but all points will be included.
func GridPointsBetween[T constraints.Signed](start GridPoint[T], end GridPoint[T]) (points []GridPoint[T]) {
	if start.R == end.R {
		return Map(func(c T) GridPoint[T] { return GridPoint[T]{R: start.R, C: c} })(IRange(start.C, end.C))
	} else if start.C == end.C {
		return Map(func(r T) GridPoint[T] { return GridPoint[T]{R: r, C: start.C} })(IRange(start.R, end.R))
	} else {
		// If the start C > end C, that means that "start" is to the right of
		// "end", so we need to switch the points around so iteration always
		// goes in the positive "c" direction
		if start.C > end.C {
			start.C, start.R, end.C, end.R = end.C, end.R, start.C, start.R
		}

		dr := end.R - start.R
		dc := end.C - start.C
		common := GCD(dr, dc)
		dr /= common
		dc /= common

		r := start.R
		c := start.C
		for c <= end.C {
			points = append(points, GridPoint[T]{R: r, C: c})
			c += dc
			r += dr
		}
		return
	}
}
