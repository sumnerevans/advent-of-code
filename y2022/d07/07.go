package d07

import (
	"sort"
	"strings"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Inode struct {
	Children map[string]Inode
	size     int
}

func (i Inode) IsDir() bool {
	return i.size == 0
}

func NewDir() Inode {
	return Inode{Children: map[string]Inode{}}
}

func NewFile(size int) Inode {
	return Inode{size: size}
}

func (i Inode) Add(path []string, size int) {
	if len(path) == 1 {
		i.Children[path[0]] = NewFile(size)
	} else {
		dir := path[0]
		if _, ok := i.Children[dir]; !ok {
			i.Children[dir] = NewDir()
		}
		i.Children[dir].Add(path[1:], size)
	}
}

func (i Inode) Size() int {
	if !i.IsDir() {
		return i.size
	}
	return lib.Sum(lib.Map(Inode.Size)(lib.Values(i.Children)))
}

type Day07 struct {
	DirSizes []int
}

func (d *Day07) LoadInput(lines []string) error {
	root := NewDir()
	path := []string{}
	for _, line := range lines {
		if line[0] == '$' {
			cmd := strings.Split(line, " ")
			if cmd[1] != "cd" {
				continue
			}

			switch cmd[2] {
			case "/":
				path = []string{}
			case "..":
				path = path[:len(path)-1]
			default:
				path = append(path, cmd[2])
			}
		} else {
			fileInfo := strings.Split(line, " ")
			if fileInfo[0] == "dir" {
				continue
			}
			root.Add(append(path, fileInfo[1]), lib.ToInt(fileInfo[0]))
		}
	}

	q := []Inode{root}

	for len(q) > 0 {
		next := q[0]
		q = q[1:]

		if next.IsDir() {
			d.DirSizes = append(d.DirSizes, next.Size())
		}

		for _, v := range next.Children {
			q = append(q, v)
		}
	}

	return nil
}

func (d *Day07) Part1() int {
	return lib.Sum(lib.Filter(d.DirSizes, func(s int) bool { return s <= 100000 }))
}

func (d *Day07) Part2() int {
	sort.Ints(d.DirSizes)
	total := 70000000
	rootSize := d.DirSizes[len(d.DirSizes)-1]
	for _, o := range d.DirSizes {
		if rootSize-o <= total-30000000 {
			return o
		}
	}
	panic("no answer")
}
