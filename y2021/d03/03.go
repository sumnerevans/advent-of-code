package d03

import (
	"github.com/rs/zerolog"

	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

type Day03 struct {
	Report []lib.Bits
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

func (d *Day03) Part2(log *zerolog.Logger) int64 {
	var oxy, co2 int64
	oxyConsider := ds.NewSetFromIter(lib.ERange(len(d.Report)))
	co2Consider := ds.NewSetFromIter(lib.ERange(len(d.Report)))

	for col := range lib.ERange(len(d.Report[0])) {
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
			}
		}
		if len(co2Consider) == 1 && co2 == 0 {
			for k := range co2Consider {
				co2 = d.Report[k].AsInt()
			}
		}
		if len(oxyConsider) == 1 && len(co2Consider) == 1 {
			break
		}
	}

	return oxy * co2
}
