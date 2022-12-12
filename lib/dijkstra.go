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
