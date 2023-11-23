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

N_list = [ 512, 724,
          1024, 1448, 2048,2896,
          4096, 5792, 8192, 11585,
          16384, 23170, 32768, 46340]
exp_list = [9, 9.5,
            10, 10.5, 11, 11.5,
            12, 12.5, 13, 13.5,
            14, 14.5, 15, 15.5]

ELP = 2**(-11.89)
alpha0 = 0.3

alpha0_list = []
alpha1_list = []


alpha0_list_2 = []
alpha1_list_2 = []

for i in range(len(N_list)):
    N = N_list[i]
    B = ((2**n)-N)/((2**n)-1)

    tmp1 = (B/N)*(3/4)
    tmp3 = (2**(-n))*(3/4)
    q_alpha0 = chi2.ppf(alpha0, 1) 

    q_alpha1 = ((tmp1+tmp3+(9/16)*ELP)*q_alpha0)/(tmp1+tmp3)
    alpha1 = 1-chi2.cdf(q_alpha1, 1)

    alpha0_list_2.append(alpha0)
    alpha1_list_2.append(alpha1)

    theta = (tmp1+tmp3+(9/16)*ELP)*q_alpha0
    
    filename = 'res_{}.txt'.format(N)
    f = open(filename,encoding='utf-8')
    text = []
    lines = f.readlines()
    for line in lines:
        line = line.replace("\n","")
        text.append(line)
    f.close()

    times = int(len(text)/4)
    
    elp_list = [[],[]]
    for j in range(times):        
        elp_list[0].append(float(text[4*j + 1])**2) 
        elp_list[1].append(float(text[4*j + 3])**2)

    for j in range(len(elp_list)):
        cnt = 0
        for item in elp_list[j]:
            if (item > theta):
                cnt += 1
        if (j == 0):   #right key
            #print("Theoretical α0：", alpha0)
            #print("Experimental α0：",1-cnt/len(elp_list[j]))
            alpha0_list.append(1-cnt/len(elp_list[j]))

        else:
            #print("Theoretical α1：", alpha1)
            #print("Experimental α1：",cnt/len(elp_list[j]))
            alpha1_list.append(cnt/len(elp_list[j]))

fig = plt.figure(figsize=(12.8,7.2))
ax = fig.add_subplot(1,1,1)
ax.plot(exp_list, alpha0_list_2, c = '#4f9da6', marker='^', label = r'$\alpha_0$')
ax.plot(exp_list, alpha0_list, c = '#ffad5a', marker='o', label = r'$\hat{\alpha}_0$')
ax.plot(exp_list, alpha1_list_2, c = '#ff5959', marker='s', label = r'$\alpha_1$')
ax.plot(exp_list, alpha1_list, c = '#706d94', marker='v', label = r'$\hat{\alpha}_1$')

plt.xlabel("log(N)", fontsize=12, family = 'Times New Roman')
plt.ylabel("Error Probability", fontsize=12, family = 'Times New Roman')
plt.xticks(exp_list, family = 'Times New Roman')
plt.yticks(np.arange(0.1,0.9,0.1), family = 'Times New Roman')
plt.legend()

#plt.show()
plt.savefig('single_DKP.pdf', bbox_inches='tight')

