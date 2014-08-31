import sys
from numpy import mean , std

def read_file2(fn):
        h=open(fn) 
        m=[]  
        first_line=True
        freq=[]
        for line in h:
                if first_line:
                        freq=map(lambda x : float(x) , line.strip().split(',')  )
                        first_line=False
                else:
                        v= map(lambda x : abs(float(x)) , line.strip().split(',')  )
                        m.append(v)

        h.close()
        return m

data = read_file2(sys.argv[1])



d=[]
for v in data:
	for x in range(len(v)):
		while len(d)<=x:
			d.append([])
		d[x].append(v[x])

sm=[]
ss=[]
for x in range(len(d)):
	sm.append(str(mean(d[x])))
	ss.append(str(std(d[x])))

print ",".join(sm)
print ",".join(ss)

