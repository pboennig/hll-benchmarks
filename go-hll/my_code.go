package main

import ("fmt"
        "github.com/clarkduvall/hyperloglog"
    )

func main(){
	fmt.Println("Hi!")
        m := uint8(10)
        hll, _ := hyperloglog.New(m)
}
