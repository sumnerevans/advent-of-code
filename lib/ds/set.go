package ds

import (
	"fmt"
	"strings"
)

type Set[T comparable] map[T]struct{}

func (s Set[T]) String() string {
	items := []string{}
	for k := range s {
		items = append(items, fmt.Sprintf("%v", k))
	}
	return fmt.Sprintf("{%s}", strings.Join(items, ", "))
}

func (s Set[T]) Contains(val T) (contains bool) {
	_, contains = s[val]
	return
}

func (s Set[T]) Equal(other Set[T]) bool {
	if len(s) != len(other) {
		return false
	}
	for k := range s {
		if !other.Contains(k) {
			return false
		}
	}
	return true
}

func (s Set[T]) Intersection(other Set[T]) Set[T] {
	newSet := Set[T]{}
	if len(other) < len(s) {
		s, other = other, s
	}
	for k := range s {
		if other.Contains(k) {
			newSet[k] = struct{}{}
		}
	}
	return newSet
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
