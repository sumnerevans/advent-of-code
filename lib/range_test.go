package lib_test

import (
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib"
)

func TestIRange(t *testing.T) {
	assert.Equal(t, []int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, lib.IRange(10))
	assert.Equal(t, []int{3, 4, 5, 6, 7, 8, 9, 10}, lib.IRange(3, 10))
	assert.Equal(t, []int{3, 5, 7, 9}, lib.IRange(3, 10, 2))
	assert.Equal(t, []int{10, 8, 6, 4}, lib.IRange(10, 3, 2))
	assert.Equal(t, []int{2}, lib.IRange(2, 2))
	assert.Equal(t, []int{4, 2}, lib.IRange(2, 4, -2))
	assert.Equal(t, []int{4, 3, 2}, lib.IRange(4, 2))
	assert.Panics(t, func() { lib.IRange(3, 10, 2, 10) })
}

func TestERange(t *testing.T) {
	assert.Equal(t, []int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}, lib.ERange(10))
	assert.Equal(t, []int{3, 4, 5, 6, 7, 8, 9}, lib.ERange(3, 10))
	assert.Equal(t, []int{3, 5, 7}, lib.ERange(3, 9, 2))
	assert.Equal(t, []int{10, 8, 6}, lib.ERange(10, 4, 2))
	assert.Equal(t, []int{}, lib.ERange(2, 2))
	assert.Equal(t, []int{4, 3}, lib.ERange(4, 2))
	assert.Equal(t, []int{8, 6, 4}, lib.ERange(8, 2, 2))
}
