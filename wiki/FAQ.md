# Frequently Asked Questions (FAQ)

This page answers the most commonly asked questions about Ghost. If you don't find your answer here, check the [Troubleshooting Guide](Troubleshooting.md) or join our [Discord community](https://discord.gg/ayz7eYvFsm).

## General Questions

### What is Ghost?

Ghost is an advanced open-source Discord selfbot with 150+ commands and a custom GUI. It allows you to automate tasks, enhance your Discord experience, and customize your interactions.

### Is Ghost safe to use?

**Important:** Ghost is against Discord's Terms of Service and can result in account termination. Use at your own risk, preferably on alternative accounts, and avoid using it in large servers or those moderated by Discord staff.

### Is Ghost free?

Yes, Ghost is completely free and open-source. However, some features may require API keys from third-party services (like weather commands requiring OpenWeatherMap keys).

### What platforms does Ghost support?

Ghost officially supports:
- **Windows** 10/11
- **macOS** (Intel and Apple Silicon)
- **Linux** (Ubuntu, Debian, Fedora, Arch, etc.)

## Installation & Setup

### What Python version do I need?

Ghost requires **Python 3.10 or higher**. Check your version with:
```bash
python --version
```

### How do I get my Discord token?

Follow [this detailed guide](https://gist.github.com/bennyscripts/49ecc1eade1796ee1d7cad9d165ffe67) to safely extract your Discord token. **Never share your token with anyone!**

### Can I use Ghost without a GUI?

Yes! Ghost automatically detects headless environments and runs in CLI mode. You can also force CLI mode by setting `DISPLAY=""` on Linux/macOS.

### Why do I need to install fonts?

Ghost's GUI uses custom fonts for the best visual experience. The built-in font checker will help you install required fonts like "Host Grotesk".

### How do I update Ghost?

```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

## Features & Functionality

### How many commands does Ghost have?

Ghost includes 150+ commands across 12 categories:
- General, Account, Fun, Info, Image, Text, Utility
- Moderation, Theming, Sniper, NSFW, Abuse

### Can I create custom commands?

Yes! Ghost has a powerful scripting system that allows you to:
- Create custom commands
- Handle Discord events
- Schedule automated tasks
- Integrate with external APIs

### What are snipers?

Snipers are features that automatically detect and claim:
- **Nitro codes** - Claim free Discord Nitro
- **Privnote links** - Read self-destructing messages

### Can I customize the appearance?

Absolutely! Ghost features:
- **GUI themes** - Customize the interface colors
- **Message themes** - Change command output styling
- **Custom themes** - Create your own themes

## Usage & Commands

### What's the default command prefix?

The default prefix is `.` (period). You can change it in `config.json`:
```json
{
    "prefix": "!"
}
```

### How do I see all commands?

Use the help command:
```
.help              # Show all command categories
.help [command]    # Get help for specific command
.[category]        # Show commands in a category (e.g., .fun)
```

### Can I use Ghost in DMs?

Yes, Ghost works in:
- Server channels
- Direct messages
- Group DMs

### Why are some commands not working?

Common issues:
- Wrong prefix
- Missing permissions
- Invalid command syntax
- Rate limiting
- Account restrictions

## Safety & Security

### Will I get banned for using Ghost?

Using Ghost violates Discord's Terms of Service and **can result in account termination**. Risk factors:
- **High risk:** Large servers, Discord staff servers, abuse commands
- **Medium risk:** Active moderation, obvious automation
- **Lower risk:** Private servers, careful usage, legitimate-looking activity

### How can I reduce ban risk?

1. **Use alt accounts** for selfbot activities
2. **Avoid abuse commands** completely
3. **Don't use in large servers** (especially Discord partner servers)
4. **Moderate your usage** - don't spam commands
5. **Keep activity natural** - don't make it obvious you're using a bot

### What if my account gets banned?

Unfortunately, Discord bans for ToS violations are typically permanent and not appealable. This is why we strongly recommend:
- Using disposable/alt accounts
- Understanding the risks
- Being extremely careful with usage

### Is my token secure?

Your token security depends on you:
- **Never share your token**
- **Use secure storage** (encrypted config files)
- **Don't screenshot** token fields
- **Monitor for unauthorized access**
- **Rotate tokens regularly**

## Technical Issues

### Ghost won't start. What should I do?

1. Check Python version (3.10+ required)
2. Install dependencies: `pip install -r requirements.txt`
3. Verify token is correct in config.json
4. Check the [Troubleshooting Guide](Troubleshooting.md)

### The GUI looks broken or fonts are missing

1. Let Ghost's font checker install required fonts
2. Restart Ghost after font installation
3. Try a different theme
4. Check display scaling settings

### Commands are slow or timing out

1. Check your internet connection
2. Verify Discord isn't experiencing issues
3. Reduce command frequency
4. Use `"style": "codeblock"` for faster responses

### Snipers aren't working

**Nitro Sniper:**
- Ensure `"enabled": true` in config
- Check internet speed and latency
- Verify webhook URL if using notifications

**Privnote Sniper:**
- Enable in configuration
- Check message scanning is working
- Test with fresh Privnote links

## Configuration

### Where is the config file?

The configuration file is `config.json` in the Ghost root directory. If it doesn't exist, copy from `config.example.json`.

### Can I have multiple configs?

Yes, you can:
- Create multiple config files
- Use different configs for different purposes
- Switch configs by renaming files

### How do I backup my settings?

```bash
cp config.json config.backup.json
```

For account backups, use Ghost's built-in backup commands.

### What APIs does Ghost support?

Ghost can integrate with:
- **SerpAPI** - Enhanced search functionality
- **Weather APIs** - Weather commands
- **Custom APIs** - Through scripting system

## Scripting & Customization

### Do I need to know Python to use Ghost?

Not for basic usage! However, Python knowledge helps with:
- Creating custom scripts
- Advanced configuration
- Troubleshooting issues
- Contributing to development

### Can I share my custom scripts?

Yes! The community welcomes script sharing:
- Share in Discord community
- Create GitHub repositories
- Follow security best practices
- Include documentation

### How do I install community scripts?

1. Download script files
2. Place in appropriate `scripts/` directory
3. Restart Ghost
4. Configure as needed

### Can scripts break Ghost?

Poorly written scripts can:
- Cause crashes
- Create security vulnerabilities
- Violate Discord ToS
- Impact performance

Always review scripts before installing!

## Updates & Development

### How often is Ghost updated?

Ghost is actively maintained with:
- Regular bug fixes
- New feature additions
- Security updates
- Community contributions

### Can I contribute to Ghost?

Yes! Contributions are welcome:
- **Bug reports** - Help identify issues
- **Feature requests** - Suggest improvements
- **Code contributions** - Submit pull requests
- **Documentation** - Improve guides and wiki

### Where can I request features?

1. Check existing GitHub issues
2. Join Discord community discussions
3. Create detailed feature requests
4. Consider implementing yourself via scripting

### Is there a roadmap?

Check the GitHub repository for:
- Open issues and milestones
- Planned features
- Development priorities
- Community suggestions

## Legal & Ethical

### Is selfbotting legal?

Selfbotting itself isn't illegal, but:
- It violates Discord's Terms of Service
- Can result in account termination
- May violate server rules
- Could impact others' experiences

### What about user privacy?

- Ghost only accesses what your Discord account can see
- No data is sent to external servers (unless using API features)
- Respect others' privacy when using commands
- Be mindful of data collection in scripts

### Can I use Ghost for business?

**Not recommended!** Business use of selfbots:
- Violates Discord ToS
- Risks account termination
- Could impact business operations
- May violate platform agreements

## Community & Support

### Where can I get help?

1. **This FAQ** - Common questions
2. **[Troubleshooting Guide](Troubleshooting.md)** - Technical issues
3. **[Discord Community](https://discord.gg/ayz7eYvFsm)** - User support
4. **GitHub Issues** - Bug reports and feature requests

### How can I help other users?

- Answer questions in Discord
- Share useful scripts and themes
- Report bugs and issues
- Improve documentation
- Contribute code

### Are there usage examples?

Yes! Examples are available in:
- Command help (`{prefix}help [command]`)
- Script templates
- Community Discord
- This wiki documentation

## Miscellaneous

### Can I run multiple Ghost instances?

Yes, but:
- Use different config files
- Avoid the same Discord account
- Be careful with rate limits
- Monitor resource usage

### Does Ghost work with Discord PTB/Canary?

Ghost should work with all Discord clients since it uses your account token, not a specific client.

### Can I use Ghost on mobile?

Ghost is designed for desktop use. While technically possible on mobile Linux environments, it's not recommended or officially supported.

### What about Discord updates?

Ghost may occasionally break with Discord updates. The development team works to fix compatibility issues quickly.

## Still Need Help?

If your question isn't answered here:

1. **Search the wiki** - Check other documentation pages
2. **Review error messages** - Often contain helpful information
3. **Join our Discord** - Get help from the community
4. **Create an issue** - For bugs or feature requests

Remember: Ghost is a community project, and user support relies on community members helping each other!

---

**Disclaimer:** Ghost is provided as-is for educational and personal use. Users are responsible for understanding and accepting the risks associated with using Discord selfbots.