import sys
from sklearn.linear_model import RandomizedLogisticRegression
from sklearn import preprocessing
from sklearn import tree
from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from numpy import mean, std
from sklearn.decomposition import PCA
from math import exp


penalty="l2"
save_file="modelU_blur_"+penalty

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


def fold_back(v):
	v2=[]
	for x in range(len(v)/2):
		v2.append( abs(v[x]) +abs(v[len(v)-x-1]))
	
	#smoothing
	v3=[]
	for x in range(len(v2)):
		if x>1 and x<len(v2)-2:
			v3.append(v2[x-2]*0.1+v2[x-1]*0.2+v2[x]*0.4+v2[x+1]*0.2+v2[x+2]*0.1)
		#if x>2 and x<len(v2)-3:
		#	v3.append(v2[x-3]*0.05+v2[x-2]*0.9+v2[x-1]*0.18+v2[x]*0.36+v2[x+1]*0.18+v2[x+2]*0.9+v2[x+3]*0.05)
		else:
			v3.append(v2[x])
	v2=v3
	#v2=v2[3:-3]
	for x in range(3):
		v2[x]=0
	for x in range(512):
		v2[-x]=0


			

	#v2=v2[20:80]
	return v2 	

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
			v= map(lambda x : abs(float(x)) , line.strip().split(',')  )
			v=fold_back(v)

			#for x in range(len(v)):
			#	if v[x]<3000:
			#		v[x]=0
			m.append(v)
	
	h.close()
	return m



negatives=[]
positives=[]
for fn in sys.argv[1:]:
	d=read_file2(fn)
	print "Loaded %d from %s" % (len(d), fn)
	if fn.find('dog')>=0:
		positives+=d
	else:
		negatives+=d

data=negatives+positives
labels=[0]*len(negatives)+[1]*len(positives)

#data = preprocessing.scale(data)

print len(data)	
#pca = PCA(n_components=2)
#data = pca.fit(data).transform(data)

train=1
if train==1:

	test_data=[]
	test_labels=[]
	train_data=[]
	train_labels=[]
	print len(data)
	for x in range(len(data)):
		if x%2==0:
			test_data.append(data[x])
			test_labels.append(labels[x])
		else:
			train_data.append(data[x])
			train_labels.append(labels[x])

	#neigh = KNeighborsClassifier(n_neighbors=10)
	#neigh.fit(train_data, train_labels) 

	#clf = NearestCentroid()
	#clf=svm.SVC()#kernel='linear')#class_weight='auto')
	#clf=svm.LinearSVC(class_weight='auto')
	#clf = tree.DecisionTreeClassifier()
	clf = LogisticRegression(penalty=penalty)
	#clf = RandomizedLogisticRegression()
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
	save_fn=save_file
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
	save_f.close()

def read_model(fn):
	h=open(fn,'r')
	lines=map(lambda x : x.strip(), h.readlines())
	intercept=float(lines[0])
	w=[]
	for x in lines[1:]:
		w.append(float(x.split()[1]))
	h.close()
	return intercept,w

def logit(i,w,v):
	c=i
	assert(len(w)==len(v))
	for x in range(len(w)):
		c+=w[x]*abs(v[x])
	return 1/(1+exp(c))

def logitc(i,w,v):
	c=i
	assert(len(w)==len(v))
	for x in range(len(w)):
		c+=w[x]*abs(v[x])
	return c

tp=0
tn=0
fn=0
fp=0

fb=0
tb=0

#print clf.predict(data)
bark=0

intercept,w=read_model(save_file)
barks=[]
ts=[]
ns=[]
print len(data)
for x in range(len(data)):
	c=int(logit(intercept,w,data[x])<0.5)
	barks.append(1-logit(intercept,w,data[x]))
	if len(barks)>8:
		barks=barks[-8:]
	#print labels[x],i
	#print labels[x],logit(intercept,w,data[x])
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
		bark-=3
		bark=max(0,bark)
		bark=min(7,bark)
	else:
		bark+=1
	#if bark>6:
	if sum(barks)>6:
		if labels[x]==1:
			tb+=1
		else:
			fb+=1
	if labels[x]==1:
		ts.append(sum(barks))
	else:
		ns.append(sum(barks))

print mean(ts),std(ts)
print mean(ns),std(ns)


print fp,tn,tp,fn
print tb,fb





vstar=[-63594.000000,2206.409851,1478.793943,662.252559,-142.781785,-390.373390,-564.930036,-488.662201,-26.604576,169.329586,311.423677,345.513351,-89.799873,-60.617094,-315.352598,80.395504,-14.673919,-105.691434,-29.744801,-41.440263,312.970713,-279.800427,-84.164385,254.199705,-1.835435,293.777372,209.906005,-276.993530,51.293463,70.213199,124.907543,123.864680,24.929524,-367.683905,-13.970873,-48.814659,-10.989534,46.912161,-122.236456,-352.416498,425.759124,199.243777,-8.079580,-177.847051,-343.839040,158.756054,165.833006,13.195015,342.130151,-172.161190,-20.438952,137.771244,-117.994232,-71.668787,421.130295,218.842146,-341.465236,-43.372637,-159.319427,17.731809,158.652647,96.679678,-117.041722,-189.202022,-49.115923,-20.959652,-67.202829,-56.117072,-155.318088,176.541355,99.600500,418.590066,35.732135,54.490825,-86.193159,23.359612,24.016943,-354.867098,-22.761411,148.556806,156.500169,330.759541,-330.432122,62.360652,194.233628,-3.970709,-65.784435,-230.543069,-312.958114,-98.341950,364.917945,-47.902138,-213.041011,140.747040,-38.619503,-27.280924,374.802535,238.323771,2.510288,-131.013624,8.809940,-190.683861,-59.080094,215.915522,129.172450,-86.377657,157.032002,-175.240732,-108.318275,38.309786,101.003294,-43.222068,-17.456255,6.978316,21.108499,-27.932819,-195.232479,-287.973997,122.422942,205.898311,186.522071,120.122863,37.220872,-54.975853,106.330820,2.097695,-122.671783,137.390645,-61.547727,55.313543,33.694745,-163.402095,57.907658,154.510405,-145.185214,-18.789222,209.033413,-284.877191,-221.787269,316.454888,-305.050690,144.325869,318.276818,-160.715775,-5.504717,102.100898,-107.372579,-28.275812,144.875511,58.475561,-28.022029,95.650370,-95.121676,139.372155,61.163540,-63.365089,91.485697,-13.534270,-70.411906,-128.878083,-189.370798,-51.194329,123.809212,145.446944,52.047522,-35.736413,1.782633,22.036819,18.193836,-56.236508,-22.119438,60.568628,108.037280,-15.620914,53.989159,-0.054580,-69.700944,7.682246,133.229476,29.469543,51.458069,40.038472,-82.859538,-162.506070,-3.697857,11.002014,-36.963636,65.397665,38.973943,-115.301105,-16.538681,88.141717,122.362268,35.718678,10.188477,-38.793111,-21.418471,99.058798,-38.213309,-30.171183,-23.674055,10.551380,126.077533,28.590781,11.660216,19.576096,-13.276500,-9.599780,-86.987244,-10.309252,-37.014012,15.439317,28.621519,12.702383,24.691020,-0.692593,36.517289,45.822813,-8.449983,-2.871271,-11.620070,29.732918,32.192913,61.131168,-1.883557,-49.347986,10.061830,35.311680,3.695486,2.256751,12.533007,-16.803062,5.275547,-3.608657,-14.822177,26.042753,3.864660,12.552733,15.546334,-23.347636,21.729574,14.253488,11.078510,23.675377,31.774845,13.789676,12.435829,8.868411,-0.563836,-6.183199,-4.688198,-7.471894,34.147840,11.512501,0.697393,8.572320,-13.000000,-1.629811,16.111187,-7.962238,12.725830,18.482588,25.334286,29.195387,15.805953,2.486934,-19.243787,0.458644,32.313173,22.676585,3.491463,2.076909,-4.704824,12.143442,23.084617,9.321088,-38.729702,-11.227472,32.737114,-15.280567,0.320012,60.507151,-16.346870,7.600433,21.508761,-5.135746,-0.767475,51.044291,37.755939,-8.629584,31.937560,1.084684,-19.835275,41.498534,-20.841205,5.416176,-16.267756,-20.592486,33.424750,10.967068,-8.225114,-31.016783,26.621727,52.761651,33.996031,1.051469,-51.681635,-25.276963,0.542141,16.487045,45.527638,42.943162,57.151419,47.026312,53.657669,-54.742348,-0.905624,0.390576,-71.356009,4.401599,62.916953,-21.727684,-36.809831,14.751113,-0.044633,-9.645376,88.186243,-8.282094,-3.423723,1.680034,-14.413527,6.860277,-32.544325,50.174086,71.619643,-33.782566,35.593748,45.259817,0.569465,48.320799,16.564095,-1.256419,11.840954,4.330398,-56.345185,-4.461439,-6.106107,-60.583097,8.033911,7.012898,-24.475042,133.337903,3.424322,-10.966294,7.414119,3.336986,1.206508,-12.802262,18.827375,38.010235,13.206489,8.054643,2.111825,106.334596,25.828236,39.942193,-26.049373,-105.696332,-24.860094,62.474785,16.402683,-53.557562,30.167910,-30.113439,-17.075490,76.203095,24.236896,-25.432321,-77.214297,-15.869620,54.991144,60.956255,107.216788,-17.371069,27.547727,-15.752795,45.123758,6.460690,-25.416619,21.540447,-8.972619,-8.022236,-29.127173,-12.621610,125.257218,-40.943028,10.874779,4.573812,-54.657124,7.512251,3.387236,-53.908446,13.614499,25.033025,15.711252,45.157248,31.162146,16.764647,56.056551,9.412896,-26.988433,88.837693,22.470200,-28.666372,15.990790,-45.492876,-42.914934,0.923408,-18.148522,99.643383,-4.847072,0.829307,-7.831056,-32.818434,7.540583,91.574023,-14.476910,-64.539603,-6.200096,-9.608646,-29.930632,63.385059,57.907212,80.308947,26.782037,57.935454,-2.581469,-16.144679,-30.776397,-62.311314,1.424177,20.762340,67.752371,3.393864,-43.268537,-7.716363,6.991268,51.220454,-20.163298,-2.792832,23.190705,-32.823941,52.470299,-41.583082,15.345615,29.384592,10.530757,52.358441,41.771526,-11.345950,-1.693059,4.342428,-1.186905,-7.960296,67.060445,-6.683408,-3.440551,25.078468,-5.179229,-50.057525,5.255482,23.549358,-8.486930,-13.467541,21.926080,19.292806,32.322456,48.618350,-24.339706,-38.561215,17.256969,26.730811,25.357451,21.165716,10.906023,17.850156,1.157593,-7.422296,-23.085661,15.246936,27.022186,35.166361,17.374329,-0.315192,-23.318496,-0.338741,1.583431,0.488263,13.126016,8.682858,13.478945,27.465194,0.452795,1.466641,-1.821490,3.673381,18.802889,25.718524,10.525908,7.765930,8.737862,-0.278872,0.000000,-6.769202,-9.073880,-6.095468,1.752284,5.988723,10.400277,10.495992,0.653106,-4.676659,-9.557358,-11.664667,3.307525,2.418905,13.553191,-3.702369,0.720883,5.517377,1.644278,2.418345,-19.227779,18.051740,5.689330,-17.966953,0.135390,-22.576731,-16.779175,22.997373,-4.417129,-6.263466,-11.528919,-11.816022,-2.455344,37.353034,1.462620,5.261892,1.218716,-5.348205,14.315552,42.369193,-52.512379,-25.195184,1.046890,23.599062,46.698939,-22.057907,-23.560007,-1.915942,-50.750214,26.077753,3.160122,-21.734174,18.985433,11.757287,-70.414013,-37.281467,59.249839,7.663012,28.652633,-3.245150,-29.538807,-18.307412,22.535373,37.031557,9.769764,4.236023,13.796670,11.700310,32.881092,-37.940357,-21.724957,-92.649491,-8.023919,-12.412051,19.911638,-5.471891,-5.703651,85.426380,5.553237,-36.727550,-39.201252,-83.930212,84.927001,-16.231930,-51.194091,1.059597,17.771175,63.039039,86.607174,27.539975,-103.401114,13.732183,61.780748,-41.284424,11.456804,8.184264,-113.695106,-73.093922,-0.778339,41.063067,-2.790976,61.052718,19.116162,-70.594882,-42.672813,28.829547,-52.947242,59.686143,37.263935,-13.311015,-35.441988,15.315687,6.245948,-2.521058,-7.699167,10.285493,72.569947,108.049652,-46.362816,-78.698917,-71.949502,-46.760373,-14.620668,21.789896,-42.522567,-0.846360,49.932693,-56.415865,25.493903,-23.110689,-14.199662,69.452125,-24.822993,-66.795098,63.293171,8.259812,-92.658139,127.324523,99.944260,-143.774087,139.723491,-66.642545,-148.150827,75.410406,2.603537,-48.673999,51.592012,13.693328,-70.709422,-28.762650,13.890259,-47.779113,47.880228,-70.690804,-31.258985,32.629699,-47.466003,7.074840,37.082280,68.379243,101.220800,27.566207,-67.157356,-79.472709,-28.646647,19.812202,-0.995451,-12.394554,-10.306681,32.085885,12.710413,-35.051950,-62.966003,9.168459,-31.911217,0.032487,41.777138,-4.636656,-80.969960,-18.034096,-31.707532,-24.840779,51.760678,102.208702,2.341642,-7.014330,23.725962,-42.260860,-25.355331,75.516062,10.904604,-58.504066,-81.759854,-24.025293,-6.898523,26.440394,14.694722,-68.409872,26.563579,21.110766,16.673151,-7.479653,-89.956170,-20.532149,-8.427996,-14.241227,9.720822,7.074134,64.514137,7.694999,27.805115,-11.672362,-21.776630,-9.726259,-19.026448,0.537094,-28.498372,-35.987220,6.678260,2.283593,9.300070,-23.946624,-26.091119,-49.855976,1.545795,40.752852,-8.361375,-29.527602,-3.109477,-1.910745,-10.677627,14.404748,-4.550718,3.132209,12.945165,-22.886039,-3.417284,-11.168428,-13.917583,21.030954,-19.694538,-12.998482,-10.165487,-21.858369,-29.517321,-12.888994,-11.695264,-8.391709,0.536817,5.923166,4.518700,7.246105,-33.319846,-11.302508,-0.688887,-8.519882,13.000000,1.639842,-16.310124,8.110171,-13.042065,-19.058506,-26.284581,-30.477094,-16.601512,-2.628207,20.462338,-0.490694,-34.784528,-24.561609,-3.805052,-2.277434,5.190973,-13.481112,-25.786170,-10.476419,43.800027,12.776098,-37.483903,17.604929,-0.370983,-70.581269,19.187356,-8.976753,-25.562276,6.141773,0.923557,-61.809979,-46.005744,10.581210,-39.406632,-1.346779,24.783393,-52.178109,26.370317,-6.896460,20.845203,26.554401,-43.375999,-14.322866,10.810454,41.026652,-35.438693,-70.686572,-45.838342,-1.426870,70.585722,34.745901,-0.750057,-22.958020,-63.808989,-60.578964,-81.148780,-67.209284,-77.189791,79.267963,1.320003,-0.573050,105.386194,-6.543907,-94.161874,32.734740,55.828352,-22.522621,0.068606,14.925987,-137.388914,12.990509,5.406650,-2.671159,23.073464,-11.057423,52.816099,-81.989549,-117.844291,55.972660,-59.384581,-76.039515,-0.963452,-82.327368,-28.420730,2.171052,-20.606352,-7.589832,99.463162,7.932187,10.934693,109.277229,-14.596654,-12.834652,45.121426,-247.627270,-6.406455,20.668772,-14.077944,-6.383701,-2.325417,24.861292,-36.838973,-74.939994,-26.236788,-16.124820,-4.260369,-216.182280,-52.919099,-82.477972,54.213593,221.713658,52.562253,-133.147190,-35.238372,115.988091,-65.863956,66.281380,37.892384,-170.497587,-54.677560,57.852836,177.118225,36.709601,-128.284627,-143.413606,-254.417498,41.576232,-66.506097,38.363086,-110.857468,-16.012766,63.556134,-54.346495,22.842234,20.608347,75.509356,33.021651,-330.746890,109.121382,-29.256052,-12.421326,149.851258,-20.793991,-9.466689,152.133860,-38.798874,-72.046337,-45.669245,-132.583356,-92.421324,-50.229401,-169.685603,-28.789486,83.410005,-277.463721,-70.928992,91.461393,-51.573245,148.330169,141.471578,-3.078031,61.176477,-339.704664,16.714352,-2.892881,27.636965,117.190696,-27.248165,-334.899717,53.589893,241.854139,23.523556,36.914986,116.453449,-249.793401,-231.178551,-324.836276,-109.773259,-240.667886,10.870055,68.921955,133.224340,273.556307,-6.342147,-93.804175,-310.618339,-15.792087,204.384530,37.009247,-34.054085,-253.436531,101.367744,14.269168,-120.445313,173.340064,-281.817473,227.213952,-85.327398,-166.316756,-60.690247,-307.343958,-249.826053,69.161404,10.522342,-27.526317,7.676633,52.552609,-452.084795,46.028366,24.217179,-180.495760,38.134082,377.243100,-40.560229,-186.228564,68.810207,112.019684,-187.220605,-169.228207,-291.461362,-451.033276,232.491638,379.576610,-175.212944,-280.213018,-274.729733,-237.266816,-126.645087,-214.997502,-14.481384,96.581861,312.964670,-215.716414,-399.749279,-545.075600,-282.802097,5.401064,421.828893,6.488955,-32.231481,-10.602448,-305.413207,-217.590072,-365.955659,-813.532957,-14.754199,-53.103239,74.199263,-171.021713,-1021.349442,-1676.455560,-857.685105,-843.742678,-1424.032166,90.897987]

print "VSTAR",logit(intercept,w,vstar),logitc(intercept,w,vstar)