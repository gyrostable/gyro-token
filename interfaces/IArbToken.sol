// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.9;

interface IArbToken {
    function bridgeMint(address account, uint256 amount) external;

    function bridgeBurn(address account, uint256 amount) external;

    function l1Address() external view returns (address);
}
