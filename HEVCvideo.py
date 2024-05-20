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
s = BitStream(filename='hd_1min.bin')

# Find the NAL unit start codes (0x000001)
nal_units = list(s.findall('0x000001', bytealigned=True))
origin = BitStream()
cipher = BitStream()
st = time.time()
# Process each NAL unit
for i in range(len(nal_units)):
    nal_start = nal_units[i]
    nal_end = nal_units[i + 1] if i < len(nal_units) - 1 else None

    # Read the NAL unit header (for example, forbidden_zero_bit and nal_unit_type)
    s.pos = nal_start + 24  # Skip the 24-bit start code
    nal_header = s.read(16)  # read 2 bytes header
    forbidden_zero_bit = nal_header.read(1)
    nal_unit_type = nal_header.read('uint:6')
    # Process the NAL unit based on your criteria
    if nal_unit_type != 0 and nal_unit_type != 1:
        continue
    fspipf = s.read(1)
    sppsi = s.read(1)
    slice_type = s.read('uint:3')
    if slice_type != 2:
        continue
    s.pos = nal_start + 48
    if nal_end:
        nal_data = s.read(nal_end - nal_start - 48)  # Exclude start code and header
    else:
        # Handle the final NAL unit cause the nal_end is none
        nal_data = s[nal_start + 48:]  # use the len of s to determine last bit.

    # Encrypt if nal type is 1. P slice
    # if nal_unit_type == 1:
    sKey = []

    for _ in range(math.ceil(len(nal_data) / 256)):  # Vi mot lan chay light sinh ra 32 byte =256 bit
        sKey.extend(ma2.run())
    # Convert from bitstream to numpy array
    nal_arr = bitStream2NParr(nal_data)
    # Encryption
    res = xor_encrypt_decrypt(nal_arr, sKey)
    # Convert from numpy array to bitstream
    result = NParr2bitStream(res)
    # Overwrite bitstream to s
    s.pos = nal_start + 48  # Skip 3 byte start and 2 byte header
    s.overwrite(result)

    origin.insert(nal_data)
    cipher.insert(result)
ed = time.time()
# with open('encr.bin', 'wb') as file:
#     s.tofile(file)
# with open('origin.bin','wb') as f:
#     origin.tofile(f)
# with open('cipher.bin','wb') as f:
#     cipher.tofile(f)
# Close the bitstream
print("Thoi gian ma hoa: ", f'{ed-st:.3f}')
# Ket luan: Ma hoa bang 3 key khac nhau cho 3 frame de ko bi loi
