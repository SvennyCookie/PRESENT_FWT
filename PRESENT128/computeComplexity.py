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

add_time = []  #store addtion times for every linear hull
multi_time = []
register = []
N = 2**62.88
times = -1
for item in mask_list:
    times += 1
    i = item[0] #input mask
    m = item[1] #output mask
    j = item[2]
    n = item[3]

    res = key_guess(i,m,j,n) 
    
    for x in range(len(res)):
        for y in range(len(res[x])):
            res[x][y] += 64

    k2_cross = res[0]  #key bits need to guess
    k1_cross = res[1]
    k28_cross = res[2]
    k29_cross = res[3]
    k30_cross = res[4]
    k2_cross.sort()
    k1_cross.sort()
    k28_cross.sort()
    k29_cross.sort()

    k_o_1 = len(k1_cross)
    k_i_1 = len(k2_cross)    
    k_i_2 = len(k28_cross) + len(k29_cross)
    k_o_2 = len(k30_cross)

    add_tmp = k_o_1*(2**k_o_1)
    add_tmp += k_o_2*(2**k_o_2)

    multi_tmp = 0

    if(i <= 8):  #TypeI
        pi = 1 #Reduction Factor
        gi = 1
        ti = [k_o_1+k_o_2]
        si = [k_o_1+k_o_2]
        Li = [2**(si[0])]

    else: #TypeII
        if ( m == 8):
            pi = 1/2
            gi = 1
            ti = [80]
            si = [80]
            Li = [((10/16)**20)*(2**si[0])]
        else:
            pi = 3/4
            gi = 2
            ti = [80, 80]
            si = [80, 80]
            Li = [((10/16)**20)*(2**si[0]), ((10/16)**20)*(2**si[1])]
        add_tmp += gi*Li[0]

    k1_green_from_ki = key_deduce(k2_cross, 0, 2, 1)
    k1_green_from_ki += key_deduce(k28_cross, 0, 28, 1)
    k1_green_from_ki += key_deduce(k29_cross, 0, 29, 1)
    k1_deduce_from_ki = list(set(k1_green_from_ki)&set(k1_cross))
    k1_deduce_from_ki.sort()

    k30_green_from_ki = key_deduce(k28_cross, 1, 28, 30)
    k30_green_from_ki += key_deduce(k2_cross, 1, 2, 30)
    k30_green_from_ki += key_deduce(k29_cross, 1, 29, 30)
    k30_deduce_from_ki = list(set(k30_green_from_ki)&set(k30_cross))
    k30_deduce_from_ki = list(set(k30_deduce_from_ki))
    k30_deduce_from_ki.sort()

    #mi: ko bits could be deduced from ki
    mi = len(k1_deduce_from_ki)+len(k30_deduce_from_ki)
    tmp_str = "$k_{1}$: "+str(minus_64(k1_deduce_from_ki))    
    str_deduced_bits_from_ki = tmp_str+"$, k_{30}$: "+ str(minus_64(k30_deduce_from_ki))
    
    #get the value of ri
    V = []
    for index in range(64):
        V.append(index+64)

    W = list(set(V)-set(k30_deduce_from_ki))

    if ( i > 8 and m == 2):     
        V1 = []
        V2 = []
        for index in range(16):
            V1.append(index*4 + 64)
            V1.append(index*4 + 65)
            V1.append(index*4 + 67)

            V2.append(index*4 + 64)
            V2.append(index*4 + 66)
            V2.append(index*4 + 67)
        W_perp = k30_deduce_from_ki

        cap_V1_W_perp = list(set(V1)&set(W_perp))
        cap_V2_W_perp = list(set(V2)&set(W_perp))

        V1_qouet = list(set(V1)-set(cap_V1_W_perp)) 
        V2_qouet = list(set(V2)-set(cap_V2_W_perp))

        r1 = len(V1_qouet)
        r2 = len(V2_qouet)

        V3 = k1_cross
        W_perp = k1_deduce_from_ki
        cap_V3_W_perp = list(set(V3) & set(W_perp))
        V3_qouet = list(set(V3)-set(cap_V3_W_perp))
        r3 = len(V3_qouet)
        

        ri = [r1+r3, r2+r3]
     
    if ( i > 8 and m == 4):
        V1 = []
        V2 = []
        for index in range(16):
            V1.append(index*4 + 64)
            V1.append(index*4 + 65)
            V1.append(index*4 + 66)

            V2.append(index*4 + 64)
            V2.append(index*4 + 65)
            V2.append(index*4 + 67)
        W_perp = k30_deduce_from_ki

        cap_V1_W_perp = list(set(V1)&set(W_perp))
        cap_V2_W_perp = list(set(V2)&set(W_perp))

        V1_qouet = list(set(V1)-set(cap_V1_W_perp)) 
        V2_qouet = list(set(V2)-set(cap_V2_W_perp))

        r1 = len(V1_qouet)
        r2 = len(V2_qouet)

        V3 = k1_cross
        W_perp = k1_deduce_from_ki
        cap_V3_W_perp = list(set(V3) & set(W_perp))
        V3_qouet = list(set(V3)-set(cap_V3_W_perp))
        r3 = len(V3_qouet)

        ri = [r1+r3, r2+r3]

    if ( i > 8 and m == 8):
        V1 = []
        for index in range(16):            
            V1.append(index*4 + 65)
            V1.append(index*4 + 66)
            V1.append(index*4 + 67)

        W_perp = k30_deduce_from_ki

        cap_V1_W_perp = list(set(V1)&set(W_perp))

        V1_qouet = list(set(V1)-set(cap_V1_W_perp)) 

        r1 = len(V1_qouet)

        V3 = k1_cross
        W_perp = k1_deduce_from_ki
        cap_V3_W_perp = list(set(V3) & set(W_perp))
        V3_qouet = list(set(V3)-set(cap_V3_W_perp))
        r3 = len(V3_qouet)

        ri = [r1+r3]

    if(i<=8):
        ri = [k_o_1+k_o_2]

    register1 = 0
    register2 = 0

    for index in range(gi):
        
        add_tmp += (N + ti[index]*(2**ti[index]))
        add_tmp += (2**(k_i_1+k_i_2))*ri[index]*(2**ri[index])
        
        multi_tmp += 2*Li[index]

        register1 += 2**ti[index]
        register2 += 2**ri[index]

    #ni: the least bits number need to carry out k_o||k_i
    k1_green_from_k30 = key_deduce(k30_cross, 0, 30, 1)
    k2_green_from_k30 = key_deduce(k30_cross, 0, 30, 2)
    k28_green_from_k30 = key_deduce(k30_cross, 0, 30, 28)
    k29_green_from_k30 = key_deduce(k30_cross, 0, 30, 29)
    ni = len(k2_cross)+len(k1_cross)+len(k28_cross)+len(k29_cross)+len(k30_cross)
    ni = ni - len(list(set(k1_green_from_k30) & set(k1_cross))) - len(list(set(k2_green_from_k30) & set(k2_cross)))-len(list(set(k28_green_from_k30) & set(k28_cross))) - len(list(set(k29_green_from_k30) & set(k29_cross)))

    add_tmp += gi*(2**ni)
    multi_tmp += 2*(2**ni)
    add_time.append(add_tmp)
    multi_time.append(multi_tmp)
    
    register.append(max(register1,register2))

##    print('\\item $L'+str(times)+'$: '+str(item)+
##            ', $g_{'+str(times)+'}='+ str(gi) +
##            ', s_{'+str(times)+'}='+ str(si) +
##            ', t_{'+str(times)+'}='+ str(ti) +
##            ', r_{'+str(times)+'}='+ str(ri) +
##            ', n_{'+str(times)+'}='+ str(ni)+'$.')
##    print('$m_{'+str(times)+'}=', mi,'$bits ('+
##            str_deduced_bits_from_ki+') could be deduced from $k_2,k_{28}, k_{29}$.')
##    print('\n')
            
print("2^", np.log2(sum(add_time)), 'times additions')

print("2^", np.log2(sum(multi_time)), 'times multiplications')
print("max register: 2^", np.log2(float(max(register))))
    

   


