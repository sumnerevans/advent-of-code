package ds_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

func TestSetIntersection(t *testing.T) {
	tests := []struct {
		a        ds.Set[int]
		b        ds.Set[int]
		expected ds.Set[int]
	}{
		{ds.SetFromValues(1, 2, 3), ds.SetFromValues(2, 3, 4), ds.SetFromValues(2, 3)},
	}
	for _, test := range tests {
		assert.True(t, test.expected.Equal(test.a.Intersection(test.b)), "test: %+v", test)
	}
}
