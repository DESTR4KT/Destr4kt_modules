# ✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦
#   _______ _      ______          _____          
#  |__   __| |    |  ____|   /\   |  __ \         
#     | |  | |__  | |__     /  \  | |  | |        
#     | |  | '_ \ |  __|   / /\ \ | |  | |        
#     | |  | | | || |____ / ____ \| |__| |        
#     |_|  |_| |_||______/_/    \_\_____/  v1.0  
#
#   ✪ Модуль сделан @destr4kt_def
# ✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦

from .. import loader, utils
import asyncio, random

def get_empty_board():
    return [[" "]*3 for _ in range(3)]

def render_board(board):
    symbols = {"X": "❌", "O": "⭕", " ": "⬜"}
    return "\n".join("".join(symbols[cell] for cell in row) for row in board)

def check_winner(board):
    for p in ["X", "O"]:
        b = board
        win = any([
            all(c == p for c in row) for row in b
        ]) or any([
            all(row[i] == p for row in b) for i in range(3)
        ]) or all([
            b[i][i] == p for i in range(3)
        ]) or all([
            b[i][2-i] == p for i in range(3)
        ])
        if win:
            return p
    return None

def board_full(board):
    return all(cell != " " for row in board for cell in row)

class TicTacToeMod(loader.Module):
    """🎮 Крестики-Нолики: игра с ИИ или вдвоём

Модуль сделан @destr4kt_def
"""
    strings = {"name": "TicTacToe"}

    def __init__(self):
        self.games = {}
        self.stats = {}

    async def client_ready(self, client, db):
        self.db = db
        self.stats = db.get("TicTacToe", "stats", {})

    def save_stats(self):
        self.db.set("TicTacToe", "stats", self.stats)

    async def tictactoeaicmd(self, message):
        """Начать игру с ИИ"""
        uid = message.chat_id
        self.games[uid] = {"board": get_empty_board(), "turn": "X", "ai": True}
        await message.edit("🎮 Игра с ИИ начата!\nХодите: .move <1-9>\n\n" + render_board(self.games[uid]["board"]))

    async def tictactoecmd(self, message):
        """Начать игру вдвоём"""
        uid = message.chat_id
        self.games[uid] = {"board": get_empty_board(), "turn": "X", "ai": False}
        await message.edit("🎮 Игра 1v1 начата!\nХодите: .move <1-9>\n\n" + render_board(self.games[uid]["board"]))

    async def movecmd(self, message):
        """Сделать ход: .move <позиция от 1 до 9>"""
        args = utils.get_args(message)
        uid = message.chat_id

        if uid not in self.games:
            await message.edit("🚫 Нет активной игры.")
            return

        game = self.games[uid]

        if check_winner(game["board"]) or board_full(game["board"]):
            del self.games[uid]
            await message.edit("🎯 Игра уже завершена!")
            return

        if not args or not args[0].isdigit() or not 1 <= int(args[0]) <= 9:
            await message.edit("❗ Укажи позицию от 1 до 9.")
            return

        pos = int(args[0]) - 1
        row, col = divmod(pos, 3)

        if game["board"][row][col] != " ":
            await message.edit("🚫 Клетка занята!")
            return

        player = game["turn"]
        game["board"][row][col] = player

        winner = check_winner(game["board"])
        full = board_full(game["board"])

        if winner or full:
            await self.end_game(message, winner, game)
            return

        game["turn"] = "O" if player == "X" else "X"

        if game["ai"] and game["turn"] == "O":
            await asyncio.sleep(0.5)
            self.ai_move(game)
            winner = check_winner(game["board"])
            full = board_full(game["board"])
            if winner or full:
                await self.end_game(message, winner, game)
                return
            game["turn"] = "X"

        await message.edit(f"🧩 Ход: {game['turn']}\n\n" + render_board(game["board"]))

    def ai_move(self, game):
        b = game["board"]
        for i in range(3):
            for j in range(3):
                if b[i][j] == " ":
                    b[i][j] = "O"
                    if check_winner(b) == "O":
                        return
                    b[i][j] = " "
        for i in range(3):
            for j in range(3):
                if b[i][j] == " ":
                    b[i][j] = "X"
                    if check_winner(b) == "X":
                        b[i][j] = "O"
                        return
                    b[i][j] = " "
        empties = [(i, j) for i in range(3) for j in range(3) if b[i][j] == " "]
        if empties:
            i, j = random.choice(empties)
            b[i][j] = "O"

    async def end_game(self, message, winner, game):
        board = render_board(game["board"])
        uid = message.chat_id
        if winner:
            text = f"🎉 Победа: {winner}!\n\n{board}"
            self.stats[str(uid)] = self.stats.get(str(uid), {"X": 0, "O": 0, "draws": 0})
            self.stats[str(uid)][winner] += 1
        else:
            text = f"🤝 Ничья!\n\n{board}"
            self.stats[str(uid)]["draws"] += 1
        self.save_stats()
        del self.games[uid]
        await message.edit(text)

    async def ttstatscmd(self, message):
        """Показать статистику"""
        uid = str(message.chat_id)
        stat = self.stats.get(uid, {"X": 0, "O": 0, "draws": 0})
        await message.edit(
            f"📊 Статистика:\n"
            f"❌ Побед X: {stat['X']}\n"
            f"⭕ Побед O: {stat['O']}\n"
            f"🤝 Ничьих: {stat['draws']}"
        )

    async def ttresetcmd(self, message):
        """Сбросить статистику"""
        uid = str(message.chat_id)
        self.stats[uid] = {"X": 0, "O": 0, "draws": 0}
        self.save_stats()
        await message.edit("♻️ Статистика сброшена.")

    async def tthelpcmd(self, message):
        """Показать список команд модуля"""
        await message.edit(
            "🕹 Команды модуля TicTacToe:\n\n"
            "• .tictactoe — начать игру вдвоём\n"
            "• .tictactoeai — начать игру с ИИ\n"
            "• .move <1-9> — сделать ход\n"
            "• .ttstats — статистика побед и ничьих\n"
            "• .ttreset — сброс статистики"
        )