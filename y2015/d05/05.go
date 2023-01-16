package d05

type Day05 struct {
	Strings []string
}

func (d *Day05) LoadInput(lines []string) error {
	d.Strings = lines
	return nil
}

func (d *Day05) NicePart1(s string) bool {
	vowels := []rune{}
	dbl := false
	for i, c := range s {
		if c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' {
			vowels = append(vowels, c)
		}
		if i > 0 {
			trailing := rune(s[i-1])
			dbl = dbl || (c == trailing)

			// It does not contain the strings ab, cd, pq, or xy, even if they
			// are part of one of the other requirements.
			if trailing == 'a' && c == 'b' {
				return false
			}
			if trailing == 'c' && c == 'd' {
				return false
			}
			if trailing == 'p' && c == 'q' {
				return false
			}
			if trailing == 'x' && c == 'y' {
				return false
			}
		}
	}
	if len(vowels) < 3 {
		return false
	}
	if !dbl {
		return false
	}
	return true
}

func (d *Day05) Part1(isTest bool) int {
	var ans int

	for _, s := range d.Strings {
		if d.NicePart1(s) {
			ans++
		}
	}

	return ans
}

func (d *Day05) NicePart2(s string) bool {
	// It contains a pair of any two letters that appears at least twice in the
	// string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not
	// like aaa (aa, but it overlaps).
	found := false
	for i := 1; i < len(s); i++ {
		substr := []rune{rune(s[i-1]), rune(s[i])}
		for j := 1; j < i-1; j++ {
			if rune(s[j-1]) == substr[0] && rune(s[j]) == substr[1] {
				found = true
				break
			}
		}
		for j := i + 2; j < len(s); j++ {
			if rune(s[j-1]) == substr[0] && rune(s[j]) == substr[1] {
				found = true
				break
			}
		}
	}
	if !found {
		return false
	}

	// It contains at least one letter which repeats with exactly one letter
	// between them, like xyx, abcdefeghi (efe), or even aaa.
	for i, c := range s {
		if i > 1 {
			trailing := rune(s[i-2])
			if c == trailing {
				return true
			}
		}
	}
	return false
}

func (d *Day05) Part2(isTest bool) int {
	var ans int

	for _, s := range d.Strings {
		if d.NicePart2(s) {
			ans++
		}
	}

	return ans
}
