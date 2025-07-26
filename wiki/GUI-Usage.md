# GUI Usage Guide

Ghost features a fully customizable graphical user interface built with modern UI components. This guide covers everything you need to know about using the GUI.

## Starting the GUI

### Requirements
- **Display/Desktop environment** (GUI mode requires a graphical interface)
- **Required fonts** (Ghost will check and help install missing fonts)

### Launch Methods

**Standard Launch:**
```bash
python ghost.py
```

**Windows:**
```cmd
python ghost.py
```

**Force GUI Mode:**
```bash
DISPLAY=:0 python ghost.py  # Linux/macOS with specific display
```

## First-Time Setup

When you first launch Ghost in GUI mode:

1. **Font Check** - Ghost verifies required fonts are installed
2. **Onboarding** - Initial setup wizard guides you through configuration
3. **Token Setup** - Enter your Discord token securely
4. **Theme Selection** - Choose your preferred visual theme

## Main Interface

### Window Layout

```
┌─────────────────────────────────────────┐
│ [Title Bar]                    [ - □ × ] │
├─────────────┬───────────────────────────┤
│             │                           │
│  Sidebar    │     Main Content Area     │
│             │                           │
│  Navigation │     Dynamic Pages         │
│             │                           │
│             │                           │
├─────────────┼───────────────────────────┤
│             │     Console Output        │
│             │                           │
└─────────────┴───────────────────────────┘
```

### Key Components

- **Sidebar Navigation** - Switch between pages
- **Main Content** - Current page content  
- **Console** - Real-time logs and output
- **Status Bar** - Connection and bot status

## Navigation Pages

### 🏠 Home Page
- **Bot Status** - Online/offline indicator
- **Quick Stats** - Command count, server count
- **Recent Activity** - Latest actions and logs
- **Quick Actions** - Common tasks and shortcuts

### ⚙️ Settings Page
- **General Settings** - Prefix, theme, basic config
- **Message Settings** - Auto-delete, display style
- **Snipers** - Nitro/Privnote sniper configuration
- **Rich Presence** - Discord activity settings
- **API Keys** - Third-party service integration

### 📜 Scripts Page
- **Custom Scripts** - User-created automation
- **Script Editor** - Built-in code editor
- **Script Manager** - Enable/disable scripts
- **Templates** - Pre-made script examples

### 🛠️ Tools Page
- **Backup Manager** - Account backup/restore
- **Token Manager** - Secure token storage
- **Theme Editor** - Customize visual appearance
- **Font Manager** - Install/manage required fonts

### 💻 Console
- **Real-time Logs** - Live command output
- **Error Messages** - Debug information
- **Bot Events** - Connection status, events
- **Command History** - Recent command execution

## Configuration Through GUI

### Basic Settings

**Bot Configuration:**
- **Token** - Your Discord account token
- **Prefix** - Command prefix (default: `.`)
- **Theme** - Visual theme selection

**Message Settings:**
- **Auto Delete** - Automatic message deletion timer
- **Display Style** - Image embeds vs text blocks
- **Rich Embeds** - Enhanced message formatting

### Advanced Settings

**Snipers:**
- **Nitro Sniper** - Enable/disable, webhook URLs
- **Privnote Sniper** - Configuration and notifications
- **Invalid Handling** - Skip expired/invalid items

**Rich Presence:**
- **Enable/Disable** - Show activity on Discord
- **Custom Status** - Personalized rich presence
- **Images** - Large/small images and tooltips

**Session Management:**
- **Device Spoofing** - Appear as desktop/mobile
- **Session Settings** - Advanced connection options

## Theme Customization

### Built-in Themes
- **Ghost** (Default) - Dark theme with blue accents
- **Light** - Clean light theme
- **High Contrast** - Accessibility-focused
- **Custom** - User-created themes

### Theme Editor
1. Navigate to **Tools > Theme Editor**
2. Select base theme or create new
3. Customize colors, fonts, spacing
4. Preview changes in real-time
5. Save and apply custom theme

### Theme Structure
```json
{
    "colors": {
        "primary": "#color",
        "secondary": "#color", 
        "accent": "#color",
        "background": "#color",
        "text": "#color"
    },
    "fonts": {
        "main": "Font Name",
        "mono": "Monospace Font"
    }
}
```

## Script Management

### Built-in Script Editor
- **Syntax Highlighting** - Python code highlighting
- **Auto-completion** - Smart suggestions
- **Error Detection** - Real-time syntax checking
- **Debug Output** - Script execution logs

### Script Features
- **Event Handlers** - React to Discord events
- **Command Extensions** - Add custom commands  
- **Automation** - Scheduled tasks
- **Integration** - Access Ghost's API

### Example Script
```python
# Custom command example
@bot.command(name="customcmd")
async def custom_command(ctx):
    await ctx.send("Hello from custom script!")

# Event handler example  
@bot.event
async def on_message(message):
    if "keyword" in message.content:
        # Custom logic here
        pass
```

## Console Usage

### Reading Logs
- **Timestamps** - All events are timestamped
- **Log Levels** - Info, Warning, Error color coding
- **Filtering** - Show/hide specific log types
- **Search** - Find specific log entries

### Console Commands
- **Clear** - Clear console output
- **Export** - Save logs to file
- **Filter** - Toggle log level visibility
- **Copy** - Copy selected text

## Shortcuts and Tips

### Keyboard Shortcuts
- `Ctrl+S` - Save current settings
- `Ctrl+R` - Restart bot
- `Ctrl+Q` - Quit application
- `F5` - Refresh current page
- `F11` - Toggle fullscreen

### Productivity Tips
1. **Pin frequently used pages** to sidebar
2. **Use console search** to find specific events
3. **Create script templates** for common tasks
4. **Export configurations** before major changes
5. **Use themes** to reduce eye strain

## Troubleshooting GUI Issues

### Font Problems
If you see font-related errors:
1. Ghost will show a font check dialog
2. Follow installation prompts
3. Restart Ghost after font installation
4. Use "Skip font check" if needed (may cause visual issues)

### Performance Issues
- **Reduce console output** - Disable verbose logging
- **Close unused pages** - Minimize memory usage
- **Update themes** - Some themes are more efficient
- **Restart regularly** - Fresh start improves performance

### Display Issues
- **Check DPI settings** - High DPI awareness is enabled
- **Update graphics drivers** - Ensure compatibility
- **Try different themes** - Some work better on specific systems
- **Adjust window size** - Minimum 600x530 pixels

### Connection Problems
- **Check token validity** - Expired tokens cause issues
- **Verify internet** - Stable connection required
- **Review proxy settings** - VPN/proxy may interfere
- **Check Discord status** - Service outages affect connectivity

## Advanced Features

### Multi-Instance Support
- Run multiple Ghost instances with different configs
- Separate console outputs
- Independent theme settings
- Isolated script environments

### Configuration Profiles
- Save multiple configuration sets
- Quick switching between profiles
- Export/import settings
- Team configuration sharing

### Plugin System
- Third-party GUI extensions
- Custom page additions
- Enhanced functionality
- Community-developed features

## Security Considerations

### Token Safety
- **Never screenshot** token fields
- **Use secure storage** - Encrypted config files
- **Regular rotation** - Change tokens periodically
- **Monitor access** - Watch for unauthorized usage

### Script Security
- **Review scripts** before running
- **Sandbox execution** - Limited script permissions
- **Source verification** - Only trusted script sources
- **Regular audits** - Check script behavior

## Getting Help

### Built-in Help
- **Tooltips** - Hover over elements for help
- **Help Pages** - Integrated documentation
- **Status Indicators** - Visual feedback on issues
- **Error Messages** - Detailed problem descriptions

### External Resources
- [Commands Reference](Commands.md) - All available commands
- [Configuration Guide](Configuration.md) - Detailed config options
- [Troubleshooting](Troubleshooting.md) - Common issues
- [Discord Community](https://discord.gg/ayz7eYvFsm) - User support

---

The Ghost GUI provides a powerful, user-friendly interface for managing your selfbot. Take time to explore all features and customize the interface to your preferences!