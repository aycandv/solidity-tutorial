from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage[-1]
    stored_value = simple_storage.retrieve()
    print("Stored value: {}".format(stored_value))


def main():
    read_contract()
