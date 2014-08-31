import sys





if len(sys.argv)!=4:
	print "%s window sum file" % sys.argv[0]
	sys.exit(1)


window_size=int(sys.argv[1])
bark_sum=float(sys.argv[2])
fn=sys.argv[3]


s=[]
b=0
h=open(fn)
for line in h:
	s.append(float(line))
	if len(s)>window_size:
		s=s[1:]
	if len(s)==window_size:
		if sum(s)<bark_sum:
			b+=1
h.close() 		
print b
