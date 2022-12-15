package lib

import (
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

func Dijkstra[K comparable](
	nextStates func(K) ds.Set[ds.Edge[K, int]],
	start K,
	endState func(K) bool,
) int {
	pq := ds.NewPriorityQueue(ds.NewPair(0, start))
	dists := map[K]int{}
	seen := ds.Set[K]{}

	for pq.Len() > 0 {
		cost, el := pq.Pop()
		if seen.Contains(el) {
			continue
		}

		if endState(el) {
			return dists[el]
		}

		seen.Add(el)

		for e := range nextStates(el) {
			if curdist, ok := dists[e.Vertex]; !ok || cost+e.Weight < curdist {
				dists[e.Vertex] = cost + e.Weight
				pq.Push(cost+e.Weight, e.Vertex)
			}
		}
	}
	panic("No path found to any end state")
}

func DijkstraG[K comparable](graph ds.WeightedGraph[K, int], start K, end K) int {
	return Dijkstra(
		func(cur K) ds.Set[ds.Edge[K, int]] { return graph[cur] },
		start,
		func(cur K) bool { return cur == end },
	)
}

func ShortestPath[K comparable](
	nextStates func(K) ds.Set[K],
	start K,
	endState func(K) bool,
) int {
	return Dijkstra(
		func(cur K) ds.Set[ds.Edge[K, int]] {
			nexts := ds.Set[ds.Edge[K, int]]{}
			for s := range nextStates(cur) {
				nexts.Add(ds.Edge[K, int]{Vertex: s, Weight: 1})
			}
			return nexts
		},
		start,
		endState,
	)
}

func ShortestPathG[K comparable](graph ds.Graph[K], start K, end K) int {
	return DijkstraG(graph.AsWeighted(), start, end)
}
