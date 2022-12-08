package lib

import "encoding/json"

func AsJSON(val any) string {
	jsonBytes, err := json.Marshal(val)
	if err != nil {
		panic(err)
	}
	return string(jsonBytes)
}
