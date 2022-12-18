package d18

import (
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Point3 struct{ x, y, z int }

type Day18 struct {
	Cubes ds.Set[Point3]
}

func (d *Day18) LoadInput(lines []string) error {
	d.Cubes = ds.Set[Point3]{}
	for _, line := range lines {
		x := lib.AllInts(line)
		d.Cubes.Add(Point3{x[0], x[1], x[2]})
	}
	return nil
}

func DetectExposed(cubes ds.Set[Point3]) int {
	exposed := 0
	for c := range cubes {
		covered := 0
		if cubes.Contains(Point3{c.x, c.y, c.z - 1}) {
			covered++
		}
		if cubes.Contains(Point3{c.x, c.y, c.z + 1}) {
			covered++
		}
		if cubes.Contains(Point3{c.x - 1, c.y, c.z}) {
			covered++
		}
		if cubes.Contains(Point3{c.x + 1, c.y, c.z}) {
			covered++
		}
		if cubes.Contains(Point3{c.x, c.y - 1, c.z}) {
			covered++
		}
		if cubes.Contains(Point3{c.x, c.y + 1, c.z}) {
			covered++
		}
		exposed += 6 - covered
	}
	return exposed
}

func (d *Day18) Part1(isTest bool) int {
	return DetectExposed(d.Cubes)
}

func (d *Day18) Part2(isTest bool) int {
	minx, maxx := lib.MinMaxListFn(d.Cubes.List(), func(p Point3) int { return p.x })
	miny, maxy := lib.MinMaxListFn(d.Cubes.List(), func(p Point3) int { return p.y })
	minz, maxz := lib.MinMaxListFn(d.Cubes.List(), func(p Point3) int { return p.z })

	invert := func(points ds.Set[Point3]) ds.Set[Point3] {
		inverted := ds.Set[Point3]{}

		for x := minx - 1; x <= maxx+1; x++ {
			for y := miny - 1; y <= maxy+1; y++ {
				for z := minz - 1; z <= maxz+1; z++ {
					if !points.Contains(Point3{x, y, z}) {
						inverted.Add(Point3{x, y, z})
					}
				}
			}
		}
		return inverted
	}

	inverted := invert(d.Cubes)

	outer := ds.Set[Point3]{}
	frontier := ds.NewSetFromValues(Point3{minx - 1, miny - 1, minz - 1})
	for len(frontier) > 0 {
		cur := frontier.Pop()
		if outer.Contains(cur) || !inverted.Contains(cur) {
			continue
		}
		outer.Add(cur)

		frontier.Add(Point3{cur.x, cur.y + 1, cur.z})
		frontier.Add(Point3{cur.x, cur.y - 1, cur.z})
		frontier.Add(Point3{cur.x + 1, cur.y, cur.z})
		frontier.Add(Point3{cur.x - 1, cur.y, cur.z})
		frontier.Add(Point3{cur.x, cur.y, cur.z + 1})
		frontier.Add(Point3{cur.x, cur.y, cur.z - 1})
	}

	return DetectExposed(invert(outer))
}
