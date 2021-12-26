import os
import json

from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")

with open("./SimpleStorage.sol") as f:
    source_code = f.read()

# Compile the source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": source_code}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# Get the necessary information from the compiled contract
with open("compiled_code.json", "w") as f:
    json.dump(compiled_sol, f, indent=4)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect to Ganache
# w3 = Web3(Web3.HTTPProvider("http://{}".format(os.getenv("GANACHE_HOST"))))
# chain_id = 5777
# my_address = os.getenv("ACCOUNT_ADDRESS")
# private_key = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/297e5d4c74d44cec8c6d0e8e7c42e8ce"))
chain_id = 4
my_address = os.getenv("ACCOUNT_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Create Contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build transaction
txn = SimpleStorage.constructor().buildTransaction(
    {
        "from": my_address,
        "chainId": chain_id,
        "gas": 1000000,
        "gasPrice": w3.toWei("10", "gwei"),
        "nonce": nonce,
    }
)

# 2. Sign transaction
signed = w3.eth.account.signTransaction(txn, private_key)

print("Deploying contract...")
# 3. Send transaction
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

# 4. Wait for transaction to be mined
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# 5. Get contract address
contract_address = tx_receipt.contractAddress
print("Contract deployed at: {}".format(contract_address))

# 6. Get contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

# 7. Call contract method
print("\nInitially stored value: {}".format(contract.functions.retrieve().call()))

# Call contract method to store value
print("\nUpdating value to 42...")
store_transaction = contract.functions.store(42).buildTransaction(
    {
        "from": my_address,
        "chainId": chain_id,
        "gas": 1000000,
        "gasPrice": w3.toWei("10", "gwei"),
        "nonce": nonce + 1,
    }
)

# Sign transaction
signed_store_transaction = w3.eth.account.signTransaction(
    store_transaction, private_key
)

# Send transaction
send_store_txn = w3.eth.sendRawTransaction(signed_store_transaction.rawTransaction)
txn_receipt = w3.eth.waitForTransactionReceipt(send_store_txn)
print("Value updated to: {}".format(contract.functions.retrieve().call()))
