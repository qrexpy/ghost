# Scripting Guide

Ghost includes powerful custom scripting capabilities that allow you to extend functionality, automate tasks, and create personalized commands. This guide covers everything you need to know about Ghost scripting.

## Overview

Ghost scripting enables you to:
- **Create custom commands** - Add your own bot commands
- **Automate tasks** - Schedule and trigger actions
- **Handle events** - Respond to Discord events
- **Extend functionality** - Add features beyond default commands
- **Integrate services** - Connect with external APIs

## Script System Architecture

### Script Types

**Command Scripts:**
- Add new commands to Ghost
- Custom command logic and responses
- Integration with Ghost's command system

**Event Scripts:**
- React to Discord events
- Background processing
- Automated responses

**Scheduled Scripts:**
- Time-based automation
- Recurring tasks
- Maintenance operations

**Integration Scripts:**
- External API connections
- Data processing
- Service integrations

## Getting Started

### Script Location

Scripts are stored in the `scripts/` directory (create if it doesn't exist):

```
ghost/
├── scripts/
│   ├── commands/
│   │   ├── my_command.py
│   │   └── another_cmd.py
│   ├── events/
│   │   ├── message_handler.py
│   │   └── user_tracker.py
│   ├── scheduled/
│   │   └── daily_backup.py
│   └── templates/
│       ├── basic_command.py
│       └── event_handler.py
```

### Basic Script Structure

```python
# Import required modules
import discord
from discord.ext import commands
import asyncio

# Script metadata
__script_name__ = "My Custom Script"
__script_version__ = "1.0.0"
__script_author__ = "Your Name"
__script_description__ = "Description of what this script does"

# Main script class
class MyScript:
    def __init__(self, bot):
        self.bot = bot
        
    # Your script logic here
    async def setup(self):
        """Called when script is loaded"""
        pass
        
    async def teardown(self):
        """Called when script is unloaded"""
        pass

# Required setup function
def setup(bot):
    return MyScript(bot)
```

## Creating Custom Commands

### Basic Command Example

```python
import discord
from discord.ext import commands

class CustomCommands:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="hello")
    async def hello_command(self, ctx, *, name: str = None):
        """Says hello to someone"""
        if name:
            await ctx.send(f"Hello, {name}!")
        else:
            await ctx.send(f"Hello, {ctx.author.name}!")
    
    @commands.command(name="roll")
    async def roll_dice(self, ctx, sides: int = 6):
        """Roll a dice with specified sides"""
        import random
        result = random.randint(1, sides)
        await ctx.send(f"🎲 You rolled a {result}!")

def setup(bot):
    script = CustomCommands(bot)
    # Register commands
    bot.add_command(script.hello_command)
    bot.add_command(script.roll_dice)
    return script
```

### Advanced Command Features

**Command with Subcommands:**
```python
@commands.group(name="admin")
async def admin_group(self, ctx):
    """Admin command group"""
    if ctx.invoked_subcommand is None:
        await ctx.send("Available admin commands: ban, kick, mute")

@admin_group.command(name="ban")
async def admin_ban(self, ctx, user: discord.User, *, reason="No reason"):
    """Ban a user"""
    # Implementation here
    pass
```

**Command with Cooldown:**
```python
@commands.command(name="expensive")
@commands.cooldown(1, 60, commands.BucketType.user)  # 1 use per 60 seconds per user
async def expensive_command(self, ctx):
    """Command with cooldown"""
    await ctx.send("This command has a cooldown!")
```

**Command with Permissions:**
```python
@commands.command(name="mod_only")
@commands.has_permissions(manage_messages=True)
async def moderator_command(self, ctx):
    """Only for users with manage messages permission"""
    await ctx.send("You have moderator permissions!")
```

## Event Handling Scripts

### Message Events

```python
import discord
from discord.ext import commands

class MessageHandler:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Handle all messages"""
        # Ignore bot messages
        if message.author.bot:
            return
            
        # Auto-reply to specific keywords
        if "hello ghost" in message.content.lower():
            await message.channel.send("Hello there! 👋")
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Handle message edits"""
        if before.content != after.content:
            print(f"Message edited: {before.content} -> {after.content}")

def setup(bot):
    handler = MessageHandler(bot)
    bot.add_cog(handler)
    return handler
```

### User Events

```python
@commands.Cog.listener()
async def on_member_join(self, member):
    """Welcome new members"""
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Welcome {member.mention} to {member.guild.name}!")

@commands.Cog.listener()
async def on_member_remove(self, member):
    """Log member departures"""
    print(f"{member.name} left {member.guild.name}")
```

## Scheduled Scripts

### Basic Scheduler

```python
import asyncio
from datetime import datetime, timedelta

class ScheduledTasks:
    def __init__(self, bot):
        self.bot = bot
        self.running = True
    
    async def setup(self):
        """Start scheduled tasks"""
        asyncio.create_task(self.daily_task())
        asyncio.create_task(self.hourly_check())
    
    async def daily_task(self):
        """Run every 24 hours"""
        while self.running:
            await asyncio.sleep(86400)  # 24 hours
            await self.perform_daily_maintenance()
    
    async def hourly_check(self):
        """Run every hour"""
        while self.running:
            await asyncio.sleep(3600)  # 1 hour
            await self.check_status()
    
    async def perform_daily_maintenance(self):
        """Daily maintenance tasks"""
        print(f"Daily maintenance at {datetime.now()}")
        # Add your maintenance code here
    
    async def check_status(self):
        """Hourly status check"""
        print(f"Status check at {datetime.now()}")
        # Add status checking logic

def setup(bot):
    scheduler = ScheduledTasks(bot)
    asyncio.create_task(scheduler.setup())
    return scheduler
```

### Advanced Scheduling with Cron

```python
import schedule
import asyncio
import threading

class CronScheduler:
    def __init__(self, bot):
        self.bot = bot
        self.scheduler_thread = None
    
    def setup_schedule(self):
        """Setup scheduled tasks"""
        schedule.every().day.at("09:00").do(self.morning_routine)
        schedule.every().hour.do(self.hourly_task)
        schedule.every().monday.at("00:00").do(self.weekly_cleanup)
    
    def run_scheduler(self):
        """Run the scheduler in a thread"""
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def start_scheduler(self):
        """Start the scheduler thread"""
        self.setup_schedule()
        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
```

## Script Integration with Ghost

### Accessing Ghost Features

**Configuration Access:**
```python
from utils.config import Config

class MyScript:
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()
        
    def get_setting(self, key):
        return self.config.get(key)
```

**Command Helper Integration:**
```python
import bot.helpers.cmdhelper as cmdhelper

async def my_command(self, ctx):
    await cmdhelper.send_message(ctx, {
        "title": "Custom Command",
        "description": "This uses Ghost's message system!",
        "color": self.config.theme.color
    })
```

**File System Access:**
```python
from utils.files import get_application_support

class DataScript:
    def __init__(self, bot):
        self.data_dir = get_application_support() + "/custom_data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_data(self, filename, data):
        with open(f"{self.data_dir}/{filename}", "w") as f:
            json.dump(data, f)
```

## API Integration Scripts

### HTTP Requests

```python
import aiohttp
import asyncio

class APIIntegration:
    def __init__(self, bot):
        self.bot = bot
        self.session = None
    
    async def setup(self):
        self.session = aiohttp.ClientSession()
    
    async def teardown(self):
        if self.session:
            await self.session.close()
    
    @commands.command(name="weather")
    async def weather_command(self, ctx, *, city: str):
        """Get weather for a city"""
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": "YOUR_API_KEY",
            "units": "metric"
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                await ctx.send(f"Weather in {city}: {temp}°C, {desc}")
            else:
                await ctx.send("City not found!")
```

### Database Integration

```python
import sqlite3
import aiosqlite

class DatabaseScript:
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "scripts/data/users.db"
    
    async def setup(self):
        """Initialize database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    points INTEGER DEFAULT 0
                )
            """)
            await db.commit()
    
    @commands.command(name="points")
    async def check_points(self, ctx, user: discord.User = None):
        """Check user points"""
        user = user or ctx.author
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT points FROM users WHERE id = ?", 
                (user.id,)
            )
            result = await cursor.fetchone()
            
            points = result[0] if result else 0
            await ctx.send(f"{user.name} has {points} points!")
```

## Script Management

### Loading Scripts

**Automatic Loading:**
- Place scripts in appropriate directories
- Ghost loads them on startup
- Scripts are automatically registered

**Manual Loading:**
```python
# In Ghost console or command
await bot.load_extension('scripts.commands.my_script')
```

### Script Configuration

**Script-specific Config:**
```python
# config/scripts/my_script.json
{
    "enabled": true,
    "settings": {
        "api_key": "your_key_here",
        "timeout": 30,
        "max_retries": 3
    }
}
```

**Loading Script Config:**
```python
import json

class ConfigurableScript:
    def __init__(self, bot):
        self.bot = bot
        self.load_config()
    
    def load_config(self):
        try:
            with open("config/scripts/my_script.json") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {"enabled": True, "settings": {}}
```

## Debugging Scripts

### Logging

```python
import logging

# Set up script logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DebuggableScript:
    def __init__(self, bot):
        self.bot = bot
        self.logger = logger
    
    async def some_function(self):
        self.logger.info("Function started")
        try:
            # Your code here
            result = await self.do_something()
            self.logger.debug(f"Result: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error in some_function: {e}")
            raise
```

### Error Handling

```python
class RobustScript:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="safe_command")
    async def safe_command(self, ctx):
        try:
            # Potentially risky operation
            await self.risky_operation()
            await ctx.send("✅ Operation successful!")
            
        except discord.HTTPException as e:
            await ctx.send(f"❌ Discord API error: {e}")
            
        except Exception as e:
            await ctx.send(f"❌ Unexpected error: {e}")
            self.logger.exception("Unexpected error in safe_command")
```

## Security Considerations

### Safe Practices

1. **Input Validation:**
```python
@commands.command(name="safe_input")
async def safe_input(self, ctx, *, user_input: str):
    # Sanitize input
    if len(user_input) > 200:
        await ctx.send("Input too long!")
        return
    
    # Validate characters
    if not user_input.isalnum():
        await ctx.send("Only alphanumeric characters allowed!")
        return
    
    # Process safe input
    await self.process_input(user_input)
```

2. **Permission Checks:**
```python
async def admin_only_function(self, ctx):
    if ctx.author.id not in self.config.get("admin_users", []):
        await ctx.send("❌ Admin only command!")
        return False
    return True
```

3. **Rate Limiting:**
```python
from collections import defaultdict
import time

class RateLimitedScript:
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = defaultdict(float)
    
    def is_on_cooldown(self, user_id, cooldown_seconds=60):
        now = time.time()
        if now - self.cooldowns[user_id] < cooldown_seconds:
            return True
        self.cooldowns[user_id] = now
        return False
```

## Script Templates

### Basic Command Template

```python
"""
Basic Command Template
Copy this template to create new commands quickly.
"""

import discord
from discord.ext import commands

class BasicCommandTemplate:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="template")
    async def template_command(self, ctx, *, args: str = None):
        """Template command description"""
        if args:
            await ctx.send(f"You said: {args}")
        else:
            await ctx.send("Hello from template command!")

def setup(bot):
    template = BasicCommandTemplate(bot)
    bot.add_command(template.template_command)
    return template
```

### Event Handler Template

```python
"""
Event Handler Template
Template for handling Discord events.
"""

import discord
from discord.ext import commands

class EventHandlerTemplate:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Handle message events"""
        if message.author.bot:
            return
        
        # Your event handling logic here
        pass
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handle reaction events"""
        # Your reaction handling logic here
        pass

def setup(bot):
    handler = EventHandlerTemplate(bot)
    bot.add_cog(handler)
    return handler
```

## Best Practices

### Code Organization

1. **Modular Design** - Keep scripts focused and small
2. **Clear Documentation** - Comment your code well
3. **Error Handling** - Always handle potential errors
4. **Configuration** - Make scripts configurable
5. **Testing** - Test scripts thoroughly before deployment

### Performance

1. **Async/Await** - Use proper async patterns
2. **Resource Cleanup** - Close connections and files
3. **Memory Management** - Avoid memory leaks
4. **Efficient Algorithms** - Optimize for performance

### Maintenance

1. **Version Control** - Track script changes
2. **Backup Scripts** - Keep backup copies
3. **Regular Updates** - Keep scripts current
4. **Monitor Performance** - Watch for issues

---

Ghost's scripting system is incredibly powerful and flexible. Start with simple scripts and gradually build more complex automation as you become familiar with the system. Happy scripting!