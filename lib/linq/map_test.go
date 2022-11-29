package linq_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/sumnerevans/advent-of-code/lib/linq"
)

func TestWhere(t *testing.T) {
	m := linq.Map(map[int]int{1: 1, 2: 2, 3: 3})
	it := m.Where(func(k int, v int) bool { return k > 1 })
	l := it.List()
	assert.Len(t, l, 2)
	assert.Equal(t, 2, l[0].Key)
	assert.Equal(t, 2, l[0].Value)
	assert.Equal(t, 3, l[1].Key)
	assert.Equal(t, 3, l[1].Value)
}

func TestMinMax(t *testing.T) {
	min, max := linq.Map(map[int]int{1: 1}).MinMax(func(k int, v int) int {
		return v
	})
	assert.Equal(t, 1, min)
	assert.Equal(t, 1, max)

	min, max = linq.Map(map[int]int{1: 1, 2: 2, 3: 3}).MinMax(func(k int, v int) int {
		return v
	})
	assert.Equal(t, 1, min)
	assert.Equal(t, 3, max)
}
