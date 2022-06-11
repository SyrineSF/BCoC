const Contract_Migration = artifacts.require("Contract");

module.exports = function (deployer) {
  deployer.deploy(Contract_Migration);
};
