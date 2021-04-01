import json
import web3
from web3 import Web3
from solc import compile_standard
from trainer import Trainer

if __name__ == "__main__":
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "HP_LR.sol": {
                "content":'''
                    pragma solidity >=0.5.0;
                    contract HyperParameter_LR {
                        uint lr_min = 1;
                        uint lr_max = 1000;
                        uint cur_lr = 1;
                        uint[] acc;

                        function get_parameters() view public returns (uint){
                            if (cur_lr <= lr_max) {
                                return cur_lr;
                            }
                            return 0;
                        }

                        function set_parameter() public{
                            cur_lr = cur_lr + 1;
                        }

                        function set_accuracy(uint pass_acc) public {
                            acc.push(pass_acc);
                        }

                        function end_of_contract() view public returns (bool){
                            return cur_lr > 1000;
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

    w3 = Web3(Web3.IPCProvider('./new_node/geth.ipc'))
    w3.eth.default_account = w3.eth.accounts[0]
    print(w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899'))

    bytecode = compiled_sol['contracts']['HP_LR.sol']['HyperParameter_LR']['evm']['bytecode']['object']

    abi = json.loads(compiled_sol['contracts']['HP_LR.sol']['HyperParameter_LR']['metadata'])['output']['abi']

    # HP = w3.eth.contract(abi=abi, bytecode=bytecode)

    # tx_hash = HP.constructor().transact()

    # # Wait for the transaction to be mined, and get the transaction receipt
    # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # print(tx_receipt.contractAddress)
    # exit()

    addr = '0xA85bAb39dA54027a14E8407EA7E3365e0a85226b'
    print(addr)

    hp = w3.eth.contract(address=addr, abi=abi)

    contract_status = hp.functions.end_of_contract().call()
    if not contract_status:
        print("Task has not been completed!")
        lr = hp.functions.get_parameters().call()
        print("Get learning rate from smart contracy : ", lr)

        lr = float(lr) / 10000.0
        
        tx_hash = hp.functions.set_parameter().transact()
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)

        # Training process...
        t = Trainer(lr)
        acc = t.train()


        # send transaction for set the accuracy to smart contract in block chain
        tx_hash = hp.functions.set_accuracy(acc).transact()
        print("--Waiting for uploading accuracy transaction be verified--")
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print("----------------------------------------------------------")
        print("Upload acc " + str(acc) + " to smart contract, success!")
        print("----------------------------------------------------------")
    else:
        print("Task completed!")
