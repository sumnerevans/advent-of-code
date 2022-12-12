package d12

import (
	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
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
	var start, end lib.Point[int]

	for r, row := range d.Map {
		for c, char := range row {
			if char == 'S' {
				start = lib.Point[int]{c, r}
			} else if char == 'E' {
				end = lib.Point[int]{c, r}
			}
		}
	}

	return lib.Dijkstra(
		func(loc lib.Point[int]) ds.Set[ds.Edge[lib.Point[int], int]] {
			curVal := d.Map[loc.Y][loc.X]
			if curVal == 'S' {
				curVal = 'a'
			}
			if curVal == 'E' {
				curVal = 'z'
			}
			adj := ds.Set[ds.Edge[lib.Point[int], int]]{}
			if loc.Y > 0 {
				ohea := d.Map[loc.Y-1][loc.X]
				if ohea == 'S' {
					ohea = 'a'
				}
				if ohea == 'E' {
					ohea = 'z'
				}
				if ohea <= curVal+1 {
					adj.Add(ds.Edge[lib.Point[int], int]{
						Weight: 1,
						Vertex: lib.Point[int]{loc.X, loc.Y - 1},
					})
				}
			}

			if loc.Y < len(d.Map)-1 {
				ohea := d.Map[loc.Y+1][loc.X]
				if ohea == 'S' {
					ohea = 'a'
				}
				if ohea == 'E' {
					ohea = 'z'
				}
				if ohea <= curVal+1 {
					adj.Add(ds.Edge[lib.Point[int], int]{
						Weight: 1,
						Vertex: lib.Point[int]{loc.X, loc.Y + 1},
					})
				}
			}
			if loc.X > 0 {
				ohea := d.Map[loc.Y][loc.X-1]
				if ohea == 'S' {
					ohea = 'a'
				}
				if ohea == 'E' {
					ohea = 'z'
				}
				if ohea <= curVal+1 {
					adj.Add(ds.Edge[lib.Point[int], int]{
						Weight: 1,
						Vertex: lib.Point[int]{loc.X - 1, loc.Y},
					})
				}
			}
			if loc.X < len(d.Map[0])-1 {
				ohea := d.Map[loc.Y][loc.X+1]
				if ohea == 'S' {
					ohea = 'a'
				}
				if ohea == 'E' {
					ohea = 'z'
				}
				if ohea <= curVal+1 {
					adj.Add(ds.Edge[lib.Point[int], int]{
						Weight: 1,
						Vertex: lib.Point[int]{loc.X + 1, loc.Y},
					})
				}
			}
			return adj
		},
		start,
		func(loc lib.Point[int]) bool {
			return loc.X == end.X && loc.Y == end.Y
		},
	)
}

func (d *Day12) Part2() int {
	var start, end lib.Point[int]

	for r, row := range d.Map {
		for c, char := range row {
			if char == 'S' {
				start = lib.Point[int]{-1, -1}
			} else if char == 'E' {
				end = lib.Point[int]{c, r}
			}
		}
	}

	return lib.Dijkstra(
		func(loc lib.Point[int]) ds.Set[ds.Edge[lib.Point[int], int]] {
			adj := ds.Set[ds.Edge[lib.Point[int], int]]{}
			if loc.X == -1 {
				for r, row := range d.Map {
					for c, char := range row {
						if char == 'S' || char == 'a' {
							adj.Add(ds.Edge[lib.Point[int], int]{
								Weight: 0,
								Vertex: lib.Point[int]{c, r},
							})
						}
					}
				}
				return adj
			}

			curVal := d.Map[loc.Y][loc.X]
			if curVal == 'S' {
				curVal = 'a'
			}
			if curVal == 'E' {
				curVal = 'z'
			}
			if loc.Y > 0 {
				ohea := d.Map[loc.Y-1][loc.X]
				if ohea == 'S' {
					ohea = 'a'
				}
				if ohea == 'E' {
					ohea = 'z'
				}
				if ohea <= curVal+1 {
					adj.Add(ds.Edge[lib.Point[int], int]{
						Weight: 1,
						Vertex: lib.Point[int]{loc.X, loc.Y - 1},
					})
				}
			}

			if loc.Y < len(d.Map)-1 {
				ohea := d.Map[loc.Y+1][loc.X]
				if ohea == 'S' {
					ohea = 'a'
				}
				if ohea == 'E' {
					ohea = 'z'
				}
				if ohea <= curVal+1 {
					adj.Add(ds.Edge[lib.Point[int], int]{
						Weight: 1,
						Vertex: lib.Point[int]{loc.X, loc.Y + 1},
					})
				}
			}
			if loc.X > 0 {
				ohea := d.Map[loc.Y][loc.X-1]
				if ohea == 'S' {
					ohea = 'a'
				}
				if ohea == 'E' {
					ohea = 'z'
				}
				if ohea <= curVal+1 {
					adj.Add(ds.Edge[lib.Point[int], int]{
						Weight: 1,
						Vertex: lib.Point[int]{loc.X - 1, loc.Y},
					})
				}
			}
			if loc.X < len(d.Map[0])-1 {
				ohea := d.Map[loc.Y][loc.X+1]
				if ohea == 'S' {
					ohea = 'a'
				}
				if ohea == 'E' {
					ohea = 'z'
				}
				if ohea <= curVal+1 {
					adj.Add(ds.Edge[lib.Point[int], int]{
						Weight: 1,
						Vertex: lib.Point[int]{loc.X + 1, loc.Y},
					})
				}
			}
			return adj
		},
		start,
		func(loc lib.Point[int]) bool {
			return loc.X == end.X && loc.Y == end.Y
		},
	)
}
