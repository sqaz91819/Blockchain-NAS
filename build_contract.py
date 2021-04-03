import json
import web3
from web3 import Web3
from solc import compile_standard

if __name__ == "__main__":
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "HP_LR.sol": {
                "content":'''
                    pragma solidity >=0.5.0;

                    contract HyperParameter_LR {

                    uint min = 0;
                    uint max = 8249;
                    uint counter = 0;
                    uint[8250] acc;

                    event parameter_log(uint counter);

                    function get_parameters() public {
                        emit parameter_log(counter);
                        if (counter < max) {
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
                    '''
            }
        
        },
        "settings":
            {
                "outputSelection": {
                    "*": {
                        "*": [
                            "metadata", "evm.bytecode"
                            , "evm.bytecode.sourceMap"
                        ]
                    }
                }
            }
    })

    w3 = Web3(Web3.IPCProvider('./node1/geth.ipc'))
    w3.eth.default_account = w3.eth.accounts[0]
    print(w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899'))

    # compile contracy and get the function abi
    bytecode = compiled_sol['contracts']['HP_LR.sol']['HyperParameter_LR']['evm']['bytecode']['object']
    abi = json.loads(compiled_sol['contracts']['HP_LR.sol']['HyperParameter_LR']['metadata'])['output']['abi']
    # initialize the contract
    HP = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = HP.constructor().transact()

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=600)

    print('Contract Address : ', tx_receipt.contractAddress)
    # print('Contract ABI     : ', abi)

    addr = tx_receipt.contractAddress
    hp = w3.eth.contract(address=addr, abi=abi)

    with open('LR_SINC.txt', 'w') as f:
        f.write(str(addr) + '\n')

    with open('abi.json', 'w') as f:
        json.dump(abi, f)