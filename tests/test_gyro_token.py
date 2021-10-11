from decimal import Decimal

import brownie
import pytest
from brownie import ZERO_ADDRESS, accounts, chain, history

from tests.conftest import INITIAL_SUPPLY

SECONDS_IN_YEAR = 365 * 86400
INFLATION_DELAY = 4 * SECONDS_IN_YEAR
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


def test_latest_inflation(gyro_token):
    created_at = history.of_address(gyro_token)[0].timestamp
    assert gyro_token.latestInflationTimestamp() == created_at + INFLATION_DELAY


def test_change_governor(gyro_token, admin):
    gyro_token.changeGovernor(accounts[2], {"from": admin})
    assert gyro_token.governor() == accounts[2]
    with brownie.reverts("can only be called by governance"):  # type: ignore
        gyro_token.changeGovernor(accounts[1], {"from": admin})
    gyro_token.changeGovernor(accounts[1], {"from": accounts[2]})
    assert gyro_token.governor() == accounts[1]


def test_mint(gyro_token, admin):
    with brownie.reverts("cannot mint before the first inflation is scheduled"):  # type: ignore
        gyro_token.mint(accounts[1], {"from": admin})

    chain.mine(timedelta=5 * SECONDS_IN_YEAR)

    with brownie.reverts("can only be called by governance"):  # type: ignore
        gyro_token.mint(accounts[1], {"from": accounts[1]})

    tx = gyro_token.mint(accounts[1], {"from": admin})

    created_at = history.of_address(gyro_token)[0].timestamp
    time_elapsed_since_inflation_start = tx.timestamp - created_at - INFLATION_DELAY
    expected_amount_minted = (
        INITIAL_SUPPLY
        * INFLATION_RATE
        * time_elapsed_since_inflation_start
        // Decimal(SECONDS_IN_YEAR)
    )
    transfer_event = tx.events[0]

    # NOTE: could mint a few seconds after the 5 years so
    # cannot check for perfect equality with 2% inflation
    assert (
        INITIAL_SUPPLY * INFLATION_RATE
        <= gyro_token.balanceOf(accounts[1])
        == expected_amount_minted
        <= INITIAL_SUPPLY * (INFLATION_RATE + Decimal("0.001"))
    )
    assert gyro_token.totalSupply() == INITIAL_SUPPLY + expected_amount_minted
    assert gyro_token.latestInflationTimestamp() == tx.timestamp

    assert transfer_event["from"] == ZERO_ADDRESS
    assert transfer_event["to"] == accounts[1]
    assert transfer_event["value"] == expected_amount_minted

    last_inflation = tx.timestamp
    chain.mine(timedelta=SECONDS_IN_YEAR // 5)

    tx = gyro_token.mint(accounts[1], {"from": admin})

    new_supply = INITIAL_SUPPLY + expected_amount_minted
    time_elapsed_since_inflation = tx.timestamp - last_inflation
    expected_amount_minted = (
        new_supply
        * INFLATION_RATE
        * time_elapsed_since_inflation
        // Decimal(SECONDS_IN_YEAR)
    )
    assert gyro_token.totalSupply() == new_supply + expected_amount_minted
