package d19

import (
	"fmt"
	"runtime"

	"github.com/sumnerevans/advent-of-code/lib"
)

type ObsidianCost struct {
	OreCost  int
	ClayCost int
}

func (o ObsidianCost) String() string {
	return fmt.Sprintf("o=%d, c=%d", o.OreCost, o.ClayCost)
}

type GeodeCost struct {
	OreCost      int
	ObsidianCost int
}

func (g GeodeCost) String() string {
	return fmt.Sprintf("o=%d, ob=%d", g.OreCost, g.ObsidianCost)
}

type Blueprint struct {
	OreCost      int
	ClayCost     int
	ObsidianCost ObsidianCost
	GeodeCost    GeodeCost
}

func (b Blueprint) String() string {
	return fmt.Sprintf("o=%d c=%d ob={%v}, g={%v}", b.OreCost, b.ClayCost, b.ObsidianCost, b.GeodeCost)
}

type Day19 struct {
	Blueprints []Blueprint
}

func (d *Day19) LoadInput(lines []string) error {
	for _, line := range lines {
		x := lib.AllInts(line)
		d.Blueprints = append(d.Blueprints, Blueprint{
			OreCost:  x[1],
			ClayCost: x[2],
			ObsidianCost: ObsidianCost{
				OreCost:  x[3],
				ClayCost: x[4],
			},
			GeodeCost: GeodeCost{
				OreCost:      x[5],
				ObsidianCost: x[6],
			},
		})
	}
	return nil
}

type DPKey struct {
	b                                                                             Blueprint
	t, ores, clays, obsidians, oreRobots, clayRobots, obsidianRobots, geodeRobots int
}

func (d DPKey) String() string {
	return fmt.Sprintf("b={%v}, t=%d, quants=[%d, %d, %d], robots=[%d, %d, %d, %d]", d.b, d.t, d.ores, d.clays, d.obsidians, d.oreRobots, d.clayRobots, d.obsidianRobots, d.geodeRobots)
}

var DP map[DPKey]int
var hits = 0

func GeodeCount(k DPKey) int {
	// fmt.Printf("%v %d %d\n", k, len(DP), hits)
	// if len(DP) > 10 {
	// 	panic("debug")
	// }
	if val, ok := DP[k]; ok {
		hits++
		// fmt.Printf("HIT %v\n", k)
		return val
	}
	if k.t == 0 {
		return 0
	}

	// Option don't make any robots
	best := k.geodeRobots

	if k.ores >= k.b.GeodeCost.OreCost && k.obsidians >= k.b.GeodeCost.ObsidianCost {
		// Option: make geode robot
		best = lib.Max(best, k.geodeRobots+GeodeCount(DPKey{
			k.b, k.t - 1,
			k.ores + k.oreRobots - k.b.GeodeCost.OreCost, k.clays + k.clayRobots, k.obsidians + k.obsidianRobots - k.b.GeodeCost.ObsidianCost,
			k.oreRobots, k.clayRobots, k.obsidianRobots, k.geodeRobots + 1,
		}))
	} else {
		if k.ores >= k.b.ObsidianCost.OreCost && k.clays >= k.b.ObsidianCost.ClayCost {
			// Option: make obsidian robot
			best = lib.Max(best, k.geodeRobots+GeodeCount(DPKey{
				k.b, k.t - 1,
				k.ores + k.oreRobots - k.b.ObsidianCost.OreCost, k.clays + k.clayRobots - k.b.ObsidianCost.ClayCost, k.obsidians + k.obsidianRobots,
				k.oreRobots, k.clayRobots, k.obsidianRobots + 1, k.geodeRobots,
			}))
		} else {
			if k.ores >= k.b.ClayCost {
				// Option: make clay robot
				best = lib.Max(best, k.geodeRobots+GeodeCount(DPKey{
					k.b, k.t - 1,
					k.ores + k.oreRobots - k.b.ClayCost, k.clays + k.clayRobots, k.obsidians + k.obsidianRobots,
					k.oreRobots, k.clayRobots + 1, k.obsidianRobots, k.geodeRobots,
				}))
			}

			// Option: make ore robot
			if k.ores >= k.b.OreCost {
				best = lib.Max(best, k.geodeRobots+GeodeCount(DPKey{
					k.b, k.t - 1,
					k.ores + k.oreRobots - k.b.OreCost, k.clays + k.clayRobots, k.obsidians + k.obsidianRobots,
					k.oreRobots + 1, k.clayRobots, k.obsidianRobots, k.geodeRobots,
				}))
			}

			maxOres := lib.MaxList([]int{k.b.OreCost, k.b.ClayCost, k.b.ObsidianCost.OreCost, k.b.GeodeCost.OreCost})
			if k.ores < maxOres || k.clays < k.b.ClayCost || k.obsidians < k.b.GeodeCost.ObsidianCost {
				best = lib.Max(best, k.geodeRobots+GeodeCount(DPKey{
					k.b, k.t - 1,
					k.ores + k.oreRobots, k.clays + k.clayRobots, k.obsidians + k.obsidianRobots,
					k.oreRobots, k.clayRobots, k.obsidianRobots, k.geodeRobots,
				}))
			}
		}
	}

	DP[k] = best
	return best
}

func (d *Day19) Part1(isTest bool) int {
	var ans int

	for i, b := range d.Blueprints {
		DP = map[DPKey]int{}
		runtime.GC()
		fmt.Printf("Test blueprint %d\n", i+1)
		ans += (i + 1) * GeodeCount(DPKey{b, 24, 0, 0, 0, 1, 0, 0, 0})
	}
	// sum of quality level of each blueprint by multiplying that blueprint's ID number

	return ans
}

func (d *Day19) Part2(isTest bool) int {
	var ans int = 1

	for i, b := range d.Blueprints {
		if i == 3 {
			break
		}

		DP = map[DPKey]int{}
		runtime.GC()
		fmt.Printf("Test blueprint %d\n", i+1)
		ans *= GeodeCount(DPKey{b, 32, 0, 0, 0, 1, 0, 0, 0})
	}
	return ans
}
