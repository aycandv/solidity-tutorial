from brownie import accounts, config, network, SimpleStorage


def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})

    stored_value = simple_storage.retrieve()
    print("Stored value: {}".format(stored_value))

    txn = simple_storage.store(42, {"from": account})
    txn.wait(1)

    stored_value = simple_storage.retrieve()
    print("Stored value: {}".format(stored_value))

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()


if __name__ == "__main__":
    main()
