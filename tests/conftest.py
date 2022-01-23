import pytest
from brownie import accounts
from brownie.network import gas_price

INITIAL_SUPPLY = 1_000_000 * 10 ** 18


@pytest.fixture(scope="session")
def admin():
    return accounts[0]


@pytest.fixture(scope="module")
def gyro_token_unititialized(admin, GyroTokenL1):
    return admin.deploy(GyroTokenL1)


@pytest.fixture(scope="module")
def gyro_token(gyro_token_unititialized):
    gyro_token_unititialized.initialize(INITIAL_SUPPLY, "Gyro", "GYRTOK")
    return gyro_token_unititialized


@pytest.fixture(scope="module")
def gyro_token_proxy(admin, gyro_token_unititialized, GyroTokenProxy):
    return admin.deploy(
        GyroTokenProxy,
        gyro_token_unititialized,
        admin,
        INITIAL_SUPPLY,
        "Gyro",
        "GYRTOK",
    )


@pytest.fixture(scope="module")
def gyro_token_l1(admin, GyroTokenL1, GyroTokenProxy):
    gyro_token_l1 = admin.deploy(GyroTokenL1)
    proxy = admin.deploy(
        GyroTokenProxy,
        gyro_token_l1,
        admin,
        INITIAL_SUPPLY,
        "Gyro",
        "GYRTOK",
    )
    proxy.changeAdmin(accounts[1], {"from": accounts[0]})
    GyroTokenProxy.remove(proxy)
    return GyroTokenL1.at(proxy.address)


@pytest.fixture(autouse=True, scope="session")
def set_gas_price():
    gas_price("1 gwei")
