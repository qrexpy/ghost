# Installation Guide

This guide will walk you through installing and setting up Ghost on your system.

## Prerequisites

Before installing Ghost, ensure you have:

- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Discord account** with a valid token
- **Internet connection**

## Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
git clone https://github.com/qrexpy/ghost
cd ghost
```

## Step 2: Create Virtual Environment

### On Windows:
```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

### On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Step 3: Install Dependencies

With your virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

## Step 4: Get Your Discord Token

⚠️ **Warning**: Your Discord token is sensitive information. Never share it with anyone!

1. Open Discord in your web browser
2. Press `F12` to open Developer Tools
3. Go to the `Network` tab
4. Send a message in any channel
5. Look for a request to `https://discord.com/api/v*/messages`
6. Click on it and find the `Authorization` header
7. Copy the token (it should start with a long string of characters)

For a detailed guide with screenshots, follow [this guide](https://gist.github.com/bennyscripts/49ecc1eade1796ee1d7cad9d165ffe67).

## Step 5: Configure Ghost

1. Copy the example configuration file:
   ```bash
   cp config.example.json config.json
   ```

2. Edit `config.json` with your preferred text editor:
   ```json
   {
       "token": "YOUR_DISCORD_TOKEN_HERE",
       "prefix": ".",
       "theme": "ghost"
   }
   ```

3. Replace `YOUR_DISCORD_TOKEN_HERE` with your actual Discord token

## Step 6: Run Ghost

### GUI Mode (Recommended):
```bash
python ghost.py
```

### CLI Mode (Headless):
```bash
export DISPLAY=  # On Linux/macOS
python ghost.py
```

Or set the environment variable on Windows and run.

## Platform-Specific Notes

### Windows
- Ghost is developed on macOS, so Windows builds may have issues
- Running from source code (as shown above) works reliably on Windows
- Make sure to use `python` instead of `python3` in commands

### macOS
- No special requirements
- Ghost works natively on macOS

### Linux
- If running headless (no display), Ghost will automatically use CLI mode
- For GUI mode, ensure you have a display server running

## Troubleshooting Installation

### Python Version Issues
If you get version errors:
```bash
python --version  # Should show 3.10 or higher
```

If not, install a newer Python version or use:
```bash
python3.10 ghost.py  # Or python3.11, python3.12, etc.
```

### Permission Errors
On Linux/macOS, you might need to make the script executable:
```bash
chmod +x ghost.py
```

### SSL Certificate Errors
Ghost automatically handles SSL certificates using the `certifi` package. If you still encounter SSL errors, try:
```bash
pip install --upgrade certifi
```

### Missing Dependencies
If imports fail, try reinstalling dependencies:
```bash
pip install --force-reinstall -r requirements.txt
```

### Font Issues (GUI Mode)
If you encounter font-related errors:
1. Ghost will automatically check for required fonts
2. Follow the font installation prompts
3. You can skip font checks by setting the appropriate config option

## First-Time Setup

When you first run Ghost:

1. **GUI Mode**: A setup window will guide you through initial configuration
2. **CLI Mode**: You'll be prompted to enter your token if not configured

## Updating Ghost

To update to the latest version:

```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

## Security Considerations

- **Never share your Discord token**
- **Keep your token secure** - don't commit it to version control
- **Use Ghost responsibly** - respect Discord's Terms of Service
- **Consider using an alt account** for selfbot activities

## Next Steps

Once Ghost is installed and configured:

1. Read the [Configuration Guide](Configuration.md) for advanced settings
2. Explore the [Commands Reference](Commands.md) to learn available commands
3. Check out the [GUI Usage Guide](GUI-Usage.md) if using GUI mode
4. Review [Safety & Legal](Safety-and-Legal.md) considerations

---

Need help? Check our [Troubleshooting Guide](Troubleshooting.md) or join our [Discord community](https://discord.gg/ayz7eYvFsm).