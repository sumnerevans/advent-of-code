package d03

import (
	"github.com/rs/zerolog"
)

type Day03 struct {
	Report []Bits
}

func (d *Day03) LoadInput(log *zerolog.Logger, lines []string) error {
	for i, line := range lines {
		d.Report = append(d.Report, []bool{})
		for _, c := range line {
			d.Report[i] = append(d.Report[i], c == '1')
		}
	}
	return nil
}

func (d *Day03) Part1(log *zerolog.Logger) int64 {
	var gamma, epsilon int64
	for col := 0; col < len(d.Report[0]); col++ {
		var ones, zeros int64
		for _, row := range d.Report {
			if row[col] {
				ones++
			} else {
				zeros++
			}
		}
		gamma = gamma << 1
		epsilon = epsilon << 1
		if ones > zeros {
			gamma |= 1
		} else {
			epsilon |= 1
		}
	}
	return gamma * epsilon
}

type Set[T comparable] map[T]struct{}

func (s Set[T]) Contains(val T) (contains bool) {
	_, contains = s[val]
	return
}

func (s Set[T]) Remove(val T) {
	delete(s, val)
}

func NewSet[T comparable](values ...T) Set[T] {
	set := Set[T]{}
	for _, v := range values {
		set[v] = struct{}{}
	}
	return set
}

func irange(start, end int) []int {
	r := []int{}
	for i := start; i <= end; i++ {
		r = append(r, i)
	}
	return r
}

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

func (d *Day03) Part2(log *zerolog.Logger) int64 {
	var oxy, co2 int64
	all := irange(0, len(d.Report)-1)
	oxyConsider := NewSet(all...)
	co2Consider := NewSet(all...)

	for col := 0; col < len(d.Report[0]); col++ {
		var oxyOnes, oxyZeros int64
		var co2Ones, co2Zeros int64
		for rowIdx, row := range d.Report {
			if oxyConsider.Contains(rowIdx) {
				if row[col] {
					oxyOnes++
				} else {
					oxyZeros++
				}
			}
			if co2Consider.Contains(rowIdx) {
				if row[col] {
					co2Ones++
				} else {
					co2Zeros++
				}
			}
		}

		oxyMostCommon := oxyOnes >= oxyZeros
		co2MostCommon := co2Ones >= co2Zeros

		for rowIdx, row := range d.Report {
			if oxyConsider.Contains(rowIdx) && row[col] != oxyMostCommon {
				oxyConsider.Remove(rowIdx)
			}
			if co2Consider.Contains(rowIdx) && row[col] == co2MostCommon {
				co2Consider.Remove(rowIdx)
			}
		}

		if len(oxyConsider) == 1 && oxy == 0 {
			for k := range oxyConsider {
				oxy = d.Report[k].AsInt()
				log.Info().Msg("oxy set")
			}
		}
		if len(co2Consider) == 1 && co2 == 0 {
			for k := range co2Consider {
				co2 = d.Report[k].AsInt()
				log.Info().Msg("co2 set")
			}
		}
		if len(oxyConsider) == 1 && len(co2Consider) == 1 {
			break
		}
	}

	return oxy * co2
}