package d15

import (
	"sort"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Sensor lib.Point[int]
type Beacon lib.Point[int]

type Pair struct {
	S Sensor
	B Beacon
}

type Day15 struct {
	SBPairs []Pair
}

func (d *Day15) LoadInput(lines []string) error {
	for _, line := range lines {
		x := lib.AllInts(line)
		d.SBPairs = append(d.SBPairs, Pair{
			S: Sensor{X: x[0], Y: x[1]},
			B: Beacon{X: x[2], Y: x[3]},
		})
	}
	return nil
}

func (d *Day15) Part1(istest bool) int {
	line := 2000000
	if istest {
		line = 10
	}

	nobeacon := ds.Set[int]{}

	for _, p := range d.SBPairs {
		maxDist := lib.AbsInt(p.S.X-p.B.X) + lib.AbsInt(p.S.Y-p.B.Y)
		eachSide := maxDist - lib.AbsInt(p.S.Y-line)
		if eachSide >= 0 {
			nobeacon.Add(p.S.X)
			for i := p.S.X - eachSide; i <= p.S.X+eachSide; i++ {
				nobeacon.Add(i)
			}
		}
	}
	for _, p := range d.SBPairs {
		if p.B.Y == line {
			nobeacon.Remove(p.B.X)
		}
	}

	return len(nobeacon)
}

func (d *Day15) Part2(istest bool) int64 {
	// The distress beacon is not detected by any sensor, but the distress
	// beacon must have x and y coordinates each no lower than 0 and no larger
	// than 4000000.

	// In the example above, the search space is smaller: instead, the x and y
	// coordinates can each be at most 20. With this reduced search area, there
	// is only a single position that could have a beacon: x=14, y=11. The
	// tuning frequency for this distress beacon is 56000011.

	boundlo := 0
	boundhi := 4000000
	if istest {
		boundlo = 0
		boundhi = 20
	}

	// fmt.Printf("%v\n", d.SBPairs)
	// candidate := ds.Set[lib.Point[int]]{}

	for y := boundlo; y < boundhi; y++ {
		// covers := ds.Set[struct{ lo, hi int }]{}
		sort.Slice(d.SBPairs, func(i, j int) bool {
			pi := d.SBPairs[i]
			pj := d.SBPairs[j]
			maxDistI := lib.AbsInt(pi.S.X-pi.B.X) + lib.AbsInt(pi.S.Y-pi.B.Y)
			maxDistJ := lib.AbsInt(pj.S.X-pj.B.X) + lib.AbsInt(pj.S.Y-pj.B.Y)
			eachSideI := maxDistI - lib.AbsInt(pi.S.Y-y)
			eachSideJ := maxDistJ - lib.AbsInt(pj.S.Y-y)

			return pi.S.X - eachSideI < pj.S.X - eachSideJ

			// return d.SBPairs[i].S.X < d.SBPairs[j].S.X
		})
		// fmt.Printf("Y %d\n", y)
		// fmt.Printf("%v\n", d.SBPairs)
		var coveredhi, coveredlo int
		for _, p := range d.SBPairs {
			maxDist := lib.AbsInt(p.S.X-p.B.X) + lib.AbsInt(p.S.Y-p.B.Y)
			eachSide := maxDist - lib.AbsInt(p.S.Y-y)
			if eachSide < 0 {
				continue
			}
			// unioned := false
			// for cover := range covers {
			// 	coveredlo := lib.Min(cover.lo, p.S.X-eachSide)
			// 	coveredhi := lib.Max(cover.hi, p.S.X+eachSide)
			// 	covers.Add(struct {
			// 		lo int
			// 		hi int
			// 	}{coveredlo, coveredhi})
			// 	covers.Remove(cover)
			// 	unioned
			// }

			// // fmt.Printf("%d %d\n", p.S.X-eachSide, p.S.X+eachSide)
			if coveredhi < p.S.X-eachSide -1{
				// candidate.Add(lib.Point[int]{p.S.X - eachSide - 1, y})
				return int64(p.S.X-eachSide-1)*4000000 + int64(y)
			}

			coveredlo = lib.Min(coveredlo, p.S.X-eachSide)
			coveredhi = lib.Max(coveredhi, p.S.X+eachSide)
			// if eachSide >= 0 {
			// 	for i := lib.Max(boundlo, p.S.X-eachSide); i <= lib.Min(boundhi-1, p.S.X+eachSide); i++ {
			// 		nobeacon.Add(i)
			// 	}
			// }
		}
		// fmt.Printf("covers %v\n", covers)
		// fmt.Printf("%d %d\n", coveredhi, coveredlo)

		// if len(nobeacon) < boundhi {
		// 	for x := boundlo; x < boundhi; x++ {
		// 		if !nobeacon.Contains(x) {
		// 			fmt.Printf("%d %d\n", x, y)
		// 			return x*4000000 + y
		// 		}
		// 	}
		// }
	}
	// fmt.Printf("candidae %v\n", candidate)
	panic("ohea")
}
