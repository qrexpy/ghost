# Credit: verticalsync 
# Github: https://github.com/verticalsync
# Discord: verticalsync.
# I have slightly modified the code to add different devices.
import uuid
from discord.gateway import DiscordWebSocket

properties = {
    "mobile": ["iOS", "Discord iOS", "iOS"],
    "desktop": ["Windows", "Discord Client", "Windows"],
    "web": ["Windows", "Chrome", "Windows"],
    "embedded": ["Xbox", "Discord Embedded", "Xbox"],
}
original_method = None
os = "mobile"

async def new_method(self):
    if original_method is None:
        return await self._identify()

    if os.lower() == "mobile":
        # credits: jsoncitron
        # issue: #16
        self._super_properties = {
          'os': 'Android',
          'browser': 'Discord Android',
          'device': 'emu64x',
          'system_locale': 'en-GB',
          'has_client_mods': False,
          'client_version': '267.0 - rn',
          'release_channel': 'alpha',
          'device_vendor_id': str(uuid.uuid4()),
          'design_id': 2,
          'browser_user_agent': '', # Not provided here but the user agent is Discord-Android/267200;RNA
          'browser_version': '',
          'os_version': '34',
          'client_build_number': 3616,
          'client_event_source': None,
        }

    else:
        self._super_properties["$os"] = properties[os][0]
        self._super_properties["$browser"] = properties[os][1]
        self._super_properties["$device"] = properties[os][2]

    return await original_method(self)

def patch_identify(new_os):
    global original_method, os

    if new_os not in properties:
        os = "desktop"
    
    os = new_os
    original_method = DiscordWebSocket.identify
    DiscordWebSocket.identify = new_method