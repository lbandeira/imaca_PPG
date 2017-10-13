import sys
from bitstring import BitArray

f = open("packet.txt", "rb")

while True:
	pkt = f.read(12)
	bitPkt = BitArray(pkt)
	if not pkt:
		break
	print(bitPkt.bin)
