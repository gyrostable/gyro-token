from brownie import GyroToken, GyroTokenProxy, ProxyAdmin  # type: ignore

from scripts.utils import get_deployer, with_gas_usage

INITIAL_SUPPLY = 13_700_000 * 10 ** 18


@with_gas_usage
def main():
    deployer = get_deployer()
    gyro_token = deployer.deploy(GyroToken)

    proxy_admin = deployer.deploy(ProxyAdmin)

    deployer.deploy(
        GyroTokenProxy, gyro_token.address, proxy_admin.address, INITIAL_SUPPLY  # type: ignore
    )
