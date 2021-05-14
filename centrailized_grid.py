from trainer import Trainer
from time import time

'''
hard code grid of parameters #=8250
'''
LR         = [0.01, 0.005, 0.001, 0.0005, 0.0001]
EPOCHS     = [5,8,10]
BATCH_SIZE = [16,136,256]
LAYERS     = [1,3,5]
WIDTH      = [8,68,128]
# LR         = [0.5, 0.025, 0.01, 0.0075, 0.005, 0.0025, 0.001, 0.00075, 0.0005, 0.00025, 0.0001]
# EPOCHS     = [5,6,7,8,9,10]
# BATCH_SIZE = [16,32,64,128,256]
# LAYERS     = [1,2,3,4,5]
# WIDTH      = [8,16,32,64,128]

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
    recorder = []
    start_t = time()
    training_t = 0
    for i in range(405):
        lr, epoch, batch, layer, width = decoder(i)
        print('Learning Rate : ', lr)
        print('Epochs        : ', epoch)
        print('Batch size    : ', batch)
        print('Layers        : ', layer)
        print('Width         : ', width)
        print("----------------------------------------------------------")
        s = time()
        trainer = Trainer(lr, epochs=epoch, batch_size=batch, n_layers=layer, n_width=width)
        acc = trainer.train()
        recorder.append(acc)
        training_t += time() - s
        print("----------------------------------------------------------")
        print("Acc is " + str(acc) + " !")
        print("----------------------------------------------------------")

    total_t = time() - start_t
    with open('centrallogging.txt', 'w') as f:
        f.write(str(total_t) + '\n')
        f.write(str(training_t) + '\n')
    with open('central.txt', 'w') as f:
        for r in recorder:
            f.write(str(r) + '\n')