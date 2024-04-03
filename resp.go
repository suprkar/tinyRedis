package main

import(
    "bufio"
    "fmt"
    "strings"
    "os"
    "strconv"
)
const(
    STRING='+'
    ERROR='-'
    INTEGER=':'
    BULK='$'
    ARRAY='*'

)
type value struct{
    typ string
    str string
    num int
    bulk string
    array []value
}
type Resp struct{
    reader* bufio.Reader
}
func NewResp(rd io.reader) * Resp{
    return & Resp{reader: bufio.NewReader(rd)
}
func(r* Resp) readLine() (line[] byte,n int,err error){
    for{
        b,err:=r.reader.readByte()
        if err!=nil{
            return nil,0,err
        }
        n+=1
        line=append(line,b)
        if len(line)>=2 && line[len(line)-2]=='\r'{
            break
        }
    }
    return line[:len(line)-2],n,nil

}

func main(){
    input:="$8\r\nSupratik\r\n"
    reader:=bufio.NewReader(strings.NewReader(input))


    b,_:=reader.ReadByte()

    if b!='$'{
        fmt.Println("Invalid type,expecting strings only")
        os.exit(1)
    }
    size,_:=reader.ReadByte()
    strSize,_:=strconv.ParseInt(string(size),10,64)

    //consume \r \n
    reader.readByte()
    reader.readByte()

    name:=make([]Byte,strSize)
    reader.Read(name)

    fmt.Println(string(name))
}
