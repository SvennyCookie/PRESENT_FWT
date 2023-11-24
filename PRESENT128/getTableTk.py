import numpy as np

s_box = [0xC,0x5,0x6,0xB,0x9,0x0,0xA,0xD,0x3,0xE,0xF,0x8,0x4,0x7,0x1,0x2]
inv_s_box = [0x5,0xE,0xF,0x8,0xC,0x1,0x2,0xD,0xB,0x4,0x6,0x3,0x0,0x7,0x9,0xA]

#right rotation
def list_move_right(a,n):
    length = len(a)
    for i in range(n):
        a.insert(0,a[length-1])
        a.pop()
    return(a)

#left rotation
def list_move_left(a,n):
    length = len(a)
    for i in range(n):
        a.insert(len(a),a[0])
        a.remove(a[0])
    return(a)

def key_up(start,end):
    a=[[0]]
    for i in range(1,128):
        a.append([i])
    for count in range(start-1,end-1,-1):
        x1 = a[123]
        x2 = a[122]
        x3 = a[121]
        x4 = a[120]
        a[123] = x1+x2+x3+x4
        a[122] = x1+x2+x3+x4
        a[121] = x1+x2+x3+x4
        a[120] = x1+x2+x3+x4

        y1 = a[127]
        y2 = a[126]
        y3 = a[125]
        y4 = a[124]
        a[127] = y1+y2+y3+y4
        a[126] = y1+y2+y3+y4
        a[125] = y1+y2+y3+y4
        a[124] = y1+y2+y3+y4
        
        list_move_left(a,61)

        for i in range(len(a)):
            a[i] = list(set(a[i]))
            a[i].sort()

    return a
#print(a)

   
def key_down(start,end):
    a=[[0]]
    for i in range(1,128):
        a.append([i])
    for count in range(start+1,end+1):
        list_move_right(a,61)
        
        x1 = a[123]
        x2 = a[122]
        x3 = a[121]
        x4 = a[120]
        a[123] = x1+x2+x3+x4
        a[122] = x1+x2+x3+x4
        a[121] = x1+x2+x3+x4
        a[120] = x1+x2+x3+x4

        y1 = a[127]
        y2 = a[126]
        y3 = a[125]
        y4 = a[124]
        a[127] = y1+y2+y3+y4
        a[126] = y1+y2+y3+y4
        a[125] = y1+y2+y3+y4
        a[124] = y1+y2+y3+y4
        
        for i in range(len(a)):
            a[i] = list(set(a[i]))
            a[i].sort()
    return a

def p_inv(k):
    k_new = [0]*len(k)
    for i in range(len(k)):
        a = k[i]%16
        b = k[i]//16 
        k_new[i] = 4*a + b
    k_new = list(set(k_new))
    k_new.sort()
    #print(k_new)
    return(k_new)

def p(k):
    k_new = [0]*len(k)   
    for i in range(len(k)):
        if (k[i] != 63):
            k_new[i] = (16*k[i])%63
        else:
            k_new[i] = 63
    k_new = list(set(k_new))
    k_new.sort()
    #print(k_new)
    return(k_new)

def activeKey(a,S,k):
    tmp = (bin(a)[2:]).zfill(4)
    for i in range(len(tmp)):
        if (tmp[i]=='1'):
            k.append(4*S+3-i)
    k = list(set(k))
    k.sort()
    #print(k)    
    return k

def s_inv(k):
    k_new = [] 
    for i in range(len(k)):
        a = k[i]//4
        k_new.append(a*4)
        k_new.append(a*4+1)
        k_new.append(a*4+2)
        k_new.append(a*4+3)
    k_new = list(set(k_new))
    k_new.sort()
    #print(k_new)
    return(k_new)

#guess bits in k2,k1,k28,k29
def key_guess(iMask,oMask,iSbox,oSbox):
    k2 = s_inv(p_inv(activeKey(iMask,iSbox,[])))
    k1 = s_inv(p_inv(k2))
    k28 = p(s_inv(activeKey(oMask,oSbox,[])))
    k29 = p(s_inv(k28))
    k30 = p(s_inv(k29))
    k1 = list(set(k1))
    k2 = list(set(k2))
    k28 = list(set(k28))
    k29 = list(set(k29))
    k30 = list(set(k30))
    #return(str(k2)+str(k1)+str(k28)+str(k29)+str(k30))
    return([k2,k1,k28,k29,k30])

def get_key_red(k_cross, flag, red_round, cross_round):
    res = []
    if (flag == 0):
        k_about_red = key_up(red_round,cross_round) 
    if (flag == 1):
        k_about_red = key_down(red_round,cross_round)
    for item in k_cross: 
        tmp = k_about_red[item] 
        for items in tmp:
            res.append(items)
    return list(set(res))

#deduced bits from other guess bits in other round
#Bigger round to smaller round(0)
def key_deduce(k_red, flag, red_round, deduce_round):
    if (flag == 0):
        k_about_red = key_up(red_round,deduce_round) 
    if (flag == 1):
        k_about_red = key_down(red_round,deduce_round)
    res = []
    for x in range(len(k_about_red)):
        if set(k_about_red[x])<set(k_red):
            res.append(x)
    return list(set(res))

#get the key index in 64-bit subkey from KS
def minus_64(b):
    a = [0]*len(b)
    for i in range(len(a)):
        a[i] = b[i]-64
    return a

#get deduced bits among crossed bits
def get_red_str(k_cross,k_green):

    k_64_cross = minus_64(k_cross)
    k_64_green = minus_64(k_green)

    k_64_cross_str = '['
    for i in range(len(k_64_cross)):
        if (k_64_cross[i] in k_64_green):
            k_64_cross_str += '\\red{'+str(k_64_cross[i])+'}, '
        else:
            k_64_cross_str += str(k_64_cross[i])+', '
    k_64_cross_str = k_64_cross_str[0:(len(k_64_cross_str)-2)]
    k_64_cross_str += ']'
    return k_64_cross_str

L11 = [0xa, 0xc]
L12 = [0xa]
L13 = [0xc]
L14 = [2,4]
L15 = [8]

L21 = [5,6,9,10]
L22 = [13,14]

L31 = [2,4,8]
L32 = [2,8]

L41 = [5,7,13,15]

mask_list = []

#HW = 1, TypeI
for i in L14:
    for j in L21:
        for m in L31:
            for n in L41:
                mask_list.append([i,m,j,n])

for i in L15:
    for j in L21:
        for m in L32:
            for n in L41:
                mask_list.append([i,m,j,n])

for i in L14:
    for j in L22:
        for m in L32:
            for n in L41:
                mask_list.append([i,m,j,n])
'''
#HW = 2, TypeII
for i in L11:
    for j in L21:
        for m in L31:
            for n in L41:
                mask_list.append([i,m,j,n])

for i in L12:
    for j in L22:
        for m in L31:
            for n in L41:
                mask_list.append([i,m,j,n])


for i in L13:
    for j in L22:
        for m in L32:
            for n in L41:
                mask_list.append([i,m,j,n])
'''

L_str = []
L = []

T_table = []
T_length = []
T_str = []

for item in mask_list:    
    i = item[0] #input mask
    m = item[1] #output mask
    j = item[2]
    n = item[3]

    res = key_guess(i,m,j,n) 
    
    for x in range(len(res)):
        for y in range(len(res[x])):
            res[x][y] += 64

    k2_cross = res[0]  
    k1_cross = res[1]
    k28_cross = res[2]
    k29_cross = res[3]
    k30_cross = res[4]
    k2_cross.sort()
    k1_cross.sort()
    k28_cross.sort()
    k29_cross.sort()

    k1_green = key_deduce(k30_cross, 0, 30, 1)
    k2_green = key_deduce(k30_cross, 0, 30, 2)
    k28_green = key_deduce(k30_cross, 0, 30, 28)
    k29_green = key_deduce(k30_cross, 0, 30, 29)

    tmp_length = len(k2_cross)+len(k1_cross)+len(k28_cross)+len(k29_cross)+len(k30_cross)
    tmp_length = tmp_length - len(list(set(k1_green) & set(k1_cross))) - len(list(set(k2_green) & set(k2_cross)))- len(list(set(k28_green) & set(k28_cross))) - len(list(set(k29_green) & set(k29_cross)))
    T_length.append(tmp_length) 

    #T_table.append([minus_64(k1_cross), minus_64(k2_cross), minus_64(k28_cross), minus_64(k29_cross)]) 
    T_table.append(str([k1_cross, k2_cross, k28_cross, k29_cross]))
    
    k1_64_cross_str = get_red_str(k1_cross,k1_green)
    k2_64_cross_str = get_red_str(k2_cross,k2_green)
    k28_64_cross_str = get_red_str(k28_cross,k28_green)
    k29_64_cross_str = get_red_str(k29_cross,k29_green)            
    
    T_str.append("$k_1$: "+str(k1_64_cross_str)+"\n$k_2$: "+str(k2_64_cross_str)+"\n$k_{28}$: "+str(k28_64_cross_str)+"\n$k_{29}$: "+str(k29_64_cross_str))

T_str_set = list(set(T_str))
T_str_set.sort()
    
for i in range(len(T_str_set)):
    cnt = 0
    tmp = ''
    #length_tmp = 0
    for j in range(len(T_str)):        
        if T_str[j] == T_str_set[i]:
            a = '['
            a += '\\texttt{'+hex(mask_list[j][0])[2:]+'}, '
            a += '\\texttt{'+hex(mask_list[j][1])[2:]+'}, '
            a += str(mask_list[j][2])+', '
            a += str(mask_list[j][3])+'], '
            tmp += a
            #print(mask_list[j])
            cnt+=1
            length_tmp = T_length[j]
##    print('$T'+str(i)+'$ of size $2^{'+str(length_tmp)+'}$')
##    print(T_str_set[i])
##    print(tmp[0:len(tmp)-2])
##    print("Number of linear hulls in this group: ", cnt)
##    print('\n')

