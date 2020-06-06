package main

import ("fmt"
        "github.com/clarkduvall/hyperloglog"
        "bufio"
        "strings"
        "os"
        "hash/fnv"
        "strconv"
    )

func main(){
        m_arg, _ := strconv.ParseInt(os.Args[1], 10, 64)
        m := uint8(m_arg)
        hll, _ := hyperloglog.New(m)
        file, _ := os.Open(os.Args[2])
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
