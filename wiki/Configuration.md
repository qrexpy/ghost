# Configuration Guide

Ghost uses a JSON configuration file (`config.json`) to store settings. This guide explains all available configuration options.

## Configuration File Location

The configuration file is located at `config.json` in the Ghost root directory. If it doesn't exist, copy it from `config.example.json`:

```bash
cp config.example.json config.json
```

## Basic Configuration

### Essential Settings

```json
{
    "token": "YOUR_DISCORD_TOKEN",
    "prefix": ".",
    "theme": "ghost"
}
```

| Setting | Description | Default | Required |
|---------|-------------|---------|----------|
| `token` | Your Discord account token | `""` | ✅ Yes |
| `prefix` | Command prefix (what you type before commands) | `"."` | ✅ Yes |
| `theme` | Active theme name | `"ghost"` | ✅ Yes |

## Advanced Configuration

### API Integration

```json
{
    "apis": {
        "serpapi": "YOUR_SERPAPI_KEY"
    }
}
```

| Setting | Description | Required |
|---------|-------------|----------|
| `serpapi` | SerpAPI key for enhanced search functionality | ❌ Optional |

### Message Settings

```json
{
    "message_settings": {
        "auto_delete_delay": 15,
        "style": "image"
    }
}
```

| Setting | Description | Options | Default |
|---------|-------------|---------|---------|
| `auto_delete_delay` | Seconds before auto-deleting command messages | Any number | `15` |
| `style` | Message display style | `"image"`, `"codeblock"` | `"image"` |

### Session Spoofing

```json
{
    "session_spoofing": {
        "enabled": false,
        "device": "desktop"
    }
}
```

| Setting | Description | Options | Default |
|---------|-------------|---------|---------|
| `enabled` | Enable session spoofing | `true`, `false` | `false` |
| `device` | Device type to spoof | `"desktop"`, `"mobile"` | `"desktop"` |

⚠️ **Warning**: Session spoofing may increase detection risk. Use with caution.

### Snipers Configuration

Ghost includes snipers for Nitro codes and Privnote links:

```json
{
    "snipers": {
        "nitro": {
            "enabled": true,
            "ignore_invalid": false,
            "webhook": "",
            "name": "nitro"
        },
        "privnote": {
            "enabled": true,
            "ignore_invalid": false,
            "webhook": "",
            "name": "privnote"
        }
    }
}
```

#### Nitro Sniper

| Setting | Description | Default |
|---------|-------------|---------|
| `enabled` | Enable Nitro code sniping | `true` |
| `ignore_invalid` | Skip invalid/expired codes | `false` |
| `webhook` | Discord webhook URL for notifications | `""` |
| `name` | Display name for sniper | `"nitro"` |

#### Privnote Sniper

| Setting | Description | Default |
|---------|-------------|---------|
| `enabled` | Enable Privnote link sniping | `true` |
| `ignore_invalid` | Skip invalid links | `false` |
| `webhook` | Discord webhook URL for notifications | `""` |
| `name` | Display name for sniper | `"privnote"` |

### Rich Presence

```json
{
    "rich_presence": {
        "enabled": false,
        "client_id": "1018195507560063039",
        "state": "ghost aint dead",
        "details": "",
        "large_image": "ghost",
        "large_text": "",
        "small_image": "",
        "small_text": "",
        "name": "Ghost"
    }
}
```

| Setting | Description | Default |
|---------|-------------|---------|
| `enabled` | Show rich presence on Discord | `false` |
| `client_id` | Discord application client ID | `"1018195507560063039"` |
| `state` | Status text | `"ghost aint dead"` |
| `details` | Detail text | `""` |
| `large_image` | Large image key | `"ghost"` |
| `large_text` | Large image tooltip | `""` |
| `small_image` | Small image key | `""` |
| `small_text` | Small image tooltip | `""` |
| `name` | Application name | `"Ghost"` |

### Rich Embed Webhook

```json
{
    "rich_embed_webhook": "https://discord.com/api/webhooks/..."
}
```

URL for sending rich embed notifications.

## Complete Configuration Example

```json
{
    "token": "YOUR_DISCORD_TOKEN_HERE",
    "prefix": ".",
    "theme": "ghost",
    "apis": {
        "serpapi": "your_serpapi_key_here"
    },
    "message_settings": {
        "auto_delete_delay": 15,
        "style": "image"
    },
    "session_spoofing": {
        "enabled": false,
        "device": "desktop"
    },
    "snipers": {
        "nitro": {
            "enabled": true,
            "ignore_invalid": false,
            "webhook": "https://discord.com/api/webhooks/your_webhook_here",
            "name": "nitro"
        },
        "privnote": {
            "enabled": true,
            "ignore_invalid": false,
            "webhook": "",
            "name": "privnote"
        }
    },
    "rich_presence": {
        "enabled": false,
        "client_id": "1018195507560063039",
        "state": "ghost aint dead",
        "details": "",
        "large_image": "ghost",
        "large_text": "",
        "small_image": "",
        "small_text": "",
        "name": "Ghost"
    },
    "rich_embed_webhook": ""
}
```

## Configuration Tips

### Security Best Practices

1. **Never share your config file** - it contains sensitive tokens
2. **Use environment variables** for tokens in production:
   ```bash
   export GHOST_TOKEN="your_token_here"
   ```
3. **Add config.json to .gitignore** to prevent accidental commits
4. **Regularly rotate your Discord token** if compromised

### Performance Optimization

1. **Disable unused snipers** to reduce resource usage
2. **Adjust auto_delete_delay** based on your needs
3. **Use codeblock style** for faster message rendering

### Webhook Setup

To set up Discord webhooks for notifications:

1. Go to your Discord server settings
2. Navigate to Integrations → Webhooks
3. Create a new webhook
4. Copy the webhook URL
5. Paste it in the appropriate config field

## Configuration Validation

Ghost automatically validates your configuration on startup. Common issues:

- **Invalid JSON syntax** - Use a JSON validator
- **Missing required fields** - Check against the example
- **Invalid token format** - Ensure token is correct
- **Invalid theme name** - Use an existing theme

## Environment Variables

You can override config values with environment variables:

```bash
export GHOST_TOKEN="your_token"
export GHOST_PREFIX="!"
export GHOST_THEME="custom_theme"
```

## Configuration Management

### Backup Configuration
```bash
cp config.json config.backup.json
```

### Reset to Defaults
```bash
cp config.example.json config.json
```

### Update Configuration
Edit the file directly or use the GUI configuration panel (if available).

---

Next: Learn about available commands in the [Commands Reference](Commands.md)