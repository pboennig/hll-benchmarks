package main

import ("fmt"
        "bufio"
        "strings"
        "os"
    )

func main(){
        file, _ := os.Open(os.Args[1])
        uniq := make(map[string]int)
        scanner := bufio.NewScanner(file)
        for scanner.Scan() {
            line := scanner.Text()
            for _, word := range strings.Fields(line) {
                if uniq[word] == 0  {
                    uniq[word] = 1
                } else {
                    uniq[word]++
                }
            }
        }
        fmt.Println(len(uniq))
}
