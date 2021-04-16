pragma solidity >= 0.4.18 ;

contract PSO_1 {

    event Particle(int LR,int Epoch,int batch,int Layer,int Width,uint counter);
    int public ALL_Best_LR ;
    int public ALL_Best_Epoch ;
    int public ALL_Best_Batch ;
    int public ALL_Best_Layer ;
    int public ALL_Best_Width ;
    int public ALL_Best_Accuracy ;

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

    int[] private CHECK =  new int[](10) ;
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

    uint public ITER = 0;
    uint public counter  = 0; 


    function set_accuracy(int acc,uint ind) public {
        Accuracy[ind] = acc ;
        CHECK[ind] = 1;
    }


    function get()  public {
        if(ITER == 0)
        {
            RANDOM_INI();
            ITER++;
        }    
        else if(ITER < 100)
        {
            
            if(counter == 10 )
            {
                int  sum = 0;
                for(uint i = 0;i<10;i++)
                {
                    sum += CHECK[i];
                }

                if(sum == 10)
                {
                    Evaluate();
                    Update_Velocity();
                    Update_Position();
                    counter = 0;
                    ITER++;

                    for(uint i = 0;i<10;i++)
                    {
                        CHECK[i] = 0;
                    }
                }
           
            }
            else{
                emit Particle(LR[counter-1],Epoch[counter-1],Batch[counter-1],Layer[counter-1],Width[counter-1],counter-1);
                counter ++;
            }

        }
        

     
   }
    function RANDOM_INI() public{
        for(uint i = 0 ; i < 10 ; i++)
        {
            //random x 
            CHECK[i] = -1;

            LR[i] = int(int(keccak256(block.timestamp, block.difficulty))%9000)+1000;

            Epoch[i] = int(int(keccak256(block.timestamp, block.difficulty))%50)+50;

            Batch[i] = int(int(keccak256(block.timestamp, block.difficulty))%40)+20;

            Layer[i] = int(int(keccak256( block.timestamp , block.difficulty))%40)+10;

            Width[i] = int(int(keccak256(block.timestamp, block.difficulty)) % 30) + 30;



            //random vector
            LR_v[i] = int(int(keccak256(block.timestamp, block.difficulty))%1998)-999;

            Epoch_v[i] = int(int(keccak256(block.timestamp, block.difficulty))%10)-5;

            Batch_v[i] = int(int(keccak256(block.timestamp, block.difficulty))%8)-4;

            Layer_v[i] = int(int(keccak256(block.timestamp, block.difficulty))%8)-4;

            Width_v[i] = int(int(keccak256(block.timestamp, block.difficulty))%6)-3;
        }
        
    }
    function Update_Velocity() public
    {
        for(uint i = 0;i < 10;i++)
        {
            int[5] memory w;
            int[5] memory c1;
            int[5] memory c2;
            for(uint j = 0;j < 5;j++)
            {
                if( j==0 )
                {
                    w[j]= 8000;
                    c1[j] = int(int(keccak256(block.timestamp, block.difficulty))%4);
                    c2[j] = int(int(keccak256(block.timestamp, block.difficulty))%4);


                }
                else{
                    w[j] = 80;
                    c1[j] = int(int(keccak256(block.timestamp, block.difficulty))%4);
                    c2[j] = int(int(keccak256(block.timestamp, block.difficulty))%4);
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
    }
    function Evaluate() public
    {
        INRANGE();
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

