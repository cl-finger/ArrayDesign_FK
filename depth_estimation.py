'''
Estimate analysable depth range using given array geometry
Input csv file of sensor locations with first column being x location (in m) and second column being y location (in m)
'''
import numpy as np
import matplotlib.pyplot as plt
import sys 


def depth_estimate(file="sensor_locations.csv",path="./",p=0.25):


	### load sensor locations
	coords = np.loadtxt(path+file)
	
	# number of sensors
	ntotal = coords.shape[0]

	### calculate azimuthal gap
	angles = np.arctan2(coords[:,0],coords[:,1])
	angles = np.mod(angles, 2*np.pi) #map angles to [0, 2*pi]
	angles_sorted = np.sort(angles)
	diffs = np.diff(angles_sorted)
	wrap_gap = 2*np.pi-(angles_sorted[1]-angles_sorted[0]) #include wrap around
	gaps = np.concatenate([diffs,[wrap_gap]])
	gaps = np.sort(gaps)
	amax = np.round(np.mean(gaps[:3])*180/np.pi,1) #average of 3 smallest gaps

	### calculate min and max inter-station distances
	diff = np.zeros((ntotal,ntotal))
	for ii in range(ntotal):
		for jj in range(ntotal):
			if ii>jj:
				diff[ii,jj] = np.sqrt((coords[ii,0]-coords[jj,0])**2+(coords[ii,1]-coords[jj,1])**2)
	diff[diff==0] = np.nan
	diff = np.sort(diff)
	diff = diff[np.isfinite(diff)]
	print(diff)
	dmin = np.mean(diff[:3]) #mean of three closest sensors
	dmax = np.mean(diff[-3:]) #mean of three farthest sensors
	
	# convert to rmin/rmax logic
	rmax = 0.5*dmax	
	rmin = dmin #only true for inner circle with 6 sensors

	### calculate expected depths
	zmin = rmin * 4*p*np.sin(amax*np.pi/180)
	zmax = rmax * 4 * p / np.pi

	### plot array designs
	fig,axs = plt.subplots(1,1,figsize=(6,6),layout='constrained')
	axs.scatter(coords[:,0],coords[:,1],c='k',label = r'$ \alpha_{max} =$'+ str(amax)+r"$ ^\circ$, ntotal = "+str(ntotal)+
		' \n $r_{min} = $'+str(np.round(rmin,3))+'m, $r_{max} = $'+str(np.round(rmax,3))+'m'+
		' \n $z_{min} = $'+str(np.round(zmin,3))+'m, $z_{max} = $'+str(np.round(zmax,3))+'m')
	
	axs.set_xlabel('x (m)')
	axs.set_ylabel('y (m)')
	axs.set_aspect('equal')
	axs.legend(loc='lower left')
	fig.savefig(path+'depth_estimation.png',dpi=300)

depth_estimate(p=1.4)
