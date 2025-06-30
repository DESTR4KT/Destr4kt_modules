# TranslateMod — переводчик текста с автоопределением языка
# Автор: @destr4kt_def | Версия: 1.3.0

from .. import loader, utils
from telethon.tl.types import Message
from deep_translator import GoogleTranslator

@loader.tds
class TranslateMod(loader.Module):
    """🪐 Многоязычный переводчик с автоопределением и редактированием сообщений."""

    strings = {
        "name": "TranslateMod",
        "langs": "📚 Популярные языки:\n\n{}",
        "langs_all": "📚 Полный список поддерживаемых языков:\n\n{}",
        "no_text": "❌ Укажи текст или ответь на сообщение.",
        "error": "⚠️ Ошибка перевода: {}",
        "loaded": (
            "🪐 <b>Модуль TranslateMod загружен ✅</b>\n"
            "👤 <b>Автор:</b> @destr4kt_def | 🏷️ <b>Версия:</b> 1.3.0\n"
            "ℹ️ <i>Многоязычный переводчик с автоопределением и редактированием сообщений</i>\n\n"
            "▫️ <code>.langs</code> 📚 Показать популярные языки с флагами\n"
            "▫️ <code>.langsall</code> 🌍 Показать полный список поддерживаемых языков по регионам\n"
            "▫️ <code>.translate</code> ✏️ Перевод текста на указанный язык (по умолчанию — на русский)\n\n"
            "👨‍💻 Developer: @destr4kt_def"
        ),
        "translate_help": (
            "✏️ <b>Перевод текста на указанный язык</b>\n\n"
            "<code>.translate [язык] <текст или ответ></code>\n"
            "Если язык не указан — используется 'ru' (русский).\n"
            "Поддерживается перевод по ответу на сообщение."
        ),
        "langs_help": "📚 <b>Показать список популярных языков</b>\n<code>.langs</code>",
        "langsall_help": "🌍 <b>Показать полный список языков по регионам</b>\n<code>.langsall</code>",
    }

    def __init__(self):
        self.name = self.strings["name"]
        self.default_lang = "ru"

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        await client.send_message("me", self.strings["loaded"])

    async def translatecmd(self, message: Message):
        """✏️ Перевод текста на указанный язык (по умолчанию — на русский)"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args and not reply:
            await utils.answer(message, self.strings["no_text"])
            return

        parts = args.split(maxsplit=1)
        target_lang = self.default_lang
        text = ""

        if len(parts) == 2:
            target_lang, text = parts
        elif reply:
            text = reply.raw_text
            if parts:
                target_lang = parts[0]
        else:
            text = args

        try:
            translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
            if message.out:
                await message.edit(translated)
            else:
                await utils.answer(message, translated)
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def langscmd(self, message: Message):
        """📚 Показать популярные языки с флагами"""
        langs = {
            "en": "🇬🇧 English",
            "ru": "🇷🇺 Russian",
            "es": "🇪🇸 Spanish",
            "de": "🇩🇪 German",
            "fr": "🇫🇷 French",
            "it": "🇮🇹 Italian",
            "pt": "🇵🇹 Portuguese",
            "ja": "🇯🇵 Japanese",
            "zh-CN": "🇨🇳 Chinese",
            "ko": "🇰🇷 Korean",
            "uk": "🇺🇦 Ukrainian",
            "ar": "🇸🇦 Arabic",
            "hi": "🇮🇳 Hindi",
            "tr": "🇹🇷 Turkish",
        }
        msg = "\n".join([f"`{code}` — {name}" for code, name in langs.items()])
        await utils.answer(message, self.strings["langs"].format(msg))

    async def langsallcmd(self, message: Message):
        """🌍 Показать полный список поддерживаемых языков с названиями стран"""
        regions = {
            "🌍 Европейские": {
                "en": "English / United Kingdom",
                "ru": "Russian / Russia",
                "fr": "French / France",
                "de": "German / Germany",
                "es": "Spanish / Spain",
                "it": "Italian / Italy",
                "pt": "Portuguese / Portugal",
                "uk": "Ukrainian / Ukraine",
                "pl": "Polish / Poland",
                "nl": "Dutch / Netherlands",
                "cs": "Czech / Czechia",
                "ro": "Romanian / Romania",
                "sv": "Swedish / Sweden",
                "fi": "Finnish / Finland",
                "no": "Norwegian / Norway",
                "da": "Danish / Denmark",
                "el": "Greek / Greece",
                "hu": "Hungarian / Hungary",
                "sk": "Slovak / Slovakia",
                "sl": "Slovenian / Slovenia",
                "bg": "Bulgarian / Bulgaria",
                "hr": "Croatian / Croatia",
                "lt": "Lithuanian / Lithuania",
                "lv": "Latvian / Latvia",
                "et": "Estonian / Estonia",
            },
            "🌏 Азиатские": {
                "ja": "Japanese / Japan",
                "zh-CN": "Chinese (Simplified) / China",
                "zh-TW": "Chinese (Traditional) / Taiwan",
                "ko": "Korean / South Korea",
                "hi": "Hindi / India",
                "th": "Thai / Thailand",
                "vi": "Vietnamese / Vietnam",
                "id": "Indonesian / Indonesia",
                "ms": "Malay / Malaysia",
                "ta": "Tamil / India",
                "te": "Telugu / India",
                "bn": "Bengali / Bangladesh",
                "fa": "Persian / Iran",
                "he": "Hebrew / Israel",
                "ur": "Urdu / Pakistan",
                "pa": "Punjabi / India",
            },
            "🌎 Американские": {
                "ht": "Haitian Creole / Haiti",
                "qu": "Quechua / Peru",
                "gn": "Guarani / Paraguay",
                "ay": "Aymara / Bolivia",
            },
            "🌍 Африканские": {
                "af": "Afrikaans / South Africa",
                "sw": "Swahili / Kenya",
                "zu": "Zulu / South Africa",
                "yo": "Yoruba / Nigeria",
                "ig": "Igbo / Nigeria",
                "am": "Amharic / Ethiopia",
                "ha": "Hausa / Nigeria",
                "st": "Sesotho / Lesotho",
            },
            "🧪 Прочие": {
                "la": "Latin / Ancient Rome",
                "eo": "Esperanto / Constructed",
                "cy": "Welsh / Wales",
                "gd": "Scots Gaelic / Scotland",
                "is": "Icelandic / Iceland",
            },
        }

        result = ""
        for region, langs in regions.items():
            result += f"<b>{region}</b>\n"
            for code, full in langs.items():
                result += f"`{code}` — {full}\n"
            result += "\n"

        await utils.answer(message, self.strings["langs_all"].format(result.strip()))