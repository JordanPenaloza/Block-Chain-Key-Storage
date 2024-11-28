// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PaillierPublicKeyStorage {
    // Public key components
    uint256 public n; // Modulus
    uint256 public g; // Generator

    // Final decrypted tally
    uint256 public finalTally; // Stores the final decrypted tally

    // Contract owner
    address public owner;

    // Events
    event PublicKeyStored(uint256 n, uint256 g);
    event FinalTallyUpdated(uint256 finalTally);

    // Modifier to restrict access to the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can call this function");
        _;
    }

    // Constructor to set the owner
    constructor() {
        owner = msg.sender;
    }

    // Function to set the public key
    function setPublicKey(uint256 _n, uint256 _g) public onlyOwner {
        n = _n;
        g = _g;

        // Emit event for transparency
        emit PublicKeyStored(_n, _g);
    }

    // Function to update the final decrypted tally
    function updateFinalTally(uint256 _finalTally) public onlyOwner {
        finalTally = _finalTally;

        // Emit event for transparency
        emit FinalTallyUpdated(_finalTally);
    }

    // Function to retrieve the public key
    function getPublicKey() public view returns (uint256, uint256) {
        return (n, g);
    }

    // Function to retrieve the final tally
    function getFinalTally() public view returns (uint256) {
        return finalTally;
    }
}
