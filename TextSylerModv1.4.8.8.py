# TextStylerMod v2.3
# by @destr4kt_def

from .. import loader, utils
from telethon import events
import asyncio

@loader.tds
class TextStylerMod(loader.Module):
    """Модуль для автоматического стилизованного текста"""

    strings = {
        "name": "TextStylerMod"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "style_mode",
                None,
                lambda: "Номер включённого стиля (1–6), либо None"
            )
        )

    async def client_ready(self, client, db):
        self.me = await client.get_me()
        text = (
            "🪐 Модуль TextStylerMod загружен ʕっ•ᴥ•ʔっ\n"
            "ℹ️ Автостиль текста сообщений\n"
            "🛠 Версия: 2.3\n\n"
            "▫️ .style <номер стиля> — включить автоматический стиль\n"
            "▫️ .stylehelp — список доступных стилей\n"
            "▫️ .styleoff — отключить автоматический стиль\n\n"
            "👤 Автор: @destr4kt_def"
        )
        print(text)

    styles = {
        "1": lambda text: f"<b>{text}</b>",               # Жирный
        "2": lambda text: f"<i>{text}</i>",               # Курсив
        "3": lambda text: f"<s>{text}</s>",               # Зачёркнутый
        "4": lambda text: f"<u>{text}</u>",               # Подчёркнутый
        "5": lambda text: f"<code>{text}</code>",         # Моно
        "6": lambda text: f"<b><i>{text}</i></b>",        # Жирный курсив
    }

    async def stylecmd(self, message):
        """<номер стиля> — включить автоматический стиль"""
        arg = utils.get_args_raw(message)
        if arg not in self.styles:
            await message.edit("❌ Укажи корректный номер стиля от 1 до 6\n👉 .stylehelp — справка по стилям")
            return
        self.set("style_mode", arg)
        await message.edit(f"✅ Стиль <b>{arg}</b> активирован.\nТеперь все твои сообщения будут форматироваться.")

    async def styleoffcmd(self, message):
        """Отключить автоматический стиль"""
        self.set("style_mode", None)
        await message.edit("🛑 Автостиль отключён.")

    async def stylehelpcmd(self, message):
        """Показать список доступных стилей"""
        text = (
            "<b>📚 Стили:</b>\n"
            "1 — <b>Жирный</b>\n"
            "2 — <i>Курсив</i>\n"
            "3 — <s>Зачёркнутый</s>\n"
            "4 — <u>Подчёркнутый</u>\n"
            "5 — <code>Моноширинный</code>\n"
            "6 — <b><i>Жирный курсив</i></b>\n\n"
            "✏️ Используй: <code>.style [номер]</code>\n"
            "❌ Отключить: <code>.styleoff</code>"
        )
        await message.edit(text)

    @loader.unrestricted
    async def watcher(self, message):
        if not message.out or not message.text or not self.get("style_mode"):
            return

        style = self.get("style_mode")
        styler = self.styles.get(style)

        if not styler:
            return

        styled_text = styler(message.raw_text)

        try:
            await message.edit(styled_text, parse_mode="html")
        except:
            pass