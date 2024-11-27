// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PaillierPublicKeyStorage {
    // Public key components
    uint256 public n; // Modulus
    uint256 public g; // Generator

    // Event for logging key storage
    event PublicKeyStored(uint256 n, uint256 g);

    // Function to set the public key (only owner or specific role can call, if needed)
    function setPublicKey(uint256 _n, uint256 _g) public {
        n = _n;
        g = _g;

        // Emit event for transparency
        emit PublicKeyStored(_n, _g);
    }

    // Retrieve the public key (optional, since n and g are public variables)
    function getPublicKey() public view returns (uint256, uint256) {
        return (n, g);
    }
}
