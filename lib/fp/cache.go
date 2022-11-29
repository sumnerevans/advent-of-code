package fp

func Cached[T comparable, U any](f func(T) U) func(T) U {
	cache := make(map[T]U)
	return func(t T) U {
		if u, ok := cache[t]; ok {
			return u
		}
		u := f(t)
		cache[t] = u
		return u
	}
}
