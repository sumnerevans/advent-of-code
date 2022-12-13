package ds_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

func TestPriorityQueue(t *testing.T) {
	pq := ds.NewPriorityQueue[rune]()
	pq.Push(0, 'A')
	pq.Push(2, 'C')
	pq.Push(1, 'B')

	i := 0
	for pq.Len() > 0 {
		priority, val := pq.Pop()
		assert.Equal(t, 'A'+rune(i), val)
		assert.Equal(t, i, priority)
		i++
	}
}
