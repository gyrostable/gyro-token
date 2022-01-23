from decimal import Decimal
import pytest

import brownie
import pytest
from brownie import ZERO_ADDRESS, accounts, chain, history

from tests.conftest import INITIAL_SUPPLY

SECONDS_IN_YEAR = 365.25 * 86400
INFLATION_DELAY = 4 * SECONDS_IN_YEAR
INFLATION_RATE = Decimal("0.02")


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_symbol(gyro_token):
    assert gyro_token.symbol() == "GYRTOK"


def test_name(gyro_token):
    assert gyro_token.name() == "Gyro"


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

    chain.sleep(int(5.0 * SECONDS_IN_YEAR))
    chain.mine()

    with brownie.reverts("can only be called by governance"):  # type: ignore
        gyro_token.mint(accounts[1], {"from": accounts[1]})

    tx = gyro_token.mint(accounts[1], {"from": admin})
    created_at = history.of_address(gyro_token)[0].timestamp

    expected_amount_minted = float(INITIAL_SUPPLY * INFLATION_RATE)
    actual_amount_minted = float(gyro_token.balanceOf(accounts[1]))
    transfer_event = tx.events[0]
    total_supply = float(gyro_token.totalSupply())

    # NOTE: could mint a few seconds after the 5 years so
    # cannot check for perfect equality with 2% inflation
    assert actual_amount_minted == pytest.approx(expected_amount_minted)
    assert total_supply == pytest.approx(INITIAL_SUPPLY + expected_amount_minted)
    assert gyro_token.latestInflationTimestamp() == tx.timestamp

    assert transfer_event["from"] == ZERO_ADDRESS
    assert transfer_event["to"] == accounts[1]
    assert float(transfer_event["value"]) == pytest.approx(expected_amount_minted)

    chain.sleep(int(0.9 * SECONDS_IN_YEAR))
    chain.mine()
    gyro_token.mint(accounts[1], {"from": admin})

    chain.sleep(int(0.1 * SECONDS_IN_YEAR))
    chain.mine()
    gyro_token.mint(accounts[1], {"from": admin})

    new_balance = float(gyro_token.balanceOf(accounts[1]))
    new_actual_amount_minted = new_balance - actual_amount_minted
    new_expected_amount_minted = total_supply * float(INFLATION_RATE)

    assert new_actual_amount_minted == pytest.approx(new_expected_amount_minted)

    expected_total_supply_after_8_years = (
        INITIAL_SUPPLY * float(1 + INFLATION_RATE) ** 8
    )

    chain.sleep(int(6 * SECONDS_IN_YEAR))
    chain.mine()
    gyro_token.mint(accounts[1], {"from": admin})

    assert float(gyro_token.totalSupply()) == pytest.approx(
        expected_total_supply_after_8_years
    )
