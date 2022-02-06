import asyncio
import random
from typing import Any, Dict, List, Optional

import tanjun
from hikari import Permissions
from hikari.embeds import Embed
from services import (
    Axolotl,
    Bird,
    Bunny,
    Capybara,
    Cat,
    Dog,
    Fox,
    Kangaroo,
    Koala,
    Lizard,
    Otter,
    Panda,
    Raccoon,
    Rat,
    RedPanda,
    Whale,
)
from tanjun import Component
from tanjun.abc import SlashContext

component: Component = Component(name="Animals")
animalTypes: List[str] = [
    "Random",
    "Axolotl",
    "Bird",
    "Bunny",
    "Cat",
    "Capybara",
    "Dog",
    "Duck",
    "Fox",
    "Kangaroo",
    "Koala",
    "Lizard",
    "Otter",
    "Panda",
    "Raccoon",
    "Rat",
    "Red Panda",
    "Shibe",
    "Whale",
]


@component.with_slash_command()
@tanjun.with_own_permission_check(Permissions.SEND_MESSAGES)
@tanjun.with_str_slash_option("type", "Choose an animal type.", choices=animalTypes)
@tanjun.as_slash_command("animal", "Fetch a random picture of the chosen animal type.")
async def CommandAnimal(
    ctx: SlashContext,
    type: str,
    config: Dict[str, Any] = tanjun.inject(type=Dict[str, Any]),
) -> None:
    """Handler for the /animal command."""

    while type == "Random":
        type = random.choice(animalTypes)

    redditLogin: Dict[str, str] = config["credentials"]["reddit"]

    result: Optional[Embed] = None
    source: int = 1

    while result is None:
        if type == "Axolotl":
            source = random.randint(1, 2)

            if source == 1:
                result = await Axolotl.AxoltlAPI()
            elif source == 2:
                result = await Axolotl.RedditAxolotls(redditLogin)
        elif type == "Bird":
            source = random.randint(1, 3)

            if source == 1:
                result = await Bird.RandomDuk()
            elif source == 2:
                result = await Bird.SomeRandomAPI()
            elif source == 3:
                result = await Bird.RedditBirbs(redditLogin)
            elif source == 4:
                result = await Bird.RedditBirdPics(redditLogin)
        elif type == "Bunny":
            source = random.randint(1, 3)

            if source == 1:
                result = await Bunny.BunniesIO()
            elif source == 2:
                result = await Bunny.RedditBunnies(redditLogin)
            elif source == 3:
                result = await Bunny.RedditRabbits(redditLogin)
        elif type == "Cat":
            source = random.randint(1, 11)

            if source == 1:
                result = await Cat.TheCatAPI(config["credentials"]["catAPI"]["apiKey"])
            elif source == 2:
                result = await Cat.CATAAS()
            elif source == 3:
                result = await Cat.RandomCat()
            elif source == 4:
                result = await Cat.SomeRandomAPI()
            elif source == 5:
                result = await Cat.ThatCopyCat()
            elif source == 6:
                result = await Cat.RedditBlurryPicturesCats(redditLogin)
            elif source == 7:
                result = await Cat.RedditCatPics(redditLogin)
            elif source == 8:
                result = await Cat.RedditCatPictures(redditLogin)
            elif source == 9:
                result = await Cat.RedditCats(redditLogin)
            elif source == 10:
                result = await Cat.RedditCatsStandingUp(redditLogin)
            elif source == 11:
                result = await Cat.RedditCursedCats(redditLogin)
        elif type == "Capybara":
            source = random.randint(1, 2)

            if source == 1:
                result = await Capybara.RedditCapybara(redditLogin)
            elif source == 2:
                result = await Capybara.RedditCrittersoncapybaras(redditLogin)
        elif type == "Dog":
            source = random.randint(1, 9)

            if source == 1:
                result = await Dog.TheDogAPI(config["credentials"]["dogAPI"]["apiKey"])
            elif source == 2:
                result = await Dog.DogCEO()
            elif source == 3:
                result = await Dog.RandomDog()
            elif source == 4:
                result = await Dog.ShibeOnline()
            elif source == 5:
                result = await Dog.SomeRandomAPI()
            elif source == 6:
                result = await Dog.RedditBlurryPicturesDogs(redditLogin)
            elif source == 7:
                result = await Dog.RedditDogPictures(redditLogin)
            elif source == 8:
                result = await Dog.RedditLookMyDog(redditLogin)
            elif source == 9:
                result = await Dog.RedditPuppies(redditLogin)
        elif type == "Duck":
            if source == 1:
                result = await Bird.RandomDuk()
        elif type == "Fox":
            source = random.randint(1, 3)

            if source == 1:
                result = await Fox.RandomFox()
            elif source == 2:
                result = await Fox.SomeRandomAPI()
            elif source == 3:
                result = await Fox.RedditFoxes(redditLogin)
        elif type == "Kangaroo":
            if source == 1:
                result = await Kangaroo.SomeRandomAPI()
        elif type == "Koala":
            source = random.randint(1, 2)

            if source == 1:
                result = await Koala.SomeRandomAPI()
            elif source == 2:
                result = await Koala.RedditKoalas(redditLogin)
        elif type == "Lizard":
            source = random.randint(1, 2)

            if source == 1:
                result = await Lizard.NekosLife()
            elif source == 2:
                result = await Lizard.RedditLizards(redditLogin)
        elif type == "Otter":
            source = random.randint(1, 2)

            if source == 1:
                result = await Otter.RedditOtterable(redditLogin)
            elif source == 2:
                result = await Otter.RedditOtters(redditLogin)
        elif type == "Panda":
            source = random.randint(1, 2)

            if source == 1:
                result = await Panda.SomeRandomAPI()
            elif source == 2:
                result = await Panda.RedditPanda(redditLogin)
        elif type == "Raccoon":
            source = random.randint(1, 3)

            if source == 1:
                result = await Raccoon.SomeRandomAPI()
            elif source == 2:
                result = await Raccoon.RedditRaccoons(redditLogin)
            elif source == 3:
                result = await Raccoon.RedditTrashPandas(redditLogin)
        elif type == "Rat":
            if source == 1:
                result = await Rat.RedditRats(redditLogin)
        elif type == "Red Panda":
            source = random.randint(1, 2)

            if source == 1:
                result = await RedPanda.SomeRandomAPI()
            elif source == 2:
                result = await RedPanda.RedditRedPandas(redditLogin)
        elif type == "Shibe":
            source = random.randint(1, 2)

            if source == 1:
                result = await Dog.ShibeOnline()
            elif source == 2:
                result = await Dog.RedditShiba(redditLogin)
        elif type == "Whale":
            if source == 1:
                result = await Whale.RedditWhales(redditLogin)

        # Sleep to prevent rate-limiting
        await asyncio.sleep(float(3))

    await ctx.respond(embed=result)
