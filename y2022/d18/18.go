package d18

import (
	"fmt"
	"sort"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Point3 struct{ x, y, z int }

type Day18 struct {
	Cubes []Point3
}

func (d *Day18) LoadInput(lines []string) error {
	for _, line := range lines {
		x := lib.AllInts(line)
		d.Cubes = append(d.Cubes, Point3{x[0], x[1], x[2]})
	}
	return nil
}

func (d *Day18) Part1(isTest bool) int {
	var ans int

	for _, c1 := range d.Cubes {
		shaded := []bool{false, false, false, false, false, false}
		for _, c2 := range d.Cubes {
			if c1.x == c2.x && c1.y == c2.y && c1.z == c2.z-1 {
				shaded[0] = true
			}
			if c1.x == c2.x && c1.y == c2.y && c1.z == c2.z+1 {
				shaded[1] = true
			}
			if c1.x == c2.x && c1.z == c2.z && c1.y == c2.y-1 {
				shaded[2] = true
			}
			if c1.x == c2.x && c1.z == c2.z && c1.y == c2.y+1 {
				shaded[3] = true
			}
			if c1.y == c2.y && c1.z == c2.z && c1.x == c2.x-1 {
				shaded[4] = true
			}
			if c1.y == c2.y && c1.z == c2.z && c1.x == c2.x+1 {
				shaded[5] = true
			}
		}
		for _, s := range shaded {
			if !s {
				ans++
			}
		}
	}

	return ans
}

func (d *Day18) Part2(isTest bool) int {
	var ans int

	minx, maxx := lib.MinMaxListFn(d.Cubes, func(p Point3) int { return p.x })
	miny, maxy := lib.MinMaxListFn(d.Cubes, func(p Point3) int { return p.y })
	minz, maxz := lib.MinMaxListFn(d.Cubes, func(p Point3) int { return p.z })

	cubesSet := ds.NewSetFromValues(d.Cubes...)
	inverted := ds.Set[Point3]{}

	for x := minx - 1; x <= maxx+1; x++ {
		for y := miny - 1; y <= maxy+1; y++ {
			for z := minz - 1; z <= maxz+1; z++ {
				if !cubesSet.Contains(Point3{x, y, z}) {
					inverted.Add(Point3{x, y, z})
				}
			}
		}
	}

	outer := ds.Set[Point3]{}
	frontier := ds.NewPriorityQueue(ds.NewPair(0, Point3{minx - 1, miny - 1, minz - 1}))
	fmt.Printf("f %v\n", frontier.String())
	for frontier.Len() > 0 {
		_, cur := frontier.Pop()
		if outer.Contains(cur) || !inverted.Contains(cur) {
			continue
		}
		outer.Add(cur)

		// up
		// if cur.y <= maxy+1 {
			up := Point3{cur.x, cur.y + 1, cur.z}
			// if inverted.Contains(up) {
			frontier.Push(0, up)
			// }
		// }
		// down
		// if cur.y >= miny-1 {
			down := Point3{cur.x, cur.y - 1, cur.z}
			// if inverted.Contains(down) {
			frontier.Push(0, down)
			// }
		// }
		// left
		// if cur.x <= minx+1 {
			left := Point3{cur.x + 1, cur.y, cur.z}
			// if inverted.Contains(left) {
			frontier.Push(0, left)
			// }
		// }
		// right
		// if cur.x >= minx-1 {
			right := Point3{cur.x - 1, cur.y, cur.z}
			// if inverted.Contains(right) {
			frontier.Push(0, right)
			// }
		// }
		// back
		// if cur.z <= minz+1 {
			back := Point3{cur.x, cur.y, cur.z + 1}
			// if inverted.Contains(back) {
			frontier.Push(0, back)
			// }
		// }
		// front
		// if cur.z >= minz-1 {
			front := Point3{cur.x, cur.y, cur.z - 1}
			// if inverted.Contains(front) {
			frontier.Push(0, front)
			// }
		// }
	}

	fmt.Printf("cs %v\n", cubesSet)
	fmt.Printf("inverted %v\n", inverted)
	fmt.Printf("inverted %v\n", len(inverted))
	fmt.Printf("outer %v\n", len(outer))
	fmt.Printf("inter %v\n", len(inverted.Intersection(outer)))
	// panic("ohea")

	filledIn := ds.Set[Point3]{}
	for x := minx; x <= maxx; x++ {
		for y := miny; y <= maxy; y++ {
			for z := minz; z <= maxz; z++ {
				if !outer.Contains(Point3{x, y, z}) {
					filledIn.Add(Point3{x, y, z})
				}
			}
		}
	}

	csl := cubesSet.List()
	sort.Slice(csl, func(i, j int) bool {
		return csl[i].x < csl[j].x || csl[i].y < csl[j].y || csl[i].z < csl[j].z
	})

	fil := filledIn.List()
	sort.Slice(fil, func(i, j int) bool {
		return fil[i].x < fil[j].x || fil[i].y < fil[j].y || fil[i].z < fil[j].z
	})

	fics := filledIn.Sub(cubesSet).List()
	sort.Slice(fics, func(i, j int) bool {
		return fics[i].x < fics[j].x || fics[i].y < fics[j].y || fics[i].z < fics[j].z
	})

	fmt.Printf("cs   : %d %v\n", len(cubesSet), csl)
	fmt.Printf("fi   : %d %v\n", len(filledIn), fil)
	fmt.Printf("fi-cs: %d %v\n", len(filledIn.Sub(cubesSet)), fics)

	for c1 := range filledIn {
		shaded := []bool{false, false, false, false, false, false}
		for c2 := range filledIn {
			if c1.x == c2.x && c1.y == c2.y && c1.z == c2.z-1 {
				shaded[0] = true
			}
			if c1.x == c2.x && c1.y == c2.y && c1.z == c2.z+1 {
				shaded[1] = true
			}
			if c1.x == c2.x && c1.z == c2.z && c1.y == c2.y-1 {
				shaded[2] = true
			}
			if c1.x == c2.x && c1.z == c2.z && c1.y == c2.y+1 {
				shaded[3] = true
			}
			if c1.y == c2.y && c1.z == c2.z && c1.x == c2.x-1 {
				shaded[4] = true
			}
			if c1.y == c2.y && c1.z == c2.z && c1.x == c2.x+1 {
				shaded[5] = true
			}
		}
		for _, s := range shaded {
			if !s {
				ans++
			}
		}
	}

	return ans
}
