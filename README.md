# Discord Omegle-Style Bot

A Python Discord bot that pairs users randomly (or by gender preference) in ephemeral text and voice channels, mimicking the Omegle experience.

## Features

* Prefix (`!`) and slash (`/`) commands:

  * Text pairing: `!start` / `/start`, `!stop` / `/stop`
  * Voice pairing: `!vstart` / `/vstart`, `!vstop` / `/vstop`
* Gender-role matching via reaction menu:

  * React with ♂️ for Male, ♀️ for Female, 🎲 for Random
  * Users are only paired if their selections match (or one/both are random)
* Ephemeral channels:

  * Temporary text/voice channels created per match
  * Channels auto-deleted when users leave or run stop command
* Configurable via `config.yaml`:

  * Bot token, prefix, guild ID, role IDs
* Modular codebase using Cogs

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/omeCord.git
   cd omeCord
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure**

   1. Copy `config.yaml.example` to `config.yaml`.
   2. Edit `config.yaml` with your:

      * `token`: Your Discord bot token
      * `prefix`: Command prefix (e.g., `!`)
      * `guild_id`: (Optional) Guild ID for faster slash command syncing
      * `roles`: Role IDs for `male` and `female` preferences

## Usage

1. **Invite the Bot**

   * Use the following URL template, replacing `YOUR_CLIENT_ID`:

     ```
     https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot%20applications.commands&permissions=274878067776
     ```
   * Ensure the bot has:

     * **Manage Channels**
     * **Connect** & **Move Members**
     * **Use Slash Commands**
     * **Add Reactions**

2. **Run the Bot**

   ```bash
   python bot.py
   ```

3. **Commands**

   * **Setup Gender Menu**: `!setup_gender`
   * **Text Pairing**: `!start` / `/start`, `!stop` / `/stop`
   * **Voice Pairing**: `!vstart` / `/vstart`, `!vstop` / `/vstop`

## Configuration File (`config.yaml`)

```yaml
token: "YOUR_DISCORD_BOT_TOKEN"
prefix: "!"
guild_id: YOUR_GUILD_ID  # optional
roles:
  male: 123456789012345678
  female: 876543210987654321
  random: null
```

## Project Structure

```
omeCord/
├── bot.py
├── config.yaml
├── requirements.txt
├── cogs/
│   ├── __init__.py
│   ├── pairing.py
│   ├── voice.py
│   └── roles.py
└── utils/
    ├── __init__.py
    └── matchmaking.py
```


---

Paste this `README.md` into your GitHub repository to guide users through setup and usage.
