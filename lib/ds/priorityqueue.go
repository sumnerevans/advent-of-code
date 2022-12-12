package ds

import (
	"container/heap"
	"fmt"
)

type priorityQueueItem struct {
	value    any
	priority int
	index    int
}

func (pqi priorityQueueItem) String() string {
	return fmt.Sprintf("{p:%d, v:%v}", pqi.priority, pqi.value)
}

// priorityQueueInner implements the heap.Interface interface. It is then
// wrapped by PriorityQueue.
type priorityQueueInner struct {
	items []*priorityQueueItem
	less  func(p1, p2 int) bool
}

// Implementation of the functions for sort.Interface.

func (pq priorityQueueInner) Len() int {
	return len(pq.items)
}

func (pq priorityQueueInner) Less(i, j int) bool {
	return pq.less(pq.items[i].priority, pq.items[j].priority)
}

func (pq priorityQueueInner) Swap(i, j int) {
	pq.items[i], pq.items[j] = pq.items[j], pq.items[i]
	pq.items[i].index = i
	pq.items[j].index = j
}

func (pq *priorityQueueInner) Push(x any) {
	n := len(pq.items)
	item := x.(*priorityQueueItem)
	item.index = n
	pq.items = append(pq.items, item)
}

func (pq *priorityQueueInner) Pop() any {
	old := pq.items
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.index = -1 // for safety
	pq.items = old[0 : n-1]
	return item
}

// PriorityQueue is a min priority queue.
type PriorityQueue[V any] struct {
	inner priorityQueueInner
}

func NewPriorityQueue[V any](items ...Pair[int, V]) PriorityQueue[V] {
	pq := PriorityQueue[V]{
		inner: priorityQueueInner{
			items: make([]*priorityQueueItem, len(items)),
			less:  func(p1, p2 int) bool { return p1 < p2 },
		},
	}
	for i, item := range items {
		pq.inner.items[i] = &priorityQueueItem{
			priority: item.First(),
			value:    item.Second(),
			index:    i,
		}
	}
	heap.Init(&pq.inner)
	return pq
}

func NewMaxPriorityQueue[V any](items ...Pair[int, V]) PriorityQueue[V] {
	pq := PriorityQueue[V]{
		inner: priorityQueueInner{
			items: make([]*priorityQueueItem, len(items)),
			less:  func(p1, p2 int) bool { return p1 > p2 },
		},
	}
	for i, item := range items {
		pq.inner.items[i] = &priorityQueueItem{
			priority: item.First(),
			value:    item.Second(),
			index:    i,
		}
	}
	heap.Init(&pq.inner)
	return pq
}

func (pq *PriorityQueue[V]) String() string {
	return fmt.Sprintf("%v", pq.inner)
}

func (pq *PriorityQueue[V]) Len() int {
	return pq.inner.Len()
}

func (pq *PriorityQueue[V]) Push(priority int, val V) {
	item := &priorityQueueItem{
		value:    val,
		priority: priority,
	}
	heap.Push(&pq.inner, item)
}

func (pq *PriorityQueue[V]) Pop() (int, V) {
	next := heap.Pop(&pq.inner).(*priorityQueueItem)
	return next.priority, next.value.(V)
}
