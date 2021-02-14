"# NeatAiGame" 

For the game itself use pygame , with 3 simple classes : Bird, Pipe and BackGround  

Neat Algorithm : this is basically an evolution algorithm , that from each run it 
chooses the nodes with the highest fitness function and chooses to use them in order to create
the new generation . This library specifically has the option to add intermediary nodes to the initial problem if
it thinks that it will help him come to a solution faster  

For neat network, inputs : BirdY , TopPipe , BottomPipe  
Output : jump or not (simple choice, this game has only one command)  
Activation Function : TanH( to map  results between -1 and 1)    
Population Size : does not really matter (chose 100 for start)    
Fitness Function : how many frames each bird survived per game ( could also pick the score )    
Max Generations : to stop the program from running forever  (30 for this example )


