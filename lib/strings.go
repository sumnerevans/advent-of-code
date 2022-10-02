package lib

import "strings"

func Lines(s string) []string {
	for s[0] == '\n' || s[len(s)-1] == '\n' {
		s = strings.Trim(s, "\n")
	}
	return strings.Split(s, "\n")
}
