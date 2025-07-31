import os
import discord
from discord import app_commands
import subprocess
from dotenv import load_dotenv
import random
from PIL import Image
from flask import Flask
from threading import Thread
# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Geervan quotes
geervan_lst = [
    "There's this mean person who keeps bullying me a lot",
    "Dude life's boring not fun at all",
    "Macha Wtf da",
    "Damm he's annoying",
    "Brooooo automating's so fun",
    "I am fucked yeah....",
    "Ayo dum or wut",
    "I did some bakchodi 😂",
    "I hate studies or even talking about it",
    "I am only good for watching sitcoms bruh"
]

# Bot setup
intents = discord.Intents.default()
activity = discord.Game(name="Finishing SpaceBasic")
client = discord.Client(intents=intents, activity=activity)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=activity)
    print(f"🤖 Bot is ready. Logged in as {client.user}")

# /hi
@tree.command(name="hi", description="Check if the bot is alive and has perms")
async def hi_command(interaction: discord.Interaction):
    await interaction.response.send_message("Yes yes Alive only not ded breh")

# /geervan
@tree.command(name="geervan", description="Random Geervan statement")
async def geervan_command(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(geervan_lst))

# /clean
@tree.command(name="clean", description="Run SpaceBasic room cleaning script")
async def clean_command(interaction: discord.Interaction):
    await interaction.response.send_message("🧹 Running cleaning script... Please wait.", )
    try:
        subprocess.run(["python", "main.py", str(interaction.user.id)], timeout=120)
        await interaction.followup.send("✅ Cleaning script triggered.")
    except Exception as e:
        await interaction.followup.send("❌ Failed to run the script.")

# /attendance
@tree.command(name="attendance", description="For Geervan and his lazy ass to check his attendance")
async def attendance_command(interaction: discord.Interaction):
    if interaction.user.id != 765413318826524682:  # Use int, not str
        await interaction.response.send_message("❌ You're not authorized to use this command.")
        return

    await interaction.response.send_message("📸 Fetching your attendance you lazy ass...")

    # Run the script
    subprocess.run(["python", "attendance.py"])

    # Send the screenshot
    try:
        img = Image.open("attendance.png")
        cropped = img.crop((260, 100, 1260, 700))
        cropped.save("cropped_screenshot.png")

        # Send the cropped screenshot
        file = discord.File("cropped_screenshot.png")
        await interaction.followup.send("Dekhle Bhai 75% se upar hi haina, warna royega baad mein", file=file)

        # Clean up both files
        os.remove("attendance.png")
        os.remove("cropped_screenshot.png")


    except Exception as e:
        await interaction.followup.send("⚠️ Failed to send screenshot.")
        print(f"Error deleting screenshot: {e}")

app = Flask('')    
@app.route('/')
def home():
    return "I'm alive!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Run bot
keep_alive()

# Run bot
client.run(DISCORD_TOKEN)
