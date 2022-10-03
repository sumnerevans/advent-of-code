package ds

type Iterator[T any] <-chan T

func NewIterator[T any](list []T) Iterator[T] {
	it := make(chan T)
	go func() {
		defer close(it)
		for _, x := range list {
			it <- x
		}
	}()
	return it
}

func (it Iterator[T]) List() []T {
	l := []T{}
	for v := range it {
		l = append(l, v)
	}
	return l
}
