import os
from brownie import GyroToken, GyroTokenProxy, ProxyAdmin  # type: ignore

from scripts.utils import get_deployer, with_gas_usage

INITIAL_SUPPLY = 13_700_000 * 10 ** 18
TOKEN_NAME = os.environ.get("TOKEN_NAME")
TOKEN_SYMBOL = os.environ.get("TOKEN_SYMBOL")
GWEI = 10 ** 9
MAX_FEE = 130 * GWEI


@with_gas_usage
def main():
    assert TOKEN_SYMBOL is not None, "TOKEN_SYMBOL env variable is not set"
    assert TOKEN_NAME is not None, "TOKEN_NAME env variable is not set"

    deployer = get_deployer()
    gyro_token = deployer.deploy(GyroToken, gas_price=MAX_FEE)

    proxy_admin = deployer.deploy(ProxyAdmin, gas_price=MAX_FEE)

    deployer.deploy(
        GyroTokenProxy,
        gyro_token.address,
        proxy_admin.address,
        INITIAL_SUPPLY,
        TOKEN_NAME,  # type: ignore
        TOKEN_SYMBOL,  # type: ignore
        gas_price=MAX_FEE,
    )
