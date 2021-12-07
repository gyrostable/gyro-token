import os
from brownie import GyroTokenArbitrum, GyroArbitrumTokenProxy, ProxyAdmin  # type: ignore

from scripts.utils import MAINNET_DEPLOYER_ADDRESS, get_deployer, with_gas_usage

TOKEN_NAME = os.environ.get("TOKEN_NAME")
TOKEN_SYMBOL = os.environ.get("TOKEN_SYMBOL")
GATEWAY_ADDRESS = "0x096760F208390250649E3e8763348E783AEF5562"
GWEI = 10 ** 9
MAX_FEE = 1 * GWEI


@with_gas_usage
def main():
    assert TOKEN_SYMBOL is not None, "TOKEN_SYMBOL env variable is not set"
    assert TOKEN_NAME is not None, "TOKEN_NAME env variable is not set"

    deployer = get_deployer()
    if len(GyroTokenArbitrum) > 0:
        gyro_token = GyroTokenArbitrum[0]
    else:
        gyro_token = deployer.deploy(GyroTokenArbitrum, gas_price=MAX_FEE)

    proxy_admin = deployer.deploy(ProxyAdmin, gas_price=MAX_FEE)
    proxy_admin.transferOwnership(MAINNET_DEPLOYER_ADDRESS, {"from": deployer})

    deployer.deploy(
        GyroArbitrumTokenProxy,
        gyro_token.address,
        proxy_admin.address,
        TOKEN_NAME,  # type: ignore
        TOKEN_SYMBOL,  # type: ignore
        GATEWAY_ADDRESS,  # type: ignore
        gas_price=MAX_FEE,
    )
