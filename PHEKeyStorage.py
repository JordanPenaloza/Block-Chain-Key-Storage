from web3 import Web3
from lightphe import LightPHE

# Connect to local Ethereum blockchain (e.g., Ganache)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Ensure connection is successful
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Ethereum blockchain.")

# Set the default account (use the first account for simplicity)
web3.eth.default_account = web3.eth.accounts[0]

# Contract ABI (replace with your compiled contract's ABI)
contract_abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "n",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "g",
				"type": "uint256"
			}
		],
		"name": "PublicKeyStored",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_n",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_g",
				"type": "uint256"
			}
		],
		"name": "setPublicKey",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "g",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getPublicKey",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "n",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Specify your deployed contract address (replace with your actual contract address)
contract_address = "0xc98423C46ec314f7a038Ab1095a1d2faB86Fa8F5"  # Address of the deployed contract

# Connect to the existing contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Generate Paillier public key using LightPHE
cs = LightPHE(algorithm_name="Paillier", key_size=256)
public_key = cs.cs.keys["public_key"]
n = public_key["n"]
g = public_key["g"]

print(f"Generated public key:\nn: {n}\ng: {g}")

# Store the public key on the blockchain
tx_hash = contract.functions.setPublicKey(n, g).transact()
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print("Public key stored on the blockchain.")

# Retrieve the public key from the blockchain
stored_n, stored_g = contract.functions.getPublicKey().call()
print(f"Retrieved public key from blockchain:\nn: {stored_n}\ng: {stored_g}")

# Verify the stored key matches the generated key
assert n == stored_n and g == stored_g, "Stored key does not match the generated key!"
print("Key verification successful.")
