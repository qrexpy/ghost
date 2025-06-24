DEFAULT_RPC = {
    "enabled": False,
    "client_id": "1018195507560063039",
    "state": "ghost aint dead",
    "details": "",
    "large_image": "https://avatars.githubusercontent.com/u/187971942?s=200&v=4",
    "large_text": "benny.fun/ghost",
    "small_image": "",
    "small_text": "",
    "name": "Ghost"
}

DEFAULT_CONFIG = {
    "token": "",
    "prefix": ".",
    "theme": "ghost",
    "apis": {
        "serpapi": ""
    },
    "message_settings": {
        "auto_delete_delay": 15,
        "style": "image"
    },
    "session_spoofing": {
        "enabled": False,
        "device": "desktop"
    },
    "snipers": {
        "nitro": {
            "enabled": True,
            "ignore_invalid": False,
            "webhook": "",
            "name": "nitro"
        },
        "privnote": {
            "enabled": True,
            "ignore_invalid": False,
            "webhook": "",
            "name": "privnote"
        }
    },
    "rich_presence": DEFAULT_RPC,
    "rich_embed_webhook": ""
}

DEFAULT_THEME = {
    "title": "ghost selfbot",
    "emoji": "\ud83d\udc7b",
    "image": "https://ghost.benny.fun/assets/ghost.png",
    "colour": "#575757",
    "footer": "ghost aint dead"
}

DEFAULT_SCRIPT = """
@ghost.command(name="example")
async def example(ctx):
    await ctx.send("Example command")
"""