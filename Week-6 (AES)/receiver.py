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

def inverse_s_box(b):
    inv_s_box = [
        ["52","09","6a","d5","30","36","a5","38","bf","40","a3","9e","81","f3","d7","fb"],
        ["7c","e3","39","82","9b","2f","ff","87","34","8e","43","44","c4","de","e9","cb"],
        ["54","7b","94","32","a6","c2","23","3d","ee","4c","95","0b","42","fa","c3","4e"],
        ["08","2e","a1","66","28","d9","24","b2","76","5b","a2","49","6d","8b","d1","25"],
        ["72","f8","f6","64","86","68","98","16","d4","a4","5c","cc","5d","65","b6","92"],
        ["6c","70","48","50","fd","ed","b9","da","5e","15","46","57","a7","8d","9d","84"],
        ["90","d8","ab","00","8c","bc","d3","0a","f7","e4","58","05","b8","b3","45","06"],
        ["d0","2c","1e","8f","ca","3f","0f","02","c1","af","bd","03","01","13","8a","6b"],
        ["3a","91","11","41","4f","67","dc","ea","97","f2","cf","ce","f0","b4","e6","73"],
        ["96","ac","74","22","e7","ad","35","85","e2","f9","37","e8","1c","75","df","6e"],
        ["47","f1","1a","71","1d","29","c5","89","6f","b7","62","0e","aa","18","be","1b"],
        ["fc","56","3e","4b","c6","d2","79","20","9a","db","c0","fe","78","cd","5a","f4"],
        ["1f","dd","a8","33","88","07","c7","31","b1","12","10","59","27","80","ec","5f"],
        ["60","51","7f","a9","19","b5","4a","0d","2d","e5","7a","9f","93","c9","9c","ef"],
        ["a0","e0","3b","4d","ae","2a","f5","b0","c8","eb","bb","3c","83","53","99","61"],
        ["17","2b","04","7e","ba","77","d6","26","e1","69","14","63","55","21","0c","7d"],
    ]
    return inv_s_box[int(b[0], 16)][int(b[1], 16)]

def circular_left_shift(s, n):
    return s[n:] + s[:n]

def circular_right_shift(s, n):
    return s[-n:] + s[:-n]

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
    words.reverse()
    return words

def inverse_shift_rows(ct):
    for i in range(4):
        ct[i] = circular_right_shift(ct[i], i)
    return ct

def inverse_sub_bytes(ct):
    temp = [[None]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            temp[i][j] = inverse_s_box(ct[i][j])
    return temp

def flatten_state(state):
    return ''.join(state[r][c] for c in range(4) for r in range(4))

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

def inverse_mix_columns(ct):
    imc = [
        ["0e", "0b", "0d", "09"],
        ["09", "0e", "0b", "0d"],
        ["0d", "09", "0e", "0b"],
        ["0b", "0d", "09", "0e"]
    ]
    temp = [[None]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            temp[i][j] = 0
            for k in range(4):
                temp[i][j] ^= gf_mul(imc[i][k], ct[k][j])
            temp[i][j] = hex(temp[i][j])[2:].rjust(2, '0')
    return temp

def AES_Decryption(ct, key):
    CT = convert_array(ct)
    keys = get_intermediate_keys(key)
    temp = [[None for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            temp[i][j] = hex(int(CT[i][j], 16) ^ int(keys[0][i][j], 16))[2:].rjust(2, '0')
    temp = inverse_shift_rows(temp)
    temp = inverse_sub_bytes(temp)
    print(f"Round 0, converted text: \"{flatten_state(temp)}\", key: \"{flatten_state(keys[0])}\"")

    for k in range(1, 10):
        for i in range(4):
            for j in range(4):
                temp[i][j] = hex(int(temp[i][j], 16) ^ int(keys[k][i][j], 16))[2:].rjust(2, '0')
        temp = inverse_mix_columns(temp)
        temp = inverse_shift_rows(temp)
        temp = inverse_sub_bytes(temp)
        print(f"Round {k}, converted text: \"{flatten_state(temp)}\", key: \"{flatten_state(keys[k])}\"")
    for i in range(4):
        for j in range(4):
            temp[i][j] = hex(int(temp[i][j], 16) ^ int(keys[10][i][j], 16))[2:].rjust(2, '0')
    print(f"Final Round, plain text: \"{flatten_state(temp)}\", key: \"{flatten_state(keys[10])}\"")
    return flatten_state(temp)

server = socket.socket()
server.bind(('127.0.0.1', 5995))
server.listen(1)
print("AES Receiver initialized and listening for sender.")
conn, addr = server.accept()
print(f"Connection established with sender at {addr}.")

ct = conn.recv(1024).decode().rstrip('\0')
print(f"\nThe received cipher text is: {ct}.\n")
key = conn.recv(1024).decode().rstrip('\0')
conn.close()
server.close()

pt = AES_Decryption(ct, key)
print(f"\nThe plain text is: {pt}.")