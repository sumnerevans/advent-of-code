package lib_test

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

func TestIntPointsBetween(t *testing.T) {
	tests := map[struct{ start, end lib.Point[int] }]ds.Set[lib.Point[int]]{
		{lib.Point[int]{X: 0, Y: 0}, lib.Point[int]{X: 0, Y: 0}}:   ds.SetFromValues(lib.Point[int]{0, 0}),
		{lib.Point[int]{X: 0, Y: 0}, lib.Point[int]{X: 1, Y: 1}}:   ds.SetFromValues(lib.Point[int]{0, 0}, lib.Point[int]{1, 1}),
		{lib.Point[int]{X: 0, Y: 0}, lib.Point[int]{X: -2, Y: -2}}: ds.SetFromValues(lib.Point[int]{0, 0}, lib.Point[int]{-1, -1}, lib.Point[int]{-2, -2}),
		{lib.Point[int]{X: 0, Y: 0}, lib.Point[int]{X: -2, Y: 2}}:  ds.SetFromValues(lib.Point[int]{0, 0}, lib.Point[int]{-1, 1}, lib.Point[int]{-2, 2}),
		{lib.Point[int]{X: 0, Y: 0}, lib.Point[int]{X: 2, Y: -2}}:  ds.SetFromValues(lib.Point[int]{0, 0}, lib.Point[int]{1, -1}, lib.Point[int]{2, -2}),
		{lib.Point[int]{X: 0, Y: 0}, lib.Point[int]{X: 1, Y: 2}}:   ds.SetFromValues(lib.Point[int]{0, 0}, lib.Point[int]{1, 2}),
		{lib.Point[int]{X: 0, Y: 9}, lib.Point[int]{X: 5, Y: 9}}:   ds.SetFromValues(lib.Point[int]{0, 9}, lib.Point[int]{1, 9}, lib.Point[int]{2, 9}, lib.Point[int]{3, 9}, lib.Point[int]{4, 9}, lib.Point[int]{5, 9}),
	}
	for test, expected := range tests {
		t.Run(fmt.Sprintf("%s -> %s", test.start, test.end), func(t *testing.T) {
			actual := ds.NewSet(lib.IntPointsBetween(test.start, test.end))
			assert.True(t, expected.Equal(actual), "%v", actual)
		})
	}
}
