# Game of Alice

What is the Game of Alice? the game of alice is mathematical and numeric puzzle game based on the game "Alice and You in the planet of numbers", but simplified for a more general and primitive game without some "Special Mechanics".
The game is composed by a table of numbers here character move is defined by the numbers on the proximity.

The game has two variations and can be played by two diferent ways, with different objectives.
1. First variation of the game you need to move character from point A to point B with minimum amount of movements.
2. Second variation of the game you need to visit every position(or squares) on the table making the table empty in the process.

# Rules

1. Your character must move the quantity of squares defined by the adjancent number.
The first rule can  be summarized by this simple image with 1D table with only 1 row.

![Rule 1](https://adeveloper-image-host.s3.us-east-2.amazonaws.com/alice_game_rules_1.png)

2. Every time that character moves a specified amount every square in that the path of the move is deleted,
if the path of movement intersect a empty square the character dies.
With the second rule the ilustration of the movement looks more like this.

![Rule 2](https://adeveloper-image-host.s3.us-east-2.amazonaws.com/alice_game_rules_2.png)

The game is made of a table of N x N numbers with randomized numbers and we can choose your initial character position randomized too, looking more like this:

(TO DO)

The only possible movements in this version of the game are Orthogonally Adjancent (Right and Straight Angles). 

# Solving the Game of Alice and the Algorithms

For resolution of this game we need to use a Directional Graph and map every node of this graph being a represetation of moveable square in the Game.
The maximum number of out connections in a node must be 4 (Top, Bottom, Left, Right).

After that is made a path finding Breath Search and is verified a possible intersection in the route.

# Solving and hacking the original game.
 
 You can see this algorithm solving the original game in this link: (TO DO)
 And the code: (TO DO)





