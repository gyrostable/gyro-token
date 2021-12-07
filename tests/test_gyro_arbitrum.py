import pytest


GATEWAY_ROUTER = "0x72Ce9c846789fdB6fC1f34aC4AD25Dd9ef7031ef"
CUSTOM_GATEWAY = "0xcEe284F754E854890e311e3280b767F80797180d"

DUMMY_L2_ADDRESS = "0xd4Ac800c1A291d3DB5Fa76536A17f2A7DB6bE96b"


@pytest.mark.mainnetFork
def test_register_token_on_l2(gyro_token_l1, accounts):
    gyro_token_l1.setArbitrumAddresses(
        CUSTOM_GATEWAY, GATEWAY_ROUTER, {"from": accounts[0]}
    )
    gyro_token_l1.registerTokenOnL2(
        DUMMY_L2_ADDRESS,  # address l2CustomTokenAddress,
        10 ** 14,  # uint256 maxSubmissionCostForCustomBridge,
        10 ** 14,  # uint256 maxSubmissionCostForRouter,
        500_000,  # uint256 maxGasForCustomBridge,
        500_000,  # uint256 maxGasForRouter,
        80 * 10 ** 9,  # uint256 gasPriceBid,
        0,  # uint256 valueForGateway,
        0,  # uint256 valueForRouter,
        accounts[0],  # address creditBackAddress
        {"from": accounts[0]},
    )
