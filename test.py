from lightphe import LightPHE

cs = LightPHE(algorithm_name="Paillier", key_size=256)
m1 = 17
c1 = cs.encrypt(plaintext = m1)
print(c1.value)