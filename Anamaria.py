import discord
import io

client = discord.Client()

announcementsQueue = []
messagecount = 1
naughtywords = ["nigger", "faggot", "tranny", "nigga", "n-i-g-g-a", "n-i-g-g-e-r"]
gameroles = []
users = []
blocked = True

class ServerUser:
 def __init__(self, id, strikes):
  self.id = id
  self.strikes = strikes

@client.event
async def on_ready():
    global users, blocked, gameroles
    server = client.get_guild(691967831071522839)
    gameroles = [server.get_role(764645286466682920)]
    warningschannel = client.get_channel(764657266011144242)
    await warningschannel.send("Anamaría live!")
    print("Anamaría live!")
    game = discord.Game("| DMs go to RojokooL")
    await client.change_presence(status=discord.Status.do_not_disturb, activity=game)
    blocked = False

@client.event
async def on_raw_reaction_add(payload):
  server = client.get_guild(691967831071522839)
  roleschannel = client.get_channel(764647043553427516)
  member = server.get_member(payload.user_id)
  reaction = payload.emoji
  try:
   message = await roleschannel.fetch_message(payload.message_id)
  except:
   return
  else:
   if message.channel != roleschannel: return
   if str(reaction) == "<:MordhauIcon:764652669137584139>": await member.add_roles(gameroles[0])

@client.event
async def on_raw_reaction_remove(payload):
  server = client.get_guild(691967831071522839)
  roleschannel = client.get_channel(764647043553427516)
  member = server.get_member(payload.user_id)
  reaction = payload.emoji
  try:
   message = await roleschannel.fetch_message(payload.message_id)
  except:
   return
  else:
   if message.channel != roleschannel: return
   if str(reaction) == "<:MordhauIcon:764652669137584139>": await member.remove_roles(gameroles[0])

@client.event
async def on_message(message):
    global users, blocked, announcementsQueue, messagecount
    messagecount += 1
    if blocked: return
    if (str(message.author)) == "Anamaría#8275": return
    print(message.content)
    server = client.get_guild(691967831071522839)
    logchannel = client.get_channel(720822158309326928)
    appealschannel = client.get_channel(720822208406093886)
    ticketschannel = client.get_channel(720822252177850490)
    requestschannel = client.get_channel(763828182247538689)
    approvechannel = client.get_channel(763844698514784276)
    anouncementschannel = client.get_channel(764636895631638548)
    warningschannel = client.get_channel(764657266011144242)
    dmchannel = client.get_channel(738760709495717958)
    mutedrole = server.get_role(720835419658387566)
    id = message.author.id
    messagestr = message.content
    messagesplit = messagestr.split(' ')
    print(message.channel.id)

    #Warnings
    if messagecount == 5 or messagecount == 100 or messagecount == 2000 or messagecount == 3000 or messagecount == 4000 or messagecount == 4500:
      await warningschannel.send(str(messagecount) + " messages in cache")

    #Announcements system
    if message.channel == requestschannel:
     announcementsQueue.append(message.content + "\nSubmitted by " + message.author.mention)
     await approvechannel.send(message.content + "\nSubmitted by " + message.author.mention + " ID: " + str(len(announcementsQueue) - 1))

    if message.channel == approvechannel:
     if messagesplit[0].lower() == "approve":
      if len(messagesplit) < 2: await approvechannel.send("Incorrect format"); return
      await anouncementschannel.send(announcementsQueue[int(messagesplit[1])])
     return

    print(announcementsQueue)
    def gettarget(id):
     target = id
     target = target[:-1]
     target = target[3:]
     return target

    def getrank(id, rank):
         member = server.get_member(int(id))
         for x in member.roles:
          if str(x) == str(rank): return True
         return False

    def strike(target):
     for x in users:
      if str(x.id) == str(target):
       count = int(x.strikes)
       count += 1
       x.strikes = str(count)
       break

    #Filter
    #Words
    for i in range(0, len(naughtywords)):
     if message.content.lower().find(naughtywords[i]) != -1:
      if (getrank(message.author.id, "Static Melee Team")) == True: return
      if (getrank(message.author.id, "Static Academy Team")) == True: return
      target = str(message.author.id)
      strike(target)
      await message.delete()
      await logchannel.send("Muted " + message.author.mention + " | " + '"' + str(message.content) + '"')
      member = server.get_member(int(target))
      role = mutedrole
      await member.add_roles(role)
      await message.author.send("You've been automatically muted for the message: " + '"' + str(message.content) + '". If you believe you were unfairly muted, you can appeal it in this DM using !appeal followed by your reasoning. (ex. "!appeal cat jumped on my keyboard")')
      return

    #Mentions
    print(len(message.mentions))
    if(len(message.mentions) > 5):
      if (getrank(message.author.id, "Static Melee Team")) == True: return
      if (getrank(message.author.id, "Static Academy Team")) == True: return
      target = str(message.author.id)
      strike(target)
      await message.delete()
      await logchannel.send("Muted " + message.author.mention + " | " + '"' + str(message.content) + '"')
      member = server.get_member(int(target))
      role = mutedrole
      await member.add_roles(role)
      await message.author.send("You've been automatically muted for the message: " + '"' + str(message.content) + '". If you believe you were unfairly muted, you can appeal it in this DM using !appeal followed by your reasoning. (ex. "!appeal cat jumped on my keyboard")')

    #DM Commands
    if (message.guild == None):
        await dmchannel.send(message.author.mention + " | " + str(message.content))
        if messagesplit[0] == ("!appeal"):

         if str(message.content) == "!appeal":
          await message.channel.send("You can't send an empty appeal. Usage: !appeal 'reason'")
          return

         member = server.get_member(int(id))

         await appealschannel.send(message.author.mention + " submitted an appeal | " + str(message.content))
         await message.channel.send("Your appeal has been submitted")

        if messagesplit[0] == ("!ticket"):
            await ticketschannel.send(message.author.mention + " | " + str(message.content))
            await message.channel.send("Your ticket has been submitted")
        if messagesplit[0] == ("!help"):
            await message.channel.send(".\n**Commands**\n**----------------**\n**!ticket** - Use to submit a support ticket directly to Static Melee staff\n**!appeal** - Use to appeal a mute you received in the Static Melee discord server")
        return

    def checkrank():
     cancontinue = False
     if (getrank(message.author.id, "Static Management")) == True: cancontinue = True
     return cancontinue

    if checkrank() == False: return

    if messagesplit[0] == ("!respond"):
     mention = messagesplit[1]
     target = gettarget(messagesplit[1])
     user = client.get_user(int(target))
     response = ""

     for x in range(2, len(messagesplit)):
      response += messagesplit[x] + " "

     await user.send("Response from administration regarding a ticket you've submitted: " + response)

    if messagesplit[0] == ("!ban"):
     mention = messagesplit[1]
     target = gettarget(messagesplit[1])
     user = client.get_user(int(target))
     member = server.get_member(user.id)
     response = ""
     for x in range(2, len(messagesplit)):
      response += messagesplit[x] + " "
     await user.send("You've been banned from Static Melee for the reason: \"" + response + "\"" + '. you can appeal it in this DM using !appeal followed by your reasoning. (ex. "!appeal cat jumped on my keyboard")')
     await member.ban(reason=response)

    if messagesplit[0] == ("!post"):
     roleschannel = client.get_channel(764647043553427516)
     messages = await roleschannel.history(limit=10).flatten()
     for x in messages: await x.delete()
     message = await roleschannel.send("Set your roles by reacting below\nMordhau: <:MordhauIcon:764652669137584139>")
     await message.add_reaction("<:MordhauIcon:764652669137584139>")

client.run("token goes here")



