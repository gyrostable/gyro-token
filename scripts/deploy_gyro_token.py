from brownie import GyroToken  # type: ignore

from scripts.utils import get_deployer, with_gas_usage

INITIAL_SUPPLY = 1_000_000_000 * 10 ** 18


@with_gas_usage
def main():
    deployer = get_deployer()
    gyro_token = deployer.deploy(GyroToken)
    gyro_token.initialize(INITIAL_SUPPLY, {"from": deployer})
