// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.9;

import "@openzeppelin/upgradeable/contracts/token/ERC20/ERC20Upgradeable.sol";

import "../interfaces/IArbToken.sol";
import "../interfaces/IL1GatewayRouter.sol";
import "../interfaces/IL1CustomGateway.sol";

contract GyroTokenArbitrum is ERC20Upgradeable, IArbToken {
    address constant L1_ADDRESS = address(0x70c4430f9d98B4184A4ef3E44CE10c320a8B7383);
    address arbitrumGatewayAddress;

    function initialize(
        string calldata name,
        string calldata symbol,
        address _arbitrumGatewayAddress
    ) external initializer {
        require(
            _arbitrumGatewayAddress != address(0),
            "arbitrumGatewayAddress cannot be the zero address"
        );
        __ERC20_init(name, symbol);
        arbitrumGatewayAddress = _arbitrumGatewayAddress;
    }

    modifier onlyGateway() {
        require(
            msg.sender == arbitrumGatewayAddress,
            "only allowed to be called by Arbitrum gateway"
        );
        _;
    }

    function bridgeMint(address account, uint256 amount) external onlyGateway {
        _mint(account, amount);
    }

    function bridgeBurn(address account, uint256 amount) external onlyGateway {
        _burn(account, amount);
    }

    function l1Address() external pure returns (address) {
        return L1_ADDRESS;
    }
}
