package ds_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

func TestGraph_Create(t *testing.T) {
	g := ds.NewGraph[int]()
	g.AddEdge(1, 2)
	g.AddEdge(2, 3)
	g.AddEdge(2, 4)

	assert.Equal(t, ds.SetFromValues(1, 2, 3, 4), g.Nodes())
}

func TestGraph_Invert(t *testing.T) {
	g := ds.NewGraph[int]()
	g.AddEdge(1, 2)
	g.AddEdge(2, 3)
	g.AddEdge(2, 4)

	inverted := ds.NewGraph[int]()
	inverted.AddEdge(2, 1)
	inverted.AddEdge(3, 2)
	inverted.AddEdge(4, 2)

	assert.Equal(t, inverted, g.Invert())
}
