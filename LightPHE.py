from lightphe import LightPHE

cs = LightPHE(algorithm_name = "Paillier")
print(cs.cs.keys)
m1 = 3
m2 = 2
c1 = cs.encrypt(plaintext = m1)
c2 = cs.encrypt(plaintext = m2)
assert cs.decrypt(c1) == m1
assert cs.decrypt(c2) == m2
print(cs.decrypt(c1 + c2))