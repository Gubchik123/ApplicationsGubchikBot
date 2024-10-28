import random

import aiohttp
import phonenumbers
from urllib.parse import urlparse

from data.constants import UKRAINIAN_NAMES, OPERATORS


def generate_name() -> str:
    """Returns random Ukrainian name."""
    return random.choice(UKRAINIAN_NAMES)


def generate_phone_number() -> str:
    """Returns random Ukrainian phone number with operator code."""
    operator_name = random.choice(list(OPERATORS.keys()))
    operator_code = random.choice(OPERATORS[operator_name])
    phone_number = phonenumbers.parse(
        f"+380{operator_code}{random.randint(1000000, 9999999)}", None
    )
    return phonenumbers.format_number(
        phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
    )


def is_valid_(url: str) -> bool:
    """Returns True if the given URL is valid, False otherwise."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


async def is_valid_aiohttp_(url: str) -> bool:
    """Returns True if the given URL is accessible, False otherwise."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status == 200
    except aiohttp.ClientError:
        return False


def extract_domain_from_(url: str) -> str:
    """Returns domain from the given URL."""
    parsed_url = urlparse(url)
    return parsed_url.netloc
