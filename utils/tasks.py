import time
import random
import logging
import asyncio

import aiohttp
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from urllib.parse import urlsplit, urlunsplit

from bot import bot
from data.config import PROXIES
from keyboards.default import get_menu_keyboard
from utils.user_manager import UserManager
from utils.services import generate_name, generate_phone_number


async def request_loop(
    user_data: dict, url: str, frequency: int, duration: int
):
    """Task for sending requests to the specified URL."""
    requests_to_send = (
        50 - user_data["applications_sent"]
        if user_data["status"] == "demo"
        else float("inf")
    )
    end_time = (time.time() + duration) if duration is not None else None

    while requests_to_send > 0:
        if end_time is not None and time.time() >= end_time:
            break
        error_message = await _parse(url)
        if error_message:
            await bot.send_message(user_data["user_id"], f"❌ {error_message}")
            break
        else:
            await UserManager.increment_temp_applications_sent(
                user_data["user_id"], url
            )
        if user_data["status"] == "demo":
            requests_to_send -= 1
        logging.info(f"Затримка перед наступним запитом: {frequency} секунд.")
        await asyncio.sleep(frequency)

    request_count = await UserManager.increase_applications_sent(
        user_data["user_id"], url
    )
    await bot.send_message(
        user_data["user_id"],
        f"✅ Відправка заявок на {url} завершена\n"
        f"✉️ Всього відправлено заявок: {request_count}",
        reply_markup=await get_menu_keyboard(user_data["user_id"]),
    )


async def _parse(url: str):
    """Parses the form from the specified URL and sends a POST request."""
    attempts = 3  # Загальна кількість спроб

    for attempt in range(attempts):
        proxy_url = random.choice(PROXIES) if PROXIES else None
        logging.info(
            f"Використання запиту з проксі: {proxy_url}"
            if proxy_url
            else "Використання запиту без проксі."
        )
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            try:
                status, html = await _send_get_request(session, url, proxy_url)
                if status != 200:
                    if attempt < attempts - 1:
                        logging.warning(
                            "Сайт недоступний. Спробуємо ще раз..."
                        )
                        await asyncio.sleep(10)  # Затримка перед повтором
                        continue  # Повертаємось до початку циклу
                    return f"Сайт недоступний. Код статусу: {status}."

                form, action = await _parse_form(html)
                logging.info(f"{action=}")
                if not form:
                    return action  # "Форма не знайдена."

                data = await _prepare_data_from_(form)
                action = await _construct_action_url(action, url)
                result = await _send_post_request(
                    session, action, data, proxy_url, attempts
                )
                return None if result is None else result
            except aiohttp.ClientError as e:
                logging.error(f"Помилка при використанні проксі: {e}")
                if attempt < attempts - 1:
                    await asyncio.sleep(10)
                else:
                    return "Проблема з проксі."
    return None  # Успішно відправлено


async def _send_get_request(
    session: aiohttp.ClientSession, url: str, proxy_url: str
) -> tuple[int, str]:
    """Sends the GET request to the specified URL."""
    logging.info(f"Надсилаємо GET запит до: {url}")
    async with session.get(
        url, proxy=proxy_url, headers={"User-Agent": generate_user_agent()}
    ) as response:
        logging.info(f"Отримано відповідь: {response.status}")
        html = await response.text()
        return response.status, html


async def _parse_form(html: str) -> tuple[BeautifulSoup | None, str]:
    """Parse the form from the HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form")
    return (
        (None, "Форма не знайдена.")
        if not form
        else (form, form.get("action"))
    )


async def _prepare_data_from_(form: BeautifulSoup) -> dict:
    """Prepares the form data to be sent."""
    data = {}
    inputs = form.find_all("input")
    for input_tag in inputs:
        input_name = input_tag.get("name")
        input_type = input_tag.get("type")

        if input_type == "name" or input_name == "name":
            data[input_name] = generate_name()
        elif input_type == "tel" or input_name in ["phone", "tel"]:
            data[input_name] = generate_phone_number()
        elif input_type == "checkbox":
            data[input_name] = "on"

    selects = form.find_all("select")
    for select in selects:
        select_name = select.get("name")
        options = select.find_all("option")
        valid_options = [option for option in options if option.get("value")]
        if valid_options:
            selected_option = random.choice(valid_options).get("value")
            data[select_name] = selected_option

    logging.info(f"Дані, які будуть надіслані: {data}")
    return data


async def _construct_action_url(action: str | None, url: str) -> str:
    """Constructs the action URL from the form action."""
    if action is None:
        return url
    if action and not action.startswith("http"):
        split_url = urlsplit(url)
        base_url_without_query = urlunsplit(
            (
                split_url.scheme,
                split_url.netloc,
                split_url.path.rstrip("/") + "/",
                "",
                "",
            )
        )
        action = f"{base_url_without_query}{action.lstrip('/')}"
    logging.info(f"Формований URL дії: {action}")
    return action


async def _send_post_request(
    session: aiohttp.ClientSession,
    action: str,
    data: dict,
    proxy_url: str,
    attempts: int,
) -> str:
    """Sends a POST request to the specified action URL."""
    for post_attempt in range(attempts):
        async with session.post(
            action, data=data, proxy=proxy_url
        ) as post_response:
            if post_response.status == 200:
                logging.info(f"Запит на {action} успішно надіслано.")
                return None  # Успішно відправлено
            else:
                logging.error(f"Помилка при відправці: {post_response.status}")
                if post_attempt < attempts - 1:
                    await asyncio.sleep(10)
                else:
                    return "Не вдалося відправити заявку."
    return "Не вдалося відправити заявку."
