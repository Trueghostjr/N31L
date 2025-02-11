import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Union

from hikari import Guild, GuildChannel, GuildThreadChannel, Role, Snowflake, User
from hikari.embeds import Embed
from loguru import logger


class Responses:
    """Class containing generic, modular response templates."""

    def ExpandUser(user: User, format: bool = True, showId: bool = True) -> str:
        """Build a reusable string for the provided identity."""

        result: str = ""

        username: str = user.username
        userId: Snowflake = user.id

        if hasattr(user, "discriminator"):
            if (discrim := int(user.discriminator)) != 0:
                username += f"#{discrim}"

        if format:
            result += f"`{username}`"
        else:
            result += username

        if showId:
            if format:
                result += f" (`{userId}`)"
            else:
                result += f" ({userId})"

        logger.trace(result)

        return result

    def ExpandRole(role: Role, format: bool = True) -> str:
        """Build a reusable string for the provided role."""

        if format:
            return f"`{role.name}` (`{role.id}`)"

        return f"{role.name} ({role.id})"

    def ExpandGuild(guild: Guild, format: bool = True) -> str:
        """Build a reusable string for the provided guild."""

        if format:
            return f"`{guild.name}` (`{guild.id}`)"

        return f"{guild.name} ({guild.id})"

    def ExpandChannel(channel: GuildChannel, format: bool = True) -> str:
        """Build a reusable string for the provided channel."""

        if format:
            return f"`#{channel.name}` (`{channel.id}`)"

        return f"#{channel.name} ({channel.id})"

    def ExpandThread(thread: GuildThreadChannel, format: bool = True) -> str:
        """Build a reusable string for the provided thread."""

        if format:
            return f"`{thread.name}` (`{thread.id}`)"

        return f"{thread.name} ({thread.id})"

    def Log(emoji: str, message: str, timestamp: Optional[datetime] = None) -> str:
        """Build a reusable log message."""

        if timestamp is None:
            timestamp = datetime.now()

        return f"[{Timestamps.LongTime(timestamp)}] :{emoji}: {message}"

    def Success(
        title: Optional[str] = None,
        url: Optional[str] = None,
        color: str = "3BA55D",
        description: Optional[str] = None,
        fields: List[Dict[str, Union[str, bool]]] = [],
        author: Optional[str] = None,
        authorUrl: Optional[str] = None,
        authorIcon: Optional[str] = None,
        thumbnail: Optional[str] = None,
        image: Optional[str] = None,
        footer: Optional[str] = None,
        footerIcon: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ) -> Embed:
        """Build a generic successful response Embed object."""

        result: Embed = Embed(
            title=title,
            description=description,
            url=url,
            color=color,
            timestamp=timestamp,
        )

        if author is not None:
            result.set_author(name=author, url=authorUrl, icon=authorIcon)

        if thumbnail is not None:
            result.set_thumbnail(thumbnail)

        if image is not None:
            result.set_image(image)

        if footer is not None:
            result.set_footer(footer, icon=footerIcon)

        for field in fields:
            result.add_field(
                field["name"], field["value"], inline=field.get("inline", True)
            )

        return result

    def Warning(
        title: Optional[str] = None,
        url: Optional[str] = None,
        color: str = "FAA81A",
        description: Optional[str] = None,
        fields: List[Dict[str, Union[str, bool]]] = [],
        author: Optional[str] = None,
        authorUrl: Optional[str] = None,
        authorIcon: Optional[str] = None,
        thumbnail: Optional[str] = None,
        image: Optional[str] = None,
        footer: Optional[str] = None,
        footerIcon: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ) -> Embed:
        """Build a generic warning response Embed object."""

        result: Embed = Embed(
            title=title,
            description=description,
            url=url,
            color=color,
            timestamp=timestamp,
        )

        if author is not None:
            result.set_author(name=author, url=authorUrl, icon=authorIcon)

        if thumbnail is not None:
            result.set_thumbnail(thumbnail)

        if image is not None:
            result.set_image(image)

        if footer is not None:
            result.set_footer(footer, icon=footerIcon)

        for field in fields:
            result.add_field(
                field["name"], field["value"], inline=field.get("inline", True)
            )

        return result

    def Fail(
        title: Optional[str] = None,
        url: Optional[str] = None,
        color: str = "ED4245",
        description: Optional[str] = None,
        fields: List[Dict[str, Union[str, bool]]] = [],
        author: Optional[str] = None,
        authorUrl: Optional[str] = None,
        authorIcon: Optional[str] = None,
        thumbnail: Optional[str] = None,
        image: Optional[str] = None,
        footer: Optional[str] = None,
        footerIcon: str = "https://i.imgur.com/IwCRM6v.png",
        timestamp: Optional[datetime] = None,
    ) -> Embed:
        """Build a generic failed response Embed object."""

        ref: str = hashlib.md5(
            str(datetime.now().timestamp()).encode("utf-8")
        ).hexdigest()

        logger.debug(f"Generated error reference {ref}")

        result: Embed = Embed(
            title=title,
            description=description,
            url=url,
            color=color,
            timestamp=timestamp,
        )

        if author is not None:
            result.set_author(name=author, url=authorUrl, icon=authorIcon)

        if thumbnail is not None:
            result.set_thumbnail(thumbnail)

        if image is not None:
            result.set_image(image)

        if footer is not None:
            result.set_footer(f"{footer} ({ref})", icon=footerIcon)
        else:
            result.set_footer(ref, icon=footerIcon)

        for field in fields:
            result.add_field(
                field["name"], field["value"], inline=field.get("inline", True)
            )

        return result


class Timestamps:
    """Class containing markdown, timestamp formatting templates."""

    def LongDate(timestamp: Union[int, float, datetime]) -> str:
        """
        Create a long date timestamp using markdown formatting.

        Example: "January 21, 2022"
        """

        if isinstance(timestamp, float):
            timestamp = int(timestamp)
        elif isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp())

        return f"<t:{timestamp}:D>"

    def ExtraLongDateShortTime(timestamp: Union[int, float, datetime]) -> str:
        """
        Create an extra long date and short time timestamp using markdown formatting.

        Example: "Friday, January 21, 2022 at 4:20 PM"
        """

        if isinstance(timestamp, float):
            timestamp = int(timestamp)
        elif isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp())

        return f"<t:{timestamp}:F>"

    def LongDateShortTime(timestamp: Union[int, float, datetime]) -> str:
        """
        Create a long date and short time timestamp using markdown formatting.

        Example: "January 21, 2022 at 4:20 PM"
        """

        if isinstance(timestamp, float):
            timestamp = int(timestamp)
        elif isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp())

        return f"<t:{timestamp}:f>"

    def LongTime(timestamp: Union[int, float, datetime]) -> str:
        """
        Create a long time timestamp using markdown formatting.

        Example: "4:20:00 PM"
        """

        if isinstance(timestamp, float):
            timestamp = int(timestamp)
        elif isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp())

        return f"<t:{timestamp}:T>"

    def Relative(timestamp: Union[int, float, datetime]) -> str:
        """
        Create a relative timestamp using markdown formatting.

        Example: "in 2 minutes" or "6 minutes ago"
        """

        if isinstance(timestamp, float):
            timestamp = int(timestamp)
        elif isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp())

        return f"<t:{timestamp}:R>"

    def ShortDate(timestamp: Union[int, float, datetime]) -> str:
        """
        Create a short date timestamp using markdown formatting.

        Example: "1/21/2022"
        """

        if isinstance(timestamp, float):
            timestamp = int(timestamp)
        elif isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp())

        return f"<t:{timestamp}:d>"

    def ShortTime(timestamp: Union[int, float, datetime]) -> str:
        """
        Create a short time timestamp using markdown formatting.

        Example: "4:20 PM"
        """

        if isinstance(timestamp, float):
            timestamp = int(timestamp)
        elif isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp())

        return f"<t:{timestamp}:t>"
