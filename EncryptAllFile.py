from bitstring import BitStream
import sys
sys.path.insert(0, 'F:/TaiLieuHocTap/sip/StreamCipher/lightWeightStreamCipher')
import lightweight as lw
import numpy as np
import math
import time
key = 0xb5f576a31909777d
key1 = 0xb51d46a31000757d
key2 = 0x829076a31909aaf3
ma = lw.light(key)
ma1 = lw.light(key1)
ma2 = lw.light(key2)


def xor_encrypt_decrypt(bin_np, key):
    key_np = np.array(key, dtype=np.uint8)
    key_np = np.resize(key_np, bin_np.shape) # Resize key stream  equal to binary stream.

    result = np.bitwise_xor(bin_np, key_np)
    return result


def bitStream2NParr(stream):
    n_arr = np.frombuffer(stream.tobytes(), dtype=np.uint8)
    return n_arr


def NParr2bitStream(np_arr):
    ret = BitStream()
    for i in np_arr:
        ret.insert('0b'+f'{i:08b}')

    return ret


# Read the HEVC bitstream file
s = BitStream(filename='out.bin')
print(len(s))
st = time.time()
sKey = []
for _ in range(math.ceil(len(s) / 256)):  # Vi mot lan chay light sinh ra 32 byte =256 bit
    sKey.extend(ma2.run())

# Convert from bitstream to numpy array
np_arr = bitStream2NParr(s)
# Encryption
res = xor_encrypt_decrypt(np_arr, sKey)
# Convert from numpy array to bitstream
result = NParr2bitStream(res)
ed = time.time()
with open('encrAll_file1.bin', 'wb') as f:
    result.tofile(f)
print("Thoi gian ma hoa: ", f'{ed-st:.3f}')