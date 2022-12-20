package d20

import (
	"github.com/sumnerevans/advent-of-code/lib"
)

type LL struct {
	Dat  int
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
		newCur := &LL{Dat: lib.ToInt(line), Prev: cur}
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
		offset := cur.Dat % (d.Len - 1)

		if offset == 0 {
			continue
		} else if offset < 0 {
			// Remove element
			cur.Prev.Next = cur.Next
			cur.Next.Prev = cur.Prev

			// Go backwards
			insert := cur
			for dx := 0; dx < -offset; dx++ {
				insert = insert.Prev
			}

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
			for dx := 0; dx < offset; dx++ {
				insert = insert.Next
			}

			// Insert after
			insert.Next.Prev = cur
			cur.Next = insert.Next
			insert.Next = cur
			cur.Prev = insert
		}
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

	for d.Seq.Dat != 0 {
		d.Seq = d.Seq.Next
	}

	for i := 0; i <= 3000; i++ {
		if i == 1000 || i == 2000 || i == 3000 {
			ans += d.Seq.Dat
		}
		d.Seq = d.Seq.Next
	}

	return ans
}

func (d *Day20) Part2(isTest bool) int {
	var ans int

	for i := 0; i < d.Len; i++ {
		d.Seq.Dat *= 811589153
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

	for d.Seq.Dat != 0 {
		d.Seq = d.Seq.Next
	}

	for i := 0; i <= 3000; i++ {
		if i == 1000 || i == 2000 || i == 3000 {
			ans += d.Seq.Dat
		}
		d.Seq = d.Seq.Next
	}

	return ans
}
