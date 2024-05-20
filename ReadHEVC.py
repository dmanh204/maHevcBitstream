from bitstring import BitStream

# Read the HEVC bitstream file
s = BitStream(filename='encr720x480_5mb.bin')

# Find the NAL unit start codes (0x000001)
nal_units = list(s.findall('0x000001', bytealigned=True))

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
    # Read the actual data (NAL unit payload)
    if nal_unit_type != 0 and nal_unit_type != 1:
        continue
    fspipf = s.read(1)
    sppsi = s.read(1)
    slice_type = s.read('uint:3')
    s.pos = nal_start + 48
    if nal_end:
        nal_data = s.read(nal_end - nal_start - 48)  # Exclude start code and header
    else:
        # Handle the final NAL unit cause the nal_end is none
        nal_data = s[nal_start + 48:]  # use the len of s to determine last bit.

    print('NAL unit type:', nal_unit_type)
    if slice_type == 2:
        print('P slice.')
