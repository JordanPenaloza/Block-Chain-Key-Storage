pragma solidity ^0.8.0;

contract KeyStorage {
    uint256[] public keyChunks;

    // Function to store larger key chunks
    function storeKey(uint256[] memory _chunks) public {
        delete keyChunks;
        for (uint i = 0; i < _chunks.length; i++) {
            keyChunks.push(_chunks[i]);
        }
    }

    function getKey() public view returns (uint256[] memory) {
        return keyChunks;
    }
}
