// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.9;

import "OpenZeppelin/openzeppelin-contracts-upgradeable@4.3.2/contracts/token/ERC20/ERC20Upgradeable.sol";

contract GyroToken is ERC20Upgradeable {
    uint64 constant INITIAL_INFLATION_RATE = 2e16;
    uint64 constant INITIAL_INFLATION_INTERVAL = 365 days;

    /// @notice address of the governance contract
    address public governor;

    /// @notice time of the next inflation
    uint64 public nextInflation;

    /// @notice interval between inflations
    uint64 public inflationInterval;

    /// @notice the percentage of new tokens minted
    uint64 public inflationRate;

    modifier governanceOnly() {
        require(msg.sender == governor, "can only be called by governance");
        _;
    }

    function initialize(uint256 initialSupply) external initializer {
        __ERC20_init("Gyroscope", "GYRO");

        governor = msg.sender;
        inflationInterval = INITIAL_INFLATION_INTERVAL;
        inflationRate = INITIAL_INFLATION_RATE;
        nextInflation = uint64(block.timestamp) + INITIAL_INFLATION_INTERVAL;

        _mint(msg.sender, initialSupply);
    }

    /// @notice mints new tokens to `account` according to the inflation schedule
    /// defined by `inflationRate` and `inflationInterval`
    /// Only governance is allowed to call this function
    function mint(address account) external governanceOnly {
        require(
            block.timestamp >= nextInflation,
            "cannot mint before inflation is scheduled"
        );
        require(account != address(0), "cannot burn to 0 address");

        uint256 amountToMint = (totalSupply() * inflationRate) / 10**decimals();

        nextInflation = uint64(block.timestamp) + inflationInterval;
        _mint(account, amountToMint);
    }
}
