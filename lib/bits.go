package lib

import (
	"strings"
)

type Bits []bool

func (b Bits) String() string {
	var builder strings.Builder
	for _, bit := range b {
		if bit {
			builder.WriteRune('1')
		} else {
			builder.WriteRune('0')
		}
	}
	return builder.String()
}

func (b Bits) AsInt() int64 {
	var val int64 = 0
	for _, bit := range b {
		val <<= 1
		if bit {
			val |= 1
		}
	}
	return val
}

func BitsOfInt(input int) Bits {
	bits := make([]bool, 32)
	for i := 0; i < 32; i++ {
		if input&(1<<i) > 0 {
			bits[i] = true
		}
	}
	return bits
}

func BitsOfInt64(input int64) Bits {
	bits := make([]bool, 64)
	for i := 0; i < 64; i++ {
		if input&(1<<i) > 0 {
			bits[i] = true
		}
	}
	return bits
}
