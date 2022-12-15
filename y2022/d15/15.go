package d15

import (
	"sort"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type SensorBeaconPair struct {
	Sensor lib.Point[int]
	Beacon lib.Point[int]
}

type Day15 struct {
	Pairs []SensorBeaconPair
}

func (d *Day15) LoadInput(lines []string) error {
	for _, line := range lines {
		x := lib.AllInts(line)
		d.Pairs = append(d.Pairs, SensorBeaconPair{
			Sensor: lib.Point[int]{X: x[0], Y: x[1]},
			Beacon: lib.Point[int]{X: x[2], Y: x[3]},
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

	for _, p := range d.Pairs {
		maxDist := lib.AbsInt(p.Sensor.X-p.Beacon.X) + lib.AbsInt(p.Sensor.Y-p.Beacon.Y)
		eachSide := maxDist - lib.AbsInt(p.Sensor.Y-line)
		if eachSide >= 0 {
			nobeacon.Add(p.Sensor.X)
			for i := p.Sensor.X - eachSide; i <= p.Sensor.X+eachSide; i++ {
				nobeacon.Add(i)
			}
		}
	}
	for _, p := range d.Pairs {
		if p.Beacon.Y == line {
			nobeacon.Remove(p.Beacon.X)
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

	for y := boundlo; y < boundhi; y++ {
		sort.Slice(d.Pairs, func(i, j int) bool {
			pi := d.Pairs[i]
			pj := d.Pairs[j]
			maxDistI := lib.AbsInt(pi.Sensor.X-pi.Beacon.X) + lib.AbsInt(pi.Sensor.Y-pi.Beacon.Y)
			maxDistJ := lib.AbsInt(pj.Sensor.X-pj.Beacon.X) + lib.AbsInt(pj.Sensor.Y-pj.Beacon.Y)
			eachSideI := maxDistI - lib.AbsInt(pi.Sensor.Y-y)
			eachSideJ := maxDistJ - lib.AbsInt(pj.Sensor.Y-y)

			return pi.Sensor.X-eachSideI < pj.Sensor.X-eachSideJ
		})

		var coveredhi, coveredlo int
		for _, p := range d.Pairs {
			maxDist := lib.AbsInt(p.Sensor.X-p.Beacon.X) + lib.AbsInt(p.Sensor.Y-p.Beacon.Y)
			eachSide := maxDist - lib.AbsInt(p.Sensor.Y-y)
			if eachSide < 0 {
				continue
			}

			if coveredhi < p.Sensor.X-eachSide-1 {
				return int64(p.Sensor.X-eachSide-1)*4000000 + int64(y)
			}

			coveredlo = lib.Min(coveredlo, p.Sensor.X-eachSide)
			coveredhi = lib.Max(coveredhi, p.Sensor.X+eachSide)
		}
	}
	panic("no answer found!")
}
