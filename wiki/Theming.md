# Theming Guide

Ghost includes a powerful theming system that allows you to customize the visual appearance of both the GUI and command outputs. This guide covers creating, editing, and managing themes.

## Overview

Ghost supports two types of themes:
- **GUI Themes** - Control the appearance of the graphical interface
- **Message Themes** - Control how command outputs are displayed in Discord

## Built-in Themes

### GUI Themes
- **Ghost (Default)** - Dark theme with blue accents
- **Light** - Clean light theme with bright colors

### Message Themes
- **Ghost** - Default styling for command outputs
- **Custom themes** - User-created message themes

## Theme Commands

### Basic Theme Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `theming` | Show theming commands | `theming <page>` |
| `themes` | List all available themes | `themes` |
| `theme` | Change active theme | `theme [name]` |

### Viewing Themes

```bash
.themes                    # List all available themes
.theme                     # Show current theme info
.theme ghost              # Switch to 'ghost' theme
```

## GUI Theme Structure

GUI themes are stored in JSON format in the `data/` directory:

### Basic Structure
```json
{
    "themes": [
        {
            "theme_name": {
                "type": "dark",
                "colors": {
                    "primary": "#433dfb",
                    "secondary": "#222324", 
                    "success": "#0abf34",
                    "info": "#2b6eff",
                    "warning": "#f39c12",
                    "danger": "#ff341f",
                    "light": "#ADB5BD",
                    "dark": "#1a1c1c",
                    "bg": "#121111",
                    "fg": "#ffffff",
                    "selectbg": "#555555",
                    "selectfg": "#ffffff",
                    "border": "#121111",
                    "inputfg": "#ffffff",
                    "inputbg": "#2f2f2f",
                    "active": "#1F1F1F"
                }
            }
        }
    ]
}
```

### Color Properties

| Property | Description | Example |
|----------|-------------|---------|
| `primary` | Primary accent color | `#433dfb` |
| `secondary` | Secondary background | `#222324` |
| `success` | Success/positive color | `#0abf34` |
| `info` | Information color | `#2b6eff` |
| `warning` | Warning color | `#f39c12` |
| `danger` | Error/danger color | `#ff341f` |
| `light` | Light text/elements | `#ADB5BD` |
| `dark` | Dark backgrounds | `#1a1c1c` |
| `bg` | Main background | `#121111` |
| `fg` | Main foreground/text | `#ffffff` |
| `selectbg` | Selection background | `#555555` |
| `selectfg` | Selection text | `#ffffff` |
| `border` | Border colors | `#121111` |
| `inputfg` | Input text color | `#ffffff` |
| `inputbg` | Input background | `#2f2f2f` |
| `active` | Active element color | `#1F1F1F` |

## Creating Custom GUI Themes

### Method 1: JSON File Creation

1. **Copy existing theme**:
   ```bash
   cp data/gui_theme.json data/gui_theme_custom.json
   ```

2. **Edit the theme file**:
   ```json
   {
       "themes": [
           {
               "my_custom_theme": {
                   "type": "dark",
                   "colors": {
                       "primary": "#ff6b6b",
                       "secondary": "#4a4a4a",
                       "bg": "#2d2d2d",
                       "fg": "#ffffff"
                       // ... other colors
                   }
               }
           }
       ]
   }
   ```

3. **Apply the theme**:
   - Restart Ghost
   - The new theme will be available in settings

### Method 2: GUI Theme Editor

1. Open Ghost GUI
2. Navigate to **Tools > Theme Editor**
3. Select "Create New Theme"
4. Customize colors using color pickers
5. Preview changes in real-time
6. Save and apply

## Message Theme Customization

Message themes control how Ghost's command outputs appear in Discord.

### Theme Components

**Title Styling:**
- Color scheme
- Font styling
- Icon usage

**Description Formatting:**
- Text layout
- Color coding
- Emphasis styles

**Embed Structure:**
- Field organization
- Footer information
- Thumbnail/image usage

### Custom Message Themes

Create custom message themes by:

1. **Using theme commands** to modify existing themes
2. **Creating theme templates** for consistent styling
3. **Configuring embed settings** in config.json

## Theme Configuration

### Global Theme Settings

In `config.json`:
```json
{
    "theme": "ghost",
    "message_settings": {
        "style": "image",
        "auto_delete_delay": 15
    }
}
```

### Per-Command Theming

Some commands support theme overrides:
```bash
.command_name --theme custom_theme
```

## Advanced Theming

### Dynamic Themes

Create themes that change based on:
- **Time of day** - Automatic light/dark switching
- **Discord status** - Theme matches your Discord status
- **Server context** - Different themes per server

### Theme Inheritance

```json
{
    "my_theme": {
        "extends": "ghost",
        "colors": {
            "primary": "#custom_color"
            // Only override specific colors
        }
    }
}
```

### Font Customization

```json
{
    "fonts": {
        "main": "Host Grotesk",
        "mono": "JetBrains Mono",
        "size": {
            "small": 10,
            "normal": 12,
            "large": 14
        }
    }
}
```

## Theme Management

### Installing Themes

**From File:**
1. Copy theme file to `data/` directory
2. Restart Ghost
3. Theme appears in themes list

**From Community:**
1. Download community theme
2. Verify theme structure
3. Install using GUI or file copy

### Exporting Themes

**GUI Method:**
1. Tools > Theme Editor
2. Select theme to export
3. Click "Export Theme"
4. Save .json file

**Manual Method:**
Copy theme section from config file

### Sharing Themes

**Theme Package Structure:**
```
my_theme/
├── theme.json          # Theme definition
├── preview.png         # Theme preview image
├── README.md          # Theme description
└── assets/            # Additional resources
    ├── icons/
    └── fonts/
```

## Color Theory for Themes

### Accessibility Considerations

**Contrast Ratios:**
- Text: Minimum 4.5:1 contrast
- Large text: Minimum 3:1 contrast
- UI elements: Minimum 3:1 contrast

**Color Blindness Support:**
- Avoid red/green only distinctions
- Use patterns or icons with colors
- Test with color blindness simulators

### Design Principles

**Dark Themes:**
- Use warm grays, not pure black
- Limit bright whites
- Ensure sufficient contrast

**Light Themes:**
- Use cool grays for backgrounds
- Ensure text readability
- Balance brightness levels

## Troubleshooting Themes

### Common Issues

**Theme Not Loading:**
- Check JSON syntax
- Verify file location
- Restart Ghost

**Colors Not Applying:**
- Clear theme cache
- Check property names
- Verify color format (#hexadecimal)

**Performance Issues:**
- Reduce complex gradients
- Optimize image assets
- Use web-safe colors

### Theme Validation

**JSON Validation:**
```bash
python -m json.tool theme.json
```

**Color Format Check:**
- Use 6-digit hex codes: `#RRGGBB`
- Avoid named colors: `red`, `blue`
- Test transparency support

## Best Practices

### Theme Development

1. **Start with existing theme** - Copy and modify
2. **Test thoroughly** - Check all UI elements
3. **Document changes** - Keep notes on modifications
4. **Version control** - Track theme changes
5. **Share responsibly** - Test before sharing

### Performance Optimization

1. **Use simple colors** - Avoid complex gradients
2. **Minimize resources** - Keep themes lightweight
3. **Test on different devices** - Ensure compatibility
4. **Cache efficiently** - Optimize for repeated use

### User Experience

1. **Maintain consistency** - Keep similar elements similar
2. **Ensure readability** - Text must be clearly visible
3. **Consider context** - Themes for different use cases
4. **Provide options** - Light and dark variants

## Theme Gallery

### Popular Community Themes

**Cyberpunk:**
- Neon accents
- Dark background
- Futuristic styling

**Minimalist:**
- Clean lines
- Limited colors
- Focus on content

**High Contrast:**
- Accessibility focused
- Strong color differences
- Clear distinctions

### Contributing Themes

1. **Create unique theme**
2. **Test extensively**
3. **Document features**
4. **Share with community**
5. **Provide support**

---

Theming allows you to make Ghost truly your own. Experiment with different color schemes and styles to create the perfect environment for your selfbot experience!