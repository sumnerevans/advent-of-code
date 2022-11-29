package lib

import (
	"strconv"
)

func ToInt(s string) (val int, err error) {
	val, err = strconv.Atoi(s)
	return
}

func ToInt64(s string) (val int64, err error) {
	val, err = strconv.ParseInt(s, 10, 64)
	return
}

func ToIntUnsafe(s string) (val int) {
	var err error
	val, err = ToInt(s)
	if err != nil {
		panic(err)
	}
	return
}

func ToInt64Unsafe(s string) (val int64) {
	var err error
	val, err = ToInt64(s)
	if err != nil {
		panic(err)
	}
	return
}

func LoadInts(lines []string) (nums []int, err error) {
	nums = make([]int, len(lines))
	for i, l := range lines {
		if val, err := ToInt(l); err != nil {
			return nil, err
		} else {
			nums[i] = val
		}
	}
	return
}

func LoadInt64s(lines []string) (nums []int64, err error) {
	nums = make([]int64, len(lines))
	for i, l := range lines {
		if val, err := ToInt64(l); err != nil {
			return nil, err
		} else {
			nums[i] = val
		}
	}
	return
}
