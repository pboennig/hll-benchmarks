/* File: go-hll.go
 * Script that estimates cardinality of a file. Reads tokens from argv[2] and enters
 * them into an estimator with precision parameter argv[1]. Prints out estimate. 
 */
package main

import ("fmt"
        "github.com/clarkduvall/hyperloglog"
        "os"
        "hash/fnv"
        "strconv"
        "bufio"
    )

func main(){
        m_arg, _ := strconv.ParseInt(os.Args[1], 10, 64)
        m := uint8(m_arg)
        hll, _ := hyperloglog.New(m)
        f, _ := os.Open(os.Args[2])
        defer f.Close()

        scanner := bufio.NewScanner(f)
        for scanner.Scan() {
            token := scanner.Text()
            h := fnv.New32a()
            h.Write([]byte(token))
            hll.Add(h)
        }
        fmt.Println(hll.Count())
}
