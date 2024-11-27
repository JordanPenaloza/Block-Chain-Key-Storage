from web3 import Web3
from lightphe import LightPHE

# Connect to local Ethereum blockchain (e.g., Ganache)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Ensure connection is successful
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Ethereum blockchain.")

# Set the default account (use the first account for simplicity)
web3.eth.default_account = web3.eth.accounts[0]

# Contract ABI and Address
contract_abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "n", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "g", "type": "uint256"}
        ],
        "name": "PublicKeyStored",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_n", "type": "uint256"},
            {"internalType": "uint256", "name": "_g", "type": "uint256"}
        ],
        "name": "setPublicKey",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getPublicKey",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
contract_address = "0xcf6aC5AFA6b926a336364629FB85Fb933D4EE846"  # Replace with your deployed contract address
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Step 1: Generate Paillier public and private keys using LightPHE
cs = LightPHE(algorithm_name="Paillier", key_size=256)
keys = cs.cs.keys
public_key = keys["public_key"]
private_key = keys["private_key"]

n = public_key["n"]
g = public_key["g"]

# Display the generated public and private keys
print(f"Generated public key:\nn: {n}\ng: {g}")
print(f"Generated private key (off-chain):\n{private_key}")

# Step 2: Store the public key on the blockchain
try:
    tx_hash = contract.functions.setPublicKey(n, g).transact()
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Public key successfully stored on the blockchain.")
except Exception as e:
    print(f"Error storing public key: {e}")

# Step 3: Retrieve and verify the stored public key
stored_n, stored_g = contract.functions.getPublicKey().call()
print(f"Stored public key on blockchain:\nn: {stored_n}\ng: {stored_g}")

# Ensure the keys match
assert n == stored_n and g == stored_g, "Stored public key does not match the generated key!"
print("Public key verification successful.")

# Step 4: Perform encrypted computations (e.g., voting simulation)
# Initialize LightPHE with the stored public key
cs.cs.keys["public_key"] = {"n": stored_n, "g": stored_g}

# Start the tally (e.g., initial vote = 1)
initial_vote = 1
encrypted_tally = cs.encrypt(plaintext=initial_vote)
print(f"Initial encrypted tally: {encrypted_tally}")

# Simulate adding votes (e.g., votes = [1, 1, 1, 1])
votes = [1, 1, 1, 1]
for vote in votes:
    encrypted_vote = cs.encrypt(plaintext=vote)
    encrypted_tally += encrypted_vote  # Homomorphic addition
    print(f"Encrypted vote added. Current tally: {encrypted_tally}")

# Step 5: Decrypt the final tally using the private key (off-chain)
final_tally = cs.decrypt(encrypted_tally)
print(f"Final tally (decrypted): {final_tally}")
