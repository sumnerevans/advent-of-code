package d04

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"

	_ "github.com/sumnerevans/advent-of-code/lib"
	_ "github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day04 struct {
	Secret []byte
}

func (d *Day04) LoadInput(lines []string) error {
	d.Secret = []byte(lines[0])
	return nil
}

func (d *Day04) Part1() int {
	for i := 1; ; i++ {
		sum := md5.Sum(append(d.Secret, []byte(fmt.Sprintf("%d", i))...))
		hash := hex.EncodeToString(sum[:])
		if hash[0] == '0' && hash[1] == '0' && hash[2] == '0' && hash[3] == '0' && hash[4] == '0' {
			return i
		}
	}
}

func (d *Day04) Part2() int {
	for i := 1; ; i++ {
		sum := md5.Sum(append(d.Secret, []byte(fmt.Sprintf("%d", i))...))
		hash := hex.EncodeToString(sum[:])
		if hash[0] == '0' && hash[1] == '0' && hash[2] == '0' && hash[3] == '0' && hash[4] == '0' && hash[5] == '0' {
			return i
		}
	}
}
