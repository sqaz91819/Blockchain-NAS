import sys
import json
import web3
from web3 import Web3
from solc import compile_standard
from trainer import Trainer
from time import time

if __name__ == "__main__":
    w3 = Web3(Web3.IPCProvider('./tzuchieh_node1/geth.ipc'))
    w3.eth.default_account = w3.eth.accounts[0]
    print(w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899'))

    start_t = time()
    training_t = 0
    n_tasks = 0

    with open('PSO_SINC.txt', 'r') as f:
        addr = f.readline().strip('\n')

    with open('PSO_abi.json') as f:
        abi = json.load(f)

    timeout_tx = []

    print('Contract Address : ', addr)
    hp = w3.eth.contract(address=addr, abi=abi)

    while True:
        print("Task has not been completed!")
        w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899')
        tx_hash = hp.functions.get().transact()
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=1200)
        except web3.exceptions.TimeExhausted:
            print("Timeout occur and write back tx to timeout list...")
            timeout_tx.append(tx_hash)
            continue
       
        n_tasks += 1
       
        log_to_process = tx_receipt['logs'][0]
        print(log_to_process)
        
        processed_log = hp.events.Particle().processLog(log_to_process)
        
        counter = processed_log['args']['counter']
        print(counter)

        lr = counter[2]
        # lr = processed_log['args']['LR']
        lr = float(lr) / float(100000)

        epochs = int(counter[3]/10)
        # epochs = processed_log['args']['Epoch']

        batch_size = pow(2,int(counter[4]/10))
        # batch_size = processed_log['args']['batch']

        layers = int(counter[5]/10)
        # layers = processed_log['args']['Layer']

        width = pow(2,int(counter[6]/10))
        with open('record.txt', 'a') as f2:
            f2.write('Number of the Iteration : '+str(counter[1]) + '\n')
            f2.write('Number of the parameters : '+str(counter[0]) + '\n')
            f2.write('Learning Rate : '+str(lr) + '\n')
            f2.write('Epochs        : '+str(epochs)+ '\n')
            f2.write('Batch size    : '+str(batch_size)+ '\n')
            f2.write('Layers        : '+str(layers)+ '\n')
            f2.write('Width         : '+str(width)+ '\n')
            f2.write("---------------------------------------------------------"+ '\n')
        f2.close()
        # width = processed_log['args']['Width']
        print('Number of the Iteration : ', counter[1])
        print('Number of the parameters : ', counter[0])
        
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
        acc = int(acc*10000)
        training_t += time() - s

        # send transaction for set the accuracy to smart contract in block chain
        w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899')
        tx_hash = hp.functions.set_accuracy(acc, counter[0]).transact()
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=1200)
        except web3.exceptions.TimeExhausted:
            print("Timeout occur in accuracy...")
            pass

        print("--Waiting for uploading accuracy transaction be verified--")
        # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print("----------------------------------------------------------")
        print("Upload acc " + str(acc) + " to smart contract, success!")
        print("----------------------------------------------------------")

    print("Task completed!")

    # print("Perform the repair process...")
    # # reprocess the timeout tx
    # for tx in timeout_tx:
    #     try:
    #         tx_receipt = w3.eth.waitForTransactionReceipt(tx, timeout=100)
    #     except web3.exceptions.TimeExhausted:
    #         print('Transaction failed and can not repair.')
    #         continue
    #     n_tasks += 1
    #     log_to_process = tx_receipt['logs'][0]
    #     processed_log = hp.events.parameter_log().processLog(log_to_process)
    #     counter = processed_log['args']['counter']
    #     lr, epochs, batch_size, layers, width = decoder(counter)
    #     print('Learning Rate : ', lr)
    #     print('Epochs        : ', epochs)
    #     print('Batch size    : ', batch_size)
    #     print('Layers        : ', layers)
    #     print('Width         : ', width)
    #     print("----------------------------------------------------------")

    #     s = time()
    #     # Training process...
    #     trainer = Trainer(lr, epochs=epochs, batch_size=batch_size, n_layers=layers, n_width=width)
    #     acc = trainer.train()
    #     training_t += time() - s

    #     # send transaction for set the accuracy to smart contract in block chain
    #     w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899')
    #     tx_hash = hp.functions.set_accuracy(acc, counter).transact()
    #     try:
    #         tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=80)
    #     except web3.exceptions.TimeExhausted:
    #         print("Timeout occur in accuracy...")
    #         pass
    #     print("--Waiting for uploading accuracy transaction be verified--")
    #     # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #     print("----------------------------------------------------------")
    #     print("Upload acc " + str(acc) + " to smart contract, success!")
    #     print("----------------------------------------------------------")
    # print("Repair process end.")

    total_t = time() - start_t
    with open('logging.txt', 'w') as f:
        f.write(str(total_t) + '\n')
        f.write(str(n_tasks) + '\n')
        f.write(str(training_t) + '\n')

    print("Total computation time : ", total_t)
    print("Processed tasks        : ", n_tasks)