import random

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


def parse_domain_from_(url: str) -> str:
    """Returns domain from the given URL."""
    domain = urlparse(url).netloc
    return domain[4:] if domain.startswith("www.") else domain
