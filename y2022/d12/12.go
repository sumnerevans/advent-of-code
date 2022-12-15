package d12

import (
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day12 struct {
	Map [][]rune
}

func (d *Day12) LoadInput(lines []string) error {
	for i, line := range lines {
		d.Map = append(d.Map, []rune{})
		for _, c := range line {
			d.Map[i] = append(d.Map[i], c)
		}
	}
	return nil
}

func (d *Day12) Part1() int {
	var start, end lib.GridPoint[int]

	for r, row := range d.Map {
		for c, char := range row {
			if char == 'S' {
				start = lib.NewGridPoint(r, c)
				d.Map[r][c] = 'a'
			} else if char == 'E' {
				end = lib.NewGridPoint(r, c)
				d.Map[r][c] = 'z'
			}
		}
	}

	return lib.Dijkstra(
		func(loc lib.GridPoint[int]) ds.Set[ds.Edge[lib.GridPoint[int], int]] {
			curVal := d.Map[loc.R][loc.C]
			adj := ds.Set[ds.Edge[lib.GridPoint[int], int]]{}
			if loc.R > 0 && d.Map[loc.R-1][loc.C] <= curVal+1 {
				adj.Add(ds.Edge[lib.GridPoint[int], int]{
					Weight: 1,
					Vertex: lib.NewGridPoint(loc.R-1, loc.C),
				})
			}
			if loc.R < len(d.Map)-1 && d.Map[loc.R+1][loc.C] <= curVal+1 {
				adj.Add(ds.Edge[lib.GridPoint[int], int]{
					Weight: 1,
					Vertex: lib.NewGridPoint(loc.R+1, loc.C),
				})
			}
			if loc.C > 0 && d.Map[loc.R][loc.C-1] <= curVal+1 {
				adj.Add(ds.Edge[lib.GridPoint[int], int]{
					Weight: 1,
					Vertex: lib.NewGridPoint(loc.R, loc.C-1),
				})
			}
			if loc.C < len(d.Map[0])-1 && d.Map[loc.R][loc.C+1] <= curVal+1 {
				adj.Add(ds.Edge[lib.GridPoint[int], int]{
					Weight: 1,
					Vertex: lib.NewGridPoint(loc.R, loc.C+1),
				})
			}
			return adj
		},
		start,
		func(loc lib.GridPoint[int]) bool {
			return loc == end
		},
	)
}

func (d *Day12) Part2() int {
	var start, end lib.GridPoint[int]
	start = lib.NewGridPoint(-1, -1)

	for r, row := range d.Map {
		for c, char := range row {
			if char == 'S' {
				d.Map[r][c] = 'a'
			} else if char == 'E' {
				end = lib.NewGridPoint(r, c)
				d.Map[r][c] = 'z'
			}
		}
	}

	return lib.Dijkstra(
		func(loc lib.GridPoint[int]) ds.Set[ds.Edge[lib.GridPoint[int], int]] {
			adj := ds.Set[ds.Edge[lib.GridPoint[int], int]]{}
			if loc.C == -1 {
				for r, row := range d.Map {
					for c, char := range row {
						if char == 'a' {
							adj.Add(ds.Edge[lib.GridPoint[int], int]{
								Weight: 0,
								Vertex: lib.NewGridPoint(r, c),
							})
						}
					}
				}
				return adj
			}

			curVal := d.Map[loc.R][loc.C]
			if loc.R > 0 && d.Map[loc.R-1][loc.C] <= curVal+1 {
				adj.Add(ds.Edge[lib.GridPoint[int], int]{
					Weight: 1,
					Vertex: lib.NewGridPoint(loc.R-1, loc.C),
				})
			}
			if loc.R < len(d.Map)-1 && d.Map[loc.R+1][loc.C] <= curVal+1 {
				adj.Add(ds.Edge[lib.GridPoint[int], int]{
					Weight: 1,
					Vertex: lib.NewGridPoint(loc.R+1, loc.C),
				})
			}
			if loc.C > 0 && d.Map[loc.R][loc.C-1] <= curVal+1 {
				adj.Add(ds.Edge[lib.GridPoint[int], int]{
					Weight: 1,
					Vertex: lib.NewGridPoint(loc.R, loc.C-1),
				})
			}
			if loc.C < len(d.Map[0])-1 && d.Map[loc.R][loc.C+1] <= curVal+1 {
				adj.Add(ds.Edge[lib.GridPoint[int], int]{
					Weight: 1,
					Vertex: lib.NewGridPoint(loc.R, loc.C+1),
				})
			}
			return adj
		},
		start,
		func(loc lib.GridPoint[int]) bool {
			return loc == end
		},
	)
}
