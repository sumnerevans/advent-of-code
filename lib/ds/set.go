package ds

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

func NewSetFromIter[T comparable](iter <-chan T) Set[T] {
	set := Set[T]{}
	for v := range iter {
		set[v] = struct{}{}
	}
	return set
}
