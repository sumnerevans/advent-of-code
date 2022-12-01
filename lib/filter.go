package lib

func Filter[T any](input []T, f func(T) bool) (output []T) {
	for _, v := range input {
		if f(v) {
			output = append(output, v)
		}
	}
	return
}

func FilterMap[T comparable, U any](input map[T]U, f func(T, U) bool) (output map[T]U) {
	output = make(map[T]U)
	for k, v := range input {
		if f(k, v) {
			output[k] = v
		}
	}
	return
}
