from brownie import ZERO_ADDRESS, accounts, web3
from brownie import GyroToken, GyroTokenProxy  # type: ignore

from tests.conftest import INITIAL_SUPPLY

ADMIN_SLOT = "0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103"


def test_initialization(gyro_token_proxy, admin):
    current_admin = web3.eth.get_storage_at(gyro_token_proxy.address, ADMIN_SLOT)
    assert current_admin.hex() == admin

    # nasty but needed to avoid ContractExists error on the line after
    GyroTokenProxy.remove(gyro_token_proxy)
    gyro_token = GyroToken.at(gyro_token_proxy.address, owner=accounts[1])

    assert gyro_token.totalSupply() == INITIAL_SUPPLY

    # restore contract containers
    GyroToken.remove(gyro_token_proxy)
    GyroTokenProxy.at(gyro_token_proxy)


def test_freeze(gyro_token_proxy):
    tx = gyro_token_proxy.freeze()
    current_admin = web3.eth.get_storage_at(gyro_token_proxy.address, ADMIN_SLOT)
    assert int.from_bytes(current_admin, byteorder="little") == 0
    assert tx.events["AdminChanged"]["newAdmin"] == ZERO_ADDRESS
