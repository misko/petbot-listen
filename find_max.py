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
        return freq,m

freq,data = read_file2(sys.argv[1])


def fold_back(v):
        v2=[]
        for x in range(len(v)/2):
                v2.append( abs(v[x]) +abs(v[len(v)-x-1]))
         
        #v2=v2[3:-3]
         
        for x in range(2):
                v2[x]=0
        for x in range(512):
                v2[-x]=0
   
        #v2=v2[20:80]
        return v2

maxes=20

mxs=[]
for v in data:
	m=[]
	v=fold_back(v)
	for x in range(maxes):
		mx=max(v)
		m.append(v.index(mx))
		v[v.index(mx)]=0
	mxs.append(m)	

print ",".join(map(lambda x : str(x), range(maxes)))
for v in mxs:
	print ",".join(map(lambda x : str(x), v))
