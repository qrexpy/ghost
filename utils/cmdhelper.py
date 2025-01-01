import os
import json
import asyncio
import discord
import requests

from . import codeblock
from . import config
from . import imgembed
from . import webhook

def cog_desc(cmd, desc):
    return f"{desc}\n{cmd}"

def get_command_help(cmd):
    prefix = ""

    if cmd.parent is not None:
        prefix = f"{cmd.parent.name} {cmd.name}"
    else:
        prefix = f"{cmd.name}"

    return prefix

def generate_help_pages(bot, cog):
    pages = []
    pages_2 = []
    commands = bot.get_cog(cog).walk_commands()
    commands_formatted = []
    commands_formatted_2 = []
    commands_2 = []
    spacing = 0

    for cmd in commands:
        if cmd.name.lower() != cog.lower():
            prefix = get_command_help(cmd)

            if len(prefix) > spacing:
                spacing = len(prefix)

            commands_2.append([prefix, cmd.description])

    for cmd in commands_2:
        commands_formatted_2.append(f"{cmd[0]}{' ' * (spacing - len(cmd[0]))} :: {cmd[1]}")
        commands_formatted.append(f"**{bot.command_prefix}{cmd[0]}** {cmd[1]}")

    commands_str = ""
    for cmd in commands_formatted:
        if len(commands_str) + len(cmd) > 300:
            pages.append(commands_str)
            commands_str = ""

        commands_str += f"{cmd}\n"

    if len(commands_str) > 0:
        pages.append(commands_str)

    commands_str = ""
    for cmd in commands_formatted_2:
        if len(commands_str) + len(cmd) > 500:
            pages_2.append(commands_str)
            commands_str = ""

        commands_str += f"{cmd}\n"

    if len(commands_str) > 0:
        pages_2.append(commands_str)

    return {"codeblock": pages_2, "image": pages}

async def rich_embed(ctx, embed):
    cfg = config.Config()
    webhook_url = cfg.get("rich_embed_webhook")
    webhook_client = webhook.Webhook.from_url(webhook_url)
    webhook_channel = ctx.bot.get_channel(int(webhook_client.channel_id))
    webhook_client.send(embed=embed.to_dict())

    async for message in webhook_channel.history(limit=1):
        try:
            resp = requests.post(
                f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages", 
                headers={"Authorization": cfg.get("token"), "Content-Type": "application/json"}, 
                data=json.dumps({
                    "content": "",
                    "flags": 0,
                    "message_reference": {
                        "channel_id": message.channel.id,
                        "guild_id": message.guild.id,
                        "message_id": message.id,
                        "type": 1
                    }
                })
            )

            if resp.status_code == 200:
                await asyncio.sleep(cfg.get("message_settings")["auto_delete_delay"])
                try:
                    requests.delete(f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages/{resp.json()['id']}", headers={"Authorization": self.cfg.get("token")})
                except:
                    pass
        
        except Exception as e:
            print(e)

async def send_message(ctx, embed_obj: dict, extra_title="", extra_message="", delete_after=None):
    cfg = config.Config()
    theme = cfg.theme
    title = embed_obj.get("title", theme.title)
    description = embed_obj.get("description", "")
    colour = embed_obj.get("colour", theme.colour)
    footer = embed_obj.get("footer", theme.footer)
    thumbnail = embed_obj.get("thumbnail", theme.image)
    codeblock_desc = embed_obj.get("codeblock_desc", description)
    if delete_after is None:
        delete_after = cfg.get("message_settings")["auto_delete_delay"]

    msg_style = cfg.get("message_settings")["style"]

    if msg_style == "embed" and cfg.get("rich_embed_webhook") == "":
        msg_style = "codeblock"

    if msg_style == "codeblock":
        description = description.replace("*", "")
        description = description.replace("`", "")

        msg = await ctx.send(str(codeblock.Codeblock(title=title, description=codeblock_desc, extra_title=extra_title)), delete_after=delete_after)
    elif msg_style == "image":
        if theme.emoji in title:
            title = title.replace(theme.emoji, "")
        
        title = title.lstrip()
        embed2 = imgembed.Embed(title=title, description=description, colour=colour)
        embed2.set_footer(text=footer)
        embed2.set_thumbnail(url=thumbnail)
        embed_file = embed2.save()
        
        msg = await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=delete_after)
        os.remove(embed_file)
    elif msg_style == "embed" and cfg.get("rich_embed_webhook") != "":
        embed = discord.Embed(title=title, description=description, colour=discord.Color.from_str(colour))
        embed.set_footer(text=footer)
        embed.set_thumbnail(url=thumbnail)

        return await rich_embed(ctx, embed)
    
    if extra_message != "":
        extra_msg = await ctx.send(extra_message, delete_after=delete_after)
        return msg, extra_msg
    
    return msg

