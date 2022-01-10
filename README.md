# Gyroscope governance token

This repository hosts the code for the Gyroscope governance token.

The token will be upgradeable to start with and will be frozen when the final
decisions on its designed are made.
The token will have a 2% inflation per year, started after the fourth year.


## Development

This project uses [brownie](https://eth-brownie.readthedocs.io/en/stable/) for building and testing.
Once brownie is installed, it can be built and tested using

```
brownie compile
# Unit tests
brownie test -m "not mainnetFork"
# Integration tests
brownie test -m "mainnetFork" --network mainnet-fork
```

Note that you will need to have the `WEB3_INFURA_PROJECT_ID` environment variable to be set for the integration tests.
