package lib

import (
	"container/heap"

	"github.com/sumnerevans/advent-of-code/lib/ds"
)

func Dijkstra[K comparable](
	nextStates func(K) ds.Set[ds.Edge[K, int]],
	start K,
	endState func(K) bool,
) int {
	pq := ds.PriorityQueue{}
	dists := map[K]int{}
	seen := ds.Set[K]{}

	pq.Push(ds.Item{
		Value:    start,
		Priority: 0,
	})
	heap.Init(&pq)

	for len(pq) > 0 {
		next := heap.Pop(&pq).(*ds.Item)
		cost := next.Priority
		el := next.Value.(K)
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
				heap.Push(&pq, ds.Item{
					Value:    e.Vertex,
					Priority: cost + e.Weight,
				})
			}
		}
	}
	panic("No path found to any end state")
}
