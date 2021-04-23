import json
import web3
from web3 import Web3
from solc import compile_standard
from trainer import Trainer
from time import time

'''
hard code grid of parameters #=8250
'''
LR         = [0.5, 0.025, 0.01, 0.0075, 0.005, 0.0025, 0.001, 0.00075, 0.0005, 0.00025, 0.0001]
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
    q  = int(counter / len(LR))
    lr = int(counter % len(LR))
    q1 = int(q / len(EPOCHS))
    epoch = int(q % len(EPOCHS))
    q2    = int(q1 / len(BATCH_SIZE))
    batch_size = int(q1 % len(BATCH_SIZE))
    q3     = int(q2 / len(LAYERS))
    layers = int(q2 % len(LAYERS))
    _      = int(q3 / len(WIDTH))
    width  = int(q3 % len(WIDTH))

    return LR[lr], EPOCHS[epoch], BATCH_SIZE[batch_size], LAYERS[layers], WIDTH[width]


if __name__ == "__main__":
    w3 = Web3(Web3.IPCProvider('./node1/geth.ipc'))
    w3.eth.default_account = w3.eth.accounts[0]
    print(w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899'))

    start_t = time()
    training_t = 0
    n_tasks = 0

    with open('LR_SINC.txt', 'r') as f:
        addr = f.readline().strip('\n')

    with open('abi.json') as f:
        abi = json.load(f)

    timeout_tx = []

    print('Contract Address : ', addr)
    hp = w3.eth.contract(address=addr, abi=abi)

    while not hp.functions.end_of_contract().call():
        print("Task has not been completed!")
        w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899')
        tx_hash = hp.functions.get_parameters().transact()
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=720)
        except web3.exceptions.TimeExhausted:
            print("Timeout occur and write back tx to timeout list...")
            timeout_tx.append(tx_hash)
            continue
        except:
            pass
        n_tasks += 1

        try:
            log_to_process = tx_receipt['logs'][0]
            processed_log = hp.events.parameter_log().processLog(log_to_process)
            counter = processed_log['args']['counter']
            print('Number of the parameters : ', counter)
            
            lr, epochs, batch_size, layers, width = decoder(counter)
        except:
            continue
        print('Learning Rate : ', lr)
        print('Epochs        : ', epochs)
        print('Batch size    : ', batch_size)
        print('Layers        : ', layers)
        print('Width         : ', width)
        print("----------------------------------------------------------")
        
        s = time()
        # Training process...
        trainer = Trainer(lr, epochs=epochs, batch_size=batch_size, n_layers=layers, n_width=width)
        acc = trainer.train()
        training_t += time() - s

        # send transaction for set the accuracy to smart contract in block chain
        w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899')
        tx_hash = hp.functions.set_accuracy(acc, counter).transact()
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=300)
        except web3.exceptions.TimeExhausted:
            print("Timeout occur in accuracy...")
            pass
        except:
            pass

        print("--Waiting for uploading accuracy transaction be verified--")
        # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print("----------------------------------------------------------")
        print("Upload acc " + str(acc) + " to smart contract, success!")
        print("----------------------------------------------------------")

    print("Task completed!")

    print("Perform the repair process...")
    # reprocess the timeout tx
    for tx in timeout_tx:
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(tx, timeout=100)
        except web3.exceptions.TimeExhausted:
            print('Transaction failed and can not repair.')
            continue
        except:
            pass
        n_tasks += 1
        try:
            log_to_process = tx_receipt['logs'][0]
            processed_log = hp.events.parameter_log().processLog(log_to_process)
            counter = processed_log['args']['counter']
            lr, epochs, batch_size, layers, width = decoder(counter)
        except:
            continue
        print('Learning Rate : ', lr)
        print('Epochs        : ', epochs)
        print('Batch size    : ', batch_size)
        print('Layers        : ', layers)
        print('Width         : ', width)
        print("----------------------------------------------------------")

        s = time()
        # Training process...
        trainer = Trainer(lr, epochs=epochs, batch_size=batch_size, n_layers=layers, n_width=width)
        acc = trainer.train()
        training_t += time() - s

        # send transaction for set the accuracy to smart contract in block chain
        w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899')
        tx_hash = hp.functions.set_accuracy(acc, counter).transact()
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=120)
        except web3.exceptions.TimeExhausted:
            print("Timeout occur in accuracy...")
            pass
        except:
            pass
        print("--Waiting for uploading accuracy transaction be verified--")
        # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print("----------------------------------------------------------")
        print("Upload acc " + str(acc) + " to smart contract, success!")
        print("----------------------------------------------------------")
    print("Repair process end.")

    total_t = time() - start_t
    with open('logging.txt', 'w') as f:
        f.write(str(total_t) + '\n')
        f.write(str(n_tasks) + '\n')
        f.write(str(training_t) + '\n')

    print("Total computation time : ", total_t)
    print("Processed tasks        : ", n_tasks)