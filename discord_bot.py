import discord
import os
import random
from dotenv import load_dotenv
from wish_handler import Wish
from gem_store_tracker import StoreTracker

wish = Wish()
tracker = StoreTracker()

load_dotenv()
token = os.getenv("DISCORD_TOKEN")


class Bot:
    def __init__(self):
        self.APP_ID = "1318637245548204135"
        self.default_channel_id = 929457317919998002
        self.message = ""
        self.endpoint = f"https://discord.com/oauth2/authorize?client_id={self.APP_ID}&permissions=2048&integration_type=0&scope=bot+applications.commands"
        self.intents = discord.Intents.default()
        self.intents.messages = True
        self.intents.message_content = True
        # Creates instance of a client, - our connection to Discord
        self.client = discord.Client(intents=self.intents)

    # bot = commands.Bot(command_prefix="!")


    def login(self):
        @self.client.event
        async def on_ready():
            print(f"We have logged in as {self.client.user}")
            channel = self.client.get_channel(self.default_channel_id)
            await channel.send('Wallet Destroyer is online. Begin requests with `Wishlist:` followed by a comma-separated list of complete item names. Bot does not support partial matches. \n\nE.g.:\n`Wishlist: Sunspear Glider, Swaggering Cape, Jackal Chair`\n\nFor financial deterrents, request `Guilt Trip`')


    def send_message(self):
        self.login()

        @self.client.event
        async def on_message(message):
            channel = str(message.channel.name)
            user_message = str(message.content)
            # Meant to prevent triggering on our own messages
            if message.author == self.client.user:
                return

            guilt_trip_list = ["Are you SURE you should be spending real money on this?",
                               "You know, I hear City of Heroes costumes are free.",
                               "Would you rather spend your money on this or on that thing you love?",
                               "Are you sure? That's good chocolate money.",
                               "I'm judging you."]

            if channel == "general":
                formatted_string = wish.format_words(user_message)
                if "Guilt Trip" in formatted_string:
                    guilt_trip_response = random.choice(guilt_trip_list)
                    await message.channel.send(guilt_trip_response)

                elif "Wishlist:" in user_message:
                    #formatted_string = wish.format_words(user_message)
                    store_results = tracker.get_gem_store(formatted_string)

                    if store_results == "":
                        await message.channel.send(f"I'm sorry, I didn't find any results.")
                    else:
                        await message.channel.send(f"Here is what you asked for:\n\n{store_results}")
                    return

        self.client.run(token)

bot = Bot()
bot.send_message()




