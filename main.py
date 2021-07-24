import discord
import asyncio
import tictactoe
# import os only if environment variable is used

client = discord.Client()

def playing_embed(board, challenger, opponent):
    embedPlay = discord.Embed(Title="Tic Tac Toe", color=0xc01111)
    embedPlay.set_thumbnail(url='https://image.flaticon.com/icons/png/512/566/566294.png')
    embedPlay.add_field(name='Challenger', value=f'{challenger}', inline=True)
    embedPlay.add_field(name='Opposition', value=f'{opponent}', inline=True)
    embedPlay.add_field(name='Board', value=tictactoe.print_board(board), inline=False)
    embedPlay.set_footer(text = 'Type \n[position]\n[position] should be replaced by 2 digit number like 11 or, 23 or, 31 where first number is the row number and second is the column number')
    return embedPlay

def intro_embed():
    embedIn = discord.Embed(title="Welcome To The Game Of Tic Tac Toe", description="**Commands:**", color=0x00eeff)
    embedIn.set_author(name="Tic Tac Toe", icon_url="https://image.flaticon.com/icons/png/512/566/566294.png")
    embedIn.set_thumbnail(url="https://cdn.discordapp.com/emojis/754600266288070806.png?v=1")
    embedIn.add_field(name="1) '_ttt'", value="Get help regarding commands of bot", inline=False)
    embedIn.add_field(name="2) '_ttt [mention]'", value="Challenge the [mention] to a game of Tic Tac Toe", inline=False)
    embedIn.set_footer(text="Do not include the quotes while using the commands \nRemove the [] while mentioning someone")
    return embedIn

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    #This list stores the people who are playing game
    #Important because cant have single player playing multiple games
    playing = list()

    if message.author == client.user:
        return

    if message.content.startswith('//hello'):
      await message.channel.send(f'Hello {message.author.mention} child')

    #Checks if the command has been executed
    if message.content.startswith('_ttt'):
        #Seperates the obtained message into words and store them in array to check for extra parms passed
        #Note: Any thing after _ttt will be considered parms(AKA PARAMETERS)
        #Just for Initial Release will implement slash-commands on later updates
        message_parts = message.content.split(' ')

        #Now Starts The Validation of the command
        #Case 1 just _ttt has been given
        if len(message_parts) == 1 and message_parts[0] == '_ttt':
            embedIntro = intro_embed()
            await message.channel.send(embed=embedIntro)
        
        #Didn't want the fucntion to go through just a single if-elsif-else statement 
        #Felt bored trying to implement it like that so I just used if statement for each new condition
        #This try..except statement is useful when the Case 2 if statement is executed
        #In that I explicitly compare element in particular index of the message_parts array
        #To prevent IndexError threw this here
        try:
            if len(message_parts) == 2 and message_parts[1][0] == '<' and message_parts[1][-1] == '>' and  message.author.mention not in playing and message_parts[1] not in playing:
                #Here we be initializing all the essential variables required to play the game
                board = tictactoe.initialize_board()
                players = tictactoe.initialize_players()
                challenger = message.author.mention
                opponent = message_parts[1]
                playing.append(challenger)
                playing.append(opponent)
                counter = 1
                validPositions = ['11', '12', '13', '21', '22', '23', '31', '32', '33']
                #This creates a object which is sent as message by the bot
                embedP = playing_embed(board, challenger, opponent)
                await message.channel.send(embed=embedP)
                #Initializations have been finished
                #Now comes the sequence of the game
                while tictactoe.validation(board, players) == 'None':
                    #Nothing fancy here just says all the odd number rounds the challenger adds symbol in the board
                    #Even number rounds the opponent adds
                    turn = 1 if counter % 2 != 0 else 2
                    player = challenger if turn == 1 else opponent
                    await message.channel.send(f"{player}'s Turn")
                    #Now considers next message of the player as place in board where the symbol will be kept
                    inpValid = False
                    #Says as long as input is not valid keep of considering the next message of the player as position in board
                    while not inpValid:
                        try:
                            #Says any new message by the user within next 60 seconds is the input
                            inp = await client.wait_for('message', timeout=60.00)
                            #now validate the input
                            if len(inp.content) == 2 and isinstance(int(inp.content), int) and inp.content in validPositions:
                                inpValid = True
                                #This part I did lazily didn't want to use much brain So tried to adapt the module in tic tac toe program to update value in board
                                #That module takes the data like this new inp i.e 111, 231 which is made of 3 digit number 
                                #first 2 represents row and column in the boarc the last number represent the player
                                #Challenger is player 1 and Opponent is player 2 
                                inp = str(inp.content)+('1' if player == challenger else '2')
                                #Inorder to prevent crazy mofos from trying to usse same position multiple time 
                                #This new position now must be removed from the list of valid positions
                                validPositions.remove(inp[0:2])
                                #Rememeber the new inp is 3 digit so using slicing this tells take the first 2 digits from left and remove it from validPosition list
                        except asyncio.TimeoutError:
                            #Now Suppose A player went AFK so waht we do?
                            #We Declare that player loser and the player who did last move as winner
                            #That's why this block of code
                            #We just state what happened and declare the winner
                            await message.channel.send(f'{player} took too long to reply :*(')
                            await message.channel.send(f'{challenger if player == opponent else opponent} is the winner')
                            await message.channel.send(f':)))')
                            await message.channel.send(f'{player} lost')
                            #After reaching here the game cant continue any longer cuz winner has already been decalred so we terminate the execution of routein
                            return
                        except ValueError:
                            #Invalid Position was provided
                            await message.channel.send(f'{player} unfortunately the position you gave was invalid\nPlease input valid position as input')
                    #Okay by now we will have obtained valid input from the player
                    #Now time to update the board on it's basis
                    #Nothing too hard here just calling a module from tictactoe.py which will update the board
                    #¯\_(ツ)_/¯ 
                    #(ಥ ͜ʖಥ)
                    board = tictactoe.update_board(inp, players, board)
                    #This too nothing hard
                    #Just says update what will be sent as message by the bot
                    embedP = playing_embed(board, challenger, opponent)
                    await message.channel.send(embed=embedP)
                    #End of the round now the things just happend untill some one wins
                    #(ಥ ͜ʖಥ)
                    counter += 1
                #Felt bored just gon print who won and lost
                if tictactoe.validation(board, players) != 'Draw': 
                    await message.channel.send(f"{challenger if tictactoe.validation(board, players) == 'X' else opponent} is the winner")
                else:
                    await message.channel.send("Damn yall smart\nGG")
                #The game has ended 
                #The players are no longer playing so have to remove them from playing list
                playing.remove(challenger)
                playing.remove(opponent)
                #Finally return cuz yk the game ended
                return   
            elif message.author.mention in playing:
                await message.channel.send(f'{message.author.mention}  you are already in a game\nComplete the on going game to play new game')
                return
            elif message_parts[1] in playing:
                await message.channel.send(f'Please wait \n{message_parts[1]} is currently in a game')
        except IndexError:
            #Line 64 look at it it says message_parts[1] what is it was just _ttt
            #message_parts[1] would not exist
            #But trying to access the index in array which does not exist returns Index Error so when that happens every thing above we just ignore it
            #to ignore we say just pass
            pass
        if len(message_parts) >= 3:
            await message.channel.send("Command Like This Doesn't Exist")

       
# Just add a Token for your app in here
# Token = os.environ['TOKEN'] OR Token = "TOKEN_GOES_HERE"
# client.run(Token)