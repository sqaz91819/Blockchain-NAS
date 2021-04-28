import sys
import json
import web3
import random
from web3 import Web3
from solc import compile_standard
from trainer import Trainer
from time import time

pop = 20
LR_max = 1000000
LR_min = 100000
Epoch_max = 10000
Epoch_min = 4000
Batch_max = 64000
Batch_min = 4000
Layer_max = 5000
Layer_min = 1000 
Width_max = 128000
Width_min = 8000
LR_max_v = 45000
LR_min_v = -45000
Epoch_max_v = 500
Epoch_min_v = -500
Batch_max_v = 3000
Batch_min_v = -3000
Layer_max_v = 200
Layer_min_v = -200
Width_max_v = 6000
Width_min_v = -6000
c_max = 40
c_min = 0

def PSO_random_initial_vector_Parameter(arr1,arr2):
    random.seed()
    for i in range(5):
        arr1.append(int(round(random.uniform(c_min,c_max))))
        arr2.append(int(round(random.uniform(c_min,c_max))))
    
def PSO_random_initial(arr) : 
    random.seed()
   
    arr[2] =  int(round(random.uniform(LR_min,LR_max)))
    arr[3] =  int(round(random.uniform(Epoch_min,Epoch_max)))
    arr[4] =  int(round(random.uniform(Batch_min,Batch_max)))
    arr[5] =  int(round(random.uniform(Layer_min,Layer_max)))
    arr[6] =  int(round(random.uniform(Width_min,Width_max)))
 
def PSO_random_initial_vector(arr) : 
    random.seed()
    arr[0] =  int(round(random.uniform(LR_min_v,LR_max_v)))
    arr[1] =  int(round(random.uniform(Epoch_min_v,Epoch_max_v)))
    arr[2] =  int(round(random.uniform(Batch_min_v,Batch_max_v)))
    arr[3] =  int(round(random.uniform(Layer_min_v,Layer_max_v)))
    arr[4] =  int(round(random.uniform(Width_min_v,Width_max_v)))

    







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
        # print(log_to_process)
        
        processed_log = hp.events.Particle().processLog(log_to_process)
        
        counter = processed_log['args']['counter']
        print(counter)
        if counter[1] == 0:
            PSO_random_initial(counter)
            tx_hash = hp.functions.get_Vector(counter[0]).transact()
            try:
                tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=1200)
            
            except web3.exceptions.TimeExhausted:
                print("Timeout occur in GET vector...")
                pass
            log_to_process = tx_receipt['logs'][0]
            processed_log = hp.events.Particle_V().processLog(log_to_process)
            counter_V = processed_log['args']['Vector']
            PSO_random_initial_vector(counter_V)

            tx_hash = hp.functions.set_Vector(counter_V,counter[0]).transact()
            try:
                tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=1200)
            
            except web3.exceptions.TimeExhausted:
                print("Timeout occur in Update Vector...")
                pass
            

        lr = counter[2]
        # lr = processed_log['args']['LR']
        lr = float(lr) / float(10000000)

        epochs = int(round(counter[3]/1000))
        # epochs = processed_log['args']['Epoch']

        batch_size = int(round(counter[4]/1000))
        # batch_size = processed_log['args']['batch']

        layers = int(round(counter[5]/1000))
        # layers = processed_log['args']['Layer']

        width = int(round(counter[6]/1000))
        
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
        print(acc)
        acc = int(acc*10)

        

        training_t += time() - s

        # send transaction for set the accuracy to smart contract in block chain
        w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899')
        tx_hash = hp.functions.set_accuracy(counter,acc, counter[0]).transact()
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
        log_to_process = tx_receipt['logs'][0]
        # print(log_to_process)
        


        
        
        processed_log = hp.events.ACC().processLog(log_to_process)
        
        AA = processed_log['args']['A']
        print(AA)

        tx_hash = hp.functions.Current_ACC().transact()
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=1200)
        
        except web3.exceptions.TimeExhausted:
            print("Timeout occur in GET Current Best...")
            pass
        log_to_process = tx_receipt['logs'][0]
        processed_log = hp.events.CURRENT_BEST_ACC().processLog(log_to_process)
        ALL_BEST = processed_log['args']['BEST_ACC']
        
        
        tx_hash = hp.functions.get_Vector(counter[0]).transact()
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=1200)
        
        except web3.exceptions.TimeExhausted:
            print("Timeout occur in GET vector...")
            pass
        log_to_process = tx_receipt['logs'][0]
        processed_log = hp.events.Particle_V().processLog(log_to_process)
        counter_V = processed_log['args']['Vector']


        
        C1_table = []
        C2_table = []
        PSO_random_initial_vector_Parameter(C1_table,C2_table)
        print(C1_table)
        print(C2_table)
        w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899')   
        tx_hash = hp.functions.set_Vector_Coef(C1_table,C2_table,counter[0]).transact()
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=1200)
        
        except web3.exceptions.TimeExhausted:
            print("Timeout occur in Update Vector Parameter...")
            pass


        with open('record8.txt', 'a') as f2:
            f2.write('Number of the Iteration : '+str(counter[1]) + '\n')
            f2.write('Number of the parameters : '+str(counter[0]) + '\n')
            f2.write('Learning Rate : '+str(lr) + '\n')
            f2.write('Epochs        : '+str(epochs)+ '\n')
            f2.write('Batch size    : '+str(batch_size)+ '\n')
            f2.write('Layers        : '+str(layers)+ '\n')
            f2.write('Width         : '+str(width)+ '\n')
            f2.write('Accuracy      : '+str(acc/1000)+'%'+'\n')
            f2.write('Current Best Accuracy      : '+str(ALL_BEST/1000)+'%'+'\n')
            f2.write('LR Epochs Batch  Layer Width : '+str(counter_V[0])+' '+str(counter_V[1])+' '+str(counter_V[2])+' '+str(counter_V[3])+' '+str(counter_V[4])+'\n')
            f2.write("---------------------------------------------------------"+ '\n')
        f2.close()
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