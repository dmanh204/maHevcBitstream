from bitstring import BitStream
c = BitStream(filename='cipher.bin')
o = BitStream(filename='origin.bin')
print(len(c))
count = 0
for _ in range(len(c)):
    i = c.read(1)
    j = o.read(1)
    if j == i:
        continue
    else:
        count += 1

hd = count/len(c)
print(f"Hamming Distance: {hd:.3f}")