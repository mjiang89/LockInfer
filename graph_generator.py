# Copyright by Meng Jiang
# A toy example for generating a random power law graph
# and injecting it with dense blocks and staircases.

import random

def create_random_powerlaw_graph(N,dstfilename):
	edge_alpha = 3.0
	deg_max = 40
	powerlaw_mu = -1.5
	temp = 2.0
	for deg in range(2,deg_max):
		temp += deg**powerlaw_mu
	powerlaw_a = N/temp
	degs_out = []
	for count in range(0,int(powerlaw_a)):
		degs_out.append(1)
		if len(degs_out) == N: break
	for deg in range(2,deg_max):
		for count in range(0,int(powerlaw_a*(deg**powerlaw_mu))):
			degs_out.append(deg)
			if len(degs_out) == N: break
		if len(degs_out) == N: break
	for i in range(len(degs_out),N):
		degs_out.append(0)
	random.shuffle(degs_out)
	fw = open(dstfilename,'w')
	for fan in range(0,N):
		set_idol = set()
		for deg in range(0,degs_out[fan]):
			idol = random.randint(0,N-1)
			if not idol in set_idol:
				fw.write(str(fan)+','+str(idol)+'\n')
				set_idol.add(idol)
	fw.close()

def inject_block(srcfilename,dstfilename,fanfilename,idolfilename,num_block,num_fan,num_idol,density,camouflage):
	N = 0
	fw = open(dstfilename,'w')
	fr = open(srcfilename,'rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		N = max(N,int(arr[0]))
		N = max(N,int(arr[1]))
		fw.write(line.strip('\r\n')+'\n')
	fr.close()
	N += 1
	N0 = N
	Ns_fan,Ns_idol = [],[]
	for b in range(0,num_block):
		Ns_fan.append([N,N+num_fan])
		N += num_fan
	for b in range(0,num_block):
		Ns_idol.append([N,N+num_idol])
		N += num_idol
	for b in range(0,num_block):
		N_fan_start,N_fan_end = Ns_fan[b][0],Ns_fan[b][1]
		N_idol_start,N_idol_end = Ns_idol[b][0],Ns_idol[b][1]
		for fan in range(N_fan_start,N_fan_end):
			set_idol = set()
			for i in range(0,int(num_idol*density)):
				idol = random.randint(N_idol_start,N_idol_end-1)
				if not idol in set_idol:
					fw.write(str(fan)+','+str(idol)+'\n')
					set_idol.add(idol)
			if camouflage == 0.0: continue
			for i in range(0,int(num_idol*density*camouflage)):
				idol = random.randint(0,N0-1)
				if not idol in set_idol:
					fw.write(str(fan)+','+str(idol)+'\n')
					set_idol.add(idol)
	fw.close()
	Nset_fan,Nset_idol = set(),set()
	for [s,e] in Ns_fan:
		for i in range(s,e):
			Nset_fan.add(i)
	for [s,e] in Ns_idol:
		for i in range(s,e):
			Nset_idol.add(i)
	fw = open(fanfilename,'w')
	for fan in Nset_fan: fw.write(str(fan)+'\n')
	fw.close()
	fw = open(idolfilename,'w')
	for idol in Nset_idol: fw.write(str(idol)+'\n')
	fw.close()

def inject_staircase(srcfilename,dstfilename,fanfilename,idolfilename,num_stair,num_fan,num_idol,num_shared_idol,density):
	N = 0
	fw = open(dstfilename,'w')
	fr = open(srcfilename,'rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		N = max(N,int(arr[0]))
		N = max(N,int(arr[1]))
		fw.write(line.strip('\r\n')+'\n')
	fr.close()
	N += 1
	N0 = N
	Ns_fan,Ns_idol = [],[]
	for b in range(0,num_stair):
		Ns_fan.append([N,N+num_fan])
		N += num_fan
	Ns_idol.append([N,N+num_idol])
	N += num_idol
	for b in range(1,num_stair):
		Ns_idol.append([N-num_shared_idol,N+num_idol-num_shared_idol])
		N += num_idol-num_shared_idol
	for b in range(0,num_stair):
		N_fan_start,N_fan_end = Ns_fan[b][0],Ns_fan[b][1]
		N_idol_start,N_idol_end = Ns_idol[b][0],Ns_idol[b][1]
		for fan in range(N_fan_start,N_fan_end):
			set_idol = set()
			for i in range(0,int(num_idol*density)):
				idol = random.randint(N_idol_start,N_idol_end-1)
				if not idol in set_idol:
					fw.write(str(fan)+','+str(idol)+'\n')
					set_idol.add(idol)
	fw.close()
	Nset_fan,Nset_idol = set(),set()
	for [s,e] in Ns_fan:
		for i in range(s,e):
			Nset_fan.add(i)
	for [s,e] in Ns_idol:
		for i in range(s,e):
			Nset_idol.add(i)
	fw = open(fanfilename,'w')
	for fan in Nset_fan: fw.write(str(fan)+'\n')
	fw.close()
	fw = open(idolfilename,'w')
	for idol in Nset_idol: fw.write(str(idol)+'\n')
	fw.close()

if __name__ == '__main__':
	create_random_powerlaw_graph(10000,'graph_random_powerlaw')
	inject_block('graph_random_powerlaw','graph_two_blocks','injectfans_two_blocks','injectidols_two_blocks',2,100,100,0.8,0.0)
	inject_block('graph_random_powerlaw','graph_two_blocks_camou','injectfans_two_blocks_camou','injectidols_two_blocks_camou',2,100,100,0.8,0.3)
	inject_staircase('graph_random_powerlaw','graph_staircase','injectfans_staircase','injectidols_staircase',3,100,100,20,0.8)