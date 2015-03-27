# Copyright by Meng Jiang
# A toy example for detecting inject node groups:
# 1) Seed selection;
# 2) Scoop (belief propagation).

import math

def select_seeds(srcfilename,ii,jj):
	krou,ktheta = 20,20
	vectorij = []
	fr = open(srcfilename,'rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		vectorij.append([float(arr[ii-1]),float(arr[jj-1])])
	fr.close()
	N = len(vectorij)
	routhetaij = []
	minrou,maxrou = 1.0,-1.0
	mintheta,maxtheta = -90.0,90.0
	for [entryi,entryj] in vectorij:
		rou = (entryi**2+entryj**2)**0.5
		if entryi == 0:
			if entryj > 0: theta = 90.0
			if entryj < 0: theta = -90.0
			if entryj == 0: theta = 0.0
		else:
			theta = math.atan(entryj/entryi)/math.pi*180.0
		routhetaij.append([rou,theta])
		minrou,maxrou = min(minrou,rou),max(maxrou,rou)
	gaprou,gaptheta = (maxrou-minrou)/krou,(maxtheta-mintheta)/ktheta
	freqrou,freqtheta = [0 for i in range(0,krou)],[0 for i in range(0,ktheta)]
	freq = [[0 for j in range(0,ktheta)] for i in range(0,krou)]
	u2irou,u2itheta = {},{}
	for u in range(0,N):
		[rou,theta] = routhetaij[u]
		irou = max(min(int((rou-minrou)/gaprou),krou-1),0)
		itheta = max(min(int((theta-mintheta)/gaptheta),ktheta-1),0)
		freqrou[irou] += 1
		u2irou[u] = irou
		if irou > 0:
			freqtheta[itheta] += 1
			u2itheta[u] = itheta
		freq[irou][itheta] += 1
	posrou = 0
	seed_start = False
	for irou in range(0,krou):
		if seed_start and freqrou[irou] > 0:
			posrou = irou
			break
		if freqrou[irou] == 0: seed_start = True
	seedrou,seedtheta = set(),set()
	for u in u2irou:
		if u2irou[u] >= posrou:
			seedrou.add(u)
	for u in u2itheta:
		seedtheta.add(u)
	return seedrou & seedtheta

def get_the_scoop(graphfilename,fanfilename,idolfilename,seeds):
	nodeij = []
	N = 0
	fr = open(graphfilename,'rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		nodei,nodej = int(arr[0]),int(arr[1])
		nodeij.append([nodei,nodej])
		N = max(N,nodei)
		N = max(N,nodej)
	fr.close()
	N += 1
	D = 1.0*len(nodeij)/N/N
	n = 10
	density = (1.0/n*math.log(1.0*n/N)*2)/math.log(D)
	injectedfans,injectedidols = set(),set()
	fr = open(fanfilename,'rb')
	for line in fr:
		injectedfans.add(int(line.strip('\r\n')))
	fr.close()
	fr = open(idolfilename,'rb')
	for line in fr:
		injectedidols.add(int(line.strip('\r\n')))
	fr.close()
	blamedfans,blamedidols = set(seeds),set()
	lastnum_fan,lastnum_idol = 0,0
	while not (len(blamedfans) == lastnum_fan and len(blamedidols) == lastnum_idol):
		lastnum_fan = len(blamedfans)
		lastnum_idol = len(blamedidols)
		nodej2num = {}
		for [nodei,nodej] in nodeij:
			if nodei in blamedfans:
				if not nodej in nodej2num:
					nodej2num[nodej] = 0
				nodej2num[nodej] += 1
		blamedidols = set()
		numedge = 0
		sort_nodej2num = sorted(nodej2num.items(),key=lambda x:-x[1])
		for item in sort_nodej2num:
			nodej,num = item[0],item[1]
			blamedidols.add(nodej)
			numedge += num
			if 1.0*numedge < density*len(blamedfans)*len(blamedidols):
				break
		nodei2num = {}
		for [nodei,nodej] in nodeij:
			if nodej in blamedidols:
				if not nodei in nodei2num:
					nodei2num[nodei] = 0
				nodei2num[nodei] += 1
		blamedfans = set()
		numedge = 0
		sort_nodei2num = sorted(nodei2num.items(),key=lambda x:-x[1])
		for item in sort_nodei2num:
			nodei,num = item[0],item[1]
			blamedfans.add(nodei)
			numedge += num
			if 1.0*numedge < density*len(blamedfans)*len(blamedidols):
				break
	TPfan = len(blamedfans & injectedfans)
	TPidol = len(blamedidols & injectedidols)
	Tfan = len(injectedfans)
	Tidol = len(injectedidols)
	Pfan = len(blamedfans)
	Pidol = len(blamedidols)
	precisionfan = 1.0*TPfan/Pfan
	recallfan = 1.0*TPfan/Tfan
	precisionidol = 1.0*TPidol/Pidol
	recallidol = 1.0*TPidol/Tidol
	print precisionfan,recallfan,precisionidol,recallidol
	
if __name__ == '__main__':
	seeds = select_seeds('u_two_blocks',1,2)
	get_the_scoop('graph_two_blocks','injectfans_two_blocks','injectidols_two_blocks',seeds)
	
	seeds = select_seeds('u_two_blocks_camou',1,2)
	get_the_scoop('graph_two_blocks_camou','injectfans_two_blocks_camou','injectidols_two_blocks_camou',seeds)
	
	seeds = select_seeds('u_staircase',1,2)
	get_the_scoop('graph_staircase','injectfans_staircase','injectidols_staircase',seeds)
