from random import getrandbits
from web3 import Web3

# Parameters for the Ethereum network
provider_url = 'HTTP://127.0.0.1:7545'
contract_address = '0x43Ef4Ab5FABedEE25B481Bf5472f56D90772Ae7a'
account = '0xD269d757021Ee7531f5DD7DE69BFC8F81F9AA1fE'
private_key = '0x9d5e30fe00d1a5f0fefbd4258b97f1818a27c6b3fa6f99d4a8ee106010ba13af'

# Contract ABI
contract_abi = [
	{
		"inputs": [],
		"name": "getKey",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "keyChunks",
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
		"inputs": [
			{
				"internalType": "uint256[]",
				"name": "_chunks",
				"type": "uint256[]"
			}
		],
		"name": "storeKey",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

# Connect to the blockchain
w3 = Web3(Web3.HTTPProvider(provider_url))
contract_address = Web3.to_checksum_address(contract_address)
account = Web3.to_checksum_address(account)
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Function to chunk large keys into uint256 segments
def chunk_key_into_uint256(key_bits):
    key = getrandbits(key_bits)
    key_hex = f"{key:0{key_bits // 4}x}"
    chunk_size = 256
    return [int(key_hex[i:i + chunk_size // 4], 16) for i in range(0, len(key_hex), chunk_size // 4)]

# Specify key sizes 
key_sizes = [2048, 4096, 8192]

for key_bits in key_sizes:
    print(f"\nTesting with {key_bits}-bit key:")
    chunks = chunk_key_into_uint256(key_bits)
    print("Generated key chunks for Solidity storage:", chunks)

    # Prepare and send the transaction to store the key in chunks
    try:
        # Send transaction to store key chunks in the contract
        transaction = contract.functions.storeKey(chunks).transact({
            'from': account,
            'gas': 3000000,
            'gasPrice': w3.to_wei('30', 'gwei')
        })

        # Wait for the transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(transaction)
        print("Transaction mined successfully!")
    except Exception as e:
        print(f"An error occurred while storing the {key_bits}-bit key: {e}")
        continue

    # Retrieve the stored key chunks from the contract to verify
    try:
        # Call the getKey function to retrieve stored chunks
        stored_chunks = contract.functions.getKey().call()
        print("Stored key chunks retrieved from contract:", stored_chunks)

        # Check if the stored chunks match the original chunks
        if stored_chunks == chunks:
            print(f"Success: Stored {key_bits}-bit key chunks match the original key chunks!")
        else:
            print(f"Error: Stored {key_bits}-bit key chunks do not match the original key chunks.")
    except Exception as e:
        print(f"An error occurred while retrieving the {key_bits}-bit key chunks: {e}")
