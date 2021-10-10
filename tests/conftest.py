import pytest
from brownie import accounts

INITIAL_SUPPLY = 1_000_000 * 10 ** 18


@pytest.fixture(scope="session")
def admin():
    return accounts[0]


@pytest.fixture(scope="module")
def gyro_token_unititialized(admin, GyroToken):
    return admin.deploy(GyroToken)


@pytest.fixture(scope="module")
def gyro_token(gyro_token_unititialized):
    gyro_token_unititialized.initialize(INITIAL_SUPPLY)
    return gyro_token_unititialized


@pytest.fixture(scope="module")
def gyro_token_proxy(admin, gyro_token_unititialized, GyroTokenProxy):
    return admin.deploy(GyroTokenProxy, gyro_token_unititialized, admin, INITIAL_SUPPLY)
