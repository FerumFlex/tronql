// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0 <0.9.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract Market is Ownable {

    // TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
    IERC20 internal usdtToken = IERC20(0xa614f803B6FD780986A42c78Ec9c7f77e6DeD13C);

    struct Plan {
        string name;
        bool active;
        uint amount;
    }

    mapping (string => Plan) private plans;

    event Payed(address sender, string userId, uint amount, string plan);
    event PlanUpdated(string _key, string _name, bool _active, uint _amount);

    function setPlan(string memory _key, string memory _name, bool _active, uint _amount) public onlyOwner {
        plans[_key] = Plan(_name, _active, _amount);
        emit PlanUpdated(_key, _name, _active, _amount);
    }

    function getPlan(string memory _key) public view returns(Plan memory) {
        require(plans[_key].amount != 0, "PLAN SHOULD EXISTS");
        return plans[_key];
    }

    function pay(string memory _key, string memory userId) public {
        require(plans[_key].amount != 0, "PLAN SHOULD EXISTS");
        require(usdtToken.transferFrom(msg.sender, address(this), plans[_key].amount), "SHOULD PAY");
        emit Payed(msg.sender, userId, plans[_key].amount, _key);
    }

    function withdraw(uint amount) public onlyOwner {
        if (amount == 0) {
            amount = usdtToken.balanceOf(address(this));
        }
        usdtToken.transfer(_msgSender(), amount);
    }
}
