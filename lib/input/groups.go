package input

func ParseGroups[T any](lines []string, fn func([]string) T) (groups []T) {
	start := 0
	for i, line := range lines {
		if line == "" {
			groups = append(groups, fn(lines[start:i]))
			start = i + 1
			continue
		}
	}
	groups = append(groups, fn(lines[start:]))
	return
}
