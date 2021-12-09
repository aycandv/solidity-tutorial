// SPDX-License-Identifier: MIT 
pragma solidity >=0.6.0 <0.9.0; 

contract SimpleStorage {
    uint256 favoriteNumber;
    struct Person {
        string name;
        uint256 favoriteNumber;
    }
    
    Person[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;
    
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
    // If you read from contract, use view
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }
    
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(Person({name: _name, favoriteNumber: _favoriteNumber}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
