import sys
from sklearn import tree
from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from numpy import mean, std
from sklearn.decomposition import PCA


def read_file2(fn):
	h=open(fn)
	m=[]
	first_line=True
	freq=[]
	for line in h:
		if first_line:
			freq=map(lambda x : float(x) , line.strip().split(',')	)
			first_line=False
		else:
			m.append( map(lambda x : abs(float(x)) , line.strip().split(',')  ) )
	h.close()
	return m


#if len(sys.argv)!=3:
#	print "%s negatives positives" % sys.argv[0]
#	sys.exit(1)


data=[]

cl=sys.argv[1]
train_fn=sys.argv[2]
test_fn=sys.argv[3]
for fn in sys.argv[4:]:
	d=read_file2(fn)
	#print "Loaded %d from %s" % (len(d), fn)
	data+=d


train_f=open(train_fn,'w')
test_f=open(test_fn,'w')

for i in range(len(data)):
	v=data[i]
	o=cl+"   "
	for x in range(len(v)):
		o=o+"%d:%f " % (x,v[x])
	if i%2==0:
		print >> test_f, o 
	else:
		print >> train_f, o
	

