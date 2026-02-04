import numpy as np
import socket

def s_box(b):
    s_box = [
        ["63","7c","77","7b","f2","6b","6f","c5","30","01","67","2b","fe","d7","ab","76"],
        ["ca","82","c9","7d","fa","59","47","f0","ad","d4","a2","af","9c","a4","72","c0"],
        ["b7","fd","93","26","36","3f","f7","cc","34","a5","e5","f1","71","d8","31","15"],
        ["04","c7","23","c3","18","96","05","9a","07","12","80","e2","eb","27","b2","75"],
        ["09","83","2c","1a","1b","6e","5a","a0","52","3b","d6","b3","29","e3","2f","84"],
        ["53","d1","00","ed","20","fc","b1","5b","6a","cb","be","39","4a","4c","58","cf"],
        ["d0","ef","aa","fb","43","4d","33","85","45","f9","02","7f","50","3c","9f","a8"],
        ["51","a3","40","8f","92","9d","38","f5","bc","b6","da","21","10","ff","f3","d2"],
        ["cd","0c","13","ec","5f","97","44","17","c4","a7","7e","3d","64","5d","19","73"],
        ["60","81","4f","dc","22","2a","90","88","46","ee","b8","14","de","5e","0b","db"],
        ["e0","32","3a","0a","49","06","24","5c","c2","d3","ac","62","91","95","e4","79"],
        ["e7","c8","37","6d","8d","d5","4e","a9","6c","56","f4","ea","65","7a","ae","08"],
        ["ba","78","25","2e","1c","a6","b4","c6","e8","dd","74","1f","4b","bd","8b","8a"],
        ["70","3e","b5","66","48","03","f6","0e","61","35","57","b9","86","c1","1d","9e"],
        ["e1","f8","98","11","69","d9","8e","94","9b","1e","87","e9","ce","55","28","df"],
        ["8c","a1","89","0d","bf","e6","42","68","41","99","2d","0f","b0","54","bb","16"],
    ]
    return s_box[int(b[0], 16)][int(b[1], 16)]


def circular_left_shift(s, n):
    return s[n:] + s[:n]

def convert_array(s):
    arr = [s[i:i+2] for i in range(0, len(s), 2)]
    return np.array(arr).reshape(4, 4).T.tolist()

def round_constant(r):
    RC = ["01", "02", "04", "08", "10", "20", "40", "80", "1B", "36"]
    return RC[r]

def g_function(w, r):
    byte = [w[i:i+2] for i in range(0, len(w), 2)]
    byte = circular_left_shift(byte, 1)
    byte = [s_box(b) for b in byte]
    RC = round_constant(r)
    byte[0] = hex(int(RC, 16) ^ int(byte[0], 16))[2:].rjust(2, '0')
    return ''.join(byte)

def get_intermediate_keys(key):
    word = [key[i:i+8] for i in range(0, 32, 8)]
    words = [convert_array(''.join(word))]
    for i in range(10):
        new_word = [None]*4
        w3 = g_function(word[3], i)
        new_word[0] = hex(int(word[0], 16) ^ int(w3, 16))[2:].rjust(8, '0')
        new_word[1] = hex(int(word[1], 16) ^ int(new_word[0], 16))[2:].rjust(8, '0')
        new_word[2] = hex(int(word[2], 16) ^ int(new_word[1], 16))[2:].rjust(8, '0')
        new_word[3] = hex(int(word[3], 16) ^ int(new_word[2], 16))[2:].rjust(8, '0')
        words.append(convert_array(''.join(new_word.copy())))
        word = new_word.copy()
    return words

def sub_bytes(pt):
    temp = [[None for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            temp[i][j] = s_box(pt[i][j])
    return temp

def shift_rows(pt):
    for i in range(4):
        pt[i] = circular_left_shift(pt[i], i)
    return pt

def gf_mul(a, b):
    A = int(a, 16)
    B = int(b, 16)
    result = 0
    for _ in range(8):
        if B & 1:
            result ^= A
        c = A & 0x80
        A <<= 1
        if c:
            A ^= 0x11B
        A &= 0xFF
        B >>= 1
    return result

def mix_columns(pt):
    mc = [
        ["02", "03", "01", "01"],
        ["01", "02", "03", "01"],
        ["01", "01", "02", "03"],
        ["03", "01", "01", "02"]
    ]
    temp = [[None]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            temp[i][j] = 0
            for k in range(4):
                temp[i][j] ^= gf_mul(mc[i][k], pt[k][j])
            temp[i][j] = hex(temp[i][j])[2:].rjust(2, '0')
    return temp

def flatten_state(state):
    return ''.join(state[r][c] for c in range(4) for r in range(4))

def AES_Encryption(pt, key):
    PT = convert_array(pt)
    keys = get_intermediate_keys(key)
    temp = [[None for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            temp[i][j] = hex(int(PT[i][j], 16) ^ int(keys[0][i][j], 16))[2:].rjust(2, '0')
    print(f"\nRound 0, converted text: \"{flatten_state(temp)}\", key: \"{flatten_state(keys[0])}\"")
    for k in range(1, 10):
        temp = sub_bytes(temp)
        temp = shift_rows(temp)
        temp = mix_columns(temp)
        for i in range(4):
            for j in range(4):
                temp[i][j] = hex(int(temp[i][j], 16) ^ int(keys[k][i][j], 16))[2:].rjust(2, '0')
        print(f"Round {k}, converted text: \"{flatten_state(temp)}\", key: \"{flatten_state(keys[k])}\"")
    temp = sub_bytes(temp)
    temp = shift_rows(temp)
    for i in range(4):
        for j in range(4):
            temp[i][j] = hex(int(temp[i][j], 16) ^ int(keys[10][i][j], 16))[2:].rjust(2, '0')
    print(f"Final Round, cipher text: \"{flatten_state(temp)}\", key: \"{flatten_state(keys[10])}\"")
    return flatten_state(temp)

print("AES Sender initialized.\n")
pt = input("Enter a 128-bit plain text in hexadecimal: ")
key = input("Enter a 128-bit key in hexadecimal: ")

ct = AES_Encryption(pt, key)
print(f"\nThe cipher text is: {ct}.")

s = socket.socket()
s.connect(('127.0.0.1', 5995))
s.send(ct.encode().ljust(1024, b'\0'))
s.send(key.encode().ljust(1024, b'\0'))
print("\nThe Cipher text and the key have been sent successfully to the receiver.")
s.close()