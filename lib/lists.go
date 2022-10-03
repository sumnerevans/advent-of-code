package lib

// Columns returns the columnar version of a grid array.
func Columns[T any](input [][]T) (columns [][]T) {
	if len(input) == 0 {
		return
	}

	columns = make([][]T, len(input[0]))
	for _, row := range input {
		for col, val := range row {
			columns[col] = append(columns[col], val)
		}
	}
	return
}
