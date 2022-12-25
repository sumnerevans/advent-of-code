package d25

import (
	"fmt"
	"math"
)

type SNAFUNum string

// "You know, I never did ask the engineers why they did that. Instead of using
// digits four through zero, the digits are 2, 1, 0, minus (written -), and
// double-minus (written =). Minus is worth -1, and double-minus is worth -2."

func (s SNAFUNum) ToInt() int64 {
	var pmult int64 = 1
	var res int64
	for place := len(s) - 1; place >= 0; place-- {
		switch s[place] {
		case '2':
			res += pmult * 2
		case '1':
			res += pmult
		case '0':
		case '-':
			res -= pmult
		case '=':
			res -= 2 * pmult
		}

		pmult *= 5
	}
	return res
}

type Day25 struct {
	Nums []SNAFUNum
}

func Pow(base, exp int64) int64 {
	return int64(math.Pow(float64(base), float64(exp)))
}

func (d *Day25) LoadInput(lines []string) error {
	for _, line := range lines {
		d.Nums = append(d.Nums, SNAFUNum(line))
	}
	return nil
}

func (d *Day25) Part1(isTest bool) string {
	var sum int64

	for _, s := range d.Nums {
		sum += s.ToInt()
	}

	fmt.Printf("TARGET SUM=%d\n", sum)

	var hipow int64 = 1
	for Pow(5, int64(hipow))*2 < sum {
		hipow *= 5
	}

	res := ""
	numMap := map[int64]string{-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}

	target := sum
	for exp := hipow; exp >= 0; exp-- {
		var m int64 = -3
		var hi, lo int64

		place := Pow(5, exp)

		for ; m <= 3; m++ {
			if place*m <= target {
				lo = m
			}
			if place*m > target {
				hi = m
				break
			}
		}

		if target-place*lo < place*hi-target {
			res += numMap[lo]
			target -= place * lo
		} else {
			res += numMap[hi]
			target -= place * hi
		}
	}

	for res[0] == '0' {
		res = res[1:]
	}

	return res
}
