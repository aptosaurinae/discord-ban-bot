# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "discord-py>=2.7.1",
# ]
# ///
"""Bot which will auto-ban on role pickup."""

import argparse
import logging
from datetime import datetime, timezone
from pathlib import Path

import discord
from discord.ext import commands

# --- Input configuration setup

parser = argparse.ArgumentParser(description="Configuration for discord bot")
parser.add_argument("--token", type=str, help="Discord Token")
parser.add_argument("--forbidden_role_id", type=str, help="ID of the role to ban")
parser.add_argument(
    "--log_channel_id",
    required=False,
    default=None,
    type=str,
    help="ID of the channel to output messages"
)

args = parser.parse_args()
TOKEN = args.token
FORBIDDEN_ROLE_IDS = {int(args.forbidden_role_id)}
LOG_CHANNEL = int(args.log_channel_id) if args.log_channel_id is not None else None

# --- Logging to file

def setup_logging():
    """Setup logger."""
    log_folder = Path(__file__).parent
    dt_now = datetime.now(timezone.utc)
    datetime_str = (
        f"{dt_now.year}-{dt_now.month}-{dt_now.day}_{dt_now.hour}-{dt_now.minute}-{dt_now.second}"
    )
    if log_folder is not None and log_folder.exists():
        log_file_path = log_folder / f"{datetime_str}_ban_bot.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[logging.FileHandler(log_file_path, encoding="utf-8")],
        )

if LOG_CHANNEL is not None:
    setup_logging()

# --- Configure bot

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None
)

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    before_roles = {r.id for r in before.roles}
    after_roles = {r.id for r in after.roles}

    added_roles = after_roles - before_roles
    forbidden_added = added_roles & FORBIDDEN_ROLE_IDS

    if forbidden_added:
        roles_to_remove = [after.guild.get_role(rid) for rid in forbidden_added]

        try:
            await after.remove_roles(*roles_to_remove, reason="Forbidden role removed before auto-ban")  # type: ignore
        except Exception as e:
            logging.info(f"Failed to remove roles from {after}: {e}")

        await after.ban(reason="Auto-ban: forbidden role added")
        logging.info(f"Banned user {after.display_name} {after.id}")

        if LOG_CHANNEL is not None:
            log_channel = after.guild.get_channel(LOG_CHANNEL)
            if log_channel:
                await log_channel.send(  # type: ignore
                    f"{after.mention} gained a forbidden role and was banned.\n"
                    f"- Created: {after.created_at.isoformat()}\n"
                    f"- Joined: {after.joined_at.isoformat() if isinstance(after.joined_at, datetime) else 'null'}\n"
                    f"- Roles: `{str([role.name for role in after.roles])[1:-1]}`"
                )
            else:
                logging.info("Attempted to send message to channel, but does not exist")

# --- Run bot

bot.run(TOKEN)
