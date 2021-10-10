from functools import lru_cache, wraps
from typing import cast

from brownie import accounts, network
from brownie.network.account import LocalAccount

DEV_CHAIN_IDS = {1337}


def is_live():
    return network.chain.id not in DEV_CHAIN_IDS


@lru_cache()
def get_deployer():
    if not is_live():
        return accounts[0]
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
