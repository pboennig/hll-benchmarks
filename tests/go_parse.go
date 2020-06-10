package main

import ("fmt"
        "os"
        "bufio"
    )

func main(){
        uniq := make(map[string]int)
        f, _ := os.Open(os.Args[1])
        defer f.Close()

        scanner := bufio.NewScanner(f)
        for scanner.Scan() {
            token := scanner.Text()
            if uniq[token] == 0 {
                uniq[token] = 1
            }
        }
        fmt.Println(len(uniq))
}
