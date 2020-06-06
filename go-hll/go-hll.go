package main

import ("fmt"
        "github.com/clarkduvall/hyperloglog"
        "bufio"
        "strings"
        "os"
        "hash/fnv"
    )

func main(){
        m := uint8(14)
        hll, _ := hyperloglog.New(m)
        file, _ := os.Open(os.Args[1])
        scanner := bufio.NewScanner(file)
        for scanner.Scan() {
            line := scanner.Text()
            for _, word := range strings.Fields(line) {
                h := fnv.New32a()
                h.Write([]byte(word))
                hll.Add(h)
            }
        }
        fmt.Println(hll.Count())
}
