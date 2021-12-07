const ethers = require("ethers");
const { Bridge } = require("arb-ts");

const walletPrivateKey = process.env.PRIVATE_KEY;

const l1Provider = new ethers.providers.JsonRpcProvider(process.env.L1RPC);
const l2Provider = new ethers.providers.JsonRpcProvider(process.env.L2RPC);
const signer = new ethers.Wallet(walletPrivateKey);

const l1Signer = signer.connect(l1Provider);
const l2Signer = signer.connect(l2Provider);

const main = async () => {
  const bridge = await Bridge.init(l1Signer, l2Signer);
  const [submissionPriceWei, _nextUpdateTimestamp] =
    await bridge.l2Bridge.getTxnSubmissionPrice(400);
  console.log(submissionPriceWei.toString());
};

main().then(console.log).catch(console.error);
