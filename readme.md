# Auto-ban Discord bot

## Running the bot

The bot can be run by installing [`uv`](https://docs.astral.sh/uv/getting-started/installation/),
then navigating to the directory with the script and running:

``` shell
uv run ban-bot.py --token "123456789" --forbidden_role_id "123456789" --log_channel_id "123456789"
```

- Token: Needs to match a bot token from the Discord Developer portal.
See instructions below for full setup.
- Forbidden role ID: Needs to match the role ID of the role you want to auto-ban when a member
gains it.
This can be found by going to Server Settings -> Roles -> right click the role and copy ID.
- Log channel ID: Optional, needs to match a channel ID in Discord.
This can be found by right clicking the appropriate channel in Discord and copying the ID.

Doing this will start the instance locally. If you want to run it on a persistent server then you
will need to remote in and use `nohup` or similar (this is how I have some basic bots set up on
my local NAS), or set this up with a Dockerfile to run it as a container.

## Creating a bot and inviting it into the server

### Creating the bot and getting a token

In order to generate a token you need to create a bot:

- Go to the [Discord Developer Applications Portal](https://discord.com/developers/applications)
- Create an application using the `New Application` button at the top right
- Set up your bot with a name on the `General Information` page, and ideally choose an
appropriate picture for your bot
- Under `Installation` in the `Install Link` drop down select `None`
- On the `Bot` page:
    - Turn off `Public Bot` and save changes
    - Turn on `Server Members Intent` and save changes
    - Click `Reset Token` to generate a new token.
    - You can now use this token as an input to the bot. Store this safely;
    if anyone gets the token they will be able to use your bot with their own code.

### Inviting the bot to your server

- On the `OAuth2` page:
    - scroll down to `OAuth2 URL Generator` and select `bot` from the
    permissions list, and make sure `Integration Type` is set to `Guild`.
    You should not need to select any sub-permissions from the `bot` list, as you can then
    configure the permissions the bot has access to via role assignment within the server.
    - Click the `copy` button at the right of the `Generated URL` field and put it in your browser.
    - This should either directly give you an invite page where you can select a discord server,
    or load up your discord desktop client and allow you to choose there.
- Once the bot is in your server you can then apply a role with ban and role management permissions.
It needs role management to remove the role before banning.
It needs ban permission to be able to ban users.
- Make sure the bot role is close to the top of your list of roles.
Ban permissions work on a hierarchy in Discord which means you need to make sure the bot has
a higher role level than the general users you want to be able to ban with it.
