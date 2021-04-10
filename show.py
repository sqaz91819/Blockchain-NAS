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
    w3 = Web3(Web3.IPCProvider('./node1/geth.ipc'))
    w3.eth.default_account = w3.eth.accounts[0]
    print(w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899'))

    with open('LR_SINC.txt', 'r') as f:
        addr = f.readline().strip('\n')

    with open('abi.json') as f:
        abi = json.load(f)

    # initialize the contract

    # Wait for the transaction to be mined, and get the transaction receipt

    print('Contract Address : ', addr)

    hp = w3.eth.contract(address=addr, abi=abi)
    results = [hp.functions.get_acc(i).call() for i in range(300)]


    print(results)

    best = max(results)
    print(best / 100)

    print('failed', results.count(0))

