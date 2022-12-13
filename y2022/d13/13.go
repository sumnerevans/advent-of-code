package d13

import (
	"encoding/json"
	"sort"

	"github.com/sumnerevans/advent-of-code/lib"
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
		d.All = append(d.All, fst, snd)
		return Pair{fst, snd}
	})
	return nil
}

func Cmp(l, r any) int {
	fstLst, fstIsList := l.([]any)
	sndLst, sndIsList := r.([]any)

	if !fstIsList && !sndIsList {
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
		if Cmp(p.Fst, p.Snd) > 0 {
			ans += i + 1
		}
	}

	return ans
}

func (d *Day13) Part2() int64 {
	var ans int64 = 1

	sort.Slice(d.All, func(i, j int) bool { return Cmp(d.All[i], d.All[j]) > 0 })
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
