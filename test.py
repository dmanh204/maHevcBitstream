import numpy as np
from bitstring import BitStream

# nal_arr = np.frombuffer(stream.tobytes(), dtype=np.uint8)
# print(nal_arr)
# arr = np.unpackbits(nal_arr)
# print(arr)
# reTurn = BitStream()
# for i in nal_arr:
#     reTurn.insert('0b'+f'{i:08b}')
# print(reTurn)

# Read the HEVC bitstream file
s = BitStream(filename='out.bin')
s2 = BitStream(filename='decrROI.bin')
count = 0
for _ in range(len(s)):
    i = s.read(1)
    j = s2.read(1)
    if j == i:
        continue
    else:
        count += 1
print("different =", count)