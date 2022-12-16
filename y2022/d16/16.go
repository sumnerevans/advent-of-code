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
	Valves    map[string]Valve
	Distances map[string]map[string]int
}

func (d *Day16) LoadInput(lines []string) error {
	valves := map[string]Valve{}
	for _, line := range lines {
		grps := lib.ReGroups(`Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)`, line)
		name := grps[0]
		flow := lib.ToInt(grps[1])
		adj := ds.Set[ds.Edge[string, int]]{}
		for _, x := range strings.Split(grps[2], ", ") {
			adj.Add(ds.Edge[string, int]{1, x})
		}
		valves[name] = Valve{Flow: flow, Adj: adj}
	}

	d.Distances = map[string]map[string]int{}
	for name := range valves {
		d.Distances[name] = map[string]int{}
		pq := ds.NewPriorityQueue(ds.NewPair(0, name))
		seen := ds.Set[string]{}
		for pq.Len() > 0 {
			cost, el := pq.Pop()
			seen.Add(el)
			if _, ok := d.Distances[name][el]; !ok {
				d.Distances[name][el] = cost
			}
			for a := range valves[el].Adj {
				if !seen.Contains(a.Vertex) {
					pq.Push(cost+1, a.Vertex)
				}
			}
		}
	}
	fmt.Printf("dist %v\n", d.Distances)

	panic(1)

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

type CurOpens struct {
	ValveAA bool
	ValveBB bool
	ValveCC bool
	ValveDD bool
	ValveEE bool
	ValveFF bool
	ValveGG bool
	ValveHH bool
	ValveII bool
	ValveJJ bool

	ValveAD bool
	ValveAN bool
	ValveBU bool
	ValveBV bool
	ValveCK bool
	ValveDS bool
	ValveDV bool
	ValveDW bool
	ValveEG bool
	ValveEL bool
	ValveEV bool
	ValveFB bool
	ValveFE bool
	ValveFT bool
	ValveGC bool
	ValveGE bool
	ValveGI bool
	ValveGS bool
	ValveGV bool
	ValveHB bool
	ValveHI bool
	ValveHO bool
	ValveHS bool
	ValveIQ bool
	ValveJA bool
	ValveJG bool
	ValveJH bool
	ValveJV bool
	ValveKS bool
	ValveKU bool
	ValveLS bool
	ValveLT bool
	ValveNK bool
	ValveNY bool
	ValveOI bool
	ValveQU bool
	ValveRD bool
	ValveRM bool
	ValveSD bool
	ValveSS bool
	ValveSV bool
	ValveTC bool
	ValveTJ bool
	ValveTV bool
	ValveUU bool
	ValveUY bool
	ValveVA bool
	ValveWB bool
	ValveWI bool
	ValveWJ bool
	ValveYC bool
	ValveYP bool
	ValveYZ bool
	ValveZH bool
	ValveZN bool
	ValveZV bool
}

func (co CurOpens) IsOpen(v string) bool {
	switch v {

	case "AA":
		return co.ValveAA
	case "BB":
		return co.ValveBB
	case "CC":
		return co.ValveCC
	case "DD":
		return co.ValveDD
	case "EE":
		return co.ValveEE
	case "FF":
		return co.ValveFF
	case "GG":
		return co.ValveGG
	case "HH":
		return co.ValveHH
	case "II":
		return co.ValveII
	case "JJ":
		return co.ValveJJ

	case "AD":
		return co.ValveAD
	case "AN":
		return co.ValveAN
	case "BU":
		return co.ValveBU
	case "BV":
		return co.ValveBV
	case "CK":
		return co.ValveCK
	case "DS":
		return co.ValveDS
	case "DV":
		return co.ValveDV
	case "DW":
		return co.ValveDW
	case "EG":
		return co.ValveEG
	case "EL":
		return co.ValveEL
	case "EV":
		return co.ValveEV
	case "FB":
		return co.ValveFB
	case "FE":
		return co.ValveFE
	case "FT":
		return co.ValveFT
	case "GC":
		return co.ValveGC
	case "GE":
		return co.ValveGE
	case "GI":
		return co.ValveGI
	case "GS":
		return co.ValveGS
	case "GV":
		return co.ValveGV
	case "HB":
		return co.ValveHB
	case "HI":
		return co.ValveHI
	case "HO":
		return co.ValveHO
	case "HS":
		return co.ValveHS
	case "IQ":
		return co.ValveIQ
	case "JA":
		return co.ValveJA
	case "JG":
		return co.ValveJG
	case "JH":
		return co.ValveJH
	case "JV":
		return co.ValveJV
	case "KS":
		return co.ValveKS
	case "KU":
		return co.ValveKU
	case "LS":
		return co.ValveLS
	case "LT":
		return co.ValveLT
	case "NK":
		return co.ValveNK
	case "NY":
		return co.ValveNY
	case "OI":
		return co.ValveOI
	case "QU":
		return co.ValveQU
	case "RD":
		return co.ValveRD
	case "RM":
		return co.ValveRM
	case "SD":
		return co.ValveSD
	case "SS":
		return co.ValveSS
	case "SV":
		return co.ValveSV
	case "TC":
		return co.ValveTC
	case "TJ":
		return co.ValveTJ
	case "TV":
		return co.ValveTV
	case "UU":
		return co.ValveUU
	case "UY":
		return co.ValveUY
	case "VA":
		return co.ValveVA
	case "WB":
		return co.ValveWB
	case "WI":
		return co.ValveWI
	case "WJ":
		return co.ValveWJ
	case "YC":
		return co.ValveYC
	case "YP":
		return co.ValveYP
	case "YZ":
		return co.ValveYZ
	case "ZH":
		return co.ValveZH
	case "ZN":
		return co.ValveZN
	case "ZV":
		return co.ValveZV
	default:
		panic(v)
	}
}

// func (co CurOpens) AllOpen() bool {
// 	return (co.ValveAA &&
// 		co.ValveBB &&
// 		co.ValveCC &&
// 		co.ValveDD &&
// 		co.ValveEE &&
// 		co.ValveFF &&
// 		co.ValveGG &&
// 		co.ValveHH &&
// 		co.ValveII &&
// 		co.ValveJJ) || (co.ValveAA &&
// 		co.ValveAD &&
// 		co.ValveAN &&
// 		co.ValveBU &&
// 		co.ValveBV &&
// 		co.ValveCK &&
// 		co.ValveDS &&
// 		co.ValveDV &&
// 		co.ValveDW &&
// 		co.ValveEG &&
// 		co.ValveEL &&
// 		co.ValveEV &&
// 		co.ValveFB &&
// 		co.ValveFE &&
// 		co.ValveFT &&
// 		co.ValveGC &&
// 		co.ValveGE &&
// 		co.ValveGI &&
// 		co.ValveGS &&
// 		co.ValveGV &&
// 		co.ValveHB &&
// 		co.ValveHI &&
// 		co.ValveHO &&
// 		co.ValveHS &&
// 		co.ValveIQ &&
// 		co.ValveJA &&
// 		co.ValveJG &&
// 		co.ValveJH &&
// 		co.ValveJV &&
// 		co.ValveKS &&
// 		co.ValveKU &&
// 		co.ValveLS &&
// 		co.ValveLT &&
// 		co.ValveNK &&
// 		co.ValveNY &&
// 		co.ValveOI &&
// 		co.ValveQU &&
// 		co.ValveRD &&
// 		co.ValveRM &&
// 		co.ValveSD &&
// 		co.ValveSS &&
// 		co.ValveSV &&
// 		co.ValveTC &&
// 		co.ValveTJ &&
// 		co.ValveTV &&
// 		co.ValveUU &&
// 		co.ValveUY &&
// 		co.ValveVA &&
// 		co.ValveWB &&
// 		co.ValveWI &&
// 		co.ValveWJ &&
// 		co.ValveYC &&
// 		co.ValveYP &&
// 		co.ValveYZ &&
// 		co.ValveZH &&
// 		co.ValveZN &&
// 		co.ValveZV)
// }

func (co CurOpens) TotalFlow(flows map[string]Valve) int {
	sum := 0
	if co.ValveAA {
		sum += flows["AA"].Flow
	}
	if co.ValveBB {
		sum += flows["BB"].Flow
	}
	if co.ValveCC {
		sum += flows["CC"].Flow
	}
	if co.ValveDD {
		sum += flows["DD"].Flow
	}
	if co.ValveEE {
		sum += flows["EE"].Flow
	}
	if co.ValveFF {
		sum += flows["FF"].Flow
	}
	if co.ValveGG {
		sum += flows["GG"].Flow
	}
	if co.ValveHH {
		sum += flows["HH"].Flow
	}
	if co.ValveII {
		sum += flows["II"].Flow
	}
	if co.ValveJJ {
		sum += flows["JJ"].Flow
	}

	if co.ValveAD {
		sum += flows["AD"].Flow
	}
	if co.ValveAN {
		sum += flows["AN"].Flow
	}
	if co.ValveBU {
		sum += flows["BU"].Flow
	}
	if co.ValveBV {
		sum += flows["BV"].Flow
	}
	if co.ValveCK {
		sum += flows["CK"].Flow
	}
	if co.ValveDS {
		sum += flows["DS"].Flow
	}
	if co.ValveDV {
		sum += flows["DV"].Flow
	}
	if co.ValveDW {
		sum += flows["DW"].Flow
	}
	if co.ValveEG {
		sum += flows["EG"].Flow
	}
	if co.ValveEL {
		sum += flows["EL"].Flow
	}
	if co.ValveEV {
		sum += flows["EV"].Flow
	}
	if co.ValveFB {
		sum += flows["FB"].Flow
	}
	if co.ValveFE {
		sum += flows["FE"].Flow
	}
	if co.ValveFT {
		sum += flows["FT"].Flow
	}
	if co.ValveGC {
		sum += flows["GC"].Flow
	}
	if co.ValveGE {
		sum += flows["GE"].Flow
	}
	if co.ValveGI {
		sum += flows["GI"].Flow
	}
	if co.ValveGS {
		sum += flows["GS"].Flow
	}
	if co.ValveGV {
		sum += flows["GV"].Flow
	}

	if co.ValveHB {
		sum += flows["HB"].Flow
	}
	if co.ValveHI {
		sum += flows["HI"].Flow
	}
	if co.ValveHO {
		sum += flows["HO"].Flow
	}
	if co.ValveHS {
		sum += flows["HS"].Flow
	}
	if co.ValveIQ {
		sum += flows["IQ"].Flow
	}
	if co.ValveJA {
		sum += flows["JA"].Flow
	}
	if co.ValveJG {
		sum += flows["JG"].Flow
	}
	if co.ValveJH {
		sum += flows["JH"].Flow
	}
	if co.ValveJV {
		sum += flows["JV"].Flow
	}
	if co.ValveKS {
		sum += flows["KS"].Flow
	}
	if co.ValveKU {
		sum += flows["KU"].Flow
	}
	if co.ValveLS {
		sum += flows["LS"].Flow
	}
	if co.ValveLT {
		sum += flows["LT"].Flow
	}
	if co.ValveNK {
		sum += flows["NK"].Flow
	}
	if co.ValveNY {
		sum += flows["NY"].Flow
	}
	if co.ValveOI {
		sum += flows["OI"].Flow
	}
	if co.ValveQU {
		sum += flows["QU"].Flow
	}
	if co.ValveRD {
		sum += flows["RD"].Flow
	}
	if co.ValveRM {
		sum += flows["RM"].Flow
	}
	if co.ValveSD {
		sum += flows["SD"].Flow
	}
	if co.ValveSS {
		sum += flows["SS"].Flow
	}
	if co.ValveSV {
		sum += flows["SV"].Flow
	}
	if co.ValveTC {
		sum += flows["TC"].Flow
	}
	if co.ValveTJ {
		sum += flows["TJ"].Flow
	}
	if co.ValveTV {
		sum += flows["TV"].Flow
	}
	if co.ValveUU {
		sum += flows["UU"].Flow
	}
	if co.ValveUY {
		sum += flows["UY"].Flow
	}
	if co.ValveVA {
		sum += flows["VA"].Flow
	}
	if co.ValveWB {
		sum += flows["WB"].Flow
	}
	if co.ValveWI {
		sum += flows["WI"].Flow
	}
	if co.ValveWJ {
		sum += flows["WJ"].Flow
	}
	if co.ValveYC {
		sum += flows["YC"].Flow
	}
	if co.ValveYP {
		sum += flows["YP"].Flow
	}
	if co.ValveYZ {
		sum += flows["YZ"].Flow
	}
	if co.ValveZH {
		sum += flows["ZH"].Flow
	}
	if co.ValveZN {
		sum += flows["ZN"].Flow
	}
	if co.ValveZV {
		sum += flows["ZV"].Flow
	}
	return sum
}

func (co CurOpens) WithOpen(v string) CurOpens {
	switch v {
	case "AA":
		co.ValveAA = true
	case "BB":
		co.ValveBB = true
	case "CC":
		co.ValveCC = true
	case "DD":
		co.ValveDD = true
	case "EE":
		co.ValveEE = true
	case "FF":
		co.ValveFF = true
	case "GG":
		co.ValveGG = true
	case "HH":
		co.ValveHH = true
	case "II":
		co.ValveII = true
	case "JJ":
		co.ValveJJ = true

	case "AD":
		co.ValveAD = true
	case "AN":
		co.ValveAN = true
	case "BU":
		co.ValveBU = true
	case "BV":
		co.ValveBV = true
	case "CK":
		co.ValveCK = true
	case "DS":
		co.ValveDS = true
	case "DV":
		co.ValveDV = true
	case "DW":
		co.ValveDW = true
	case "EG":
		co.ValveEG = true
	case "EL":
		co.ValveEL = true
	case "EV":
		co.ValveEV = true
	case "FB":
		co.ValveFB = true
	case "FE":
		co.ValveFE = true
	case "FT":
		co.ValveFT = true
	case "GC":
		co.ValveGC = true
	case "GE":
		co.ValveGE = true
	case "GI":
		co.ValveGI = true
	case "GS":
		co.ValveGS = true
	case "GV":
		co.ValveGV = true
	case "HB":
		co.ValveHB = true
	case "HI":
		co.ValveHI = true
	case "HO":
		co.ValveHO = true
	case "HS":
		co.ValveHS = true
	case "IQ":
		co.ValveIQ = true
	case "JA":
		co.ValveJA = true
	case "JG":
		co.ValveJG = true
	case "JH":
		co.ValveJH = true
	case "JV":
		co.ValveJV = true
	case "KS":
		co.ValveKS = true
	case "KU":
		co.ValveKU = true
	case "LS":
		co.ValveLS = true
	case "LT":
		co.ValveLT = true
	case "NK":
		co.ValveNK = true
	case "NY":
		co.ValveNY = true
	case "OI":
		co.ValveOI = true
	case "QU":
		co.ValveQU = true
	case "RD":
		co.ValveRD = true
	case "RM":
		co.ValveRM = true
	case "SD":
		co.ValveSD = true
	case "SS":
		co.ValveSS = true
	case "SV":
		co.ValveSV = true
	case "TC":
		co.ValveTC = true
	case "TJ":
		co.ValveTJ = true
	case "TV":
		co.ValveTV = true
	case "UU":
		co.ValveUU = true
	case "UY":
		co.ValveUY = true
	case "VA":
		co.ValveVA = true
	case "WB":
		co.ValveWB = true
	case "WI":
		co.ValveWI = true
	case "WJ":
		co.ValveWJ = true
	case "YC":
		co.ValveYC = true
	case "YP":
		co.ValveYP = true
	case "YZ":
		co.ValveYZ = true
	case "ZH":
		co.ValveZH = true
	case "ZN":
		co.ValveZN = true
	case "ZV":
		co.ValveZV = true
	}
	return co
}

type CurState struct {
	Open   CurOpens
	CurPos string
	Time   int
	Flow   int
}

// This isn't really BFS, I have no idea what it is
func BFS(
	nextStates func(CurState) ds.Set[CurState],
	start CurState,
	endState func(CurState) bool,
	maxFLowPerMinute int,
) int {
	// endStates := []CurState{}

	pq := ds.NewPriorityQueue(ds.NewPair(0, start))
	// seen := ds.Set[CurState]{}

	i := 0
	best := 0

	for pq.Len() > 0 {
		if i%10000000 == 0 {
			fmt.Printf("%d %d\n", pq.Len(), i)
		}
		i++
		_, el := pq.Pop()
		// if seen.Contains(el) {
		// 	continue
		// }

		if endState(el) {
			if el.Flow > best {
				fmt.Printf("%v\n", el)
				best = el.Flow
				fmt.Printf("best %d\n", best)
			}
			// fmt.Printf("ES %v\n", el)
			// endStates = append(endStates, el)
			continue
		}

		if el.Flow+(maxFLowPerMinute)*(29-el.Time) < best {
			continue
		}

		// if el.Open.AllOpen() {
		// 	continue
		// }

		// seen.Add(el)

		for e := range nextStates(el) {
			// if seen.Contains(e) {
			// 	continue
			// }
			pq.Push(0, e)
		}
	}

	return best
}

func (d *Day16) Part1(isTest bool) int {
	var ans int

	start := CurState{
		Open:   CurOpens{},
		CurPos: "AA",
		Time:   1,
		Flow:   0,
	}

	maxFlowPerMinute := lib.Sum(lib.Map(func(v Valve) int {
		return v.Flow
	})(lib.Values(d.Valves)))

	return BFS(
		func(cur CurState) ds.Set[CurState] {
			// fmt.Printf("cur %v\n", cur)
			next := ds.Set[CurState]{}

			// Open the valve
			if !cur.Open.IsOpen(cur.CurPos) {
				next.Add(
					CurState{
						Open:   cur.Open.WithOpen(cur.CurPos),
						CurPos: cur.CurPos,
						Time:   cur.Time + 1,
						Flow:   cur.Flow + cur.Open.TotalFlow(d.Valves),
					},
				)
			}

			// Move
			for v := range d.Valves[cur.CurPos].Adj {
				if cur.Time+v.Weight <= 30 {
					next.Add(
						CurState{
							Open:   cur.Open,
							CurPos: v.Vertex,
							Time:   cur.Time + v.Weight,
							Flow:   cur.Flow + cur.Open.TotalFlow(d.Valves),
						},
					)
				}
			}

			// Stay
			next.Add(
				CurState{
					Open:   cur.Open,
					CurPos: cur.CurPos,
					Time:   cur.Time + 1,
					Flow:   cur.Flow + cur.Open.TotalFlow(d.Valves),
				},
			)
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
