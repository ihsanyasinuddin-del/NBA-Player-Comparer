# NBA Player Comparer 

#### Description:
The project is a simple Python program that takes user input of a specific NBA Regular Season (e.g 2020-21), followed by the input of the name of two players.

The program then retrieves data from NBA.com using the 'nba_api' library and displays each player's:

- Points per game
- Field goal percentage
- Free throw percentage
- Three-point percentage
- Rebounds per game
- Assists per game
- Steals per game
- Blocks per game
- Turnovers per game

After displaying both players' statistics, the program will output a comparison, listing each category and the name of the player which performed better in said category.

The logic for the turnovers was written separately, as fewer turnovers is a better performance, as opposed to the rest of the statistics in which a higher number is superior.

The program also includes input validation, in which if a player's name is not found, the program will output an error message and ask again for the player's name. 

If a player's name is found however they did not play in the season provided, the program informs the user and asks for another player's name.

The project contains a test file using 'pytest' which tests the player lookup, statistics retrieval, and statistics display functions.

The program uses 'rich' to tidy up the appearance of the output in the terminal.