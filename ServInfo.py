from .. import loader, utils
import time
import datetime
import psutil
import subprocess
import platform

@loader.tds
class ServInfoMod(loader.Module):
    """📊 Модуль ServInfo - расширенная информация о системе"""
    strings = {"name": "ServInfo"}

    async def servinfocmd(self, message):
        """Полная статистика бота и сервера"""
        start = time.time()
        await message.edit("<b>🔄 Сбор данных...</b>")
        
        # Основные метрики
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ping = (time.time() - start) * 1000
        
        # Информация о системе
        try:
            cpu_usage = f"{psutil.cpu_percent()}%"
            cpu_count = psutil.cpu_count()
            cpu_freq = f"{psutil.cpu_freq().current:.0f}MHz" if hasattr(psutil.cpu_freq(), 'current') else "N/A"
            
            mem = psutil.virtual_memory()
            mem_total = f"{mem.total/1024/1024:.1f} MB"
            mem_used = f"{mem.used/1024/1024:.1f} MB"
            mem_percent = f"{mem.percent}%"
            
            disk = psutil.disk_usage('/')
            disk_total = f"{disk.total/1024/1024:.1f} GB"
            disk_used = f"{disk.used/1024/1024:.1f} GB"
            disk_percent = f"{disk.percent}%"
            
            boot_time = psutil.boot_time()
            uptime = str(datetime.timedelta(seconds=int(time.time() - boot_time)))
            
            proc = psutil.Process()
            bot_uptime = str(datetime.timedelta(seconds=int(time.time() - proc.create_time())))
            bot_mem = f"{proc.memory_info().rss/1024/1024:.1f} MB"
            
            os_info = f"{platform.system()} {platform.release()}"
            
            result = (
                f"<b>🖥 Серверная информация</b>\n"
                f"<b>OS:</b> {os_info}\n"
                f"<b>CPU:</b> {cpu_count} ядер, {cpu_usage} ({cpu_freq})\n"
                f"<b>RAM:</b> {mem_used}/{mem_total} ({mem_percent})\n"
                f"<b>Disk:</b> {disk_used}/{disk_total} ({disk_percent})\n"
                f"<b>Uptime:</b> {uptime}\n\n"
                
                f"<b>🤖 Информация о боте</b>\n"
                f"<b>Время:</b> {now}\n"
                f"<b>Пинг:</b> {ping:.2f} мс\n"
                f"<b>Память:</b> {bot_mem}\n"
                f"<b>Uptime:</b> {bot_uptime}\n\n"
                
                f"<i>⚙️ by @g4ivx | v1.4.8.8</i>"
            )
            
        except Exception as e:
            result = f"<b>⚠️ Ошибка:</b> {str(e)}"
        
        await message.edit(result)