# Commands Reference

Ghost includes 150+ commands across 12 categories. This comprehensive reference documents all available commands.

## Command Usage

All commands use the prefix specified in your config (default: `.`)

**Format**: `{prefix}{command} [required] <optional>`

- `[required]` - Required parameters
- `<optional>` - Optional parameters 
- `{prefix}` - Your configured command prefix

## Quick Command List

Use `{prefix}help` to see all available commands or `{prefix}help [command]` for specific command info.

---

## 🏠 General Commands

Basic commands and help functionality.

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `help` | Get help with commands | `help <command>` | - |

---

## 👤 Account Commands

Manage your Discord account settings and backups.

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `account` | Account commands menu | `account` | `acc` |
| `backups` | List your account backups | `backups` | - |
| `hypesquad` | Change your hypesquad house | `hypesquad [house]` | `changehypesquad` |
| `status` | Change your status | `status [status]` | `changestatus` |
| `customstatus` | Set custom status | `customstatus [text]` | `changecustomstatus` |
| `clearstatus` | Clear custom status | `clearstatus` | - |
| `playing` | Set playing status | `playing [game]` | `changeplaying` |
| `streaming` | Set streaming status | `streaming [title]` | `changestreaming` |
| `nickname` | Change nickname | `nickname [name]` | `changenickname`, `nick` |
| `clearnickname` | Clear nickname | `clearnickname` | `resetnickname`, `clearnick` |
| `discordtheme` | Change Discord theme | `discordtheme [theme]` | `changetheme` |
| `yoinkrpc` | Copy user's rich presence | `yoinkrpc [user]` | `rpcyoink`, `stealrpc` |

**Account Status Options:**
- `online` - Green dot
- `idle` - Yellow dot  
- `dnd` - Red dot
- `invisible` - Offline appearance

**Hypesquad Houses:**
- `bravery` - Purple house
- `brilliance` - Yellow house
- `balance` - Green house

---

## 🎮 Fun Commands

Entertainment and games.

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `fun` | Fun commands menu | `fun <page>` | - |
| `rickroll` | Never gonna give you up | `rickroll` | - |
| `coinflip` | Flip a coin | `coinflip` | `cf` |
| `iq` | Get user's IQ rating | `iq [user]` | `howsmart`, `iqrating` |
| `howgay` | Get gayness percentage | `howgay [user]` | `gay`, `gayrating` |
| `howblack` | Get blackness percentage | `howblack [user]` | `black`, `blackrating` |
| `pp` | Get user's size | `pp [user]` | `dick`, `dicksize`, `penis` |
| `rps` | Rock paper scissors | `rps` | - |

---

## 📊 Info Commands

Information gathering and lookup tools.

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `info` | Info commands menu | `info <page>` | `information` |
| `iplookup` | Lookup IP address info | `iplookup [ip]` | `ipinfo` |
| `userinfo` | Get user information | `userinfo <user>` | `ui` |

---

## 🖼️ Image Commands

Image manipulation and generation.

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `img` | Image commands menu | `img <page>` | - |
| (Various image manipulation commands) | | | |

---

## 📝 Text Commands

Text manipulation and formatting tools.

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `text` | Text commands menu | `text <page>` | - |
| (Various text manipulation commands) | | | |

---

## 🛠️ Utility Commands

Useful tools and utilities.

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `util` | Utility commands menu | `util <page>` | - |
| (Various utility commands) | | | |

---

## 🛡️ Moderation Commands

Server management tools (use with caution).

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `mod` | Moderation commands menu | `mod <page>` | - |
| (Various moderation commands) | | | |

---

## 🎨 Theming Commands

Theme management and customization.

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `theming` | Theming commands menu | `theming <page>` | - |
| (Various theming commands) | | | |

---

## 🎯 Sniper Commands

Nitro and Privnote sniping functionality.

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `sniper` | Sniper commands menu | `sniper <page>` | - |
| (Various sniper commands) | | | |

---

## 🔞 NSFW Commands

Adult content commands (18+ only).

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `nsfw` | NSFW commands menu | `nsfw <page>` | - |
| (Various NSFW commands) | | | |

⚠️ **Warning**: These commands are for adult users only and should be used responsibly.

---

## ⚠️ Abuse Commands

Potentially harmful commands (use with extreme caution).

| Command | Description | Usage | Aliases |
|---------|-------------|--------|---------|
| `abuse` | Abuse commands menu | `abuse <page>` | - |
| `spam` | Spam messages | `spam [amount] [message]` | - |
| `servernuke` | Server destruction | `servernuke` | `nukeserver` |
| `channelflood` | Create many channels | `channelflood [name]` | - |
| `channelspam` | Spam channel messages | `channelspam [amount] [message]` | - |
| `channelping` | Ping user in all channels | `channelping [user] [amount]` | - |
| `massping` | Ping all server users | `massping [amount] [guild_id]` | `hahafunny` |
| `pollspam` | Spam polls | `pollspam` | - |

🚨 **EXTREME WARNING**: These commands can result in immediate account termination. Use only on test servers with disposable accounts. We are not responsible for any consequences.

---

## Command Categories Summary

| Category | Count | Risk Level | Description |
|----------|-------|------------|-------------|
| General | 1 | ✅ Safe | Basic help commands |
| Account | 12+ | ⚠️ Low | Account management |
| Fun | 8+ | ✅ Safe | Entertainment commands |
| Info | 3+ | ✅ Safe | Information gathering |
| Image | 10+ | ✅ Safe | Image manipulation |
| Text | 10+ | ✅ Safe | Text tools |
| Utility | 15+ | ✅ Safe | Useful utilities |
| Moderation | 10+ | ⚠️ Medium | Server management |
| Theming | 5+ | ✅ Safe | Customization |
| Sniper | 5+ | ⚠️ Medium | Content sniping |
| NSFW | 8+ | ⚠️ Medium | Adult content |
| Abuse | 8+ | 🚨 High | Destructive actions |

## Command Tips

### Safe Usage
1. **Test commands** on private servers first
2. **Read descriptions** carefully before using
3. **Avoid abuse commands** unless absolutely necessary
4. **Use appropriate channels** for NSFW content

### Performance
1. **Use aliases** for frequently used commands
2. **Check help pages** with `{prefix}help [command]`
3. **Use command menus** to browse categories

### Risk Management
1. **Never use abuse commands** on important servers
2. **Be cautious with moderation** commands
3. **Respect server rules** and Discord TOS
4. **Use alt accounts** for high-risk activities

## Examples

### Basic Usage
```
.help                    # Show all commands
.help userinfo          # Get help for specific command
.userinfo @someone      # Get user information
.coinflip               # Flip a coin
```

### Account Management
```
.status dnd             # Set status to Do Not Disturb
.customstatus Coding    # Set custom status
.nickname NewName       # Change nickname
.hypesquad bravery     # Join purple hypesquad
```

### Information
```
.iplookup 8.8.8.8      # Lookup Google's DNS
.userinfo              # Your own info
.userinfo @friend      # Friend's info
```

## Getting More Help

- Use `{prefix}[category]` to see category-specific commands
- Use `{prefix}help [command]` for detailed command help
- Check the [Troubleshooting Guide](Troubleshooting.md) for issues
- Join our [Discord community](https://discord.gg/ayz7eYvFsm) for support

---

**Remember**: Always use Ghost responsibly and in accordance with Discord's Terms of Service. We are not responsible for any consequences resulting from misuse of these commands.