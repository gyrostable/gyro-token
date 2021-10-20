import os
from brownie import GyroToken, GyroTokenProxy, ProxyAdmin  # type: ignore

from scripts.utils import get_deployer, with_gas_usage

INITIAL_SUPPLY = 13_700_000 * 10 ** 18
TOKEN_NAME = os.environ.get("TOKEN_NAME")
TOKEN_SYMBOL = os.environ.get("TOKEN_SYMBOL")


@with_gas_usage
def main():
    assert TOKEN_SYMBOL is not None, "TOKEN_SYMBOL env variable is not set"
    assert TOKEN_NAME is not None, "TOKEN_NAME env variable is not set"

    deployer = get_deployer()
    gyro_token = deployer.deploy(GyroToken)

    proxy_admin = deployer.deploy(ProxyAdmin)

    deployer.deploy(
        GyroTokenProxy,
        gyro_token.address,
        proxy_admin.address,
        INITIAL_SUPPLY,
        TOKEN_NAME,  # type: ignore
        TOKEN_SYMBOL,  # type: ignore
    )
