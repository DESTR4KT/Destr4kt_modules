from .. import loader, utils
import subprocess

@loader.tds
class SpeedTestMod(loader.Module):
    """
    Тест скорости интернета с speedtest.net
    """
    strings = {"name": "SpeedTest", "version": "1.5.0"}

    async def client_ready(self, client, db):
        """Инициализация модуля и проверка статуса Premium."""
        self.premium = getattr(await client.get_me(), 'premium', False)

    async def speedcmd(self, message):
        """
        Запустить тест скорости интернета
        """
        # Определяем эмодзи по умолчанию
        EMOJI = {
            'header': "⚡️",
            'server': "📡",  
            'ping': "⏱️",   
            'download_upload_line_prefix': "📊",
            'share': "🔗",
            'dev': "✨"
        }

        # Если у пользователя Telegram Premium, заменяем эмодзи на премиумные
        if self.premium:
            EMOJI['header'] = "<emoji document_id=5881806211195605908>📸</emoji>"
            EMOJI['server'] = "<emoji document_id=5879785854284599288>ℹ️</emoji>"
            EMOJI['ping'] = "<emoji document_id=5890925363067886150>✨</emoji>"
            EMOJI['download_upload_line_prefix'] = "<emoji document_id=5874986954180791957>📶</emoji>"
            EMOJI['share'] = "<emoji document_id=6039451237743595514>📎</emoji>"
            EMOJI['dev'] = "<emoji document_id=5805532930662996322>✅</emoji>"

        await message.edit(f"{EMOJI['header']} <b>Запускаю тест скорости...</b>\n<i>Это может занять некоторое время (до 1-2 минут).</i>", parse_mode='html')

        try:
            # Запускаем команду speedtest-cli
            process = subprocess.run(
                ["speedtest-cli", "--secure", "--share"],
                capture_output=True,
                text=True,
                check=False
            )
            
            stdout = process.stdout
            stderr = process.stderr
            returncode = process.returncode

            # Обработка ошибок выполнения команды
            if returncode != 0:
                error_output = stderr if stderr else stdout
                await message.edit(f"⚠️ <b>Ошибка при выполнении speedtest (код {returncode}):</b>\n<code>{error_output}</code>", parse_mode='html')
                return

            if not stdout:
                await message.edit(f"⚠️ <b>Ошибка:</b> Не удалось получить вывод от speedtest-cli. Проверьте установку или права доступа.", parse_mode='html')
                return

            # Парсим вывод speedtest-cli для извлечения нужных данных
            parsed_data = {}
            for line in stdout.split('\n'):
                if "Hosted by" in line:
                    parts = line.split("Hosted by ", 1)[1]
                    server_name_loc = parts.split('[')[0].strip()
                    ping_match = parts.split(']: ')[-1].replace(' ms', '').strip()
                    
                    server_location_match = server_name_loc.split('(')[-1].replace(')', '').strip() if '(' in server_name_loc else "Неизвестно"
                    parsed_data['server_display'] = server_location_match
                    parsed_data['server_ping'] = ping_match
                elif "Download:" in line:
                    parsed_data['download'] = line.replace("Download: ", "").strip()
                elif "Upload:" in line:
                    parsed_data['upload'] = line.replace("Upload: ", "").strip()
                elif "Share results:" in line:
                    parsed_data['share_link'] = line.replace("Share results: ", "").strip()

            # Формируем итоговое сообщение
            result_lines = [
                f"<b>{EMOJI['header']} Результаты SpeedTest</b>",
                f"{EMOJI['server']} <b>Сервер:</b> {parsed_data.get('server_display', 'Неизвестно')}",
                f"{EMOJI['ping']} <b>Пинг:</b> {parsed_data.get('server_ping', 'N/A')} мс",
                f"{EMOJI['download_upload_line_prefix']} <b>Загрузка:</b> {parsed_data.get('download', 'N/A')} | <b>Отдача:</b> {parsed_data.get('upload', 'N/A')}",
            ]
            if parsed_data.get('share_link'):
                result_lines.append(f"{EMOJI['share']} <b>Поделиться:</b> <a href='{parsed_data['share_link']}'>Результат</a>")
            
            result_lines.append(f"\n{EMOJI['dev']} developer @g4ivx | dev_test | v{self.strings['version']}")

            final_message = "\n".join(result_lines)
            await message.edit(final_message, parse_mode='html')

        except FileNotFoundError:
            await message.edit("⚠️ <b>Ошибка:</b> Команда `speedtest-cli` не найдена.\nПожалуйста, установите ее на ваш сервер. Например: `sudo apt install speedtest-cli` или `pip install speedtest-cli`", parse_mode='html')
        except Exception as e:
            await message.edit(f"⚠️ <b>Произошла ошибка:</b> {e}", parse_mode='html')