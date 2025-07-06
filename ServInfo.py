from .. import loader, utils
import time, datetime, psutil, platform, subprocess

@loader.tds
class ServInfoMod(loader.Module):
    """Мониторинг сервера и бота"""
    strings = {"name": "ServInfo", "version": "1.7.1"}

    async def client_ready(self, client, db):
        self.premium = getattr(await client.get_me(), 'premium', False)

    async def servinfocmd(self, message):
        """Получить расширенную статистику"""
        start = time.time()
        
        # Emoji только для заголовков и разработчика
        EMOJI = {
            'header': "<emoji document_id=5877260593903177342>⚙</emoji>" if self.premium else "🖥️",
            'bot_header': "<emoji document_id=5310095495153065318>◽️</emoji>" if self.premium else "🤖",
            'dev': "<emoji document_id=5890925363067886150>✨</emoji>"
        }

        await message.edit(f"{EMOJI['header']} <b>Анализ системы...</b>", parse_mode='html')

        try:
            # Системная информация
            os_info = subprocess.getoutput("lsb_release -d").split(":")[1].strip() if platform.system() == "Linux" else platform.system()
            net = psutil.net_io_counters()
            proc = psutil.Process()
            
            result = (
                f"<b>{EMOJI['header']} Системная информация</b>\n"
                f"<b>OS:</b> {os_info}\n"
                f"<b>Ядро:</b> {platform.release()}\n"
                f"<b>CPU:</b> {psutil.cpu_count()} ядер, {psutil.cpu_percent()}%\n"
                f"<b>RAM:</b> {psutil.virtual_memory().used/1024/1024:.1f}MB/{psutil.virtual_memory().total/1024/1024:.1f}MB\n"
                f"<b>Disk:</b> {psutil.disk_usage('/').used/1024/1024/1024:.1f}GB/{psutil.disk_usage('/').total/1024/1024/1024:.1f}GB\n"
                f"<b>Сеть:</b> ▲ {net.bytes_sent/1024/1024:.1f}MB ▼ {net.bytes_recv/1024/1024:.1f}MB\n"
                f"<b>Процессы:</b> {len(psutil.pids())}\n"
                f"<b>Аптайм:</b> {str(datetime.timedelta(seconds=int(time.time() - psutil.boot_time())))}\n\n"
                
                f"<b>{EMOJI['bot_header']} Информация о боте</b>\n"
                f"<b>Время:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"<b>Пинг:</b> {(time.time() - start) * 1000:.2f}мс\n"
                f"<b>Память:</b> {proc.memory_info().rss/1024/1024:.1f}MB\n"
                f"<b>Аптайм:</b> {str(datetime.timedelta(seconds=int(time.time() - proc.create_time())))}\n\n"
                
                f"{EMOJI['dev']} developer @g4ivx | dev_test | v1.7.1"
            )
            
            await message.edit(result, parse_mode='html')
        except Exception as e:
            await message.edit(f"⚠️ <b>Ошибка:</b> {str(e)}", parse_mode='html')
