package lib

import "fmt"

func Assert(fact bool, msg string, args ...any) {
	if !fact {
		panic(fmt.Sprintf(msg, args...))
	}
}
