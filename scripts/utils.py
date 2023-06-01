import os
from functools import lru_cache, wraps
from typing import cast

from brownie import accounts, network
from brownie.network.account import ClefAccount, LocalAccount

DEV_CHAIN_IDS = {1337}
MAINNET_DEPLOYER_ADDRESS = "0x196BC79fEe5dad65Bdc0781955F17B184451Ad36"


def is_live():
    return network.chain.id not in DEV_CHAIN_IDS


def connect_to_clef():
    if not any(isinstance(acc, ClefAccount) for acc in accounts):
        print("Connecting to clef...")
        accounts.connect_to_clef()


def get_clef_account(address: str):
    connect_to_clef()
    matching = [acc for acc in accounts if acc.address == address]
    if not matching:
        raise ValueError(f"could not find account for {address}")
    return cast(LocalAccount, matching[0])


@lru_cache()
def get_deployer():
    if not is_live():
        return accounts[0]
    if network.chain.id == 1:
        return get_clef_account(MAINNET_DEPLOYER_ADDRESS)
    elif network.chain.id == 42161:
        return accounts.add(os.environ["ARBITRUM_PRIVATE_KEY"])
    if network.chain.id == 42:
        return cast(LocalAccount, accounts.load("kovan-master"))
    if network.chain.id == 137:
        return cast(LocalAccount, accounts.load("gyro-deployer"))
    if network.chain.id in {4, 421611}:  # rinkeby or arbitrum rinkeby
        return cast(LocalAccount, accounts.load("rinkeby-master"))
    raise ValueError(f"chain id {network.chain.id} not yet supported")


def with_gas_usage(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        balance = get_deployer().balance()
        result = f(*args, **kwargs)
        gas_used = float(balance - get_deployer().balance()) / 1e18
        print(f"Gas used in deployment: {gas_used:.4f} ETH")
        return result

    return wrapper
