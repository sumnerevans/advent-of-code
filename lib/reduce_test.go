package lib_test

import (
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/sumnerevans/advent-of-code/lib"
)

func TestSum(t *testing.T) {
	assert.EqualValues(t, 0, lib.Sum([]int64{0, 0, 0}))
	assert.EqualValues(t, 10, lib.Sum([]int64{1, 2, 3, 4}))
	assert.EqualValues(t, 10, lib.Sum([]int64{1, 4, 0, 5}))
}
