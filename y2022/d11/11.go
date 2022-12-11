package d11

import (
	"fmt"
	"regexp"

	"github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

// Each monkey has several attributes:

// - Starting items lists your worry level for each item the monkey is
// currently holding in the order they will be inspected.

// - Operation shows how your worry level changes as that monkey inspects an
// item. (An operation like new = old * 5 means that your worry level after the
// monkey inspected the item is five times whatever your worry level was before
// inspection.)
// Test shows how the monkey uses your worry level to decide where to throw an item next.
// If true shows what happens with an item if the Test was true.
// If false shows what happens with an item if the Test was false.

// Monkey 0:
//   Starting items: 79, 98
//   Operation: new = old * 19
//   Test: divisible by 23
//     If true: throw to monkey 2
//     If false: throw to monkey 3

type Item struct {
	Mod2  int64
	Mod3  int64
	Mod5  int64
	Mod7  int64
	Mod11 int64
	Mod13 int64
	Mod17 int64
	Mod19 int64
	Mod23 int64
}

func NewItem(val int64) Item {
	return Item{
		Mod2:  val % 2,
		Mod3:  val % 3,
		Mod5:  val % 5,
		Mod7:  val % 7,
		Mod11: val % 11,
		Mod13: val % 13,
		Mod17: val % 17,
		Mod19: val % 19,
		Mod23: val % 23,
	}
}

func (m Item) DoOp(op func(int64) int64) Item {
	return Item{
		Mod2:  op(m.Mod2) % 2,
		Mod3:  op(m.Mod3) % 3,
		Mod5:  op(m.Mod5) % 5,
		Mod7:  op(m.Mod7) % 7,
		Mod11: op(m.Mod11) % 11,
		Mod13: op(m.Mod13) % 13,
		Mod17: op(m.Mod17) % 17,
		Mod19: op(m.Mod19) % 19,
		Mod23: op(m.Mod23) % 23,
	}
}

func (m Item) Test(divisor int64) bool {
	switch divisor {
	case 2:
		return (m.Mod2 == 0)
	case 3:
		return (m.Mod3 == 0)
	case 5:
		return (m.Mod5 == 0)
	case 7:
		return (m.Mod7 == 0)
	case 11:
		return (m.Mod11 == 0)
	case 13:
		return (m.Mod13 == 0)
	case 17:
		return (m.Mod17 == 0)
	case 19:
		return (m.Mod19 == 0)
	case 23:
		return (m.Mod23 == 0)
	default:
		fmt.Printf("%d\n", divisor)
		panic("test")
	}
}

type Monkey struct {
	Items     []int64
	NewItems  []Item
	Operation func(int64) int64
	Test      int64
	DestTrue  int
	DestFalse int
}

type Day11 struct {
	Monkeys []Monkey
}

func OpGenerator(op string, operand string) func(int64) int64 {
	if op == "+" {
		return func(x int64) int64 {
			return x + lib.ToInt64(operand)
		}
	} else if operand == "old" {
		return func(x int64) int64 {
			return x * x
		}
	} else {
		return func(x int64) int64 {
			return x * lib.ToInt64(operand)
		}
	}
}

func (d *Day11) LoadInput(lines []string) error {
	opRe := regexp.MustCompile("Operation: new = old (.) (.*)")
	d.Monkeys = lib.ParseGroups(lines, func(s []string) Monkey {
		startingItems := lib.AllInts64(s[1])
		newItems := []Item{}
		for _, i := range startingItems {
			newItems = append(newItems, NewItem(i))
		}

		operation := opRe.FindStringSubmatch(s[2])
		op := operation[1]
		operand := operation[2]

		test := lib.AllInts64(s[3])[0]
		testTrue := lib.AllInts(s[4])[0]
		testFalse := lib.AllInts(s[5])[0]

		return Monkey{
			Items:     startingItems,
			NewItems:  newItems,
			Operation: OpGenerator(op, operand),
			Test:      test,
			DestTrue:  testTrue,
			DestFalse: testFalse,
		}
	})
	return nil
}

func (d *Day11) Part1() int {
	touches := map[int]int{}
	for i := range d.Monkeys {
		touches[i] = 0
	}

	for i := 0; i < 20; i++ {
		for mIdx, monkey := range d.Monkeys {
			for _, item := range monkey.Items {
				touches[mIdx]++
				newWorry := monkey.Operation(item) / 3
				if newWorry%monkey.Test == 0 {
					d.Monkeys[monkey.DestTrue].Items = append(d.Monkeys[monkey.DestTrue].Items, newWorry)
				} else {
					d.Monkeys[monkey.DestFalse].Items = append(d.Monkeys[monkey.DestFalse].Items, newWorry)
				}
			}
			d.Monkeys[mIdx].Items = []int64{}
		}
	}

	y := lib.TopN(lib.Values(touches), 2)
	return y[0] * y[1]
}

func (d *Day11) Part2Old() int {
	// The non-stupid way of doing this is to realize that all of the divisors
	// for the test are prime numbers, and will not remove any important
	// factors. Thus, instead of doing all of this horrible logic with Items, I
	// could have just done modulo by the product of all of the test divisors
	// instead.

	touches := map[int]int{}
	for i := range d.Monkeys {
		touches[i] = 0
	}

	for i := 0; i < 10000; i++ {
		for mIdx, monkey := range d.Monkeys {
			for _, item := range monkey.NewItems {
				touches[mIdx]++
				newItem := item.DoOp(monkey.Operation)

				if newItem.Test(monkey.Test) {
					d.Monkeys[monkey.DestTrue].NewItems = append(d.Monkeys[monkey.DestTrue].NewItems, newItem)
				} else {
					d.Monkeys[monkey.DestFalse].NewItems = append(d.Monkeys[monkey.DestFalse].NewItems, newItem)
				}
			}
			d.Monkeys[mIdx].NewItems = []Item{}
		}
	}

	y := lib.TopN(lib.Values(touches), 2)
	return y[0] * y[1]
}

func (d *Day11) Part2() int {
	touches := map[int]int{}
	var testProd int64 = 1
	for i, m := range d.Monkeys {
		touches[i] = 0
		testProd *= m.Test
	}

	for i := 0; i < 10000; i++ {
		for mIdx, monkey := range d.Monkeys {
			for _, item := range monkey.Items {
				touches[mIdx]++
				newWorry := monkey.Operation(item) % testProd

				if newWorry%monkey.Test == 0 {
					d.Monkeys[monkey.DestTrue].Items = append(d.Monkeys[monkey.DestTrue].Items, newWorry)
				} else {
					d.Monkeys[monkey.DestFalse].Items = append(d.Monkeys[monkey.DestFalse].Items, newWorry)
				}
			}
			d.Monkeys[mIdx].Items = []int64{}
		}
	}

	y := lib.TopN(lib.Values(touches), 2)
	return y[0] * y[1]
}
