package lib

import (
	"strconv"
)

func ToInt(s string) (val int) {
	var err error
	val, err = strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return
}

func ToInt64(s string) (val int64) {
	var err error
	val, err = strconv.ParseInt(s, 10, 64)
	if err != nil {
		panic(err)
	}
	return
}

func LoadInts(lines []string) (nums []int) {
	nums = make([]int, len(lines))
	for i, l := range lines {
		nums[i] = ToInt(l)
	}
	return
}

func LoadInt64s(lines []string) (nums []int64) {
	nums = make([]int64, len(lines))
	for i, l := range lines {
		nums[i] = ToInt64(l)
	}
	return
}
