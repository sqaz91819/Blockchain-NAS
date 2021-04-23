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
                        uint public pop = 25;
                        uint public ITERATION = 10;

                        event Particle(int []counter);
                        event ACC(int []A);
                        event Particle_V(int []Vector);
                        event CURRENT_BEST_ACC(int BEST_ACC);
                        int public ALL_Best_LR ;
                        int public ALL_Best_Epoch ;
                        int public ALL_Best_Batch ;
                        int public ALL_Best_Layer ;
                        int public ALL_Best_Width ;
                        int public ALL_Best_Accuracy ;
                        int[] public TEST =  new int[](7);
                        int[] public TEST_V =  new int[](5);
                        int[] public CHECK =  new int[](pop) ;

                        int[] private P_Best_LR =  new int[](pop) ;
                        int[] private P_Best_Epoch = new int[](pop);
                        int[] private P_Best_Batch = new int[](pop);
                        int[] private P_Best_Layer = new int[](pop);
                        int[] private P_Best_Width = new int[](pop);
                        int[] private P_Best_Accuracy = new int[](pop);

                        int[] private LR = new int[](pop);
                        int[] private Epoch = new int[](pop);
                        int[] private Batch = new int[](pop);
                        int[] private Layer = new int[](pop);
                        int[] private Width = new int[](pop);
                        int[] public Accuracy = new int[](pop);
                        
                        int[] private LR_v = new int[](pop);
                        int[] private Epoch_v = new int[](pop);
                        int[] private Batch_v = new int[](pop);
                        int[] private Layer_v = new int[](pop);
                        int[] private Width_v = new int[](pop);

                        int constant LR_max = 5000000;
                        int constant LR_min = 100000;
                        int constant Epoch_max = 10000;
                        int constant Epoch_min = 5000;
                        int constant Batch_max = 8000;
                        int constant Batch_min = 4000;
                        int constant Layer_max = 5000;
                        int constant Layer_min = 1000; 
                        int constant Width_max = 7000;
                        int constant Width_min = 3000;

                        int public ITER = 0;
                        int public counter  = 0; 
                        uint public randNonce = 0;
                        uint public randNonce1 = 0;


                        function Current_ACC() public {
                            
                            emit CURRENT_BEST_ACC(ALL_Best_Accuracy);
                        }

                        function set_accuracy(int acc,int ind) public {
                            Accuracy[uint(ind)] = acc ;
                            CHECK[uint(ind)] = 1;
                            emit ACC(CHECK);
                        }

                         function end_of_contract() view public returns (bool){
                            return ITER > int(ITERATION) ;
                        }
                        function get_Vector(int counter) public{
                            
                            TEST_V[0] = LR_v[uint(counter)];
                            TEST_V[1] = Epoch_v[uint(counter)];
                            TEST_V[2] = Batch_v[uint(counter)];
                            TEST_V[3] = Layer_v[uint(counter)];
                            TEST_V[4] = Width_v[uint(counter)];

                            return Particle_V(TEST_V);
                        }
                        function get()  public  {
                            if(ITER == 0 && counter==0)
                            {
                                RANDOM_INI();
                                RANDOM_VECTOR() ;
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
                            else if(ITER < int(ITERATION))
                            {
                                
                                if(counter == int(pop) )
                                {
                                    uint  sum = 0;
                                    
                                    for(uint i = 0;i<pop;i++)
                                    {
                                        sum += uint(CHECK[i]);
                                    }

                                    if(sum == pop)
                                    {
                                        ITER++;
                                        counter = 0;        
                                        Evaluate();
                                        Update_Velocity();
                                        Update_Position();

                                        for(uint j = 0;j<pop;j++)
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
                                        TEST[0] = -1;
                                        TEST[1] = -1;
                                        TEST[2] = -1;
                                        TEST[3] = -1;
                                        TEST[4] = -1;
                                        TEST[5] = -1;
                                        TEST[6] = -1;
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
                            else if(ITER == int(ITERATION))
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
                            for(uint i = 0 ; i < pop ; i++)
                            {
                                //random x 
                                randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    
                                
                                CHECK[i] = 0;

                                LR[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%900000)+100000;

                                randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    

                                Epoch[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%5000)+5000;

                                randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    

                                Batch[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%4000)+2000;

                                randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    

                                Layer[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%4000)+1000;

                                randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    

                                Width[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))% 3000) + 3000;



                             
                            }
                            INRANGE();
                            
                        }
                        function RANDOM_VECTOR() public{
                            for(uint i=0;i<pop;i++)
                            {

                                randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;     
                                randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender)))%7) ;  
                                    //random vector
                                LR_v[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce,randNonce1)))%90000)-45000;

                                randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    
                                randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender)))%7) ; 

                                Epoch_v[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce,randNonce1)))%500)-250;

                                randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    
                                randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender)))%7) ; 

                                Batch_v[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce,randNonce1)))%400)-200;

                                randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    
                                randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender)))%7) ; 

                                Layer_v[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce,randNonce1)))%400)-200;

                                randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    
                                randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender)))%7) ; 

                                Width_v[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce,randNonce1)))%300)-150;
                            }
                        }
                        function Update_Velocity() public
                        {
  
                            // Defining a function to generate
                            // a random number
                         
                            randNonce+=10;  
                          
                            for(uint i = 0;i < pop;i++)
                            {
                                int[5] memory w;
                                int[5] memory c1;
                                int[5] memory c2;
                                for(uint j = 0;j < 5;j++)
                                {
                                    if( j==0 )
                                    {
                                        w[j]= 7;

                                        randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    
                                        randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%7) ; 

                                        c1[j] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%300);

                                        //c1[j] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%4);
                                                                                                                        
                                        randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    
                                        randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%7) ; 


                                        c2[j] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%400);


                                    }
                                    else{
                                        w[j] = 7;

                                        randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    
                                        randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%7) ; 

                                        c1[j] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%300);

                                        randNonce = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%50) ;    
                                        randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%7) ; 

                                        c2[j] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp,msg.sender, randNonce)))%400);
                                    }
                                }

                                LR_v[i] = LR_v[i] * w[0] + c1[0] * (P_Best_LR[i] - LR_v[i] ) /100 + c2[0] * (ALL_Best_LR - LR_v[i]) /100;
                                Epoch_v[i] = Epoch_v[i]*w[1] + c1[1] * (P_Best_LR[i] - Epoch_v[i]) /100  + c2[1] * (ALL_Best_Epoch - Epoch_v[i])/100 ;
                                Batch_v[i] = Batch_v[i]*w[2] + c1[2] * (P_Best_Batch[i] - Batch_v[i])/100  + c2[2] * (ALL_Best_Batch - Batch_v[i])/100 ;
                                Layer_v[i] = Layer_v[i]*w[3] + c1[3]*(P_Best_Layer[i] - Layer_v[i]) /100 + c2[3]*(ALL_Best_Layer - Layer_v[i])/100 ;
                                Width_v[i] = Width_v[i]*w[4] + c1[4]*(P_Best_Width[i] - Width_v[i]) /100 + c2[4]*(ALL_Best_Width - Width_v[i])/100 ;
                            }


                        }
                        function Update_Position() public
                        {
                            for(uint i = 0;i < pop;i++)
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
                            for(uint i = 0;i < pop;i++)
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
                            for(uint i = 0;i < pop;i++)
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

    w3 = Web3(Web3.IPCProvider('./node1/geth.ipc'))
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