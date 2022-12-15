package d%DAYNUM%

import (
	"fmt"

	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day%DAYNUM% struct {

}

func (d *Day%DAYNUM%) LoadInput(lines []string) error {
	for _, line := range lines {
		fmt.Printf("%s\n", line)

	}
	return nil
}

func (d *Day%DAYNUM%) Part1(isTest bool) int {
	var ans int

	return ans
}

func (d *Day%DAYNUM%) Part2(isTest bool) int {
	var ans int

	return ans
}
