import discord
import asyncio
from datetime import datetime
import random
import requests
import html
import requests
ID = ' https://discordapp.com/oauth2/authorize?client_id=774641201273896971&scope=bot&permissions=0'

# Parameters for open Trivia API
parameters = {
    "amount": 20,
    "type": "boolean"
}
messages = joined = 0
generator_list = ["meme1.jpg", "meme2.jpg", "meme3.jpg"]
question_list = []
answer_list = []
current_index = 0
running = False


def generate():
    global parameters, question_list, answer_list, current_index

    URL = requests.get('https://opentdb.com/api.php', params=parameters)

    data = URL.json()
    for q in data["results"]:
        question_list.append(html.unescape(q["question"]))
        answer_list.append(q["correct_answer"])
    return str(question_list[current_index])


# Reads the token
def read_token():
    with open('token.txt', 'r') as t:
        lines = t.readlines()
        return lines[0].strip()


token = read_token()

# Connect with client
client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("dataForServer.txt", "a") as f:
                now = datetime.now()

                current_time = now.strftime("%H:%M:%S")
                f.write(f"Time {str(current_time)}:, messages: {messages}, Members joined: {joined} \n")
            messages = 0
            joined = 0

            await asyncio.sleep(120)
        except Exception as e:
            print(e)


@client.event
async def on_member_join(members):
    global joined
    joined += 1
    for channel in members.guild.channels:
        if str(channel) == "general":
            await channel.send("Welcome to the server {}".format(members.mention))


@client.event
async def on_message(message):
    global messages, running, current_index
    messages += 1
    valid_users = ["RedX#1048"]
    id = client.get_guild(365661657378193409)
    channels = ["general"]
    swear_words = ["100", "yes"]

    for word in swear_words:
        if message.content.count(word) > 0:
            print("a swear word was sent")
            await message.channel.purge(limit=1)

    if message.content == "!help":
        embedded_message = discord.Embed(title="Bot commands", description="Useful commands")
        embedded_message.add_field(name="!hello", value="Greets the user")
        embedded_message.add_field(name="!users", value="Prints the number of users")
        embedded_message.add_field(name="!meme", value="Generates a random meme :)")
        embedded_message.add_field(name="!trivia", value="Play a game of trivia")
        await message.channel.send(embed=embedded_message)

    if message.content.find("!test") != -1:
        await message.channel.send("Hello")
    elif message.content.find("!users") != -1:
        await message.channel.send(f""" # of members: {id.member_count}""")

    elif message.content == "!meme":
        await message.channel.send('Hello', file=discord.File(random.choice(generator_list)))
    elif message.content == "!trivia":
        running = True

        await message.channel.send(f"type True or False to answer\n{generate()} ")
    if message.content.lower() == "true" or message.content.lower() == "false" and running:

        if message.content == answer_list[current_index]:
            print(answer_list[current_index])
            await message.channel.send("You got it correct!   Press q to quit")
        elif message.content.lower() == "q":
            message.channel.send("Okay, quitting")
            running = False

        else:
            await message.channel.send("Incorrect :(   Press q to quit")
        if running:
            await message.channel.send(generate())
        current_index += 1
    if message.content == "!tictactoe":
        pass
        # insert tic tac toe game

@client.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel == "general":
            await member.send_message(f"""Welcome to the server {member.mention}""")


@client.event
async def on_member_update(before, after):
    nick = after.nick
    if nick:
        if nick.lower().count("akki") > 0:
            lastNick = before.nick
            if lastNick:
                await after.edit(nick=lastNick)
            else:
                await after.edit(nick="no")


client.loop.create_task(update_stats())
# Run Client
client.run(token)
