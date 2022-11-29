package math_test

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/sumnerevans/advent-of-code/lib/ds"
	"github.com/sumnerevans/advent-of-code/lib/math"
)

func TestIntPointsBetween(t *testing.T) {
	tests := map[struct{ start, end math.Point[int] }]ds.Set[math.Point[int]]{
		{math.Point[int]{X: 0, Y: 0}, math.Point[int]{X: 0, Y: 0}}:   ds.NewSet(math.Point[int]{0, 0}),
		{math.Point[int]{X: 0, Y: 0}, math.Point[int]{X: 1, Y: 1}}:   ds.NewSet(math.Point[int]{0, 0}, math.Point[int]{1, 1}),
		{math.Point[int]{X: 0, Y: 0}, math.Point[int]{X: -2, Y: -2}}: ds.NewSet(math.Point[int]{0, 0}, math.Point[int]{-1, -1}, math.Point[int]{-2, -2}),
		{math.Point[int]{X: 0, Y: 0}, math.Point[int]{X: -2, Y: 2}}:  ds.NewSet(math.Point[int]{0, 0}, math.Point[int]{-1, 1}, math.Point[int]{-2, 2}),
		{math.Point[int]{X: 0, Y: 0}, math.Point[int]{X: 2, Y: -2}}:  ds.NewSet(math.Point[int]{0, 0}, math.Point[int]{1, -1}, math.Point[int]{2, -2}),
		{math.Point[int]{X: 0, Y: 0}, math.Point[int]{X: 1, Y: 2}}:   ds.NewSet(math.Point[int]{0, 0}, math.Point[int]{1, 2}),
		{math.Point[int]{X: 0, Y: 9}, math.Point[int]{X: 5, Y: 9}}:   ds.NewSet(math.Point[int]{0, 9}, math.Point[int]{1, 9}, math.Point[int]{2, 9}, math.Point[int]{3, 9}, math.Point[int]{4, 9}, math.Point[int]{5, 9}),
	}
	for test, expected := range tests {
		t.Run(fmt.Sprintf("%s -> %s", test.start, test.end), func(t *testing.T) {
			actual := ds.NewSetFromIter(math.IntPointsBetween(test.start, test.end))
			assert.True(t, expected.Equal(actual), "%v", actual)
		})
	}
}
