import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
 
client = discord.Client()

 
help_message = ["To receive a quote, please use the command $quote . To add to the list of encouraging phrases, please use the command $new . To delete an encouraging phrase, please use the command $del followed by a number. To see a list of submitted phrases, use $list . To stop me from responding please use the command $responding false . To turn responding back on, please use the command $responding true ."
  ]

starter_encouragements=["don't worry you've got this!", "I know you can figure it out", "try a little harder next time!"]

if "responding" not in db.keys():
  db["responding"] = True
 
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)
 
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
 
def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements
 
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
 
@client.event
async def on_message(message):
  if message.author == client.user:
    return
 
  msg = message.content
 
  if msg.startswith("$quote"):
    quote = get_quote()
    await message.channel.send(quote)

  elif db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options +db["encouragements"].value
      
    if msg.startswith("$new"):
      encouraging_message = msg.split("$new ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New encouraging message added.")
  
 
    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split("$del",1)[1])
        delete_encouragment(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)
  
    if msg.startswith("$list"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)
    
    if msg.startswith("$help"):
      await message.channel.send(help_message)

    else:
      await message.channel.send("Your command or phrase was not recognized. Please type $help for a list of acceptable commands.")
      await message.channel.send("Also " + random.choice(starter_encouragements))

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]
 
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
  

  

keep_alive()
my_secret = os.environ['botkey']
client.run(my_secret)
 