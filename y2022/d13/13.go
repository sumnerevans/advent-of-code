package d13

import (
	"encoding/json"
	"fmt"
	"sort"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Pair struct {
	Fst any
	Snd any
}

type Day13 struct {
	All   []any
	Pairs []Pair
}

func (d *Day13) LoadInput(lines []string) error {
	d.All = []any{}
	dividers := []string{"[[2]]", "[[6]]"}
	for _, line := range dividers {
		l := []any{}
		err := json.Unmarshal([]byte(line), &l)
		if err != nil {
			panic(err)
		}
		d.All = append(d.All, l)
	}

	for _, line := range lines {
		if line == "" {
			continue
		}
		l := []any{}
		err := json.Unmarshal([]byte(line), &l)
		if err != nil {
			panic(err)
		}
		d.All = append(d.All, l)
	}
	d.Pairs = lib.ParseGroups(lines, func(s []string) Pair {
		fst := []any{}
		err := json.Unmarshal([]byte(s[0]), &fst)
		if err != nil {
			panic(err)
		}
		snd := []any{}
		err = json.Unmarshal([]byte(s[1]), &snd)
		if err != nil {
			panic(err)
		}
		return Pair{fst, snd}
	})
	return nil
}

func Cmp(l, r any) int {
	fstLst, fstIsList := l.([]any)
	sndLst, sndIsList := r.([]any)

	if !fstIsList && !sndIsList {
		// fmt.Printf("l %f r %f\n", l.(float64), r.(float64))
		if l.(float64) < r.(float64) {
			return 1
		} else if l.(float64) == r.(float64) {
			return 0
		} else {
			return -1
		}
	}

	if !fstIsList {
		fstLst = []any{l}
	}

	if !sndIsList {
		sndLst = []any{r}
	}

	for i := 0; i < lib.Min(len(fstLst), len(sndLst)); i++ {
		c := Cmp(fstLst[i], sndLst[i])
		if c < 0 {
			return -1
		} else if c > 0 {
			return 1
		}
	}
	if len(fstLst) < len(sndLst) {
		return 1
	} else if len(fstLst) == len(sndLst) {
		return 0
	} else {
		return -1
	}
}

func (d *Day13) Part1() int {
	var ans int

	for i, p := range d.Pairs {
		// fmt.Printf("PAIR %d\n", i+1)
		// fmt.Printf("PAIR %v %v\n", p.Fst, p.Snd)
		c := Cmp(p.Fst, p.Snd)
		// fmt.Printf("CMP %d\n", c)
		if c > 0 {
			fmt.Printf("%d IN RIGHT ORDER\n", i+1)
			ans += i + 1
		}
	}

	return ans
}

func (d *Day13) Part2() int64 {
	var ans int64 = 1

	fmt.Printf("%v\n", d.All)
	sort.Slice(d.All, func(i, j int) bool {
		return Cmp(d.All[i], d.All[j]) > 0
	})
	fmt.Printf("%v\n", d.All)
	for i := 0; i < len(d.All); i++ {
		if outer, ok := d.All[i].([]any); ok {
			if len(outer) != 1 {
				continue
			}
			if inner, ok2 := outer[0].([]any); ok2 {
				if len(inner) != 1 {
					continue
				}
				if v, ok := inner[0].(float64); ok && v == 2.0 {
					ans *= int64(i + 1)
				}
				if v, ok := inner[0].(float64); ok && v == 6.0 {
					ans *= int64(i + 1)
				}
			}
		}
	}

	return ans
}
