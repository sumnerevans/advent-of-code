package ds

type Pair[A, B any] struct {
	fst A
	snd B
}

func NewPair[A, B any](a A, b B) Pair[A, B] {
	return Pair[A, B]{fst: a, snd: b}
}

func (p Pair[A, B]) First() A {
	return p.fst
}

func (p Pair[A, B]) Second() B {
	return p.snd
}
