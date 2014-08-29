import sys
from sklearn import preprocessing
from sklearn import tree
from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from numpy import mean, std
from sklearn.decomposition import PCA

def read_file(fn):
	h=open(fn)
	m=[]
	channels=[]
	for x in range(471):
		channels.append([])
	lines=h.readlines()
	freqs=lines[:471]
	lines=lines[940:] #skip the first 940 lines
	assert(len(lines)%471==0)
	for x in range(len(lines)):
		if x%471==0:
			if len(m)>0:
				if 0>1: #sum(m[-1])<80000:
					m=m[:-1]
			m.append([])
		channels[x%471].append(abs(float(lines[x])))
		m[-1].append(abs(float(lines[x])))
	h.close()
	print "loaded ", len(m) , "from ", fn
	#for ch in range(471):
	#	print ch,mean(channels[ch]),std(channels[ch])
	return m

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


negatives=[]
positives=[]
for fn in sys.argv[1:]:
	d=read_file2(fn)
	print "Loaded %d from %s" % (len(d), fn)
	if fn.find('dog')>=0:
		positives+=d
	else:
		negatives+=d
#negatives_fn=sys.argv[1]
#positives_fn=sys.argv[2]

#negatives=read_file2(negatives_fn)
#positives=read_file2(positives_fn)

'''
def cost(v):
	c=0
	for x in range(256,256+1):
		c+=v[x]
	#for x in range(54,57):
	#	c-=3*v[x]
	return c
	

s=[]
for n in negatives:
	#s.append(cost(n))
	s.append(sum(n))
#print mean(s),std(s)	

s=[]
for p in positives:
	s.append(sum(p))
	#s.append(cost(p))
#print mean(s),std(s)	

def classify(v,t):
	#if sum(v)<80000:
	#	return False
	c=cost(v)
	return c<t


tp=0
tn=0
fn=0
fp=0

thres=188
for v in negatives:
 	if classify(v,thres):
		fp+=1
	else:
		tn+=1

for v in positives:
	if classify(v,thres):
		tp+=1
	else:
		fn+=1

print fp,tn,tp,fn'''
		

#sys.exit(1)
#data=negatives[:2000]+positives[:2000]
#labels=[0]*len(negatives[:2000])+[1]*len(positives[:2000])

data=negatives+positives
labels=[0]*len(negatives)+[1]*len(positives)

#data = preprocessing.scale(data)

#pca = PCA(n_components=2)
#data = pca.fit(data).transform(data)


test_data=[]
test_labels=[]
train_data=[]
train_labels=[]
print len(data)
for x in range(len(data)):
	if x%4==0:
		test_data.append(data[x])
		test_labels.append(labels[x])
	else:
		train_data.append(data[x])
		train_labels.append(labels[x])

#neigh = KNeighborsClassifier(n_neighbors=10)
#neigh.fit(train_data, train_labels) 


#clf = NearestCentroid()
#clf=svm.SVC()
#clf=svm.LinearSVC()
#clf = tree.DecisionTreeClassifier(max_depth=1)
clf = LogisticRegression(penalty='l1')
#clf = LogisticRegression()
clf.fit(train_data, train_labels) 
#clf.sparsify()
#print clf.tree_
#with open("output.dot", "w") as output_file:
#    tree.export_graphviz(clf, out_file=output_file)
print "TEST"
tp=0
tn=0
fn=0
fp=0
#print clf.predict(data)
bark=0
for x in range(len(data)):
	c=clf.predict(data[x])
	if labels[x]==1:
		if c==1:
			tp+=1
		else:
			fn+=1	
	else:
		if c==1:
			fp+=1
		else:
			tn+=1
	if c==0:
		bark-=2
		bark=max(0,bark)
		bark=min(7,bark)
	else:
		bark+=1
	#if bark>4:
	#	print "BARK",labels[x],c,data[x][256]-188
	#else:
	#	print labels[x],c,data[x][256]-188
		
		
print fp,tn,tp,fn
print clf.get_params()
i=0
a = clf.coef_
save_fn="model"
save_f=open(save_fn,'w')
print >> save_f, clf.intercept_[0]
for x in a[0]:
	print >> save_f, i,x
	i+=1
	#print x, clf.predict(test_data[x]), test_labels[x]
	#print x, neigh.predict(test_data[x]), test_labels[x]
#print "TRAIN"
#for x in range(len(train_data)):
#	print x, clf.predict(train_data[x]), train_labels[x]
