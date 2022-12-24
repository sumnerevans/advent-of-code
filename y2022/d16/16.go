package d16

import (
	"fmt"
	"sort"
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
	Dists      map[string]map[string]int

	DFS2Memo          map[Option]int
	DFS2Hit, DFS2Miss int
	DFS2Pruned        int
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

	d.Dists = map[string]map[string]int{}
	for startloc := range d.Valves {
		q := []ds.Edge[string, int]{{startloc, 0}}
		s := ds.Set[string]{}
		d.Dists[startloc] = map[string]int{}
		for len(q) > 0 {
			cur := q[0]
			q = q[1:]
			if s.Contains(cur.Vertex) {
				continue
			}
			s.Add(cur.Vertex)
			d.Dists[startloc][cur.Vertex] = cur.Weight

			for adj := range d.Valves[cur.Vertex].Adj {
				q = append(q, ds.Edge[string, int]{adj.Vertex, cur.Weight + 1})
			}
		}
	}
	d.DFS2Memo = map[Option]int{}

	return nil
}

type CurOpens int64

func (co CurOpens) String(maskMap map[string]int64) string {
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

	sort.Slice(opens, func(i, j int) bool { return opens[i] < opens[j] })

	return "[" + strings.Join(opens, ", ") + "]"
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
	if int64(co)&mask > 0 {
		panic("already open")
	}
	return CurOpens(int64(co) | mask)
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
					fmt.Printf("best2 %d: %s pruned=%d\n", best, e.String(d.ValveMasks), pruning)
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

type Option struct {
	Open           CurOpens
	CurPos, ElePos string
	Time           int
}

func (o Option) String(maskMap map[string]int64) string {
	return fmt.Sprintf("{%s @%s,%s t=%d}", o.Open.String(maskMap), lib.ColorString(o.CurPos, lib.ColorBlue), lib.ColorString(o.ElePos, lib.ColorBlue), o.Time)
}

func (d *Day16) DFS2(minutes int, maxFlowPerMinute int, opt Option) int {
	indent := ""
	for i := 0; i < opt.Time; i++ {
		indent += " "
	}

	// fmt.Printf("%sDFS %s\n", indent, opt.String(d.ValveMasks))

	if v, ok := d.DFS2Memo[opt]; ok {
		d.DFS2Hit++
		// fmt.Printf("%sMEM -> %d\n", indent, v)
		return v
	}
	d.DFS2Miss++

	if opt.Time == minutes {
		total := opt.Open.TotalFlow(d.ValveMasks, d.Valves)
		d.DFS2Memo[opt] = total
		// fmt.Printf("%sBC -> %d\n", indent, total)
		return total
	} else if opt.Time > minutes {
		panic(">MIN")
	}

	options := []Option{}

	// Both open (must be at different places)
	if opt.CurPos != opt.ElePos &&
		d.Valves[opt.CurPos].Flow > 0 && !opt.Open.IsOpen(d.ValveMasks[opt.CurPos]) &&
		d.Valves[opt.ElePos].Flow > 0 && !opt.Open.IsOpen(d.ValveMasks[opt.ElePos]) {
		options = append(options, Option{opt.Open.WithOpen(d.ValveMasks[opt.CurPos]).WithOpen(d.ValveMasks[opt.ElePos]), opt.CurPos, opt.ElePos, opt.Time + 1})
	}
	// We open, elephant moves
	if d.Valves[opt.CurPos].Flow > 0 && !opt.Open.IsOpen(d.ValveMasks[opt.CurPos]) {
		for adj := range d.Valves[opt.ElePos].Adj {
			options = append(options, Option{opt.Open.WithOpen(d.ValveMasks[opt.CurPos]), opt.CurPos, adj.Vertex, opt.Time + 1})
		}
	}
	// Elephant opens, we move
	if d.Valves[opt.ElePos].Flow > 0 && !opt.Open.IsOpen(d.ValveMasks[opt.ElePos]) {
		for adj := range d.Valves[opt.CurPos].Adj {
			options = append(options, Option{opt.Open.WithOpen(d.ValveMasks[opt.ElePos]), adj.Vertex, opt.ElePos, opt.Time + 1})
		}
	}
	// Both move
	closestClosedToCur := lib.Values(lib.FilterMap(d.Dists[opt.CurPos], func(a string, dist int) bool {
		return a != opt.CurPos && d.Valves[a].Flow > 0 && !opt.Open.IsOpen(d.ValveMasks[a])
	}))
	closestClosedToEle := lib.Values(lib.FilterMap(d.Dists[opt.ElePos], func(a string, dist int) bool {
		return a != opt.ElePos && d.Valves[a].Flow > 0 && !opt.Open.IsOpen(d.ValveMasks[a])
	}))
	if len(closestClosedToCur) > 0 && len(closestClosedToEle) > 0 {
		curMinDist := lib.MinList(closestClosedToCur)
		eleMinDist := lib.MinList(closestClosedToEle)
		moveDist := lib.Min(curMinDist, eleMinDist)
		if opt.Time+moveDist <= minutes {
			for curAdj, curDist := range d.Dists[opt.CurPos] {
				if curDist != moveDist {
					continue
				}
				for eleAdj, eleDist := range d.Dists[opt.ElePos] {
					if eleDist != moveDist {
						continue
					}
					options = append(options, Option{opt.Open, curAdj, eleAdj, opt.Time + moveDist})
				}
			}
		}
	}

	if len(options) == 0 {
		// Nothing we can do, just stay
		// fmt.Printf("STAY %v\n", opt.Open.String(d.ValveMasks))
		// TODO is this off by 1? maybe the base case should be 0
		options = append(options, Option{opt.Open, opt.CurPos, opt.ElePos, opt.Time + 1})
	}

	sort.Slice(options, func(i, j int) bool {
		return options[i].Open.Count() > options[j].Open.Count()
	})

	best := 0
	for _, o := range options {
		flow := (o.Time - opt.Time) * opt.Open.TotalFlow(d.ValveMasks, d.Valves)
		// if flow+(minutes-o.Time)*maxFlowPerMinute < best {
		// 	d.DFS2Pruned++
		// 	continue
		// }
		if o.CurPos > o.ElePos {
			o.CurPos, o.ElePos = o.ElePos, o.CurPos
		}

		step := d.DFS2(minutes, maxFlowPerMinute, o)
		if opt.Time == 1 || opt.Time == 10 || opt.Time == 15 {
			// fmt.Printf("STEP %v: %d\n", o.String(d.ValveMasks), step)
			fmt.Printf("STAT %d h=%d m=%d\n", opt.Time, d.DFS2Hit, d.DFS2Miss)
		}
		best = lib.Max(best, flow+step)
	}
	// fmt.Printf("%s-> %d\n", indent, best)
	d.DFS2Memo[opt] = best
	return best
}

func (d *Day16) Part2(isTest bool) int {
	maxFlowPerMinute := lib.Sum(lib.Map(func(v Valve) int {
		return v.Flow
	})(lib.Values(d.Valves)))

	d.DFS2Memo = map[Option]int{}
	val := d.DFS2(26, maxFlowPerMinute, Option{0, "AA", "AA", 1})
	fmt.Printf("PRUNED %d\n", d.DFS2Pruned)
	return val
}
