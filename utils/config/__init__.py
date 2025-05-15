from .rich_presence import RichPresence
from .sniper import Sniper
from .theme import Theme
from .config import Config
from .token import Token

VERSION = "4.0.0"
PRODUCTION = False
MOTD = "stupid restructure fuck your mum"
CHANGELOG = """New:
  - Added checks for no desktop interface and will run headless if so
  - Added rich embed mode! Nope this isn't using web embeds.
  - Added rich embed webhook to GUI
  - Add spam command
  - Add proper uptime
  - Add mutual server members command!
  - Add clearcache command
  - Add massping command
  - Add embed message style option in gui
  - Added aura and gyatt commands (proper brainrot)
  - Added challenge and achievement commands using api.alexflipnote.dev
  - Added rainbow reaction and rainbow codeblock using ascii colours
  - Added ascii colours to codeblock for future changes to codeblock mode
  - Add dm channel check for clear command
  - Add yoinkrpc command and more customisable rich presence
  - Add no_response option to restart, useful for executing the command within another command
  - Add command history command
  - Add custom pypresence git to requirements for custom names in RPC
  - Add rich presence customisation in gui

Fix:
  - Fix codeblock styling for footers
  - Fix RPS description not showing
  - Fix dox command
  - Fix search command
  - Fix hyperlink
  - Fixed soundboard and playsound command.

Change:
  - Rename config to config.example.json and add default config to gitingore so config isnt overwritten when merging changes.
  - Edit RPC error log
  - Update NSFW commands to use nekobot
  - Improve generate help commands and add custom emojis to titles
  - Improve config command
  - Adding short and long formatting for uptime
  - Improved specs command
  - Allowed delete_after to be disabled
  - Improve send_message
  - Adjust headerless check to check for ttkbootstrap not tkinter
  - Improve banner printing
  - Search now searches through command aliases
  - Make print_banner get terminal width for correct dash size"""