package strs

import (
	"regexp"
	"strings"

	"github.com/sumnerevans/advent-of-code/lib/ds"
	"github.com/sumnerevans/advent-of-code/lib/fp"
)

func Lines(s string) []string {
	for s[0] == '\n' || s[len(s)-1] == '\n' {
		s = strings.Trim(s, "\n")
	}
	return strings.Split(s, "\n")
}

var IntegerRegex = regexp.MustCompile(`\d+`)

func AllInts(s string) ds.Iterator[int] {
	return fp.MapStrInt(IntegerRegex.FindAllString(s, -1))
}

func AllInts64(s string) ds.Iterator[int64] {
	return fp.MapStrInt64(IntegerRegex.FindAllString(s, -1))
}
