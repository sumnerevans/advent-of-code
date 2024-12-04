package d03

import (
	"regexp"

	"github.com/sumnerevans/advent-of-code/lib"
)

type Day03 struct {
	instrs []string
}

func (d *Day03) LoadInput(lines []string) error {
	for _, line := range lines {
		d.instrs = append(d.instrs, line)
	}
	return nil
}

func (d *Day03) Part1(isTest bool) int {
	var ans int

	r := regexp.MustCompile(`mul\((\d+),(\d+)\)`)

	for _, line := range d.instrs {
		for _, match := range r.FindAllStringSubmatch(line, -1) {
			ans += lib.ToInt(match[1]) * lib.ToInt(match[2])
		}
	}

	return ans
}

func (d *Day03) Part2(isTest bool) int {
	var ans int

	r := regexp.MustCompile(`(?:mul\((\d+),(\d+)\)|do\(\)|don't\(\))`)

	enabled := true
	for _, line := range d.instrs {
		for _, match := range r.FindAllStringSubmatch(line, -1) {
			if match[0] == "do()" {
				enabled = true
			} else if match[0] == "don't()" {
				enabled = false
			} else if enabled {
				ans += lib.ToInt(match[1]) * lib.ToInt(match[2])
			}
		}
	}

	return ans
}
