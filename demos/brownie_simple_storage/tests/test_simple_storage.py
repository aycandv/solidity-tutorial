from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]

    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected_value = 0

    # Assert
    assert expected_value == starting_value


def test_updating_value():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})

    # Act
    simple_storage.store(42, {"from": account})

    stored_value = simple_storage.retrieve()
    expected_value = 42

    # Assert
    assert expected_value == stored_value
