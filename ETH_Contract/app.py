import json
from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

print(w3.isConnected())
w3.eth.defaultAccount = w3.eth.accounts[0]

abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"created_by","type":"string"},{"internalType":"string","name":"created_at","type":"string"},{"internalType":"string","name":"file_hash","type":"string"},{"internalType":"string","name":"status","type":"string"}],"name":"createCase","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"updated_by","type":"string"},{"internalType":"string","name":"updated_at","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"vote_app","type":"uint256"},{"internalType":"uint256","name":"vote_din","type":"uint256"},{"internalType":"uint256","name":"vote_count","type":"uint256"}],"name":"setNewDescriptor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"updated_by","type":"string"},{"internalType":"string","name":"updated_at","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"vote_app","type":"uint256"},{"internalType":"uint256","name":"vote_din","type":"uint256"},{"internalType":"uint256","name":"vote_count","type":"uint256"}],"name":"setoldDescriptor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"getLastDesc","outputs":[{"components":[{"internalType":"string","name":"updated_by","type":"string"},{"internalType":"string","name":"updated_at","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"vote_app","type":"uint256"},{"internalType":"uint256","name":"vote_din","type":"uint256"},{"internalType":"uint256","name":"vote_count","type":"uint256"}],"internalType":"structContract.Desc","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"getCase","outputs":[{"internalType":"string","name":"created_by","type":"string"},{"internalType":"string","name":"created_at","type":"string"},{"internalType":"string","name":"file_hash","type":"string"},{"internalType":"string","name":"status","type":"string"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[],"name":"getLastCaseIndex","outputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"stateMutability":"view","type":"function","constant":true}]')
address = w3.toChecksumAddress("0x720719Ca06Cf67Ca06cE81eB2F553a1FAc16aF16")

contract = w3.eth.contract(address=address, abi=abi)



print(contract.functions.getCase(2).call())