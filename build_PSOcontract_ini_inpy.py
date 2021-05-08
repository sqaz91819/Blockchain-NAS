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
                        uint public pop = 20;
                        uint public ITERATION = 20;
                        uint public Parameter = 5;

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

                        int constant LR_max = 100000;
                        int constant LR_min = 1000;
                        int constant Epoch_max = 10000;
                        int constant Epoch_min = 4000;
                        int constant Batch_max = 64000;
                        int constant Batch_min = 4000;
                        int constant Layer_max = 5000;
                        int constant Layer_min = 1000; 
                        int constant Width_max = 128000;
                        int constant Width_min = 8000;

                        int constant LR_max_v = 1237;
                        int constant LR_min_v = -1237;
                        int constant Epoch_max_v = 125;
                        int constant Epoch_min_v = -125;
                        int constant Batch_max_v = 750;
                        int constant Batch_min_v = -750;
                        int constant Layer_max_v = 50;
                        int constant Layer_min_v = -50; 
                        int constant Width_max_v = 1500;
                        int constant Width_min_v = -1500;

                      
                        int[] private c1 = new int[](pop*Parameter);
                        int[] private c2 = new int[](pop*Parameter);

                        int public ITER = 0;
                        int public counter  = 0; 
                        uint public randNonce = 0;
                        uint public randNonce1 = 0;


                        function Current_ACC() public {
                            
                            emit CURRENT_BEST_ACC(ALL_Best_Accuracy);
                        }

                        function set_accuracy(int [] memory Coef,int acc ,int ind) public {
                           
                            LR[uint(ind)] = Coef[2];
                            Epoch[uint(ind)] =Coef[3] ;
                            Batch[uint(ind)] = Coef[4];
                            Layer[uint(ind)] = Coef[5];
                            Width[uint(ind)] = Coef[6];
                            Accuracy[uint(ind)] = acc ;
                            CHECK[uint(ind)] = 1;
                            emit ACC(CHECK);
                            
                        }
                        function set_Vector(int [] memory Coef,int ind) public {
                            LR_v[uint(ind)] = Coef[0];
                            Epoch_v[uint(ind)] = Coef[1];
                            Batch_v[uint(ind)] = Coef[2];
                            Layer_v[uint(ind)] = Coef[3];
                            Width_v[uint(ind)] = Coef[4];
                            
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
                        function set_Vector_Coef(int [] memory FIRST,int [] memory SECOND,int counter) public{
                            
                            
                            uint j =uint(counter)*(Parameter);
                            for(uint i=0;i<5;i++)
                            {
                                
                                c1[j] = FIRST[i] ;
                                c2[j] = SECOND[i];
                                j++;
                            }
                            
                        }
                        function get()  public  {
                            if(ITER == 0 && counter==0)
                            {
                                //RANDOM_INI();
                                //RANDOM_VECTOR() ;
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

                                       
                                        TEST[0] = counter;
                                        TEST[1] = ITER;
                                        TEST[2] = LR[uint(counter)];
                                        TEST[3] = Epoch[uint(counter)];
                                        TEST[4] = Batch[uint(counter)];
                                        TEST[5] = Layer[uint(counter)];
                                        TEST[6] = Width[uint(counter)];
                                        emit Particle(TEST);
                                        for(uint j = 0;j<pop;j++)
                                        {
                                            CHECK[j] = 0;
                                        }
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
                                randNonce += uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp, randNonce)))%50) ;    
                                //randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp)))%7) ;  

                                CHECK[i] = 0;

                                LR[i] = int(uint(keccak256(abi.encodePacked(block.timestamp, randNonce)))% (uint(LR_max-LR_min)))+LR_min;

                                randNonce += uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp, randNonce)))%1052) ;    
                                //randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp)))%7) ;  

                                Epoch[i] = int( uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp, randNonce)))% (uint(Epoch_max-Epoch_min)) )+Epoch_min;


                                randNonce += uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp, randNonce)))%31) ;    
                                //randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp)))%7) ;  

                                Batch[i] = int(uint(keccak256(abi.encodePacked(block.timestamp, randNonce)))%(uint(Batch_max-Batch_min)))+Batch_min;

       

                                randNonce += uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp, randNonce)))%890) ;    
                                //randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp)))%7) ;  

                                Layer[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp, randNonce)))%(uint(Layer_max-Layer_min)))+Layer_min;

                                randNonce += uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp, randNonce)))%87) ;    
                               // randNonce1 = uint(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp)))%7) ;  

                                Width[i] = int(uint(keccak256(abi.encodePacked(block.difficulty,block.timestamp, randNonce)))% (uint(Width_max-Width_min)) )+ Width_min;




                             
                            }
                            INRANGE();
                            
                        }
                        function Vector_In_Range() private{
                            for(uint i=0;i<pop;i++)
                            {
                                if(LR_v[i] > LR_max_v)
                                {
                                    LR_v[i] = LR_max_v;
                                }
                                else if (LR_v[i] < LR_min_v)
                                {
                                    LR_v[i] = LR_min_v;
                                }
                                if(Epoch_v[i] > Epoch_max_v)
                                {
                                    Epoch_v[i] = Epoch_max_v;
                                }
                                else if (Epoch_v[i] <  Epoch_min_v)
                                {
                                    Epoch_v[i] = Epoch_min_v;
                                }

                                if(Batch_v[i] > Batch_max_v)
                                {
                                    Batch_v[i] = Batch_max_v;
                                }
                                else if (Batch_v[i] < Batch_min_v)
                                {
                                    Batch_v[i] = Batch_min_v;
                                }

                                if(Layer_v[i] > Layer_max_v)
                                {
                                    Layer_v[i] = Layer_max_v;

                                }
                                else if (Layer_v[i] < Layer_min_v)
                                {
                                    Layer_v[i] = Layer_min_v;
                                }

                                if(Width_v[i] > Width_max_v)
                                {
                                    Width_v[i] = Width_max_v;
                                }
                                else if (Width_v[i] < Width_min_v)
                                {
                                    Width_v[i] = Width_min_v;
                                }
                            }   
                        }
                        function Update_Velocity() public
                        {
  
                            // Defining a function to generate
                            // a random number
                         
                          
                            for(uint i = 0;i < pop;i++)
                            {
                                int w = 2;
                               

                                LR_v[i] = LR_v[i] * w /int(1000) + int(c1[(i*Parameter)+0]) * (int(P_Best_LR[i]) - int(LR_v[i])) /int(1000) + int(c2[(i*Parameter)+0]) * (int(ALL_Best_LR) - int(LR_v[i])) /int(1000);
                                Epoch_v[i] = Epoch_v[i]*w/int(1000) + int(c1[(i*Parameter)+1])* (int(P_Best_Epoch[i]) - int(Epoch_v[i])) / int(1000) + int(c2[(i*Parameter)+1]) * (int(ALL_Best_Epoch) - int(Epoch_v[i]) )/int(1000) ;
                                Batch_v[i] = Batch_v[i]*w/int(1000) + int(c1[(i*Parameter)+2]) * (int(P_Best_Batch[i]) - int(Batch_v[i]) )/int(1000)  + int(c2[(i*Parameter)+2]) * (int(ALL_Best_Batch) - int(Batch_v[i]) )/int(1000) ;
                                Layer_v[i] = Layer_v[i]*w/int(1000) + int(c1[(i*Parameter)+3]) * (int(P_Best_Layer[i]) - int(Layer_v[i]) ) /int(1000) + int(c2[(i*Parameter)+3]) *(int(ALL_Best_Layer) - int(Layer_v[i]) )/int(1000) ;
                                Width_v[i] = Width_v[i]*w/int(1000) + int(c1[(i*Parameter)+4]) * ( int(P_Best_Width[i]) - int(Width_v[i]) ) /int(1000) + int(c2[(i*Parameter)+4]) *(int(ALL_Best_Width) - int(Width_v[i]) ) /int(1000) ;

                                
                            }

                            Vector_In_Range();
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