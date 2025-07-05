# meta developer: @destr4kt_def
# module: hentay.py
# 🔞 NSFW + NUDE + GIF-комбо by @destr4kt_def

__version__ = (1, 3, 0)

from .. import loader
import requests
import asyncio

@loader.tds
class HentayMod(loader.Module):
    """🔞 Модуль для NSFW, NUDE и Hentai GIF"""

    strings = {"name": "Hentay"}

    async def hentaycmd(self, message):
        """Прислать случайную NSFW-картинку"""
        if not message.is_private:
            m = await message.reply("❌ К сожалению, данный модуль работает только в личных сообщениях.")
            await asyncio.sleep(3)
            await m.delete()
            return
        msg = await message.reply("🔍 ищу хентай фотки...")
        try:
            r = requests.get("https://api.waifu.im/search", params={"is_nsfw": "true"})
            r.raise_for_status()
            data = r.json()["images"][0]
            url = data["url"]
            cap = "🖼 Вот твоё хентай-арт\n👤 by @destr4kt_def"
            try: await msg.delete()
            except: pass
            await message.client.send_file(message.chat_id, url, caption=cap)
        except Exception as e:
            await msg.edit(f"💥 Ошибка:\n<code>{e}</code>")

    async def fhentaycmd(self, message):
        """Прислать откровенный NSFW"""
        if not message.is_private:
            m = await message.reply("❌ К сожалению, данный модуль работает только в личных сообщениях.")
            await asyncio.sleep(3)
            await m.delete()
            return
        msg = await message.reply("🔍 ищу тебе откровенный NSFW...")
        try:
            r = requests.get("https://api.waifu.im/search", params={
                "is_nsfw": "true",
                "included_tags": "hentai"
            })
            r.raise_for_status()
            data = r.json()["images"][0]
            url = data["url"]
            cap = "🔥 Откровенный NSFW доставлен!\n👤 by @destr4kt_def"
            try: await msg.delete()
            except: pass
            await message.client.send_file(message.chat_id, url, caption=cap)
        except Exception as e:
            await msg.edit(f"💥 Ошибка:\n<code>{e}</code>")

    async def hentaygifcmd(self, message):
        """Прислать NSFW-хентай GIF"""
        if not message.is_private:
            m = await message.reply("❌ К сожалению, данный модуль работает только в личных сообщениях.")
            await asyncio.sleep(3)
            await m.delete()
            return
        msg = await message.reply("🔍 ищу хентай GIF...")
        try:
            r = requests.get("https://api.waifu.im/search", params={
                "is_nsfw": "true",
                "gif": "true"
            })
            r.raise_for_status()
            data = r.json()["images"][0]
            url = data["url"]
            cap = "💦 Сочная NSFW GIF подъехала\n👤 by @destr4kt_def"
            try: await msg.delete()
            except: pass
            await message.client.send_file(message.chat_id, url, caption=cap)
        except Exception as e:
            await msg.edit(f"💥 Ошибка:\n<code>{e}</code>")

    async def helphentaycmd(self, message):
        """Показать помощь по hentay-модулю"""
        await message.reply(
            "<b>🔞 Hentay Module Help</b>\n\n"
            "📸 <b>Описание:</b>\n"
            "Модуль выдаёт NSFW, откровенные арты и гифки.\n\n"
            "📌 <b>Команды:</b>\n"
            "• <code>.hentay</code> — обычная NSFW‑картинка\n"
            "• <code>.fhentay</code> — откровенный NSFW (18+)\n"
            "• <code>.hentaygif</code> — NSFW GIF\n"
            "• <code>.helphentay</code> — помощь по модулю\n\n"
            "👤 Автор: @destr4kt_def\n"
            "📦 Версия: 1.3.0"
        )