import json
import web3
from web3 import Web3
from solc import compile_standard
from trainer import Trainer
import seaborn as sns

'''
hard code grid of parameters
'''
LR         = [0.1, 0.05, 0.025, 0.01, 0.005, 0.0025, 0.001, 0.0005, 0.00025, 0.0001]
EPOCHS     = [5,6,7,8,9,10]
BATCH_SIZE = [16,32,64,128,256]
LAYERS     = [1,2,3,4,5]
WIDTH      = [8,16,32,64,128]

'''
Example : 777

777 / 10 = 77
777 % 10 =  7  => lr

77  /  5 = 15
77  %  5 =  2  => epoch

15  /  5 =  3
15  %  5 =  0  => batch

3   /  5 =  0
3   %  5 =  3  => layers

0   /  5 =  0
0   %  5 =  0  => width
'''
def decoder(counter):
    q = int(counter / len(LR))
    lr = int(counter % len(LR))
    q1 = int(q / len(EPOCHS))
    epoch = int(q % len(EPOCHS))
    q2 = int(q1 / len(BATCH_SIZE))
    batch_size = int(q1 % len(BATCH_SIZE))
    q3 = int(q2 / len(LAYERS))
    layers = int(q2 % len(LAYERS))
    _ = int(q3 / len(WIDTH))
    width = int(q3 % len(WIDTH))

    return LR[lr], EPOCHS[epoch], BATCH_SIZE[batch_size], LAYERS[layers], WIDTH[width]


if __name__ == "__main__":
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "HP_LR.sol": {
                "content":'''
                    pragma solidity >=0.5.0;

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

    # compile contracy and get the function abi
    bytecode = compiled_sol['contracts']['HP_LR.sol']['HyperParameter_LR']['evm']['bytecode']['object']
    abi = json.loads(compiled_sol['contracts']['HP_LR.sol']['HyperParameter_LR']['metadata'])['output']['abi']

    w3 = Web3(Web3.IPCProvider('./node1/geth.ipc'))
    w3.eth.default_account = w3.eth.accounts[0]
    print(w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899'))

    f = open('LR_SINC.txt', 'r')
    addr = f.readline().strip('\n')
    f.close()

    # initialize the contract

    # Wait for the transaction to be mined, and get the transaction receipt
    # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # print(tx_receipt.contractAddress)

    print('Contract Address : ', addr)

    hp = w3.eth.contract(address=addr, abi=abi)
    results = [hp.functions.get_acc(i).call() for i in range(6250)]


    print(results)

    best = max(results)
    print(best / 100)

    print('failed', results.count(0))
    # while not contract_status:
    #     print("Task has not been completed!")
    #     w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899')
    #     tx_hash = hp.functions.get_parameters().transact()
    #     tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=600)
    #     # print(tx_receipt)

    #     log_to_process = tx_receipt['logs'][0]
    #     processed_log = hp.events.parameter_log().processLog(log_to_process)
    #     counter = processed_log['args']['counter']
    #     print('Number of the parameters : ', counter)
        
    #     lr, epochs, batch_size, layers, width = decoder(counter)
    #     print('Learning Rate : ', lr)
    #     print('Epochs        : ', epochs)
    #     print('Batch size    : ', batch_size)
    #     print('Layers        : ', layers)
    #     print('Width         : ', width)
    #     print("----------------------------------------------------------")
        
    #     # Training process...
    #     t = Trainer(lr, epochs=epochs, batch_size=batch_size, n_layers=layers, n_width=width)
    #     acc = t.train()


    #     # send transaction for set the accuracy to smart contract in block chain
    #     tx_hash = hp.functions.set_accuracy(acc, counter).transact()
    #     print("--Waiting for uploading accuracy transaction be verified--")
    #     # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #     print("----------------------------------------------------------")
    #     print("Upload acc " + str(acc) + " to smart contract, success!")
    #     print("----------------------------------------------------------")
    #     contract_status = hp.functions.end_of_contract().call()

    # print("Task completed!")
