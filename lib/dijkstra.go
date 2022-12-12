package lib

import (
	"container/heap"
	"fmt"

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
		fmt.Printf("PQ\n")
		for _, v := range pq {
			fmt.Printf("%s\n", v.String())
		}
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

		fmt.Printf("NS:\n")
		ns := nextStates(el)
		for v := range ns {
			fmt.Printf("%v\n", v.Vertex)
		}

		for e := range ns {
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
