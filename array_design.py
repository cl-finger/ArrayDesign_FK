'''
Plot array designs following equations based on assumed penetration depth (p) and target depths (zmin,zmax)
'''
import numpy as np
import matplotlib.pyplot as plt
import sys 


def array_design(zmin,zmax,p=0.25,a_max = 60,ntotal=12,path="./"):

	### input parameters ###
	# target depths
	# zmin = 50 #m
	# zmax = 300 #m
	# assumed penetration depths
	# p = 0.25
	# max. azimuthal gap of inner circle
	# a_max = 60 #degrees
	# total number of available stations total (inner circle calculated from azimuthal gap and outer is rest)
	# ntotal = 12

	### calculate number of stations for 2 circles
	no_r = 2
	# number of stations per circle (inner first, outer second) 
	n = [int(360/a_max),ntotal-(int(360/a_max))]
	if n[1] <= 0:
		print('Not enough station to fill both circles with this azimuthal gap! Aborting!')
		sys.exit()

	### calculate rmin and rmax
	rmin = zmin/(4*p*np.sin(np.pi/n[0]))
	rmax = (np.pi*zmax)/(4*p)

	### caculate sensor locations using rmin and rmax
	xmin=np.zeros(n[0]) # x-location of sensors on inner circle
	xmax=np.zeros(n[1]) # x-location of sensors on outer circle
	ymin=np.zeros(n[0]) # y-location of sensors on inner circle
	ymax=np.zeros(n[1]) # y-location of sensors on outer circle

	### calculate sensor locations based on array design
	# inner circle
	for kk in range(int(n[0])):
		phi = kk*360/int(n[0])
		xmin[kk] = rmin*np.sin(phi*np.pi/180)
		ymin[kk] = rmin*np.cos(phi*np.pi/180)
	# outer circle
	for kk in range(int(n[1])):
		phi = kk*360/int(n[1])+0.5*360/int(n[1]) #staggered
		xmax[kk] = rmax*np.sin(phi*np.pi/180)
		ymax[kk] = rmax*np.cos(phi*np.pi/180)

	### save sensor locations as csv coordinate list
	coords = np.zeros((ntotal,2))
	coords[:,0] = np.concatenate((xmin[:],xmax[:]))
	coords[:,1] = np.concatenate((ymin[:],ymax[:]))
	np.savetxt(path+'sensor_locations.csv',coords,header = 'x (m), y(m)',fmt  = '%.3f')

	### calculate final azimuthal gap
	angles = np.arctan2(coords[:,0],coords[:,1])
	angles = np.mod(angles, 2*np.pi) #map angles to [0, 2*pi]
	angles_sorted = np.sort(angles)
	diffs = np.diff(angles_sorted)
	wrap_gap = 2*np.pi-(angles_sorted[1]-angles_sorted[0]) #include wrap around
	gaps = np.concatenate([diffs,[wrap_gap]])
	amax = np.round(np.min(gaps)*180/np.pi,1)

	### plot array designs
	fig,axs = plt.subplots(1,1,figsize=(6,6),layout='constrained')
	axs.scatter(coords[:,0],coords[:,1],c='k',label = r'$ \alpha_{max} =$'+ str(amax)+r"$ ^\circ$, ntotal = "+str(ntotal)+' ('+str(n[0])+', '+str(n[1])+')')
	#plot rmin and rmax
	axs.plot((0,xmin[1]),(0,ymin[1]),ls='-',c='grey')	
	axs.text(0.6*xmin[1],2*ymin[1],'$r_{min} = $'+str(int(rmin))+' m',c='grey')	
	axs.plot((0,xmax[3]),(0,ymax[3]),ls='-',c='grey')	
	axs.text(0.5*xmax[3],0.8*ymax[3],'$r_{max} = $'+str(int(rmax))+' m',c='grey')	
	
	axs.set_xlabel('x (m)')
	axs.set_ylabel('y (m)')
	axs.set_aspect('equal')
	axs.legend(loc='lower left')
	fig.savefig(path+'array_design.png',dpi=300)

array_design(1000,5000,p=1.4)
