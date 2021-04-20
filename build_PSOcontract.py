import json
import web3
from web3 import Web3
from solc import compile_standard

if __name__ == "__main__":
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "PSO.sol": {
                "content":'''
                    pragma solidity >= 0.5.2;
                    contract PSO_1 {

                        event Particle(int []counter);
                        event ACC(int []A);
                        int public ALL_Best_LR ;
                        int public ALL_Best_Epoch ;
                        int public ALL_Best_Batch ;
                        int public ALL_Best_Layer ;
                        int public ALL_Best_Width ;
                        int public ALL_Best_Accuracy ;
                        int[] public TEST =  new int[](7);
                        int[] public CHECK =  new int[](10) ;

                        int[] private P_Best_LR =  new int[](10) ;
                        int[] private P_Best_Epoch = new int[](10);
                        int[] private P_Best_Batch = new int[](10);
                        int[] private P_Best_Layer = new int[](10);
                        int[] private P_Best_Width = new int[](10);
                        int[] private P_Best_Accuracy = new int[](10);

                        int[] private LR = new int[](10);
                        int[] private Epoch = new int[](10);
                        int[] private Batch = new int[](10);
                        int[] private Layer = new int[](10);
                        int[] private Width = new int[](10);
                        int[] private Accuracy = new int[](10);
                        
                        int[] private LR_v = new int[](10);
                        int[] private Epoch_v = new int[](10);
                        int[] private Batch_v = new int[](10);
                        int[] private Layer_v = new int[](10);
                        int[] private Width_v = new int[](10);
                        int[] private Accuracy_v = new int[](10);

                        int constant LR_max = 10000;
                        int constant LR_min = 1000;
                        int constant Epoch_max = 100;
                        int constant Epoch_min = 50;
                        int constant Batch_max = 60;
                        int constant Batch_min = 20;
                        int constant Layer_max = 50;
                        int constant Layer_min = 10;
                        int constant Width_max = 60;
                        int constant Width_min = 30;

                        int public ITER = 0;
                        int public counter  = 0; 
                        uint public randNonce = 0;


                        function set_accuracy(int acc,int ind) public {
                            Accuracy[uint(ind)] = acc ;
                            CHECK[uint(ind)] = 1;
                            emit ACC(CHECK);
                        }

                         function end_of_contract() view public returns (bool){
                            return ITER >= 30 ;
                        }

                        function get()  public  {
                            if(ITER == 0 && counter==0)
                            {
                                RANDOM_INI();
                                TEST[0] = counter;
                                TEST[1] = ITER;
                                TEST[2] = LR[uint(counter)];
                                TEST[3] = Epoch[uint(counter)];
                                TEST[4] = Batch[uint(counter)];
                                TEST[5] = Layer[uint(counter)];
                                TEST[6] = Width[uint(counter)];
                                emit Particle(TEST);
                                counter ++;
                            }    
                            else if(ITER < 30)
                            {
                                
                                if(counter == 10 )
                                {
                                    uint  sum = 0;
                                    
                                    for(uint i = 0;i<10;i++)
                                    {
                                        sum += uint(CHECK[i]);
                                    }

                                    if(sum == 10)
                                    {
                                        ITER++;
                                        counter = 0;        
                                        Evaluate();
                                        Update_Velocity();
                                        Update_Position();

                                        for(uint j = 0;j<10;j++)
                                        {
                                            CHECK[j] = 0;
                                        }
                                        TEST[0] = counter;
                                        TEST[1] = ITER;
                                        TEST[2] = LR[uint(counter)];
                                        TEST[3] = Epoch[uint(counter)];
                                        TEST[4] = Batch[uint(counter)];
                                        TEST[5] = Layer[uint(counter)];
                                        TEST[6] = Width[uint(counter)];
                                        emit Particle(TEST);
                                        counter ++;
                                    }
                                    else{
                                        TEST[0] = 0;
                                        TEST[1] = 0;
                                        TEST[2] = 0;
                                        TEST[3] = 0;
                                        TEST[4] = 0;
                                        TEST[5] = 0;
                                        TEST[6] = 0;
                                        emit Particle(TEST);
                                    }
                            
                                }
                                else{
                                    TEST[0] = counter;
                                    TEST[1] = ITER;
                                    TEST[2] = LR[uint(counter)];
                                    TEST[3] = Epoch[uint(counter)];
                                    TEST[4] = Batch[uint(counter)];
                                    TEST[5] = Layer[uint(counter)];
                                    TEST[6] = Width[uint(counter)];
                                    emit Particle(TEST);
                                    counter ++;
                                }

                            }
                            else if(ITER == 30)
                            {
                                TEST[0] = counter;
                                TEST[1] = ITER;
                                TEST[2] = ALL_Best_LR;
                                TEST[3] = ALL_Best_Epoch;
                                TEST[4] = ALL_Best_Batch ;
                                TEST[5] = ALL_Best_Layer;
                                TEST[6] = ALL_Best_Width;
                            }
                            

                        
                    }
                        function RANDOM_INI() public{
                            for(uint i = 0 ; i < 10 ; i++)
                            {
                                //random x 
                                CHECK[i] = 0;

                                LR[i] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%9000)+1000;

                                Epoch[i] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%50)+50;

                                Batch[i] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%40)+20;

                                Layer[i] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%40)+10;

                                Width[i] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))% 30) + 30;



                                //random vector
                                LR_v[i] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%1998)-999;

                                Epoch_v[i] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%10)-5;

                                Batch_v[i] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%8)-4;

                                Layer_v[i] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%8)-4;

                                Width_v[i] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%6)-3;
                            }
                            INRANGE();
                            
                        }
                        function Update_Velocity() public
                        {
  
                            // Defining a function to generate
                            // a random number
                         
                            randNonce++;  
                          
                            for(uint i = 0;i < 10;i++)
                            {
                                int[5] memory w;
                                int[5] memory c1;
                                int[5] memory c2;
                                for(uint j = 0;j < 5;j++)
                                {
                                    if( j==0 )
                                    {
                                        w[j]= 800;
                                        c1[j] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%4000);
                                        c2[j] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%4000);


                                    }
                                    else{
                                        w[j] = 8;
                                        c1[j] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%4000);
                                        c2[j] = int(uint(keccak256(abi.encodePacked(block.timestamp,msg.sender, randNonce)))%4000);
                                    }
                                }

                                LR_v[i] = LR_v[i] * w[0] + c1[0] * (P_Best_LR[i] - LR_v[i] ) + c2[0] * (ALL_Best_LR - LR_v[i]);
                                Epoch_v[i] = Epoch_v[i]*w[1] + c1[1] * (P_Best_LR[i] - Epoch_v[i]) + c2[1] * (ALL_Best_Epoch - Epoch_v[i]);
                                Batch_v[i] = Batch_v[i]*w[2] + c1[2] * (P_Best_Batch[i] - Batch_v[i]) + c2[2] * (ALL_Best_Batch - Batch_v[i]);
                                Layer_v[i] = Layer_v[i]*w[3] + c1[3]*(P_Best_Layer[i] - Layer_v[i]) + c2[3]*(ALL_Best_Layer - Layer_v[i]);
                                Width_v[i] = Width_v[i]*w[4] + c1[4]*(P_Best_Width[i] - Width_v[i]) + c2[4]*(ALL_Best_Width - Width_v[i]);
                            }

                            // Test_random =  mulDiv (uint x, uint y, uint z)

                        }
                        function Update_Position() public
                        {
                            for(uint i = 0;i < 10;i++)
                            {
                                LR[i] = LR[i] + LR_v[i];
                                Epoch[i] = Epoch[i] + Epoch_v[i]; 
                                Batch[i] = Batch[i] + Batch_v[i];
                                Layer[i] = Layer[i] + Layer_v[i];
                                Width[i] = Width[i] + Width_v[i];
                            }
                            INRANGE();
                        }
                        function Evaluate() public
                        {
                            for(uint i = 0;i < 10;i++)
                            {
                                if(Accuracy[i] > P_Best_Accuracy[i])
                                {
                                    P_Best_Accuracy[i] = Accuracy[i];
                                    P_Best_LR[i] = LR[i];
                                    P_Best_Epoch[i] = Epoch[i];
                                    P_Best_Batch[i] = Batch[i];
                                    P_Best_Layer[i] = Layer[i];
                                    P_Best_Width[i] = Width[i];
                                    P_Best_Accuracy[i] = Accuracy[i];

                                    if( P_Best_Accuracy[i] > ALL_Best_Accuracy )
                                    {
                                        ALL_Best_Accuracy = P_Best_Accuracy[i];
                                        ALL_Best_LR = P_Best_LR[i];
                                        ALL_Best_Epoch = P_Best_Epoch[i];
                                        ALL_Best_Batch = P_Best_Batch[i];
                                        ALL_Best_Layer = P_Best_Layer[i];
                                        ALL_Best_Width = P_Best_Width[i];
                                    }
                                }
                            }
                        }
                        function INRANGE() private
                        {
                            for(uint i = 0;i < 10;i++)
                            {
                                if(LR[i] > LR_max )
                                {
                                    LR[i] = LR_max;
                                }
                                else if( LR[i] < LR_min )
                                {               
                                    LR[i] = LR_min;
                                }
                                
                                if(Epoch[i] > Epoch_max)
                                {
                                    Epoch[i] = Epoch_max;
                                }
                                else if (Epoch[i] < Epoch_min)
                                {
                                    Epoch[i] = Epoch_min;
                                }
                                if(Batch[i] > Batch_max)
                                {
                                    Batch[i] = Batch_max;
                                }
                                else if(Batch[i] < Batch_min)
                                {
                                    Batch[i] = Batch_min;
                                }
                                if(Layer[i] > Layer_max)
                                {
                                    Layer[i] = Layer_max;
                                }
                                else if (Layer[i] < Layer_min)
                                {
                                    Layer[i] = Layer_min;
                                }
                                if(Width[i] > Width_max)
                                {
                                    Width[i] = Width_max;
                                }
                                else if(Width[i] < Width_min)
                                {
                                    Width[i] = Width_min;
                                }


                            }
                            
                        }



                        // function mulDiv ()public pure returns (uint)
                        // {  
                            
                        //     uint w = 8000;
                            
                        //     uint c1 = uint8(uint256(keccak256(block.timestamp, block.difficulty))%40000);

                        //     uint c2 = uint8(uint256(keccak256(block.timestamp, block.difficulty))%40000);

                            
                        //     return x * y / z;
                        
                        // }

                        }
                            
                              '''
                            }
                                }
        
        ,
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

    w3 = Web3(Web3.IPCProvider('./tzuchieh_node1/geth.ipc'))
    w3.eth.default_account = w3.eth.accounts[0]
    print(w3.geth.personal.unlock_account(w3.eth.default_account, 'rx0899'))

    # compile contracy and get the function abi
    # bytecode = ""
    bytecode = compiled_sol['contracts']['PSO.sol']['PSO_1']['evm']['bytecode']['object']
    abi = json.loads(compiled_sol['contracts']['PSO.sol']['PSO_1']['metadata'])['output']['abi']
    # with open('PSO_abi.json') as f:
    #     abi = json.load(f)
    # initialize the contract
    HP = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = HP.constructor().transact()

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=600)

    print('Contract Address : ', tx_receipt.contractAddress)
    # print('Contract ABI     : ', abi)

    addr = tx_receipt.contractAddress
    hp = w3.eth.contract(address=addr, abi=abi)

    with open('PSO_SINC.txt', 'w') as f:
        f.write(str(addr) + '\n')

    with open('PSO_abi.json', 'w') as f:
        json.dump(abi, f)