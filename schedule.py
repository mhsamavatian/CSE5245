

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os.path
import re
import sys
import math
import numpy as np

def compute_time(num_clusters,compute_cycles,assigned_jobs):
    times = []
    for i in range(0,num_clusters):
        time = [0]
        it=1
        for job in assigned_jobs[i]:
            time.append(time[it-1]+compute_cycles[job][i])
            it+=1
        times.append(time)
    
    print ([i[-1] for i in times])
    return times

def round_robin(num_clusters,sorted_idx):
    assigned_jobs = []
    for i in range(0,num_clusters):
        jobs_list=[]
		#for j in range(0,freq[i].shape[0]):
        for j in range(i,sorted_idx.shape[0],num_clusters):
            jobs_list.append(sorted_idx[j])
        assigned_jobs.append(jobs_list)
    return assigned_jobs
    #print (assigned_jobs)
def segment(num_clusters,sorted_idx):
    assigned_jobs = []
    seg = math.ceil(sorted_idx.shape[0]/num_clusters)
    for i in range(0,num_clusters):
        jobs_list=[]
        for j in range(i*seg,min((i+1)*seg,sorted_idx.shape[0])):
            jobs_list.append(sorted_idx[j])
        assigned_jobs.append(jobs_list)
    return assigned_jobs
def weighted_segment(num_clusters,sorted_idx,freq):
    assigned_jobs = []
    seg = [0]
    sum = np.sum(freq)
    for i in range(0,num_clusters):
        seg.append(math.ceil(sorted_idx.shape[0]*freq[i]/sum))
    for i in range(0,num_clusters):
        jobs_list=[]
        for j in range(seg[i],min(seg[i+1]+seg[i],sorted_idx.shape[0])):
            jobs_list.append(sorted_idx[j])
        assigned_jobs.append(jobs_list)
    return assigned_jobs

def LPT(assigned_jobs, compute_cycles,freq,times):
    #compute accomulative time
    #times = compute_time(freq.shape[0],compute_cycles,assigned_jobs)
    #m_time = times
    n_transfers=0
    while True:
        finish_lasts = [i[-1] for i in times]
        #print (finish_lasts)
        finish_lasts_sorted_idx = np.argsort(finish_lasts)

        latest_machine_idx = finish_lasts_sorted_idx[-1]
        #if len(assigned_jobs[latest_machine_idx]) == 0:
        #    exit()
        latest_job_idx = assigned_jobs[latest_machine_idx][-1]
        current_finish_last = finish_lasts[latest_machine_idx]
        for i in range(0,freq.shape[0]):
            last_job_finish_time = times[i][-1]
            transfer = False
            if last_job_finish_time + compute_cycles[latest_job_idx][i] < current_finish_last:
                #transfer
                n_transfers+=1
                del assigned_jobs[latest_machine_idx][-1]
                assigned_jobs[i].append(latest_job_idx)
                times[i].append(last_job_finish_time + compute_cycles[latest_job_idx][i])
                del times[latest_machine_idx][-1]
                transfer = True
                #print ("Transfer from machin "+ str(latest_machine_idx)+ " to machine " +str(i) +" job id "+str(latest_job_idx) )
                #compute_time(freq.shape[0],compute_cycles,assigned_jobs)
                break

        if not transfer:
            break
    print (n_transfers)
    return assigned_jobs
def  compute_compute_cycles(mul,freq):
	compute_cycles = np.zeros((mul.shape[0],freq.shape[0]),dtype=float)
	for i in range(0,compute_cycles.shape[0]):
		compute_cycles[i] = mul[i]/freq
	return compute_cycles
	
def scheduling(matrix,mul,device,freq):
	sorted_idx = np.argsort(mul)[::-1]
    #print (sorted_idx)
	compute_cycles = compute_compute_cycles(mul,freq)
    #print (compute_cycles)

    #RR scheduling
	print("Round Ronbin")
	assigned_jobs = round_robin(freq.shape[0],sorted_idx)
	times=compute_time(freq.shape[0],compute_cycles,assigned_jobs)
	optimized_scheduling = LPT(assigned_jobs, compute_cycles,freq, times)
	compute_time(freq.shape[0],compute_cycles,optimized_scheduling)
	print("segmentation")
	assigned_jobs = segment(freq.shape[0],sorted_idx)
	times=compute_time(freq.shape[0],compute_cycles,assigned_jobs)
	optimized_scheduling = LPT(assigned_jobs, compute_cycles,freq, times)
	compute_time(freq.shape[0],compute_cycles,optimized_scheduling)
	print("weighted segmentation")
	assigned_jobs = weighted_segment(freq.shape[0],sorted_idx,freq)
	times = compute_time(freq.shape[0],compute_cycles,assigned_jobs)
	optimized_scheduling = LPT(assigned_jobs, compute_cycles,freq, times)
	compute_time(freq.shape[0],compute_cycles,optimized_scheduling)
	#print (len(optimized_scheduling))
	return optimized_scheduling

def main():
    pass
if __name__ == '__main__':
    main()