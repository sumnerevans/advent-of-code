package input

import "github.com/sumnerevans/advent-of-code/lib/ds"

func ParseGroups[T any](lines []string, fn func([]string) T) ds.Iterator[T] {
	it := make(chan T)
	go func() {
		defer close(it)
		start := 0
		for i, line := range lines {
			if line == "" {
				it <- fn(lines[start:i])
				start = i + 1
				continue
			}
		}
		it <- fn(lines[start:])
	}()
	return it
}
