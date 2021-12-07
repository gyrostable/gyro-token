// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.9;

interface ICustomToken {
    function registerTokenOnL2(
        address l2CustomTokenAddress,
        uint256 maxSubmissionCostForCustomBridge,
        uint256 maxSubmissionCostForRouter,
        uint256 maxGasForCustomBridge,
        uint256 maxGasForRouter,
        uint256 gasPriceBid,
        uint256 valueForGateway,
        uint256 valueForRouter,
        address creditBackAddress
    ) external payable;

    function isArbitrumEnabled() external view returns (uint8);
}
