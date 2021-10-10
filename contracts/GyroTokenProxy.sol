// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.9;

import "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";
import {ProxyAdmin as ProxyAdminBase} from "@openzeppelin/contracts/proxy/transparent/ProxyAdmin.sol";

contract GyroTokenProxy is TransparentUpgradeableProxy {
    constructor(
        address logic,
        address admin,
        uint256 initialSupply
    )
        TransparentUpgradeableProxy(
            logic,
            admin,
            abi.encodeWithSignature("initialize(uint256)", initialSupply)
        )
    {}

    /// @notice Set the admin to address(0), which will result in freezing
    /// the implementation of the token
    /// This is a non-reversible action
    function freeze() external ifAdmin {
        emit AdminChanged(_getAdmin(), address(0));
        StorageSlot.getAddressSlot(_ADMIN_SLOT).value = address(0);
    }
}

/// @notice Only used to make ProxyAdmin available in project contracts
contract ProxyAdmin is ProxyAdminBase {

}
