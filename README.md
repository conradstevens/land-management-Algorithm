**Land Management Algorithm Reinforcement Learning**

This is a Reinforcement Learning Land Management Algorithm. Through a combination of Q-learning and final score optimization, the player/robot/smiley-face learns to cover the land entirely while minimizing the amount of wasted steps.

The only input into the neural network is its immediate surroundings. These squares are coloured, while the other squares not visible to the player are dark blue. To quantify its surroundings, plantable land is assigned a value of 1 and unplantable land is assigned a value of 0. Remark, for the time being I have not distinguished walkable and unplantable land, this could be potentially useful in situations where a perfect score is not attainable.

The neural network is a PyTorch network with the input layer the flattened surroundings. This feeds a single hidden layer consisting of 64 or 32 nodes. Which feeds a final output layer of size 4, each node determining what direction the player should move in (left, up, right, down).


![image](https://user-images.githubusercontent.com/3459566/147376755-4e8cb454-0266-4863-9fb6-c32413343f4c.png)


![Alt Text](https://media4.giphy.com/media/5l7kRWtG3cyWkos6dU/giphy.gif?cid=790b76118116ca6fee029c441b66209a3e33bd58db1e867a&rid=giphy.gif&ct=g)     ![Alt Text](https://media3.giphy.com/media/KqS8BMqPaw44c7Rgfy/giphy.gif?cid=790b76111c94944984417eeec64e75f8f577a11d46340473&rid=giphy.gif&ct=g)




