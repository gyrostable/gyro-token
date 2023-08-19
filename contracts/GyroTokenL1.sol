// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.9;

import "@openzeppelin/upgradeable/contracts/token/ERC20/ERC20Upgradeable.sol";

import "./GyroToken.sol";
import "../interfaces/ICustomToken.sol";
import "../interfaces/IL1GatewayRouter.sol";
import "../interfaces/IL1CustomGateway.sol";

contract GyroTokenL1 is GyroToken, ICustomToken {
    /// @notice this is used by the Arbitrum bridge registration callback
    bool public shouldRegisterArbitrumGateway;

    /// @notice address of the arbitrum bridge
    address arbitrumBridge;

    /// @notice address of the arbitrum router
    address arbitrumRouter;

    /// @notice returns uint8(`0xa4b1`) == `0xb1` if the contract is enabled on Arbitrum
    /// as per the `ArbitrumEnabledToken` specs
    /// https://github.com/OffchainLabs/arbitrum/blob/master/packages/arb-bridge-peripherals/contracts/tokenbridge/ethereum/ICustomToken.sol#L22
    function isArbitrumEnabled() external view override returns (uint8) {
        require(shouldRegisterArbitrumGateway, "not registered on Arbitrum");
        return 0xb1;
    }

    function setArbitrumAddresses(address _arbitrumBridge, address _arbitrumRouter)
        external
        governanceOnly
    {
        require(
            _arbitrumBridge != address(0) && _arbitrumRouter != address(0),
            "cannot set bridge or router to 0 address"
        );
        arbitrumBridge = _arbitrumBridge;
        arbitrumRouter = _arbitrumRouter;
    }

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
    ) external payable override governanceOnly {
        require(
            arbitrumBridge != address(0) && arbitrumRouter != address(0),
            "arbitrum addresses not initialized"
        );
        require(
            msg.value == (valueForGateway + valueForRouter),
            "msg.value must equal valueForGateway + valueForRouter"
        );

        // we temporarily set `shouldRegisterGateway` to true for the callback in registerTokenToL2 to succeed
        bool prev = shouldRegisterArbitrumGateway;
        shouldRegisterArbitrumGateway = true;

        IL1CustomGateway(arbitrumBridge).registerTokenToL2{value: valueForGateway}(
            l2CustomTokenAddress,
            maxGasForCustomBridge,
            gasPriceBid,
            maxSubmissionCostForCustomBridge,
            creditBackAddress
        );

        IL1GatewayRouter(arbitrumRouter).setGateway{value: valueForRouter}(
            arbitrumBridge,
            maxGasForRouter,
            gasPriceBid,
            maxSubmissionCostForRouter,
            creditBackAddress
        );

        shouldRegisterArbitrumGateway = prev;
    }
}
