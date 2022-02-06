import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import hikari
import psutil
import tanjun
from helpers import Buttons, Responses, Timestamps
from hikari import DMChannel, Guild, InteractionChannel, Permissions, User
from hikari.embeds import Embed
from hikari.impl.bot import GatewayBot
from hikari.impl.special_endpoints import ActionRowBuilder
from hikari.interactions.base_interactions import InteractionMember
from hikari.presences import Activity, ActivityType, Status
from hikari.users import UserImpl
from loguru import logger
from tanjun import Component
from tanjun.abc import SlashContext
from tanjun.commands import SlashCommandGroup

component: Component = Component(name="Admin")

send: SlashCommandGroup = component.with_slash_command(
    tanjun.slash_command_group("send", "Slash Commands to send messages from N31L.")
)
set: SlashCommandGroup = component.with_slash_command(
    tanjun.slash_command_group("set", "Slash Commands to manage N31L.")
)


@component.with_slash_command()
@tanjun.with_own_permission_check(Permissions.SEND_MESSAGES)
@tanjun.with_user_slash_option("user", "Desired user to fetch the profile of.")
@tanjun.as_slash_command("profile", "Fetch detailed information for the provided user.")
async def CommandProfile(
    ctx: SlashContext, user: Union[InteractionMember, UserImpl]
) -> None:
    """Handler for the /profile command."""

    if hasattr(user, "user") is True:
        try:
            user.user = await ctx.rest.fetch_user(user.id)
        except Exception as e:
            logger.warning(
                f"Failed to fetch user {Responses.ExpandUser(user.id, False)}, {e}"
            )

    fields: List[Dict[str, Any]] = []
    altAvatar: Optional[str] = None
    accent: Optional[str] = None

    if hasattr(user, "nickname") is True:
        if (nickname := user.nickname) is not None:
            fields.append({"name": "Nickname", "value": nickname, "inline": True})

    if hasattr(user, "created_at") is True:
        if (created := user.created_at) is not None:
            fields.append(
                {
                    "name": "Created",
                    "value": Timestamps.Relative(created),
                    "inline": True,
                }
            )

    if hasattr(user, "joined_at") is True:
        if (joined := user.joined_at) is not None:
            fields.append(
                {"name": "Joined", "value": Timestamps.Relative(joined), "inline": True}
            )

    if hasattr(user, "premium_since") is True:
        if (booster := user.premium_since) is not None:
            fields.append(
                {
                    "name": "Nitro Booster",
                    "value": f"Since {Timestamps.Relative(booster)}",
                    "inline": True,
                }
            )

    if hasattr(user, "communication_disabled_until") is True:
        if (timeout := user.communication_disabled_until()) is not None:
            fields.append(
                {
                    "name": "Timed Out",
                    "value": f"Until {Timestamps.Relative(timeout)}",
                    "inline": True,
                }
            )

    if hasattr(user, "is_pending") is True:
        if user.is_pending is True:
            fields.append({"name": "Passed Screening", "value": "No", "inline": True})

    if hasattr(user, "is_mute") is True:
        if user.is_mute is True:
            fields.append({"name": "Muted", "value": "Yes", "inline": True})

    if hasattr(user, "is_deaf") is True:
        if user.is_deaf is True:
            fields.append({"name": "Deafened", "value": "Yes", "inline": True})

    if hasattr(user, "guild_avatar_url") is True:
        if (url := user.guild_avatar_url) is not None:
            altAvatar = url

    if hasattr(user, "accent_color") is True:
        if (color := user.accent_color) is not None:
            accent = str(color).replace("#", "")

    result: Embed = Responses.Success(
        color=accent,
        fields=fields,
        author=f"{user.username}#{user.discriminator}",
        authorIcon=altAvatar,
        thumbnail=user.default_avatar_url
        if (avatar := user.avatar_url) is None
        else avatar,
        image=None if hasattr(user, "user") is False else user.user.banner_url,
        footer=user.id,
        timestamp=None if created is None else created.astimezone(),
    )

    await ctx.respond(embed=result)


@component.with_slash_command()
@tanjun.with_own_permission_check(Permissions.SEND_MESSAGES)
@tanjun.as_slash_command("server", "Fetch detailed information for the current server.")
async def CommandServer(ctx: SlashContext) -> None:
    """Handler for the /server command."""

    server: Guild = await ctx.fetch_guild()
    fields: List[Dict[str, Any]] = []

    if hasattr(server, "owner_id") is True:
        if (owner := server.owner_id) is not None:
            fields.append({"name": "Owner", "value": f"<@{owner}>", "inline": True})

    if hasattr(server, "created_at") is True:
        if (created := server.created_at) is not None:
            fields.append(
                {
                    "name": "Created",
                    "value": Timestamps.Relative(created),
                    "inline": True,
                }
            )

    if hasattr(server, "shard_id") is True:
        if (shard := server.shard_id) is not None:
            fields.append({"name": "Shard", "value": f"{shard:,}", "inline": True})

    await ctx.respond(
        embed=Responses.Success(
            title=server.name,
            url=None
            if (vanity := server.vanity_url_code) is None
            else f"https://discord.gg/{vanity}",
            description=server.description,
            fields=fields,
            thumbnail=server.icon_url,
            image=server.banner_url,
            footer=server.id,
            timestamp=server.created_at,
        )
    )


@component.with_slash_command()
@tanjun.with_own_permission_check(Permissions.SEND_MESSAGES)
@tanjun.as_slash_command(
    "status", "Get the status of N31L, a utilitarian bot for the Call of Duty server."
)
async def CommandStatus(ctx: SlashContext) -> None:
    """Handler for the /status command."""

    stats: List[Dict[str, Any]] = []
    external: ActionRowBuilder = ActionRowBuilder()

    # Make a request to Discord to determine the REST latency
    timeStart: float = datetime.now().timestamp()
    await ctx.rest.fetch_my_user()
    timeEnd: float = datetime.now().timestamp()

    stats.append(
        {
            "name": "Python",
            "value": f"[`{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}`](https://www.python.org/)",
            "inline": True,
        }
    )
    stats.append(
        {
            "name": "Hikari",
            "value": f"[`{hikari.__version__}`]({hikari.__url__})",
            "inline": True,
        }
    )
    stats.append(
        {
            "name": "Tanjun",
            "value": f"[`{tanjun.__version__}`]({tanjun.__url__})",
            "inline": True,
        }
    )
    stats.append(
        {
            "name": "REST Latency",
            "value": f"{round((timeEnd - timeStart) * 1000):,}ms",
            "inline": True,
        }
    )
    stats.append(
        {"name": "CPU Usage", "value": f"{psutil.cpu_percent():,}%", "inline": True}
    )
    stats.append(
        {
            "name": "Memory Usage",
            "value": f"{psutil.virtual_memory().percent:,}%",
            "inline": True,
        }
    )

    external = Buttons.Link(external, "GitHub", "https://github.com/EthanC/N31L")
    external = Buttons.Link(external, "Discord", "https://discord.gg/CallofDuty")

    await ctx.respond(
        embed=Responses.Success(
            color="00FF00",
            description="N31L is a utilitarian bot for the [Call of Duty server](https://discord.gg/CallofDuty).\n\nThe commands and functionality of this bot are purpose-built and primarily intended for the Moderators of the server. Because of this, the current bot instance is not available to be invited to other servers.",
            fields=stats,
            author="N31L",
            authorUrl="https://github.com/EthanC/N31L",
            authorIcon="https://i.imgur.com/cGtkGuI.png",
            footer="Developed by Lacking#0001",
            footerIcon="https://i.imgur.com/KZnKBn2.gif",
        ),
        component=external,
    )


@send.with_command
@tanjun.with_owner_check()
@tanjun.with_str_slash_option("content", "Enter the message content.")
@tanjun.with_user_slash_option("user", "Choose a user to send a message to.")
@tanjun.as_slash_command(
    "direct_message",
    "Send a direct message from N31L.",
    default_permission=False,
    default_to_ephemeral=True,
)
async def CommandSendDirectMessage(ctx: SlashContext, user: User, content: str) -> None:
    """Handler for the /send direct_message command."""

    try:
        dm: DMChannel = await ctx.rest.create_dm_channel(user.id)

        await ctx.rest.create_message(dm.id, content)
    except Exception as e:
        logger.error(
            f"Failed to send direct message to {Responses.ExpandUser(user, False)}, {e}"
        )
        logger.trace(content)

        await ctx.respond(
            embed=Responses.Fail(
                description=f"Failed to send direct message to {Responses.ExpandUser(user)}, {e}"
            )
        )

        return

    await ctx.respond(
        embed=Responses.Success(
            description=f"Direct Message sent to {Responses.ExpandUser(user)}."
        )
    )

    logger.success(
        f"{Responses.ExpandUser(ctx.author, False)} sent a direct message to {Responses.ExpandUser(user, False)}"
    )


@send.with_command
@tanjun.with_owner_check()
@tanjun.with_str_slash_option("content", "Enter the message content.")
@tanjun.with_channel_slash_option("channel", "Choose a channel to send a message to.")
@tanjun.as_slash_command(
    "message",
    "Send a message from N31L.",
    default_permission=False,
    default_to_ephemeral=True,
)
async def CommandSendMessage(
    ctx: SlashContext, channel: InteractionChannel, content: str
) -> None:
    """Handler for the /send message command."""

    try:
        await ctx.rest.create_message(channel.id, content)
    except Exception as e:
        logger.error(
            f"Failed to send message to {Responses.ExpandChannel(channel, False)}, {e}"
        )
        logger.trace(content)

        await ctx.respond(
            embed=Responses.Fail(
                description=f"Failed to send message to {Responses.ExpandChannel(channel)}, {e}"
            )
        )

        return

    await ctx.respond(
        embed=Responses.Success(
            description=f"Message sent to {Responses.ExpandChannel(channel)}."
        )
    )

    logger.success(
        f"{Responses.ExpandUser(ctx.author, False)} sent a message to {Responses.ExpandChannel(channel, False)}"
    )


@set.with_command
@tanjun.with_owner_check()
@tanjun.with_str_slash_option(
    "url",
    "Twitch stream URL to be used for the Streaming activity type.",
    default=None,
)
@tanjun.with_str_slash_option("name", "Enter an activity name.")
@tanjun.with_int_slash_option(
    "type",
    "Choose an activity type.",
    choices={
        "Competing in": ActivityType.COMPETING.value,
        "Listening to": ActivityType.LISTENING.value,
        "Playing": ActivityType.PLAYING.value,
        "Streaming": ActivityType.STREAMING.value,
        "Watching": ActivityType.WATCHING.value,
    },
)
@tanjun.as_slash_command(
    "activity", "Set the presence activity for N31L.", default_permission=False
)
async def CommandSetActivity(
    ctx: SlashContext,
    type: int,
    name: str,
    url: Optional[str] = None,
    bot: GatewayBot = tanjun.inject(type=GatewayBot),
) -> None:
    """Handler for the /set activity command."""

    try:
        await bot.update_presence(activity=Activity(name=name, url=url, type=type))
    except Exception as e:
        logger.error(
            f"Failed to set presence activity to {ActivityType(type).name} {name}, {e}"
        )

        await ctx.respond(
            embed=Responses.Fail(description=f"Failed to set presence activity, {e}")
        )

        return

    await ctx.respond(
        embed=Responses.Success(
            description=f"Set presence activity to `{ActivityType(type).name}` `{name}`."
        )
    )


@set.with_command
@tanjun.with_owner_check()
@tanjun.with_str_slash_option(
    "url", "Direct URL to an image. Leave empty to use a default avatar.", default=None
)
@tanjun.as_slash_command("avatar", "Set the avatar for N31L.", default_permission=False)
async def CommandSetAvatar(ctx: SlashContext, url: Optional[str]) -> None:
    """Handler for the /set avatar command."""

    try:
        if url is not None:
            await ctx.rest.edit_my_user(avatar=url)
        else:
            await ctx.rest.edit_my_user(avatar=None)
    except Exception as e:
        logger.error(f"Failed to set avatar to {url}, {e}")

        await ctx.respond(
            embed=Responses.Fail(description=f"Failed to set avatar, {e}")
        )

        return

    await ctx.respond(
        embed=Responses.Success(description=f"Set avatar to `{url}`.", image=url)
    )


@set.with_command
@tanjun.with_owner_check()
@tanjun.with_str_slash_option(
    "type",
    "Choose a status type.",
    choices={
        "Do Not Disturb": Status.DO_NOT_DISTURB.value,
        "Idle": Status.IDLE.value,
        "Online": Status.ONLINE.value,
    },
)
@tanjun.as_slash_command(
    "status", "Set the presence status for N31L.", default_permission=False
)
async def CommandSetStatus(
    ctx: SlashContext, type: str, bot: GatewayBot = tanjun.inject(type=GatewayBot)
) -> None:
    """Handler for the /set status command."""

    color: Optional[str] = None

    if type == Status.DO_NOT_DISTURB:
        color = "ED4245"
    elif type == Status.IDLE:
        color = "FAA81A"
    elif type == Status.ONLINE:
        color = "3BA55D"

    try:
        await bot.update_presence(status=type)
    except Exception as e:
        logger.error(f"Failed to set presence status to {Status(type).name}, {e}")

        await ctx.respond(
            embed=Responses.Fail(description=f"Failed to set presence status, {e}")
        )

        return

    await ctx.respond(
        embed=Responses.Success(
            color=color, description=f"Set presence status to `{Status(type).name}`."
        )
    )


@set.with_command
@tanjun.with_owner_check()
@tanjun.with_str_slash_option("input", "Enter a username.")
@tanjun.as_slash_command(
    "username", "Set the username for N31L.", default_permission=False
)
async def CommandSetUsername(ctx: SlashContext, input: str) -> None:
    """Handler for the /set username command."""

    try:
        await ctx.rest.edit_my_user(username=input)
    except Exception as e:
        logger.error(f"Failed to set username to {input}, {e}")

        await ctx.respond(
            embed=Responses.Fail(description=f"Failed to set username, {e}")
        )

        return

    await ctx.respond(
        embed=Responses.Success(description=f"Set username to `{input}`.")
    )
