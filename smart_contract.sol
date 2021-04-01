pragma solidity ^0.7.0;

contract HyperParameter_LR {

  uint min = 0;
  uint max = 6249;
  uint counter = 0;
  uint[6250] acc;

  event parameter_log(uint counter);

  function get_parameters() public {
      emit parameter_log(counter);
      if (counter <= max) {
        counter = counter + 1;
      }
  }

  function set_accuracy(uint pass_acc, uint index) public {
      acc[index] = pass_acc;
  }

  function end_of_contract() view public returns (bool){
      return counter > max;
  }
  // fucking idiot
  function get_acc(uint index) view public returns(uint) {
    return acc[index];
  }
}