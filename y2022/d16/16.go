package d16

import (
	"fmt"
	"strings"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Valve struct {
	Flow int
	Adj  ds.Set[ds.Edge[string, int]]
}

type Day16 struct {
	Valves     map[string]Valve
	ValveMasks map[string]int64
	Distances  map[string]map[string]int
}

func (d *Day16) LoadInput(lines []string) error {
	d.Valves = map[string]Valve{}
	for _, line := range lines {
		grps := lib.ReGroups(`Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)`, line)
		name := grps[0]
		flow := lib.ToInt(grps[1])
		adj := ds.Set[ds.Edge[string, int]]{}
		for _, x := range strings.Split(grps[2], ", ") {
			adj.Add(ds.Edge[string, int]{1, x})
		}
		d.Valves[name] = Valve{Flow: flow, Adj: adj}
	}

	d.Distances = map[string]map[string]int{}
	for name := range d.Valves {
		d.Distances[name] = map[string]int{}
		pq := ds.NewPriorityQueue(ds.NewPair(0, name))
		seen := ds.Set[string]{}
		for pq.Len() > 0 {
			cost, el := pq.Pop()
			seen.Add(el)
			if _, ok := d.Distances[name][el]; !ok {
				d.Distances[name][el] = cost
			}
			for a := range d.Valves[el].Adj {
				if !seen.Contains(a.Vertex) {
					pq.Push(cost+1, a.Vertex)
				}
			}
		}
	}
	fmt.Printf("dist %v\n", d.Distances)

	d.ValveMasks = map[string]int64{}
	i := 0
	for name := range d.Valves {
		d.ValveMasks[name] = 1 << i
		i++
	}
	// fmt.Printf("VM %v\n", d.ValveMasks)
	// for k, v := range d.ValveMasks {
	// 	fmt.Printf("k: %s\n", k)
	// 	fmt.Printf("v: %v\n", lib.BitsOfInt64(v).String())
	// }

	// 	handled := ds.Set[string]{}
	// 	for {
	// 		haszero := false
	// 		for name, valve := range valves {
	// 			if handled.Contains(name) || valve.Flow > 0 {
	// 				continue
	// 			}
	// 			fmt.Printf("%v\n", valves)
	// 			fmt.Printf("ZERO %s %v\n", name, valve)
	// 			haszero = true

	// 			for n, v := range valves {
	// 				for a := range v.Adj {
	// 					if a.Vertex == name {
	// 						valves[n].Adj.Remove(a)
	// 						for a := range valve.Adj {
	// 							valves[n].Adj.Add(ds.Edge[string, int]{a.Weight + 1, a.Vertex})
	// 						}
	// 						break
	// 					}
	// 				}
	// 			}

	// 			handled.Add(name)

	// 			break
	// 		}
	// 		fmt.Printf("%v\n", valves)
	// 		if !haszero {
	// 			break
	// 		}
	// 	}

	// d.Valves = valves
	// fmt.Printf("FINAL\n\n%v\n", d.Valves)
	// panic("ohea")

	return nil
}

type CurOpens int64

func (co CurOpens) String(maskMap map[string]int64) string {
	return "[" + strings.Join(co.Opens(maskMap), ", ") + "]"
}

func (co CurOpens) IsOpen(mask int64) bool {
	return int64(co)&mask > 0
}

func (co CurOpens) Count() (count int) {
	var i int64
	for ; i < 64; i++ {
		if int64(co)&i > 0 {
			count++
		}
	}
	return count
}

func (co CurOpens) AllOpen(maskMap map[string]int64, valves map[string]Valve) bool {
	for name, valve := range valves {
		if valve.Flow > 0 && int64(co)&maskMap[name] == 0 {
			return false
		}
	}
	return true
}

func (co CurOpens) TotalFlow(maskMap map[string]int64, flows map[string]Valve) int {
	maskToName := map[int64]string{}
	for k, v := range maskMap {
		maskToName[v] = k
	}
	var i int64
	total := 0
	for ; i < 64; i++ {
		if int64(co)&(1<<i) > 0 {
			total += flows[maskToName[1<<i]].Flow
		}
	}
	return total
}

func (co CurOpens) WithOpen(mask int64) CurOpens {
	if co.IsOpen(mask) {
		panic("already open")
	}
	return CurOpens(int64(co) | mask)
}

func (co CurOpens) Opens(maskMap map[string]int64) []string {
	maskToName := map[int64]string{}
	for k, v := range maskMap {
		maskToName[v] = k
	}

	var i int64
	opens := []string{}
	for ; i < 64; i++ {
		if int64(co)&(1<<i) > 0 {
			opens = append(opens, maskToName[1<<i])
		}
	}
	return opens
}

type CurState struct {
	Open   CurOpens
	CurPos string
	Time   int
	Flow   int
}

func (cs CurState) String(maskMap map[string]int64) string {
	return fmt.Sprintf("{%s @%s t=%d f=%d}", cs.Open.String(maskMap), cs.CurPos, cs.Time, cs.Flow)
}

type Cons[T any] struct {
	Car T
	Cdr *Cons[T]
}

type Stack[T any] struct {
	head *Cons[T]
}

func (s *Stack[T]) Len() int {
	i := 0
	cur := s.head
	for cur != nil {
		i++
		cur = cur.Cdr
	}
	return i
}

func (s *Stack[T]) Push(x T) {
	if s.head == nil {
		s.head = &Cons[T]{Car: x}
	} else {
		s.head = &Cons[T]{Car: x, Cdr: s.head}
	}
}

func (s *Stack[T]) Peek() *T {
	if s.head == nil {
		return nil
	}
	return &s.head.Car
}

func (s *Stack[T]) Pop() T {
	if s.head == nil {
		panic("pop from empty stack")
	}

	top := s.head.Car
	s.head = s.head.Cdr
	return top
}

// This isn't really DFS, I have no idea what it is.
func DFS(
	d *Day16,
	nextStates func(CurState) ds.Set[CurState],
	start CurState,
	endState func(CurState) bool,
	maxFlowPerMinute int,
) int {
	// endStates := []CurState{}

	pq := ds.NewMaxPriorityQueue(ds.NewPair(0, start))
	// stack := Stack[CurState]{}
	// stack.Push(start)
	// pq := ds.NewPriorityQueue(ds.NewPair(0, start))
	// seen := ds.Set[CurState]{}

	i := 0
	best := 0

	pruning := 0

	// for stack.Peek() != nil {
	for pq.Len() > 0 {
		if i%1000000 == 0 {
			// fmt.Printf("%d %d\n", stack.Len(), i)
			fmt.Printf("%d %d\n", pq.Len(), i)
			// cur := stack.head
			// for cur != nil {
			// 	fmt.Printf("%v\n", cur.Car.String(d.ValveMasks))
			// 	cur = cur.Cdr
			// }
		}
		i++
		// el := stack.Pop()
		_, el := pq.Pop()
		// fmt.Printf("el %v\n", el.String(d.ValveMasks))
		// if seen.Contains(el) {
		// 	continue
		// }

		if endState(el) {
			if el.Flow > best {
				// fmt.Printf("%v\n", el.String(d.ValveMasks))
				best = el.Flow
				fmt.Printf("best %d: %s\n", best, el.String(d.ValveMasks))
			}
			// fmt.Printf("ES %v\n", el)
			// endStates = append(endStates, el)
			continue
		}

		if el.Flow+(maxFlowPerMinute)*(30-el.Time) < best {
			pruning++
			continue
		}

		// seen.Add(el)

		// nexts := nextStates(el).List()
		// sort.Slice(nexts, func(i, j int) bool {
		// 	if nexts[i].Open.Count() < nexts[j].Open.Count() {
		// 		return true
		// 	} else if nexts[i].Flow < nexts[j].Flow {
		// 		return true
		// 	}
		// 	return false
		// 	// return nexts[i].Flow < nexts[j].Flow
		// })

		// for _, e := range nexts {
		for e := range nextStates(el) {
			// if seen.Contains(e) {
			// 	fmt.Printf("=============HERE\n", )
			// 	continue
			// }
			// fmt.Printf("NEXT %v\n", e.String(d.ValveMasks))
			// if seen.Contains(e) {
			// 	continue
			// }
			pq.Push(e.Open.Count(), e)
		}
	}

	fmt.Printf("PRUNED %d\n", pruning)

	return best
}

func (d *Day16) Part1(isTest bool) int {
	var ans int

	// valveMasks := map[string]int64{}
	// i := 0
	// for name := range d.Valves {
	// 	valveMasks[name] = 1 << i
	// 	i++
	// }
	// fmt.Printf("%v\n", valveMasks)
	// panic(1)

	start := CurState{
		Open:   0,
		CurPos: "AA",
		Time:   0,
		Flow:   0,
	}

	maxFlowPerMinute := lib.Sum(lib.Map(func(v Valve) int {
		return v.Flow
	})(lib.Values(d.Valves)))

	return DFS(
		d,
		func(cur CurState) ds.Set[CurState] {
			// fmt.Printf("cur %v\n", cur)
			next := ds.Set[CurState]{}
			// if cur.Open.AllOpen(d.ValveMasks, d.Valves) {
			// 	next.Add(
			// 		CurState{
			// 			Open:   cur.Open,
			// 			CurPos: cur.CurPos,
			// 			Time:   30,
			// 			Flow:   cur.Flow + (30-cur.Time)*cur.Open.TotalFlow(d.ValveMasks, d.Valves),
			// 		},
			// 	)
			// 	return next
			// }

			// Stay
			if cur.Open.AllOpen(d.ValveMasks, d.Valves) {
				next.Add(
					CurState{
						Open:   cur.Open,
						CurPos: cur.CurPos,
						Time:   30,
						Flow:   cur.Flow + (30-cur.Time)*cur.Open.TotalFlow(d.ValveMasks, d.Valves),
					},
				)
			} else {
				// Open the valve
				if d.Valves[cur.CurPos].Flow > 0 && !cur.Open.IsOpen(d.ValveMasks[cur.CurPos]) {
					next.Add(
						CurState{
							Open:   cur.Open.WithOpen(d.ValveMasks[cur.CurPos]),
							CurPos: cur.CurPos,
							Time:   cur.Time + 1,
							Flow:   cur.Flow + cur.Open.TotalFlow(d.ValveMasks, d.Valves),
						},
					)
				}

				// Move
				// for vert, dist := range d.Distances[cur.CurPos] {
				// 	if cur.Time+dist <= 30 && !cur.Open.IsOpen(d.ValveMasks[vert]) && d.Valves[vert].Flow > 0 {
				// 		next.Add(
				// 			CurState{
				// 				Open:   cur.Open,
				// 				CurPos: vert,
				// 				Time:   cur.Time + dist,
				// 				Flow:   cur.Flow + dist*cur.Open.TotalFlow(d.ValveMasks, d.Valves),
				// 			},
				// 		)
				// 	}
				// }
				for v := range d.Valves[cur.CurPos].Adj {
					if cur.Time+1 <= 30 {
						next.Add(
							CurState{
								Open:   cur.Open,
								CurPos: v.Vertex,
								Time:   cur.Time + 1,
								Flow:   cur.Flow + cur.Open.TotalFlow(d.ValveMasks, d.Valves),
							},
						)
					}
				}
			}

			return next
		},
		start,
		func(cur CurState) bool {
			if cur.Time > 30 {
				panic(">30")
			}
			return cur.Time == 30
		}, maxFlowPerMinute)

	// fmt.Printf("%v\n", best)
	// fmt.Printf("d %v\n", lib.MaxList(lib.Values(dists)))
	// fmt.Printf("d %v\n", lib.MinList(lib.Values(dists)))
	// return x

	return ans
}

func (d *Day16) Part2(isTest bool) int {
	var ans int

	return ans
}
