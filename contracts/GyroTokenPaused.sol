// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.9;

import "./GyroTokenV3.sol";

contract GyroTokenPaused is GyroTokenV3 {
    function _beforeTokenTransfer(
        address,
        address,
        uint256
    ) internal virtual override {
        revert("token is temporarily paused");
    }
}
