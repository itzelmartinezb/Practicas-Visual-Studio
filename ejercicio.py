input("Enter para tabla P y Q: ")
P = [1,1,0,0]
Q = [1,0,1,0]
for p,q in zip(P,Q):
    print(f"{p} {q} | y:{p&q} o:{p|q}")