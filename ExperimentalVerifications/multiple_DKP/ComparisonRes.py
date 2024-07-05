import random
import time
import openpyxl
import math
import numpy as np

from scipy import stats
from scipy.stats import norm
from scipy.stats import f
from scipy.stats import chi2
import matplotlib.pyplot as plt

lineNum = 24
n = 16
p_list = [3/4,3/4,1/2,1,1,1]
ELP_list = [2**(-11.89), 2**(-11.84), 2**(-11.61), 2**(-12.35), 2**(-13.05), 2**(-12.35)]
M = len(ELP_list)
N_list = [ 512, 724,
          1024, 1448, 2048,2896,
          4096, 5792, 8192, 11585,
          16384, 23170, 32768, 46340]
exp_list = [9, 9.5,
            10, 10.5, 11, 11.5,
            12, 12.5, 13, 13.5,
            14, 14.5, 15, 15.5]
lam_list = []
lam_list_euro24 = []
lam_list_euro24_alpha1 = []
for i in range(len(N_list)):
    N = N_list[i]
    B = ((2**n)-N)/((2**n)-1)
    
    lam = 0
    lam_euro24 = 0
    lam_euro24_alpha1 = 0
    for j in range(len(ELP_list)):
        lam += (B/N + (2**(-n)) + p_list[j]*ELP_list[j])
        lam_euro24 += (B/N + p_list[j]*ELP_list[j])
        lam_euro24_alpha1 += (B/N + (2**(-n))*p_list[j])
    lam_list.append(lam/M)
    lam_list_euro24.append(lam_euro24/M)
    lam_list_euro24_alpha1.append(lam_euro24_alpha1/M)
#print(lam_list)
alpha0 = 0.3

alpha0_list_1 = [] #experimantal values
alpha1_list_1 = []
alpha0_list_2 = [] #theory values
alpha1_list_2 = []

alpha0_list_1_euro24 = []
alpha1_list_1_euro24 = []
alpha0_list_2_euro24 = []
alpha1_list_2_euro24 = []

for i in range(len(N_list)):
    N = N_list[i]
    B = ((2**n)-N)/((2**n)-1)
    lam = lam_list[i]

    #choose data set
    #filename = 'data_independentKey\\res_{}.txt'.format(N)
    filename = 'data_withKeySchedule\\res_{}.txt'.format(N)
    f = open(filename,encoding='utf-8')
    text = []
    lines = f.readlines()
    for line in lines:
        line = line.replace("\n","")
        text.append(float(line)**2)    
    f.close()
    times = int(len(text)/lineNum)    
    elp_list = [[],[]]
    for j in range(times):
        tmp_right = 0
        tmp_wrong = 0
        for k in range(len(p_list)):  
            tmp_right += (1/p_list[k])*(text[lineNum*j+2*k+1])
            tmp_wrong += (1/p_list[k])*(text[lineNum*j+2*k+1+int(lineNum/2)])
        elp_list[0].append(tmp_right)
        elp_list[1].append(tmp_wrong)
        
    #euro24
    lam_euro24 = lam_list_euro24[i]
    lam_euro24_alpha1 = lam_list_euro24_alpha1[i]
    N_euro24 = N
    q_alpha0_euro24 = chi2.ppf(alpha0, M)
    theta_euro24 = q_alpha0_euro24 * lam_euro24
    q_alpha1_euro24 = theta_euro24/lam_euro24_alpha1
    alpha1_euro24 = 1-chi2.cdf(q_alpha1_euro24, M)
    
    alpha0_list_2_euro24.append(alpha0)
    alpha1_list_2_euro24.append(alpha1_euro24)   
    for j in range(len(elp_list)):
        cnt = 0
        for item in elp_list[j]:
            if (item > theta_euro24):
                cnt += 1
        if (j == 0):
            alpha0_list_1_euro24.append(1-cnt/len(elp_list[j]))
        else:
            alpha1_list_1_euro24.append(cnt/len(elp_list[j]))

    #our model
    q_alpha0 = chi2.ppf(alpha0, M)
    theta = q_alpha0*lam
    q_alpha1 = theta/((B/N)+2**(-n))   
    alpha1 = 1-chi2.cdf(q_alpha1, M)
    
    alpha0_list_2.append(alpha0)
    alpha1_list_2.append(alpha1)
    for j in range(len(elp_list)):
        cnt = 0
        for item in elp_list[j]:
            if (item > theta):
                cnt += 1
        if (j == 0):   #right key
            #print("Theoretical α0：", alpha0)
            #print("Experimental α0：",1-cnt/len(elp_list[j]))
            alpha0_list_1.append(1-cnt/len(elp_list[j]))
        else:
            #print("Theoretical α1：", alpha1)
            #print("Experimental α1：",cnt/len(elp_list[j]))
            alpha1_list_1.append(cnt/len(elp_list[j]))

fig = plt.figure(figsize=(12.8,7.2))

ax = fig.add_subplot(1,1,1)
ax.plot(exp_list, alpha0_list_2_euro24, linestyle = '--', c = '#4f9da6', marker='^', label = r'$\alpha_0$, Paper[31]')
ax.plot(exp_list, alpha0_list_1_euro24, linestyle = '--', c = '#ffad5a', marker='o', label = r'$\hat{\alpha_0}, Paper [31]$')
ax.plot(exp_list, alpha1_list_2_euro24, linestyle = '--', c = '#ff5959', marker='s', label = r'$\alpha_1, Paper [31]$')
ax.plot(exp_list, alpha1_list_1_euro24, linestyle = '--', c = '#706d94', marker='v', label = r'$\hat{\alpha_1}, Paper [31]$')

ax.plot(exp_list, alpha0_list_2, c = '#4f9da6', marker='^', label = r'$\alpha_0, Our$')
ax.plot(exp_list, alpha0_list_1, c = '#ffad5a', marker='o', label = r'$\hat{\alpha_0}, Our$')
ax.plot(exp_list, alpha1_list_2, c = '#ff5959', marker='s', label = r'$\alpha_1, Our$')
ax.plot(exp_list, alpha1_list_1, c = '#706d94', marker='v', label = r'$\hat{\alpha_1}, Our$')

plt.xlabel("log(N)", fontsize=24, family = 'Times New Roman')
plt.ylabel("Error Probability", fontsize=24, family = 'Times New Roman')
plt.xticks(exp_list, fontsize=24, family = 'Times New Roman')
plt.yticks(np.arange(0.1,0.9,0.1), fontsize=24, family = 'Times New Roman')
plt.legend(fontsize=10)

plt.show()
