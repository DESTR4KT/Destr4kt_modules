# TextStylerMod v2.2
# by @destr4kt_def

from .. import loader, utils
from telethon import events
import asyncio

@loader.tds
class TextStylerMod(loader.Module):
    """Автостиль текста сообщений"""

    strings = {"name": "TextStylerMod"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "style_mode",
                None,
                lambda: "Номер включённого стиля (1–7), либо None"
            )
        )

    async def client_ready(self, client, db):
        self.me = await client.get_me()
        text = (
            "🪐 Модуль TextStylerMod загружен ʕっ•ᴥ•ʔっ\n"
            "ℹ️ Автостиль текста сообщений\n"
            "🛠 Версия: 2.2\n\n"
            "▫️ .style <номер стиля> — включить автоматический стиль\n"
            "▫️ .stylehelp — список доступных стилей\n"
            "▫️ .styleoff — отключить автоматический стиль\n\n"
            "👤 Автор: @destr4kt_def"
        )
        print(text)

    styles = {
        "1": lambda t: f"<b>{t}</b>",
        "2": lambda t: f"<i>{t}</i>",
        "3": lambda t: f"<s>{t}</s>",
        "4": lambda t: f"<u>{t}</u>",
        "5": lambda t: f"<spoiler>{t}</spoiler>",
        "6": lambda t: f"<code>{t}</code>",
        "7": lambda t: f"<b><i>{t}</i></b>",  # Жирный курсив
    }

    async def stylecmd(self, message):
        """<номер стиля> — включить автоматический стиль"""
        arg = utils.get_args_raw(message)
        if arg not in self.styles:
            await message.edit("❌ Укажи номер стиля от 1 до 7\n👉 .stylehelp — список стилей")
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
            "5 — <spoiler>Скрытый</spoiler>\n"
            "6 — <code>Моноширинный</code>\n"
            "7 — <b><i>Жирный курсив</i></b>\n\n"
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

        if style == "5":
            try:
                await message.delete()
                await message.client.send_message(
                    message.chat_id,
                    styled_text,
                    parse_mode="html"
                )
            except:
                pass
        else:
            try:
                await message.edit(styled_text, parse_mode="html")
            except:
                pass