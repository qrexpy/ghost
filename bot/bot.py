import discord
import time
import random
import certifi
import os
import asyncio
import inspect
import importlib.util
import sys

os.environ["SSL_CERT_FILE"] = certifi.where()
from discord.ext import commands, tasks

from utils import files
from utils.config import Config
import utils.console as console

import bot.helpers.sessionspoof as sessionspoof
import bot.helpers.cmdhelper as cmdhelper
from bot.helpers import get_external_asset, generate_activity_json

import bot.commands as ghost_commands
import bot.events as ghost_events

import asyncio
import random

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

class Ghost(commands.Bot):
    def __init__(self, controller):
        self.cfg = Config()
        self.controller = controller
        self.session_spoofing, self.session_spoofing_device = self.cfg.get_session_spoofing()

        if self.session_spoofing:
            sessionspoof.patch_identify(self.session_spoofing_device)

        super().__init__(command_prefix=self.cfg.get("prefix"), self_bot=True, help_command=None)
        self.start_time = None
        self.files = files

    def _setup_scripts(self):
        scripts = self.cfg.get_scripts()

        for script in scripts:
            script_name = script.replace(".py", "")
            script_path = files.get_application_support() + f"/scripts/{script}"

            try:
                os.chmod(script_path, 0o755)  # Give execute permissions
                spec = importlib.util.spec_from_file_location(script_name, script_path)
                if spec is None or spec.loader is None:
                    raise ImportError(f"Invalid spec for {script_name} (spec: {spec})")

                module = importlib.util.module_from_spec(spec)

                # Inject dependencies before execution
                ghost = commands  # Alias for commands
                module.discord = discord
                module.bot = self
                module.commands = commands
                module.ghost = ghost
                module.console = console
                module.cmdhelper = cmdhelper
                module.asyncio = asyncio
                module.time = time
                module.tasks = tasks
                module.random = random
                module.os = os
                module._ghost_config = self.cfg
                module._ghost_session_spoofer = sessionspoof
                module._ghost_bot_controller = self.controller
                module.files = self.files

                sys.modules[f"scripts.{script_name}"] = module  # Register module
                spec.loader.exec_module(module)  # Execute the script after injection

                module._themes_path = files.get_themes_path
                for _, obj in inspect.getmembers(module):
                    if isinstance(obj, commands.Command):
                        self.add_command(obj)
                    
                    if isinstance(obj, commands.Cog):
                        self.add_cog(obj)

                self.controller.add_startup_script(script_name + ".py")
                console.print_info(f"Loaded script: {script_name}")

            except Exception as e:
                console.print_error(f"Error loading script: {script_name} - {e}")

    async def on_ready(self):
        try:
            self.start_time = time.time()
            self.cfg.add_token(self.cfg.get("token"), self.user.name, self.user.id)
            await self.load_cogs()

            text = f"Logged in as {self.user.name}"
            if str(self.user.discriminator) != "0":
                text += f"#{self.user.discriminator}"
            
            try:
                console.clear()
                console.resize(columns=90, rows=25)
                console.print_banner()
            except:
                pass
            
            self.controller.bot_running = True
            console.print_info(text)
            console.print_info(f"You can now use commands with {self.cfg.get('prefix')}")
            print()

            if self.session_spoofing:
                console.print_info(f"Spoofing session as {self.session_spoofing_device}")
                # console.print_warning("Your account is at higher risk of termination by using session spoofer.")
            
            self._setup_scripts()
            await self.controller.setup_webhooks()
            self.controller.spypet.set_bot(self)
            
        except Exception as e:
            console.print_error(str(e))

        cfg_rpc = self.cfg.get("rich_presence")
        if cfg_rpc["enabled"]:
            external_assets = {
                "large_image": await get_external_asset(self, cfg_rpc.get("large_image"), cfg_rpc.get("client_id")) if cfg_rpc.get("large_image") else None,
                "small_image": await get_external_asset(self, cfg_rpc.get("small_image"), cfg_rpc.get("client_id")) if cfg_rpc.get("small_image") else None
            }
            
            activity_json = generate_activity_json(cfg_rpc, external_assets)
            await self.change_presence(activity=discord.Activity(**activity_json), afk=True)
        
    async def load_cogs(self):
        cogs = [
            ghost_commands.Account, ghost_commands.Fun, ghost_commands.General, ghost_commands.Img,
            ghost_commands.Info, ghost_commands.Mod, ghost_commands.Nsfw, ghost_commands.Text,
            ghost_commands.Theming, ghost_commands.Util, ghost_commands.Abuse, ghost_commands.Sniper,
            ghost_events.NitroSniper, ghost_events.PrivnoteSniper
        ]

        for cog in cogs:
            if cog == ghost_commands.Util or cog == ghost_commands.Sniper:
                await self.add_cog(cog(self, self.controller))
            else:
                await self.add_cog(cog(self))

    async def on_command(self, ctx):
        try:
            await ctx.message.delete()
        except Exception as e:
            console.print_error(str(e))

        command = ctx.message.content[len(self.command_prefix):]
        console.print_cmd(command)
        self.cfg.add_command_history(command)

    async def on_command_error(self, ctx, error):
        console.print_error(str(error))

        try:
            await ctx.message.delete()
        except Exception as e:
            console.print_error(str(e))

        try:
            await cmdhelper.send_message(ctx, {
                "title": "Error",
                "description": str(error),
                "colour": "#ff0000"
            })
        except Exception as e:
            console.print_error(f"{e}")
            
    async def on_message_delete(self, message):
        if message.author.id == self.user.id:
            return
        delete_time = time.time()
        self.controller.gui.home_page.add_discord_log(message.author, message, delete_time)

    def run_bot(self):
        try:
            console.clear()
            console.print_info("Starting Ghost...")
            # self.run(self.cfg.get("token"), log_handler=console.handler)
            self.run(self.cfg.get("token"), log_handler=None)
        except Exception as e:
            console.print_error(str(e))
            exit(1)


if __name__ == "__main__":
    bot = Ghost()
    bot.run_bot()
