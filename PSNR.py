import numpy as np
from math import log10, sqrt
from bitstring import BitStream


def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if (mse == 0):  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 10 * log10(max_pixel / sqrt(mse))
    return psnr

def main():
    ori = BitStream(filename='origin.bin')
    cip = BitStream(filename='cipher.bin')
    ori_np = np.frombuffer(ori.tobytes(), dtype=np.uint8)
    cip_np = np.frombuffer(cip.tobytes(), dtype=np.uint8)
    result = PSNR(ori_np, cip_np)
    print("PSNR=", result)
if __name__ == '__main__':
    main()