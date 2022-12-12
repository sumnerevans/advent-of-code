package lib_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/sumnerevans/advent-of-code/lib"
	"github.com/sumnerevans/advent-of-code/lib/ds"
)

func TestInference(t *testing.T) {
	basicExample := map[string]ds.Set[string]{
		"A": ds.NewSet([]string{"X", "Y"}),
		"B": ds.NewSet([]string{"Y"}),
		"C": ds.NewSet([]string{"X", "Z"}),
	}

	inferred := lib.InferOneFromPossibles(basicExample)
	assert.Equal(t, map[string]string{
		"A": "X",
		"B": "Y",
		"C": "Z",
	}, inferred)
}
