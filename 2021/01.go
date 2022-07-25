package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const DAY = 1

func main() {
	text, err := os.ReadFile("inputs/01.txt")
	if err != nil {
		log.Fatal("Error reading input")
	}
	lines := strings.Split(string(text), "\n")
	lines = lines[:len(lines)-1]

	nums := make([]int, 0)
	for _, l := range lines {
		n, err := strconv.Atoi(l)
		if err != nil {
			log.Fatalf("Line was not a number: %s", l)
		}
		nums = append(nums, n)
	}

	a := 0
	for i := 0; i < len(nums)-1; i++ {
		if nums[i] < nums[i+1] {
			a++
		}
	}
	fmt.Println(a)

	b := 0
	for i := 0; i < len(nums)-3; i++ {
		if nums[i]+nums[i+1]+nums[i+2] < nums[i+1]+nums[i+2]+nums[i+3] {
			b++
		}
	}
	fmt.Println(b)
}
