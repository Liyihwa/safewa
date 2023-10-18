from .. import logwa

def from_edge_copy():
    logwa.info("Please input headers from edge, end by Ctrl+D")
    lines=[]
    res={}
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:   #通过Ctrl+D返回该异常
            break
    for i in range(0,len(lines),2):
        if not lines[i].startswith(":"):
            if lines[i].endswith(":"):
                lines[i]=lines[i][:-1]
            res[lines[i]]=lines[i+1]
    return res

if __name__=='__main__':
    print(from_edge_copy())