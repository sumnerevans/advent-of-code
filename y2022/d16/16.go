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
}

func (d *Day16) LoadInput(lines []string) error {
	d.Valves = map[string]Valve{}
	for _, line := range lines {
		grps := lib.ReGroups(`Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)`, line)
		name := grps[0]
		flow := lib.ToInt(grps[1])
		adj := ds.Set[ds.Edge[string, int]]{}
		for _, x := range strings.Split(grps[2], ", ") {
			adj.Add(ds.NewEdge(x, 1))
		}
		d.Valves[name] = Valve{Flow: flow, Adj: adj}
	}

	d.ValveMasks = map[string]int64{}
	i := 0
	for name := range d.Valves {
		d.ValveMasks[name] = 1 << i
		i++
	}

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
		if int64(co)&(1<<i) > 0 {
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
	ElePos string
	Time   int
	Flow   int
}

func (cs CurState) String(maskMap map[string]int64) string {
	return fmt.Sprintf("{%s Y@%s E@%s t=%d f=%d}", cs.Open.String(maskMap), cs.CurPos, cs.ElePos, cs.Time, cs.Flow)
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

// This isn't really DFS, I have no idea what it is. All I know that it's a
// horrible mess and I'm very ashamed of it lol.
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
	seen := ds.Set[CurState]{}

	i := 0
	best := 0

	pruning := 0

	// for stack.Peek() != nil {
	for pq.Len() > 0 {
		if i%10000000 == 0 {
			// fmt.Printf("%d %d\n", stack.Len(), i)
			fmt.Printf("%d %d %d pruned=%d\n", pq.Len(), i, len(seen), pruning)
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
		if seen.Contains(el) {
			// fmt.Printf("BAR\n", )
			continue
		}

		seen.Add(el)

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
			if seen.Contains(e) {
				// fmt.Printf("FOO\n", )
				continue
			}

			if endState(e) {
				if e.Flow > best {
					// fmt.Printf("%v\n", el.String(d.ValveMasks))
					best = e.Flow
					fmt.Printf("best2 %d: %s\n", best, e.String(d.ValveMasks))
				}
				// fmt.Printf("ES %v\n", el)
				// endStates = append(endStates, el)
				continue
			}

			if e.Flow+(maxFlowPerMinute)*(30-e.Time) < best {
				pruning++
				continue
			}

			pq.Push(e.Open.Count()*1000+e.Flow, e)
		}
	}

	fmt.Printf("ITERS %d\n", i)
	fmt.Printf("PRUNED %d\n", pruning)

	return best
}

func (d *Day16) Part1(isTest bool) int {
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
			next := ds.Set[CurState]{}

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
}

func (d *Day16) Part2(isTest bool) int {
	start := CurState{
		Open:   0,
		CurPos: "AA",
		ElePos: "AA",
		Time:   0,
		Flow:   0,
	}

	maxFlowPerMinute := lib.Sum(lib.Map(func(v Valve) int {
		return v.Flow
	})(lib.Values(d.Valves)))

	return DFS(
		d,
		func(cur CurState) ds.Set[CurState] {
			next := ds.Set[CurState]{}

			// Stay
			if cur.Open.AllOpen(d.ValveMasks, d.Valves) {
				next.Add(
					CurState{
						Open:   cur.Open,
						CurPos: cur.CurPos,
						ElePos: cur.ElePos,
						Time:   26,
						Flow:   cur.Flow + (26-cur.Time)*cur.Open.TotalFlow(d.ValveMasks, d.Valves),
					},
				)
				return next
			} else {
				// Just you open the valve, elephant moves
				if d.Valves[cur.CurPos].Flow > 0 && !cur.Open.IsOpen(d.ValveMasks[cur.CurPos]) {
					for v := range d.Valves[cur.ElePos].Adj {
						if cur.Time+1 <= 26 {
							next.Add(
								CurState{
									Open:   cur.Open.WithOpen(d.ValveMasks[cur.CurPos]),
									CurPos: cur.CurPos,
									ElePos: v.Vertex,
									Time:   cur.Time + 1,
									Flow:   cur.Flow + cur.Open.TotalFlow(d.ValveMasks, d.Valves),
								},
							)
						}
					}
				}
				// Just elephant opens the valve, you move
				if d.Valves[cur.ElePos].Flow > 0 && !cur.Open.IsOpen(d.ValveMasks[cur.ElePos]) {
					for v := range d.Valves[cur.CurPos].Adj {
						if cur.Time+1 <= 26 {
							next.Add(
								CurState{
									Open:   cur.Open.WithOpen(d.ValveMasks[cur.ElePos]),
									CurPos: v.Vertex,
									ElePos: cur.ElePos,
									Time:   cur.Time + 1,
									Flow:   cur.Flow + cur.Open.TotalFlow(d.ValveMasks, d.Valves),
								},
							)
						}
					}
				}
				// Both open valves (must be at different valves)
				if d.ValveMasks[cur.ElePos] != d.ValveMasks[cur.CurPos] &&
					d.Valves[cur.ElePos].Flow > 0 && !cur.Open.IsOpen(d.ValveMasks[cur.ElePos]) &&
					d.Valves[cur.CurPos].Flow > 0 && !cur.Open.IsOpen(d.ValveMasks[cur.CurPos]) {
					next.Add(
						CurState{
							Open:   cur.Open.WithOpen(d.ValveMasks[cur.ElePos]).WithOpen(d.ValveMasks[cur.CurPos]),
							CurPos: cur.CurPos,
							ElePos: cur.ElePos,
							Time:   cur.Time + 1,
							Flow:   cur.Flow + cur.Open.TotalFlow(d.ValveMasks, d.Valves),
						},
					)
				}

				// Both move
				for newCurPos := range d.Valves[cur.CurPos].Adj {
					for newElePos := range d.Valves[cur.ElePos].Adj {
						if cur.Time+1 <= 26 {
							next.Add(
								CurState{
									Open:   cur.Open,
									CurPos: newCurPos.Vertex,
									ElePos: newElePos.Vertex,
									Time:   cur.Time + 1,
									Flow:   cur.Flow + cur.Open.TotalFlow(d.ValveMasks, d.Valves),
								},
							)
						}
					}
				}
			}

			return next
		},
		start,
		func(cur CurState) bool {
			if cur.Time > 26 {
				panic(">26")
			}
			return cur.Time == 26
		}, maxFlowPerMinute)
}
