import pytest
from brownie import accounts

INITIAL_SUPPLY = 100 * 10 ** 18


@pytest.fixture(scope="session")
def admin():
    return accounts[0]


@pytest.fixture(scope="module")
def gyro_token(admin, GyroToken):
    token = admin.deploy(GyroToken)
    token.initialize(INITIAL_SUPPLY)
    return token
