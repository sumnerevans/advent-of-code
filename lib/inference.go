package lib

import "github.com/sumnerevans/advent-of-code/lib/ds"

// InferOneFromPossibles goes through a dictionary of key to potential values
// and computes the true value using simple inference where if a key can only
// be a single value, then it must be that value. For example:
//
//	A -> {X, Y}
//	B -> {Y}
//	C -> {X, Z}
//
// then B must be Y, which means that A cannot be Y, thus A must be X, and by
// the same logic C must be Z.
//
// This function only works if the inference is in fact solvable.
func InferOneFromPossibles[K, V comparable](possibles map[K]ds.Set[V]) map[K]V {
	inferred := map[K]V{}
	for len(possibles) > 0 {
		// Find the item that only has one possibility associated with it and
		// pull it out of the possibles dictionary. Then, remove that
		// possibility from all the other sets.
		for key, possibleFields := range possibles {
			if len(possibleFields) == 1 {
				inferredValue := possibleFields.List()[0]
				for key := range possibles {
					possibles[key].Remove(inferredValue)
				}
				inferred[key] = inferredValue
				delete(possibles, key)
				break
			}
		}
	}
	return inferred
}
