from decimal import Decimal

import brownie
import pytest
from brownie import ZERO_ADDRESS, accounts, chain, history

from tests.conftest import INITIAL_SUPPLY

SECONDS_IN_YEAR = 365 * 86400
INFLATION_RATE = Decimal("0.02")


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_symbol(gyro_token):
    assert gyro_token.symbol() == "GYRO"


def test_name(gyro_token):
    assert gyro_token.name() == "Gyroscope"


def test_initial_supply(gyro_token):
    assert gyro_token.totalSupply() == INITIAL_SUPPLY


def test_initial_governor(gyro_token, admin):
    assert gyro_token.governor() == admin


def test_initial_inflation_rate(gyro_token):
    assert gyro_token.inflationRate() == INFLATION_RATE * 10 ** 18


def test_initial_inflation_interval(gyro_token):
    assert gyro_token.inflationInterval() == SECONDS_IN_YEAR


def test_next_inflation(gyro_token):
    created_at = history.of_address(gyro_token)[0].timestamp
    assert gyro_token.nextInflation() == created_at + SECONDS_IN_YEAR


def test_change_governor(gyro_token, admin):
    gyro_token.changeGovernor(accounts[2], {"from": admin})
    assert gyro_token.governor() == accounts[2]
    with brownie.reverts("can only be called by governance"):  # type: ignore
        gyro_token.changeGovernor(accounts[1], {"from": admin})
    gyro_token.changeGovernor(accounts[1], {"from": accounts[2]})
    assert gyro_token.governor() == accounts[1]


def test_mint(gyro_token, admin):
    with brownie.reverts("cannot mint before inflation is scheduled"):  # type: ignore
        gyro_token.mint(accounts[1], {"from": admin})

    chain.mine(timedelta=SECONDS_IN_YEAR)

    with brownie.reverts("can only be called by governance"):  # type: ignore
        gyro_token.mint(accounts[1], {"from": accounts[1]})

    expected_amount_minted = INITIAL_SUPPLY * INFLATION_RATE

    tx = gyro_token.mint(accounts[1], {"from": admin})
    transfer_event = tx.events[0]

    assert gyro_token.balanceOf(accounts[1]) == expected_amount_minted
    assert gyro_token.totalSupply() == INITIAL_SUPPLY + expected_amount_minted
    assert gyro_token.nextInflation() == tx.timestamp + SECONDS_IN_YEAR

    assert transfer_event["from"] == ZERO_ADDRESS
    assert transfer_event["to"] == accounts[1]
    assert transfer_event["value"] == expected_amount_minted

    with brownie.reverts("cannot mint before inflation is scheduled"):  # type: ignore
        gyro_token.mint(accounts[1], {"from": admin})
