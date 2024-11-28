import json
from seal import *
from web3 import Web3

def generate_and_print_public_key():
    # Set encryption parameters
    parms = EncryptionParameters(scheme_type.bgv)
    poly_modulus_degree = 1024
    parms.set_poly_modulus_degree(poly_modulus_degree)
    parms.set_coeff_modulus(CoeffModulus.BFVDefault(poly_modulus_degree))
    parms.set_plain_modulus(PlainModulus.Batching(poly_modulus_degree, 20))

    # Create SEALContext
    context = SEALContext(parms)

    # Generate keys
    keygen = KeyGenerator(context)
    public_key = keygen.create_public_key()

    # Save public key to a file
    public_key_file = "public_key.seal"
    public_key.save(public_key_file)

    # Read and return serialized public key
    with open(public_key_file, "rb") as f:
        public_key_data = f.read()
        return public_key_data


def chunk_data_to_uint256(data):
    """Chunk byte data into uint256-sized integers."""
    chunks = []
    for i in range(0, len(data), 32):  # 32 bytes = 256 bits
        chunk = data[i:i + 32]
        chunks.append(int.from_bytes(chunk, "big"))
    return chunks


def store_key(contract, public_key_chunks, account):
    # Store public key chunks in the deployed contract
    tx_hash = contract.functions.storePublicKey(public_key_chunks).transact({"from": account})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Public key successfully stored on the blockchain.")


def retrieve_and_verify_key(contract, original_key):
    # Retrieve the key chunks
    chunks = contract.functions.getPublicKey().call()
    reconstructed_key = b"".join(chunk.to_bytes(32, "big") for chunk in chunks)

    # Verify if the original and reconstructed keys match
    if reconstructed_key == original_key:
        print("Public key verification successful!")
    else:
        print("Public key verification failed!")


if __name__ == "__main__":
    # Blockchain connection setup
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Update with your blockchain provider
    web3.eth.default_account = web3.eth.accounts[0]  # Replace with your account

    # Contract details
    contract_address = "0xFd7257cc8eA0e55842AE00e0cFE64a919276BF09"  # Replace with your deployed contract address
    contract_abi = [
	{
		"inputs": [
			{
				"internalType": "uint256[]",
				"name": "chunks",
				"type": "uint256[]"
			}
		],
		"name": "storePublicKey",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getPublicKey",
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
		"name": "publicKeyChunks",
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

    # Create a contract instance
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Generate public key
    serialized_key = generate_and_print_public_key()

    # Chunk data for Solidity
    public_key_chunks = chunk_data_to_uint256(serialized_key)

    # Store key in contract
    store_key(contract, public_key_chunks, web3.eth.default_account)

    # Retrieve and verify key
    retrieve_and_verify_key(contract, serialized_key)
