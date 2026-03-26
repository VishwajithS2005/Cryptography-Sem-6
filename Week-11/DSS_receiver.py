import socket
import copy

s = socket.socket()
s.bind(('',10000))
s.listen(10)
c, addr = s.accept()
pqg = c.recv(1024).decode()
[p,q,g,y] = pqg.split(',')
[p,q,g,y] = [int(p),int(q),int(g),int(y)]
print(f"P: {p}\n\nQ: {q}\n\nG: {g}\n")
print(f"Sender Public Key(Y): {y}\n")
c.send("ack".encode())
[plain,r,s]=c.recv(1024).decode().split(',')
[plain,r,s]=[plain,int(r),int(s)]
err=input("Simulate error? Y/N: ")
if(err=="Y"): plain=plain[:3]+chr(ord(plain[3])+2)+plain[4:]
print(f"\nMessage (M): {plain}\n\nReceived R: {r}\n\nReceived S: {s}\n")

buffers = [
0x6A09E667F3BCC908, 0xBB67AE8584CAA73B, 0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1, 
0x510E527FADE682D1, 0x9B05688C2B3E6C1F, 0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179 
]
K = [
0x428A2F98D728AE22, 0x7137449123EF65CD, 0xB5C0FBCFEC4D3B2F, 0xE9B5DBA58189DBBC,
0x3956C25BF348B538, 0x59F111F1B605D019, 0x923F82A4AF194F9B, 0xAB1C5ED5DA6D8118,
0xD807AA98A3030242, 0x12835B0145706FBE, 0x243185BE4EE4B28C, 0x550C7DC3D5FFB4E2,
0x72BE5D74F27B896F, 0x80DEB1FE3B1696B1, 0x9BDC06A725C71235, 0xC19BF174CF692694,
0xE49B69C19EF14AD2, 0xEFBE4786384F25E3, 0x0FC19DC68B8CD5B5, 0x240CA1CC77AC9C65,
0x2DE92C6F592B0275, 0x4A7484AA6EA6E483, 0x5CB0A9DCBD41FBD4, 0x76F988DA831153B5,
0x983E5152EE66DFAB, 0xA831C66D2DB43210, 0xB00327C898FB213F, 0xBF597FC7BEEF0EE4,
0xC6E00BF33DA88FC2, 0xD5A79147930AA725, 0x06CA6351E003826F, 0x142929670A0E6E70,
0x27B70A8546D22FFC, 0x2E1B21385C26C926, 0x4D2C6DFC5AC42AED, 0x53380D139D95B3DF,
0x650A73548BAF63DE, 0x766A0ABB3C77B2A8, 0x81C2C92E47EDAEE6, 0x92722C851482353B,
0xA2BFE8A14CF10364, 0xA81A664BBC423001, 0xC24B8B70D0F89791, 0xC76C51A30654BE30,
0xD192E819D6EF5218, 0xD69906245565A910, 0xF40E35855771202A, 0x106AA07032BBD1B8,
0x19A4C116B8D2D0C8, 0x1E376C085141AB53, 0x2748774CDF8EEB99, 0x34B0BCB5E19B48A8,
0x391C0CB3C5C95A63, 0x4ED8AA4AE3418ACB, 0x5B9CCA4F7763E373, 0x682E6FF3D6B2B8A3,
0x748F82EE5DEFB2FC, 0x78A5636F43172F60, 0x84C87814A1F0AB72, 0x8CC702081A6439EC,
0x90BEFFFA23631E28, 0xA4506CEBDE82BDE9, 0xBEF9A3F7B2C67915, 0xC67178F2E372532B,
0xCA273ECEEA26619C, 0xD186B8C721C0C207, 0xEADA7DD6CDE0EB1E, 0xF57D4F7FEE6ED178,
0x06F067AA72176FBA, 0x0A637DC5A2C898A6, 0x113F9804BEF90DAE, 0x1B710B35131C471B,
0x28DB77F523047D84, 0x32CAAB7B40C72493, 0x3C9EBE0A15C9BEBC, 0x431D67C49C100D4C,
0x4CC5D4BECB3E42B6, 0x597F299CFC657E2A, 0x5FCB6FAB3AD6FAEC, 0x6C44198C4A475817,
]
state = copy.deepcopy(buffers)

def Convert_hex_to_int(h):
    if(h==''): return 0
    else: return int(h,16)

def Number_of_blocks(l):
    n = (-l-1-128)%1024
    if(n==0): n=1024
    return((l+128+n+1)//1024, n)

def rotr(w,n):
    w=bin(w)[2:].rjust(64,'0')
    w=w[-n:]+w[:-n]
    return int(w,2)

def s_512(w,n):
    nums=[(1,8,7),(19,61,6)]
    x=nums[n]
    w=Convert_hex_to_int(w)
    return (rotr(w,x[0]) ^ rotr(w,x[1]) ^ w>>x[2])

def sigma(w,n):
    nums=[(28,34,39),(14,18,41)]
    x=nums[n]
    return (rotr(w,x[0]) ^ rotr(w,x[1]) ^ rotr(w,x[2]))

def ch(e,f,g):
    return (e & f) ^ ((e ^ (2**64-1)) & g)

def maj(a,b,c):
    return (a & b) ^ (b & c) ^ (c & a) 

def Generate_words(msg):
    w = []
    for i in range(16):
        w.append(msg[16*i:16*i+16])
    for i in range(16,80):
        nw = ((s_512(w[i-2],1)+s_512(w[i-15],0)+Convert_hex_to_int(w[i-16])+Convert_hex_to_int(w[i-7]))%(2**64))
        w.append(hex(nw)[2:])
    return w

def SHA_512(msg):
    [a,b,c,d,e,f,g,h]=state
    words = Generate_words(hex(msg)[2:].rjust(256,'0'))
    for r in range(80):
        t1 = (h+ch(e,f,g)+sigma(e,1)+Convert_hex_to_int(words[r])+K[r])%(2**64)
        t2 = (sigma(a,0)+maj(a,b,c))%(2**64)
        nh = g
        ng = f
        nf = e
        ne = (d+t1)%(2**64)
        nd = c
        nc = b
        nb = a
        na = (t1+t2)%(2**64)
        a,b,c,d,e,f,g,h = na,nb,nc,nd,ne,nf,ng,nh
    strout = "0x"
    for x in [a,b,c,d,e,f,g,h]:
        strout+=hex(x)[2:].rjust(16,'0')
    bufs = [a,b,c,d,e,f,g,h]
    strout = "0x"
    for i in range(8):
        state[i] = (state[i] + bufs[i])%(2**64)
        strout+=hex(state[i])[2:].rjust(16,'0')

h = plain.encode('ascii').hex()
l = 4*len(h)
print(f"Input bits: {l}")
h = (Convert_hex_to_int(h)<<1) + 1
nblocks, npadding = Number_of_blocks(l)
h = (h<<(npadding+128))+(l)
print(f"Number of blocks: {nblocks}\n")
blocks = []
for i in range(nblocks):
    blocks.append(Convert_hex_to_int(hex(h)[2+256*i:258+256*i].rjust(256,'0')))
for block in blocks: SHA_512(block)
strout = "0x"
for i in range(8):
    strout+=hex(state[i])[2:].rjust(16,'0')
print(f"Final Hash: {strout}\n")
hash=int(strout,16)
w=pow(s,-1,q)
u1=(hash*w)%q
u2=(r*w)%q
v=((pow(g,u1,p)*pow(y,u2,p))%p)%q
print(f"W: {w}\n\nU1: {u1}\n\nU2: {u2}\n\nV: {v}\n")
if(v==r): print("VERIFIED SIGNATURE")
else: print("INVALID SIGNATURE")