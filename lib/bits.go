package lib

type Bits []bool

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
