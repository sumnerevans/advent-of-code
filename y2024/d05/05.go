package d05

import (
	"github.com/sumnerevans/advent-of-code/lib"
	"golang.org/x/exp/slices"
)

type Order struct {
	Before int
	After  int
}

type Day05 struct {
	orders      []Order
	pages       [][]int
	beforeAfter map[int][]int
}

func (d *Day05) LoadInput(lines []string) error {
	var inPages bool
	d.beforeAfter = map[int][]int{}
	for _, line := range lines {
		if line == "" {
			inPages = true
			continue
		}
		nums := lib.AllInts(line)
		if inPages {
			d.pages = append(d.pages, nums)
		} else {
			d.orders = append(d.orders, Order{nums[0], nums[1]})
			if _, ok := d.beforeAfter[nums[0]]; !ok {
				d.beforeAfter[nums[0]] = []int{}
			}
			d.beforeAfter[nums[0]] = append(d.beforeAfter[nums[0]], nums[1])
		}
	}
	return nil
}

func (d *Day05) Part1(isTest bool) int {
	var ans int

pagesloop:
	for _, pageNums := range d.pages {
		for _, order := range d.orders {
			bi := slices.Index(pageNums, order.Before)
			ai := slices.Index(pageNums, order.After)
			if bi < 0 || ai < 0 {
				continue
			} else if bi > ai {
				continue pagesloop
			}
		}
		ans += pageNums[len(pageNums)/2]
	}

	return ans
}

func (d *Day05) Part2(isTest bool) int {
	var ans int

	for _, pageNums := range d.pages {
		var bad bool
		for _, order := range d.orders {
			bi := slices.Index(pageNums, order.Before)
			ai := slices.Index(pageNums, order.After)
			if bi < 0 || ai < 0 {
				continue
			} else if bi > ai {
				bad = true
				break
			}
		}
		if bad {
			slices.SortFunc(pageNums, func(first, second int) bool {
				if afters, ok := d.beforeAfter[first]; ok {
					return slices.Contains(afters, second)
				} else if afters, ok := d.beforeAfter[second]; ok {
					return !slices.Contains(afters, first)
				} else {
					return false
				}
			})
			ans += pageNums[len(pageNums)/2]
		}
	}

	return ans
}
