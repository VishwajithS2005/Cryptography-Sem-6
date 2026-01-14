IP = input("IP: ").split(" ")
IP = [int(i) for i in IP]

IP_inv = []
for i in range(len(IP)):
    IP_inv.append(IP.index(i+1)+1)

print(IP_inv)