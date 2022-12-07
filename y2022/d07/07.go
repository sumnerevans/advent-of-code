package d07

import (
	"fmt"
	"sort"
	"strings"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Item struct {
	IsDir bool
	Items map[string]*Item
	Size  int
}

func NewItem() *Item {
	return &Item{Items: map[string]*Item{}}
}

func (i *Item) Add(name string, size int) {
	if dir, filename, found := strings.Cut(name, "/"); found {
		if _, ok := i.Items[dir]; !ok {
			i.Items[dir] = NewItem()
		}
		i.Items[dir].IsDir = true
		i.Items[dir].Add(filename, size)
	} else {
		i.Items[name] = &Item{Items: map[string]*Item{}, Size: size}
	}
}

func (i Item) SizeR() int {
	if i.Size > 0 {
		return i.Size
	}
	s := 0
	for _, v := range i.Items {
		s += v.SizeR()
	}
	return s
}

type Day07 struct {
	Root *Item
}

func (d *Day07) LoadInput(lines []string) error {
	d.Root = NewItem()
	d.Root.IsDir = true
	path := []string{}
	for _, line := range lines {
		if line[0] == '$' {
			// fmt.Printf("%s\n", line)
			cmd := strings.Split(line, " ")
			if cmd[1] == "cd" {
				switch cmd[2] {
				case "/":
					path = []string{}
				case "..":
					path = path[:len(path)-1]
				default:
					path = append(path, cmd[2])
				}
			} else {
				// fmt.Printf("LS %s\n", line)
			}
		} else {
			fileInfo := strings.Split(line, " ")
			switch fileInfo[0] {
			case "dir":
				// TODO
			default:
				size := lib.ToInt(fileInfo[0])
				name := fileInfo[1]
				parts := []string{}
				parts = append(parts, path...)
				parts = append(parts, name)
				// fmt.Printf("%v\n", parts)
				d.Root.Add(strings.Join(parts, "/"), size)
			}
		}
		fmt.Printf("%v\n", d.Root)
	}
	return nil
}

func (d *Day07) Part1() int {
	var ans int

	q := []*Item{d.Root}

	for len(q) > 0 {
		next := q[0]
		q = q[1:]

		s := next.SizeR()
		if next.IsDir && s <= 100000 {
			ans += s
		}

		for _, v := range next.Items {
			q = append(q, v)
		}
	}

	return ans
}

func (d *Day07) Part2() int {
	var ans int

	q := []*Item{d.Root}
	sizes := map[*Item]int{}

	for len(q) > 0 {
		next := q[0]
		q = q[1:]

		s := next.SizeR()
		if next.IsDir {
			sizes[next] = s
		}

		for _, v := range next.Items {
			q = append(q, v)
		}
	}

	fmt.Printf("ohea\n", )
	opts := []int{}
	for k, v := range sizes {
		fmt.Printf("%v %v\n", k, v)
		opts = append(opts, v)
	}

	sort.Ints(opts)
	fmt.Printf("%v\n", opts)
	total := 70000000
	taken := d.Root.SizeR()
	for _, o := range opts {
		if (taken - o) <= total -30000000 {
			return o
		}
	}

	return ans
}
