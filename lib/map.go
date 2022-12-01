package lib

func Map[T any, U any](f func(T) U) func([]T) []U {
	return func(input []T) (out []U) {
		for _, v := range input {
			out = append(out, f(v))
		}
		return
	}
}

func MapStrInt(input []string) []int {
	return Map(ToInt)(input)
}

func MapStrInt64(input []string) []int64 {
	return Map(ToInt64)(input)
}
