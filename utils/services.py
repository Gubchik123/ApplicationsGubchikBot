import random
import asyncio

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


def get_active_request_loop_tasks_count(user_id: int) -> int:
    """Returns the number of active request loop tasks for the user with the given ID."""
    return sum(
        task.get_name().startswith(f"request_loop-user_{user_id}_")
        for task in asyncio.all_tasks()
    )


def create_request_loop_task(state_data: dict):
    """Creates a task for sending requests with the given state data."""
    from utils.tasks import request_loop

    asyncio.create_task(
        request_loop(
            user_data={
                "user_id": state_data["user_id"],
                "status": state_data["user_status"],
                "applications_sent": state_data["user_applications_sent"],
            },
            url=state_data["url"],
            frequency=state_data["frequency"],
            duration=state_data["duration"],
        ),
        name=f"request_loop-user_{state_data['user_id']}_url_{state_data['url']}",
    )


def cancel_request_loop_task_for_(user_id: int) -> str:
    """Cancels the request loop task for the user with the given ID."""
    (task,) = [
        task
        for task in asyncio.all_tasks()
        if task.get_name().startswith(f"request_loop-user_{user_id}_")
    ]
    url = task.get_name().split("_")[-1]
    task.cancel()
    return url
