# Troubleshooting Guide

This guide covers common issues and their solutions when using Ghost. Before creating an issue, please check this guide first.

## General Issues

### Ghost Won't Start

**Symptoms:**
- Application fails to launch
- Error messages on startup
- Immediate crash

**Solutions:**

1. **Check Python Version:**
   ```bash
   python --version  # Should be 3.10 or higher
   ```
   If version is too old, install Python 3.10+

2. **Verify Dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Check File Permissions:**
   ```bash
   chmod +x ghost.py  # Linux/macOS
   ```

4. **Clear Cache:**
   ```bash
   rm -rf __pycache__/  # Remove Python cache
   rm -rf .venv/        # Delete and recreate venv
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Invalid Token Errors

**Symptoms:**
- "Invalid token" error message
- Login failures
- Authorization errors

**Solutions:**

1. **Get Fresh Token:**
   - Open Discord in browser
   - Follow [token guide](https://gist.github.com/bennyscripts/49ecc1eade1796ee1d7cad9d165ffe67)
   - Replace token in config.json

2. **Check Token Format:**
   - Token should be a long string of characters
   - No spaces or extra characters
   - Properly quoted in JSON

3. **Account Issues:**
   - Ensure account isn't banned
   - Check if account has 2FA enabled
   - Verify account is in good standing

### Connection Problems

**Symptoms:**
- Frequent disconnections
- Timeout errors
- Network-related failures

**Solutions:**

1. **Check Internet Connection:**
   ```bash
   ping discord.com
   ```

2. **Proxy/VPN Issues:**
   - Disable VPN temporarily
   - Check proxy settings
   - Try different network

3. **Firewall Settings:**
   - Allow Python through firewall
   - Check port restrictions
   - Whitelist Discord domains

## GUI-Specific Issues

### Font Problems

**Symptoms:**
- Missing text or symbols
- Font warning dialogs
- Visual glitches

**Solutions:**

1. **Install Required Fonts:**
   - Let Ghost's font checker install fonts
   - Manually install Host Grotesk font
   - Restart Ghost after font installation

2. **Skip Font Check (Temporary):**
   ```python
   # In config.json, add:
   "skip_font_check": true
   ```

3. **System Font Issues:**
   ```bash
   # Linux: Install font packages
   sudo apt install fonts-liberation fonts-dejavu
   
   # macOS: Install via Homebrew
   brew install font-hack-nerd-font
   
   # Windows: Download and install fonts manually
   ```

### Display Issues

**Symptoms:**
- Blurry text
- Incorrect scaling
- Layout problems

**Solutions:**

1. **DPI Scaling:**
   - Ghost enables high DPI awareness automatically
   - Adjust system display scaling
   - Try different theme

2. **Resolution Problems:**
   - Minimum window size: 600x530
   - Ensure adequate screen resolution
   - Try windowed mode instead of fullscreen

3. **Graphics Driver:**
   - Update graphics drivers
   - Try software rendering mode
   - Check OpenGL support

### GUI Won't Start

**Symptoms:**
- Blank window
- Immediate GUI crash
- Falls back to CLI mode

**Solutions:**

1. **Display Environment:**
   ```bash
   # Check display variable
   echo $DISPLAY
   
   # Set display if needed
   export DISPLAY=:0
   ```

2. **Headless Environment:**
   - GUI requires display server
   - Use CLI mode on headless systems
   - Consider VNC for remote GUI

3. **Dependencies:**
   ```bash
   # Install GUI dependencies
   pip install ttkbootstrap tkinter
   ```

## Command Issues

### Commands Not Working

**Symptoms:**
- Commands don't respond
- "Command not found" errors
- Partial functionality

**Solutions:**

1. **Check Prefix:**
   ```json
   // In config.json
   "prefix": "."  // Ensure correct prefix
   ```

2. **Permission Issues:**
   - Check Discord permissions
   - Verify bot can send messages
   - Check channel restrictions

3. **Command Conflicts:**
   - Check for duplicate commands
   - Disable conflicting scripts
   - Review custom commands

### Slow Response Times

**Symptoms:**
- Commands take long to execute
- Timeouts
- Performance issues

**Solutions:**

1. **Optimize Settings:**
   ```json
   {
       "message_settings": {
           "auto_delete_delay": 0,  // Disable auto-delete
           "style": "codeblock"     // Faster than image
       }
   }
   ```

2. **Network Optimization:**
   - Use wired connection
   - Reduce concurrent commands
   - Check API rate limits

3. **System Resources:**
   - Close unnecessary applications
   - Increase available RAM
   - Use SSD instead of HDD

## Configuration Issues

### Config File Problems

**Symptoms:**
- "Config error" messages
- Settings not saving
- JSON syntax errors

**Solutions:**

1. **Validate JSON:**
   ```bash
   python -m json.tool config.json
   ```

2. **Reset Configuration:**
   ```bash
   cp config.example.json config.json
   ```

3. **Common JSON Errors:**
   - Missing commas between items
   - Trailing commas (not allowed)
   - Unmatched quotes or brackets
   - Invalid escape sequences

### Theme Issues

**Symptoms:**
- Theme not loading
- Visual glitches
- Missing theme elements

**Solutions:**

1. **Reset Theme:**
   ```json
   "theme": "ghost"  // Reset to default
   ```

2. **Theme File Issues:**
   - Check theme JSON syntax
   - Verify theme file location
   - Restart Ghost after theme changes

3. **Custom Theme Problems:**
   - Validate color format (#hexadecimal)
   - Check all required properties
   - Test with default theme first

## Sniper Issues

### Nitro Sniper Not Working

**Symptoms:**
- Codes not detected
- False positives
- No notifications

**Solutions:**

1. **Configuration:**
   ```json
   {
       "snipers": {
           "nitro": {
               "enabled": true,
               "ignore_invalid": false,
               "webhook": "your_webhook_url"
           }
       }
   }
   ```

2. **Network Timing:**
   - Ensure fast internet connection
   - Reduce latency to Discord
   - Check for rate limiting

3. **Code Detection:**
   - Check Discord message history
   - Verify code format recognition
   - Test with known valid codes

### Privnote Sniper Issues

**Symptoms:**
- Links not intercepted
- Access failures
- Content not retrieved

**Solutions:**

1. **Enable Sniper:**
   ```json
   {
       "snipers": {
           "privnote": {
               "enabled": true,
               "ignore_invalid": false
           }
       }
   }
   ```

2. **Link Detection:**
   - Verify Privnote URL format
   - Check message scanning
   - Test with fresh links

## Platform-Specific Issues

### Windows Issues

**Common Problems:**
- Path separator issues
- PowerShell execution policy
- Windows Defender interference

**Solutions:**

1. **Execution Policy:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Antivirus Exclusion:**
   - Add Ghost folder to antivirus exclusions
   - Whitelist Python processes
   - Temporarily disable real-time scanning

3. **Path Issues:**
   - Use forward slashes in paths
   - Avoid spaces in directory names
   - Use short path names

### macOS Issues

**Common Problems:**
- Gatekeeper warnings
- Permission dialogs
- Homebrew conflicts

**Solutions:**

1. **Gatekeeper:**
   ```bash
   sudo xattr -r -d com.apple.quarantine /path/to/ghost
   ```

2. **Permissions:**
   - Grant terminal permissions in System Preferences
   - Allow Python in Privacy settings
   - Accept security prompts

### Linux Issues

**Common Problems:**
- Missing system packages
- Display server issues
- Permission problems

**Solutions:**

1. **Install Dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3-tk python3-pip
   
   # Fedora
   sudo dnf install python3-tkinter python3-pip
   
   # Arch
   sudo pacman -S tk python-pip
   ```

2. **Display Issues:**
   ```bash
   # Check X11
   echo $DISPLAY
   xhost +local:
   
   # Wayland compatibility
   export GDK_BACKEND=x11
   ```

## Performance Issues

### High Memory Usage

**Symptoms:**
- Ghost consumes excessive RAM
- System slowdown
- Out of memory errors

**Solutions:**

1. **Optimize Settings:**
   - Disable unused snipers
   - Reduce auto-delete delay
   - Limit console output

2. **Memory Leaks:**
   - Restart Ghost regularly
   - Check for script issues
   - Monitor memory usage

3. **System Optimization:**
   - Close other applications
   - Increase virtual memory
   - Use 64-bit Python

### High CPU Usage

**Symptoms:**
- Constant high CPU utilization
- System becomes unresponsive
- Fan noise increases

**Solutions:**

1. **Identify Cause:**
   - Check running scripts
   - Monitor command usage
   - Review event handlers

2. **Optimization:**
   - Reduce polling frequency
   - Optimize scripts
   - Disable unnecessary features

## Network Issues

### Rate Limiting

**Symptoms:**
- "Rate limited" errors
- Commands failing
- Temporary blocks

**Solutions:**

1. **Respect Rate Limits:**
   - Reduce command frequency
   - Add delays between commands
   - Use rate limit handling

2. **Configuration:**
   ```python
   # Add delays in scripts
   import asyncio
   await asyncio.sleep(1)  # 1 second delay
   ```

### API Errors

**Symptoms:**
- HTTP error codes
- Discord API failures
- Service unavailable errors

**Solutions:**

1. **Check Discord Status:**
   - Visit Discord status page
   - Check for ongoing incidents
   - Wait for service restoration

2. **Retry Logic:**
   - Implement exponential backoff
   - Handle transient errors
   - Log error details

## Debugging Tips

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Console Debugging

1. **Check Console Output:**
   - Look for error messages
   - Note warning patterns
   - Check connection status

2. **Verbose Mode:**
   ```bash
   python ghost.py --verbose
   ```

### Log Files

```python
# Enable file logging
import logging
logging.basicConfig(
    filename='ghost.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Getting Help

### Self-Help Resources

1. **Check this guide first**
2. **Review error messages carefully**
3. **Search existing issues on GitHub**
4. **Check Discord discussions**

### Community Support

1. **Discord Community:**
   [![Discord](https://discord.com/api/guilds/1302632843176050738/widget.png?style=banner3)](https://discord.gg/ayz7eYvFsm)

2. **GitHub Issues:**
   - Create detailed issue reports
   - Include error messages
   - Provide system information
   - Describe reproduction steps

### Issue Report Template

When creating an issue, include:

```
**Environment:**
- OS: [Windows/macOS/Linux + version]
- Python version: [output of python --version]
- Ghost version: [latest commit hash]

**Problem Description:**
[Clear description of the issue]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [...]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Error Messages:**
[Paste any error messages]

**Additional Context:**
[Any other relevant information]
```

---

If your issue isn't covered here, don't hesitate to reach out to the community for help!