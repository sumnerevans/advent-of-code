package ds

import (
	"golang.org/x/exp/constraints"
)

// Weighted

type Edge[V comparable, W constraints.Ordered] struct {
	Vertex V
	Weight W
}

type WeightedGraph[V comparable, W constraints.Ordered] map[V]Set[Edge[V, W]]

func NewWeightedGraph[V comparable, W constraints.Ordered]() WeightedGraph[V, W] {
	return WeightedGraph[V, W]{}
}

func (g WeightedGraph[V, W]) AddEdge(v1, v2 V, weight W) {
	if _, ok := g[v1]; !ok {
		g[v1] = Set[Edge[V, W]]{}
	}
	g[v1].Add(Edge[V, W]{
		Weight: weight,
		Vertex: v2,
	})
}

func (g WeightedGraph[V, W]) Nodes() (nodes Set[V]) {
	nodes = Set[V]{}
	for k, v := range g {
		nodes.Add(k)
		for v := range v {
			nodes.Add(v.Vertex)
		}
	}
	return
}

func (g WeightedGraph[V, W]) Invert() WeightedGraph[V, W] {
	inverted := WeightedGraph[V, W]{}
	for key, values := range g {
		for val := range values {
			inverted.AddEdge(val.Vertex, key, val.Weight)
		}
	}
	return inverted
}

func (g WeightedGraph[V, W]) AsUnweighted() Graph[V] {
	unweighted := NewGraph[V]()
	for key, values := range g {
		for val := range values {
			unweighted.AddEdge(key, val.Vertex)
		}
	}
	return unweighted
}

// Unweighted

type Graph[V comparable] struct {
	underlying WeightedGraph[V, int]
}

func NewGraph[V comparable]() Graph[V] {
	return Graph[V]{underlying: NewWeightedGraph[V, int]()}
}

func (g Graph[V]) AddEdge(v1, v2 V) {
	g.underlying.AddEdge(v1, v2, 1)
}

func (g Graph[V]) Nodes() (nodes Set[V]) {
	return g.underlying.Nodes()
}

func (g Graph[V]) Invert() Graph[V] {
	return g.underlying.Invert().AsUnweighted()
}

func (g Graph[V]) AsWeighted() WeightedGraph[V, int] {
	return g.underlying
}
