from web3 import Web3
from lightphe import LightPHE


class PaillierBlockchain:
    def __init__(self, blockchain_url, contract_address, abi):
        # Connect to Ethereum blockchain
        self.web3 = Web3(Web3.HTTPProvider(blockchain_url))
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum blockchain.")
        self.web3.eth.default_account = self.web3.eth.accounts[0]
        # Initialize contract
        self.contract = self.web3.eth.contract(address=contract_address, abi=abi)
        print(f"Connected to blockchain at {blockchain_url}")

    def store_public_key(self, n, g):
        """Store the public key on-chain."""
        try:
            tx_hash = self.contract.functions.setPublicKey(n, g).transact()
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print("Public key successfully stored on the blockchain.")
        except Exception as e:
            print(f"Error storing public key: {e}")

    def retrieve_public_key(self):
        """Retrieve the public key from the blockchain."""
        n, g = self.contract.functions.getPublicKey().call()
        print(f"Retrieved public key from blockchain:\nn: {n}\ng: {g}")
        return n, g

    def store_final_tally(self, final_tally):
        """Store the final decrypted tally on-chain."""
        try:
            tx_hash = self.contract.functions.updateFinalTally(final_tally).transact()
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print("Final tally successfully updated on the blockchain.")
        except Exception as e:
            print(f"Error updating final tally: {e}")


class PaillierEncryption:
    def __init__(self, key_size=256):
        # Generate Paillier keys
        self.cs = LightPHE(algorithm_name="Paillier", key_size=key_size)
        self.keys = self.cs.cs.keys
        self.public_key = self.keys["public_key"]
        self.private_key = self.keys["private_key"]

    def display_keys(self):
        """Display the public and private keys."""
        print(f"Generated public key:\nn: {self.public_key['n']}\ng: {self.public_key['g']}")
        print(f"Generated private key (off-chain):\n{self.private_key}")

    def encrypt(self, plaintext):
        """Encrypt a plaintext value."""
        return self.cs.encrypt(plaintext=plaintext)

    def decrypt(self, ciphertext):
        """Decrypt a ciphertext value."""
        return self.cs.decrypt(ciphertext)


def main():
    # Blockchain configuration
    BLOCKCHAIN_URL = "http://127.0.0.1:7545"  # Local Ganache blockchain
    CONTRACT_ADDRESS = "0xC50B3b7398dE3b19D85DBE8215aBe5C163D3b53A"  # Replace with your deployed contract address
    CONTRACT_ABI = [
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
            "anonymous": False,
            "inputs": [
                {"indexed": False, "internalType": "uint256", "name": "finalTally", "type": "uint256"}
            ],
            "name": "FinalTallyUpdated",
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
            "inputs": [
                {"internalType": "uint256", "name": "_finalTally", "type": "uint256"}
            ],
            "name": "updateFinalTally",
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

    # Initialize blockchain and encryption objects
    blockchain = PaillierBlockchain(BLOCKCHAIN_URL, CONTRACT_ADDRESS, CONTRACT_ABI)
    paillier = PaillierEncryption(key_size=256)

    # Step 1: Display and store the public key
    paillier.display_keys()
    blockchain.store_public_key(paillier.public_key["n"], paillier.public_key["g"])

    # Step 2: Perform encrypted computations (e.g., voting simulation)
    initial_vote = 1
    encrypted_tally = paillier.encrypt(plaintext=initial_vote)
    print(f"Initial encrypted tally: {encrypted_tally}")

    votes = [1, 1, 1, 1]  # Example votes
    for vote in votes:
        encrypted_vote = paillier.encrypt(plaintext=vote)
        encrypted_tally += encrypted_vote
        print(f"Encrypted vote added. Current tally: {encrypted_tally}")

    # Step 3: Decrypt final tally and store on-chain
    final_tally = paillier.decrypt(encrypted_tally)
    print(f"Final tally (decrypted): {final_tally}")
    blockchain.store_final_tally(final_tally)


if __name__ == "__main__":
    main()
