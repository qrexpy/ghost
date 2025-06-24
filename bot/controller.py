import os
import sys
import time
import json
import asyncio
import threading
import discord
import requests

from io import BytesIO
from PIL import Image, ImageTk
from bot.bot import Ghost
from utils import console, files
from utils.config import Config
from bot.helpers import cmdhelper, imgembed
import utils.webhook as webhook_client
from gui.helpers.images import resize_and_sharpen
from bot.tools import SpyPet

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

class BotController:
    def __init__(self):
        self.cfg = Config()
        self.bot = None
        self.gui = None
        self.loop = None
        self.bot_thread = None
        self.running = False
        self.bot_running = False
        self.startup_scripts = []
        self.presence = self.cfg.get_rich_presence()
        self.spypet = SpyPet(self)

    def start_spypet(self):
        if not self.spypet.bot:
            self.spypet.set_bot(self.bot)
            console.success("SpyPet bot set successfully.")
        else:
            console.warning("SpyPet bot is already set.")
        
        if not self.spypet.member_id:
            console.error("SpyPet member ID is not set. Please set it in the settings.")
            return

        asyncio.run_coroutine_threadsafe(self.spypet.start(), self.loop)
        console.success("SpyPet started successfully!")

    def stop_spypet(self):
        if self.spypet.running:
            asyncio.run_coroutine_threadsafe(self.spypet.stop(), self.loop)
            console.success("SpyPet stopped successfully!")
        else:
            console.warning("SpyPet is not running.")
            
    def get_mutual_guilds_spypet(self):
        if self.spypet.running:
            return asyncio.run_coroutine_threadsafe(self.spypet.get_mutual_guilds(), self.loop).result()
        else:
            console.warning("SpyPet is not running. Cannot get mutual guilds.")
            return []

    def add_startup_script(self, script):
        self.startup_scripts.append(script)

    def set_gui(self, gui):
        self.gui = gui
        self.spypet.set_gui(gui.tools_page.spypet_page)
        
    def check_token(self):
        resp = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": self.cfg.get("token")})
        if resp.status_code == 200:
            return True
        return False

    def _stop_rich_presence(self):
        if self.rpc is not None:
            self.rpc.close()
            self.rpc = None

    def start(self):
        if self.cfg.get("token") == "":
            os.execl(sys.executable, sys.executable, *sys.argv)
            
        if not self.check_token():
            self.cfg.set("token", "", save=True)
            console.error("Invalid token! Token has been reset. Now restarting...")
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            console.success("Token is valid.")
        
        # console.clear()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.running = True
        self.bot = Ghost(self)
        self.loop.create_task(self.bot.start(token=self.cfg.get("token"), reconnect=True))
        threading.Thread(target=self.loop.run_forever, daemon=True).start()
        print("[BotController] Bot is running.")

    def stop(self):
        if self.bot and self.loop:
            self.bot_running = False
            self.running = False
            print("[BotController] Stopping bot...")

            async def shutdown():
                self.bot._stop_rich_presence()
                await self.bot.close()
                print("[BotController] Bot has been stopped.")

            asyncio.run_coroutine_threadsafe(shutdown(), self.loop)

    def restart(self):
        self.startup_scripts = []
        self.bot_running = False
        self.running = False
        print("[BotController] Restarting bot...")
        self.stop()
        threading.Timer(3, self.start).start()  # Non-blocking delay before restart

    def check_setup_webhooks(self):
        if os.path.exists(files.get_application_support() + "/data/cache/CREATE_WEBHOOKS"):
            with open(files.get_application_support() + "/data/cache/CREATE_WEBHOOKS", "r") as f:
                if f.read() == "True":
                    return True
        return False
    
    def delete_setup_webhooks(self):
        if os.path.exists(files.get_application_support() + "/data/cache/CREATE_WEBHOOKS"):
            os.remove(files.get_application_support() + "/data/cache/CREATE_WEBHOOKS")
    
    def _create_webhook(self, channel_id, name, avatar_url = ""):
        payload = {
            "name": name,
            "avatar": "data:image/jpeg;base64," + webhook_client.encode_image(avatar_url) if avatar_url else "",
            "channel_id": channel_id
        }

        resp = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/webhooks", headers={"Content-Type": "application/json", "Authorization": self.cfg.get("token")}, data=json.dumps(payload))
        return webhook_client.Webhook(**resp.json())

    async def setup_webhooks(self, checks=True):
        if checks:
            if not self.check_setup_webhooks():
                return
            
            self.delete_setup_webhooks()
            
        snipers = self.cfg.get_snipers()
        
        try:
            template = await self.bot.fetch_template("3RK8gFtuFznh")
            guild = await template.create_guild("Ghost Webhooks")
        except:
            print("[BotController] Couldn't create server.")
            return
        
        try:
            icon = "https://ghost.benny.fun/assets/ghost.png"
            icon_bytes = requests.get(icon).content
            await guild.edit(icon=icon_bytes)
        except:
            print("[BotController] Couldn't set server icon.")

        for channel in guild.channels:
            try:
                await channel.delete()
            except:
                print(f"[BotController] Couldn't delete channel: {channel.name}")
        
        webhook_category = await guild.create_category("Webhooks")

        for sniper in snipers:
            channel = await webhook_category.create_text_channel(sniper.name.capitalize())
            webhook = self._create_webhook(channel.id, sniper.name.capitalize())
            sniper.set_webhook(webhook, notify=False)
            
        rich_embeds_channel = await webhook_category.create_text_channel("embeds")
        webhook = self._create_webhook(rich_embeds_channel.id, "Embeds")
        self.cfg.config["rich_embed_webhook"] = webhook.url
        self.cfg.save()
        
        console.success("Webhooks have been setup!")
        
        # try:
        #     main_channel = guild.system_channel
        #     print(main_channel)
        #     if not main_channel:
        #         for channel in guild.channels:
        #             if channel.name == "general" and isinstance(channel, discord.TextChannel):
        #                 main_channel = channel
        #                 break
                    
        #     if not main_channel:
        #         main_channel = await guild.create_text_channel("general")
                        
        #     webhook = await main_channel.create_webhook(name="Ghost")
        #     await webhook.send(embed=discord.Embed(title="Ghost", description="Webhooks have been setup! If there are any problems, please try restarting Ghost.", color=discord.Color.green()))
        #     await webhook.delete()
        # except:
        #     print("[BotController] Couldn't send message to main channel.")
        
    def restart_gui(self):
        if self.gui:
            # self.gui._restart_bot()
            self.gui.run_on_main_thread(self.gui._restart_bot)

    def switch_account(self, token):
        self.cfg.set("token", token)
        self.cfg.save()
        self.restart_gui()
        
    def get_user_from_id(self, user_id):
        return self.bot.get_user(user_id)

    def get_avatar_from_url(self, url, size=50, radius=5):
        url = url.split("?")[0]
        if url.endswith(".gif"):
            url = url.replace(".gif", ".png")
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            # image = image.resize((size, size))
            image = resize_and_sharpen(image, (size, size))
            image = imgembed.add_corners(image, radius)
            return ImageTk.PhotoImage(image)
        
        return None

    def get_avatar(self, size=50, radius=5):
        try:
            url = self.get_user().avatar.url if self.get_user() else None
        except:
            # url = "https://ia600305.us.archive.org/31/items/discordprofilepictures/discordblue.png"
            url = "https://ghost.benny.fun/assets/ghost.png"
        
        if url:
            return self.get_avatar_from_url(url, size, radius)
        
    def set_prefix(self, prefix):
        self.bot.command_prefix = prefix


    async def get_user_from_id_async(self, user_id):
        print(f"[BotController] Getting user from ID: {user_id}")
        try:
            return await self.bot.fetch_user(user_id) if self.bot else None
        except Exception as e:
            console.print_error(f"Error getting user from ID {user_id}: {e}")
            return None

    def get_user_from_id(self, user_id):
        return asyncio.run_coroutine_threadsafe(self.get_user_from_id_async(user_id), self.loop).result()

    get_user    = lambda self: self.bot.user if self.bot else None
    get_friends = lambda self: self.bot.friends if self.bot else None
    get_guilds  = lambda self: self.bot.guilds if self.bot else None
    get_uptime  = lambda self: cmdhelper.format_time(time.time() - self.bot.start_time, short_form=True) if self.bot else "0:00:00"
    get_latency = lambda self: f"{round(self.bot.latency * 1000)}ms" if self.bot else "0ms"