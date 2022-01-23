// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.9;

import "@openzeppelin/upgradeable/contracts/token/ERC20/ERC20Upgradeable.sol";

import "./GyroToken.sol";
import "../libraries/LogExpMath.sol";
import "../interfaces/ICustomToken.sol";
import "../interfaces/IL1GatewayRouter.sol";
import "../interfaces/IL1CustomGateway.sol";

contract GyroTokenL1 is GyroToken, ICustomToken {
    using LogExpMath for uint256;

    /// @notice this is used by the Arbitrum bridge registration callback
    bool public shouldRegisterArbitrumGateway;

    /// @notice address of the arbitrum bridge
    address arbitrumBridge;

    /// @notice address of the arbitrum router
    address arbitrumRouter;

    /// @notice mints new tokens to `account` according to the inflation schedule
    /// defined by `inflationRate` and `inflationInterval`
    /// Only governance is allowed to call this function
    function mint(address account) external virtual governanceOnly {
        require(
            block.timestamp >= latestInflationTimestamp,
            "cannot mint before the first inflation is scheduled"
        );
        require(account != address(0), "cannot mint to 0 address");

        uint256 timeEllapsedSinceLastInflation = block.timestamp - latestInflationTimestamp;
        uint256 exponent = (timeEllapsedSinceLastInflation * ONE) / SECONDS_IN_YEAR;
        uint256 currentSupply = totalSupply();
        uint256 newSupply = (currentSupply * (ONE + inflationRate).pow(exponent)) / ONE;
        uint256 amountToMint = newSupply - currentSupply;

        latestInflationTimestamp = uint64(block.timestamp);
        _mint(account, amountToMint);
    }

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
