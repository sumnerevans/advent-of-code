package d20

import (
	"github.com/sumnerevans/advent-of-code/lib"
)

type X struct {
	Offset int
	Val    int
}

type LL struct {
	Dat  X
	Next *LL
	Prev *LL
}

type Day20 struct {
	Seq *LL
	Len int
}

func (d *Day20) LoadInput(lines []string) error {
	var cur *LL
	d.Len = len(lines)
	for _, line := range lines {
		newCur := &LL{Dat: X{Offset: lib.ToInt(line) % (d.Len - 1), Val: lib.ToInt(line)}, Prev: cur}
		if d.Seq == nil {
			d.Seq = newCur
		} else {
			cur.Next = newCur
		}
		cur = newCur
	}
	cur.Next = d.Seq
	d.Seq.Prev = cur
	return nil
}

func Mix(d *Day20, moveOrder []*LL) {
	for _, cur := range moveOrder {
		// fmt.Printf("%v\n", cur)
		// x := cur
		// for i := 0; i < d.Len; i++ {
		// 	fmt.Printf("%d -> ", x.Dat.Val)
		// 	x = x.Next
		// }
		// fmt.Printf("\n")

		if cur.Dat.Offset == 0 {
			continue
		}

		if cur.Dat.Offset < 0 {
			// Remove element
			cur.Prev.Next = cur.Next
			cur.Next.Prev = cur.Prev

			// Go backwards
			insert := cur
			for dx := 0; dx < (-cur.Dat.Offset); dx++ {
				insert = insert.Prev
			}

			// fmt.Printf("%v\n", insert)
			// Insert before
			insert.Prev.Next = cur
			cur.Prev = insert.Prev
			cur.Next = insert
			insert.Prev = cur
		} else {
			// Remove element
			cur.Prev.Next = cur.Next
			cur.Next.Prev = cur.Prev

			// Go forwards
			insert := cur
			for dx := 0; dx < cur.Dat.Offset; dx++ {
				insert = insert.Next
			}

			// Insert after
			insert.Next.Prev = cur
			cur.Next = insert.Next
			insert.Next = cur
			cur.Prev = insert
		}

		// x := cur
		// for i := 0; i < d.Len; i++ {
		// 	fmt.Printf("%d -> ", x.Dat)
		// 	x = x.Next
		// }
		// fmt.Printf("\n", )
	}
}

func (d *Day20) Part1(isTest bool) int {
	var ans int

	moveOrder := []*LL{}
	for i := 0; i < d.Len; i++ {
		moveOrder = append(moveOrder, d.Seq)
		d.Seq = d.Seq.Next
	}

	Mix(d, moveOrder)

	for d.Seq.Dat.Val != 0 {
		d.Seq = d.Seq.Next
	}

	for i := 0; i <= 3000; i++ {
		if i == 1000 || i == 2000 || i == 3000 {
			ans += d.Seq.Dat.Val
		}
		d.Seq = d.Seq.Next
	}

	return ans
}

func (d *Day20) Part2(isTest bool) int {
	var ans int

	for i := 0; i < d.Len; i++ {
		d.Seq.Dat.Val *= 811589153
		d.Seq.Dat.Offset = d.Seq.Dat.Val % (d.Len - 1)
		d.Seq = d.Seq.Next
	}

	moveOrder := []*LL{}
	for i := 0; i < d.Len; i++ {
		moveOrder = append(moveOrder, d.Seq)
		d.Seq = d.Seq.Next
	}

	for i := 0; i < 10; i++ {
		Mix(d, moveOrder)
	}

	for d.Seq.Dat.Val != 0 {
		d.Seq = d.Seq.Next
	}

	for i := 0; i <= 3000; i++ {
		if i == 1000 || i == 2000 || i == 3000 {
			ans += d.Seq.Dat.Val
		}
		d.Seq = d.Seq.Next
	}

	return ans
}
