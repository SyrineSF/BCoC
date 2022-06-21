from datetime import datetime
from uuid import uuid4
import json
from web3 import Web3
import hashlib
from flask_mail import Mail, Message
from flask import current_app

""" ganache contract setup """
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))
w3.eth.defaultAccount = w3.eth.accounts[0]

abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"created_by","type":"string"},{"internalType":"string","name":"created_at","type":"string"},{"internalType":"string","name":"file_hash","type":"string"},{"internalType":"string","name":"status","type":"string"},{"internalType":"string","name":"description","type":"string"}],"name":"createCase","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"getCase","outputs":[{"internalType":"string","name":"created_by","type":"string"},{"internalType":"string","name":"created_at","type":"string"},{"internalType":"string","name":"file_hash","type":"string"},{"internalType":"string","name":"status","type":"string"},{"internalType":"string","name":"description","type":"string"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[],"name":"getLastCaseIndex","outputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"updated_by","type":"string"},{"internalType":"string","name":"updated_at","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"vote_app","type":"uint256"},{"internalType":"uint256","name":"vote_din","type":"uint256"},{"internalType":"uint256","name":"vote_count","type":"uint256"},{"internalType":"uint256","name":"report_index","type":"uint256"}],"name":"setNewDescriptor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"updated_by","type":"string"},{"internalType":"string","name":"updated_at","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"vote_app","type":"uint256"},{"internalType":"uint256","name":"vote_din","type":"uint256"},{"internalType":"uint256","name":"vote_count","type":"uint256"},{"internalType":"uint256","name":"report_index","type":"uint256"}],"name":"setoldDescriptor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"getLastDesc","outputs":[{"components":[{"internalType":"string","name":"updated_by","type":"string"},{"internalType":"string","name":"updated_at","type":"string"},{"internalType":"string","name":"report_hash","type":"string"},{"internalType":"uint256","name":"vote_app","type":"uint256"},{"internalType":"uint256","name":"vote_din","type":"uint256"},{"internalType":"uint256","name":"vote_count","type":"uint256"},{"internalType":"uint256","name":"report_index","type":"uint256"}],"internalType":"structContract.Desc","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"getLastDescIndex","outputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"x","type":"uint256"}],"name":"getDesc","outputs":[{"components":[{"internalType":"string","name":"updated_by","type":"string"},{"internalType":"string","name":"updated_at","type":"string"},{"internalType":"string","name":"report_hash","type":"string"},{"internalType":"uint256","name":"vote_app","type":"uint256"},{"internalType":"uint256","name":"vote_din","type":"uint256"},{"internalType":"uint256","name":"vote_count","type":"uint256"},{"internalType":"uint256","name":"report_index","type":"uint256"}],"internalType":"structContract.Desc","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"status","type":"string"}],"name":"setStatus","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"denie","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
address = w3.toChecksumAddress("0xB18714B5b444BDdCbC8096D18997bCA6f6892bAB")

contract = w3.eth.contract(address=address, abi=abi)
""" ganache contract setup """


def get_form_to_dict(form):
    dic = {}
    if "_id" not in form:
        dic["_id"] = str(uuid4())
    for key, value in form.items():
        dic[key] = value
    dic["created_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    dic["updated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return dic

def create_case(mongo_file, dic):
    trans = contract.functions.createCase(mongo_file["index"],
                                          dic["created_by"], dic["created_at"],
                                          dic["file_hash"], "closed", dic["description"]
                                          ).transact()
    w3.eth.waitForTransactionReceipt(trans)

def get_case(index):
    trans = contract.functions.getCase(int(index)).call()
    return trans

def update_description(id, dic):
    trans = contract.functions.setNewDescriptor(int(id),
                                          dic["updated_by"], dic["created_at"],
                                          dic["report_hash"], 0, 0, 0, dic["report_index"]
                                          ).transact()
    w3.eth.waitForTransactionReceipt(trans)
    contract.functions.setStatus(int(id), "pending").transact()
    w3.eth.waitForTransactionReceipt(trans)

def update_old_description(id, dic):
    trans = contract.functions.setoldDescriptor(int(id),
                                          dic["updated_by"], dic["created_at"],
                                          dic["report_hash"], 0, 0, 0, dic["report_index"]
                                          ).transact()
    w3.eth.waitForTransactionReceipt(trans)
    contract.functions.setStatus(int(id), "pending").transact()
    w3.eth.waitForTransactionReceipt(trans)

def change_status_approve(id):
    trans = contract.functions.setStatus(int(id), "closed").transact()
    w3.eth.waitForTransactionReceipt(trans)


def change_status_denied(id):
    trans = contract.functions.setStatus(int(id), "reopen").transact()
    w3.eth.waitForTransactionReceipt(trans)

def get_description_index(index):
    trans = contract.functions.getLastDescIndex(index).call()
    return trans    

def get_description(index, cell):
    trans = contract.functions.getDesc(index, cell).call()
    return trans

def approve_vote(id):
    trans = contract.functions.approve(int(id)).transact()
    w3.eth.waitForTransactionReceipt(trans)


def denie_vote(id):
    trans = contract.functions.denie(int(id)).transact()
    w3.eth.waitForTransactionReceipt(trans)

def get_lastDesc(index):
    trans = contract.functions.getLastDesc(int(index)).call()
    return trans

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()


def send_email(subject, message, reciver):
    with current_app.app_context():
        mail = Mail()
        msg = Message(subject, sender = 'hidoussiabdou5@gmail.com', recipients = [reciver])
        msg.body = message
        mail.send(msg)