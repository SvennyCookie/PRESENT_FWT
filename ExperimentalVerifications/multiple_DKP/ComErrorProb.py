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

length = 16

q_list = [3/4,3/4,1/2,1,1,1]
elp_list = [2**(-11.89), 2**(-11.84), 2**(-11.61), 2**(-12.35), 2**(-13.05), 2**(-12.35)]
M = len(elp_list)


N_list = [ 512, 724,
          1024, 1448, 2048,2896,
          4096, 5792, 8192, 11585,
          16384, 23170, 32768, 46340]
exp_list = [9, 9.5,
            10, 10.5, 11, 11.5,
            12, 12.5, 13, 13.5,
            14, 14.5, 15, 15.5]

lam_list = []
for i in range(len(N_list)):
    N = N_list[i]
    B = ((2**length)-N)/((2**length)-1)

    sigma_list = []    
    for j in range(len(elp_list)):
        sigma_list.append(B/N + (2**(-length)) + q_list[j]*elp_list[j])

    lam = len(sigma_list)/(2*sum(sigma_list))
    lam_list.append(lam)

#print(lam_list)

alpha0 = 0.3

alpha0_list = []
alpha1_list = []

alpha0_list_2 = []
alpha1_list_2 = []

for i in range(len(N_list)):
    N = N_list[i]
    B = ((2**length)-N)/((2**length)-1)
    lam = lam_list[i]

    q_alpha0 = chi2.ppf(alpha0, M)
    theta = q_alpha0/(2*lam)

    q_alpha1 = theta/((B/N)+2**(-length))    
    alpha1 = 1-chi2.cdf(q_alpha1, M)
    
    alpha0_list_2.append(alpha0)
    alpha1_list_2.append(alpha1)
    
    filename = 'res_{}.txt'.format(N)
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
        for k in range(len(q_list)):  
            tmp_right += (1/q_list[k])*(text[lineNum*j+2*k+1])
            tmp_wrong += (1/q_list[k])*(text[lineNum*j+2*k+1+int(lineNum/2)])
        elp_list[0].append(tmp_right)
        elp_list[1].append(tmp_wrong)

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
plt.savefig('multiple_DKP.pdf', bbox_inches='tight')

