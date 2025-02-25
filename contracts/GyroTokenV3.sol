// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.9;

import "./GyroToken.sol";

contract GyroTokenV3 is GyroToken {
    bool internal _inflationReinitialized; // this was used in V2 so the slot here is already set to true
    bool internal _inflationReinitializedV2;

    function reinitializeLatestInflationV2(uint256 launchTime) external {
        require(!_inflationReinitializedV2, "already reinitialized");
        latestInflationTimestamp = uint64(launchTime) + INITIAL_INFLATION_DELAY;
        _inflationReinitializedV2 = true;
    }
}
