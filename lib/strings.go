package lib

import (
	"regexp"
	"strings"
)

func Lines(s string) []string {
	for s[0] == '\n' || s[len(s)-1] == '\n' {
		s = strings.Trim(s, "\n")
	}
	return strings.Split(s, "\n")
}

var IntegerRegex = regexp.MustCompile(`-?\d+`)

func AllInts(s string) []int {
	return MapStrInt(IntegerRegex.FindAllString(s, -1))
}

func AllInts64(s string) []int64 {
	return MapStrInt64(IntegerRegex.FindAllString(s, -1))
}

func ReGroups(regexStr, str string) []string {
	re := regexp.MustCompile(regexStr)
	return re.FindStringSubmatch(str)[1:]
}
