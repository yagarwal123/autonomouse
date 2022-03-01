import numpy as np
with open("0007A0F7C4_1/TTL high millis - 0007A0F7C4_1.csv") as ttl_file:
    ttl_file = np.loadtxt(ttl_file)
print(ttl_file)
TTLarray = list(ttl_file)