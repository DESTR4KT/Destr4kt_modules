from .. import loader, utils
import time
import datetime
import psutil
import platform
import subprocess

@loader.tds
class ServInfoMod(loader.Module):
    """Мониторинг сервера и бота"""
    strings = {
        "name": "ServInfo",
        "version": "1.6.1",
        "description": "Полная статистика сервера и бота"
    }

    async def servinfocmd(self, message):
        """Получить статистику"""
        start = time.time()
        
        # Кастомные emoji (оставляем как есть)
        SERVER_EMOJI = "<emoji document_id=5775870512127283512>🍏</emoji>"
        BOT_EMOJI = "<emoji document_id=6035084557378654059>👤</emoji>"
        DEV_EMOJI = "<emoji document_id=5890925363067886150>✨</emoji>"
        
        # Стандартные emoji для всех строк
        EMOJI = {
            'os': "🖥️",
            'kernel': "⚙️",
            'cpu': "🧠", 
            'ram': "💾",
            'disk': "💽",
            'net': "🌐",
            'proc': "🔄",
            'uptime': "⏱️",
            'time': "🕒",
            'ping': "📶",
            'mem': "📊"
        }
        
        await message.edit(f"{SERVER_EMOJI} <b>Сбор данных...</b>", parse_mode='html')
        
        try:
            # Получаем данные об ОС
            try:
                os_info = subprocess.check_output("lsb_release -d", shell=True).decode().split(":")[1].strip()
            except:
                os_info = platform.system()
            
            # Сетевые метрики
            net = psutil.net_io_counters()
            
            # Основные метрики
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ping = (time.time() - start) * 1000
            
            # Форматирование вывода
            result = (
                f"{SERVER_EMOJI} <b>Серверная информация</b>\n"
                f"{EMOJI['os']} <b>OS:</b> {os_info}\n"
                f"{EMOJI['kernel']} <b>Ядро:</b> {platform.release()}\n"
                f"{EMOJI['cpu']} <b>CPU:</b> {psutil.cpu_count()} ядер, {psutil.cpu_percent()}%\n"
                f"{EMOJI['ram']} <b>RAM:</b> {psutil.virtual_memory().used/1024/1024:.1f}MB/{psutil.virtual_memory().total/1024/1024:.1f}MB\n"
                f"{EMOJI['disk']} <b>Disk:</b> {psutil.disk_usage('/').used/1024/1024/1024:.1f}GB/{psutil.disk_usage('/').total/1024/1024/1024:.1f}GB\n"
                f"{EMOJI['net']} <b>Сеть:</b> ▲ {net.bytes_sent/1024/1024:.1f}MB ▼ {net.bytes_recv/1024/1024:.1f}MB\n"
                f"{EMOJI['proc']} <b>Процессы:</b> {len(psutil.pids())}\n"
                f"{EMOJI['uptime']} <b>Uptime:</b> {str(datetime.timedelta(seconds=int(time.time() - psutil.boot_time())))}\n\n"
                
                f"{BOT_EMOJI} <b>Информация о боте</b>\n"
                f"{EMOJI['time']} <b>Время:</b> {now}\n"
                f"{EMOJI['ping']} <b>Пинг:</b> {ping:.2f}мс\n"
                f"{EMOJI['mem']} <b>Память:</b> {psutil.Process().memory_info().rss/1024/1024:.1f}MB\n"
                f"{EMOJI['uptime']} <b>Uptime:</b> {str(datetime.timedelta(seconds=int(time.time() - psutil.Process().create_time())))}\n\n"
                
                f"{DEV_EMOJI} developer @g4ivx | dev_test | v1.6.1"
            )
            
            await message.edit(result, parse_mode='html')
        except Exception as e:
            await message.edit(f"⚠️ <b>Ошибка:</b> {str(e)}", parse_mode='html')