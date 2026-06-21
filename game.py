import tkinter as tk
from tkinter import font
import math
import random
import time
import os
import sys

# ========== ВСТРОЕННЫЕ ЗВУКИ (без внешних файлов) ==========
class SoundMaker:
    """Генератор звуков прямо в коде (без внешних файлов)"""
    
    @staticmethod
    def beep(freq=440, duration=200):
        """Создаёт звук через системный динамик"""
        try:
            if sys.platform == "win32":
                import winsound
                winsound.Beep(freq, duration)
            else:
                # Для Linux/Mac - печатаем символ
                print('\a', end='', flush=True)
        except:
            pass
    
    @staticmethod
    def click():
        SoundMaker.beep(800, 50)
    
    @staticmethod
    def success():
        SoundMaker.beep(523, 150)
        time.sleep(0.1)
        SoundMaker.beep(659, 150)
        time.sleep(0.1)
        SoundMaker.beep(784, 200)
    
    @staticmethod
    def fail():
        SoundMaker.beep(300, 300)
        time.sleep(0.1)
        SoundMaker.beep(200, 400)
    
    @staticmethod
    def win():
        for note in [523, 587, 659, 784, 880, 988, 1047]:
            SoundMaker.beep(note, 100)
            time.sleep(0.05)
    
    @staticmethod
    def ambient():
        """Имитация фоновой атмосферы (короткие звуки)"""
        pass  # Тишина, чтобы не раздражала

# ========== ГЛАВНАЯ ИГРА ==========
class SuperLabGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧪 ПОБЕГ ИЗ ЛАБОРАТОРИИ")
        self.root.geometry("1000x800")
        self.root.configure(bg='#0a0a1a')
        self.root.resizable(False, False)
        
        # Игровые переменные
        self.card = False
        self.power = False
        self.step = 0
        self.attempts = 0
        self.animating = False
        self.player_x = 450
        self.player_y = 380
        self.walk_frame = 0
        
        # ===== ПЕРСОНАЖ =====
        self.player_emoji = "🧑‍🔬"
        self.player_name = "Учёный"
        
        # Верхняя панель с информацией о персонаже
        self.top_frame = tk.Frame(root, bg='#0a0a1a', height=60)
        self.top_frame.pack(fill=tk.X, pady=5)
        
        self.player_label = tk.Label(
            self.top_frame,
            text=f"{self.player_emoji} {self.player_name}",
            font=("Arial", 16, "bold"),
            fg='#ffd700',
            bg='#0a0a1a'
        )
        self.player_label.pack(side=tk.LEFT, padx=20)
        
        # Инвентарь
        self.inventory_label = tk.Label(
            self.top_frame,
            text="🎒 Инвентарь: ",
            font=("Arial", 12),
            fg='#88ccff',
            bg='#0a0a1a'
        )
        self.inventory_label.pack(side=tk.LEFT, padx=20)
        
        self.inventory_items = tk.Label(
            self.top_frame,
            text="(пусто)",
            font=("Arial", 12),
            fg='#666677',
            bg='#0a0a1a'
        )
        self.inventory_items.pack(side=tk.LEFT)
        
        # Счётчик попыток
        self.attempts_label = tk.Label(
            self.top_frame,
            text=f"🎮 Попыток: {self.attempts}",
            font=("Arial", 12),
            fg='#666677',
            bg='#0a0a1a'
        )
        self.attempts_label.pack(side=tk.RIGHT, padx=20)
        
        # ===== ХОЛСТ ДЛЯ РИСОВАНИЯ =====
        self.canvas = tk.Canvas(
            root,
            width=950,
            height=480,
            bg='#0a0a1a',
            highlightthickness=2,
            highlightcolor='#ffd700'
        )
        self.canvas.pack(pady=5)
        
        # ===== ТЕКСТ ИСТОРИИ =====
        self.text_frame = tk.Frame(root, bg='#0a0a1a')
        self.text_frame.pack(pady=10, fill=tk.X, padx=30)
        
        self.story_text = tk.Text(
            self.text_frame,
            height=3,
            font=("Comic Sans MS", 13),
            fg='#ffffff',
            bg='#1a1a2e',
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=3,
            highlightthickness=1,
            highlightcolor='#ffd700'
        )
        self.story_text.pack(fill=tk.X)
        self.story_text.config(state=tk.DISABLED)
        
        # ===== СТАТУС БАР =====
        self.status_bar = tk.Label(
            root,
            text="🔍 Добро пожаловать в лабораторию!",
            font=("Arial", 11),
            fg='#888899',
            bg='#0a0a1a'
        )
        self.status_bar.pack()
        
        # ===== КНОПКИ =====
        self.button_frame = tk.Frame(root, bg='#0a0a1a')
        self.button_frame.pack(pady=15)
        
        self.btn1 = self.create_button(
            "🔍 ВЫБОР 1",
            '#00ff88',
            self.choice1,
            '#00cc66'
        )
        self.btn1.pack(side=tk.LEFT, padx=20)
        
        self.btn2 = self.create_button(
            "🚪 ВЫБОР 2",
            '#ff6b6b',
            self.choice2,
            '#cc5555'
        )
        self.btn2.pack(side=tk.LEFT, padx=20)
        
        # Кнопка перезапуска
        self.restart_btn = self.create_button(
            "🔄 НАЧАТЬ ЗАНОВО",
            '#ffd93d',
            self.restart,
            '#ccaa33',
            width=20
        )
        
        # ===== ПОДСКАЗКИ =====
        self.hint_label = tk.Label(
            root,
            text="💡 Подсказка: Исследуйте всё вокруг!",
            font=("Arial", 10, "italic"),
            fg='#555566',
            bg='#0a0a1a'
        )
        self.hint_label.pack(pady=5)
        
        # Запуск игры
        self.show_scene(0)
    
    def create_button(self, text, color, command, hover_color=None, width=18):
        """Создаёт красивую кнопку"""
        if hover_color is None:
            hover_color = color
        
        btn = tk.Button(
            self.button_frame,
            text=text,
            font=("Arial", 13, "bold"),
            width=width,
            height=2,
            bg=color,
            fg='#000000',
            relief=tk.RAISED,
            bd=4,
            cursor='hand2',
            command=command,
            activebackground=hover_color,
            activeforeground='#000000'
        )
        
        # Эффекты наведения
        def on_enter(e):
            btn.config(bg=hover_color, bd=5)
            SoundMaker.click()
        
        def on_leave(e):
            btn.config(bg=color, bd=4)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn
    
    # ========== РИСОВАНИЕ ПЕРСОНАЖА ==========
    def draw_player(self, x, y, frame=0):
        """Рисует персонажа на холсте"""
        self.canvas.delete("player")
        
        # Тело персонажа (круг)
        body_color = '#ffd93d'
        if frame % 2 == 0:
            body_color = '#ffcc00'
        
        # Тень
        self.canvas.create_oval(x-25, y+30, x+25, y+40, 
                                fill='#00000033', outline='', tags="player")
        
        # Тело
        self.canvas.create_oval(x-22, y-20, x+22, y+22, 
                                fill=body_color, outline='#cc9900', 
                                width=2, tags="player")
        
        # Глаза
        self.canvas.create_oval(x-10, y-5, x-3, y+3, 
                                fill='white', outline='black', tags="player")
        self.canvas.create_oval(x+3, y-5, x+10, y+3, 
                                fill='white', outline='black', tags="player")
        
        # Зрачки (смотрят в сторону движения)
        self.canvas.create_oval(x-7, y-2, x-5, y+1, 
                                fill='black', tags="player")
        self.canvas.create_oval(x+5, y-2, x+7, y+1, 
                                fill='black', tags="player")
        
        # Рот (улыбка или серьёзный)
        if frame % 4 < 2:
            self.canvas.create_arc(x-8, y+3, x+8, y+12, 
                                   start=0, extent=-180, 
                                   style=tk.ARC, width=2, 
                                   outline='black', tags="player")
        else:
            self.canvas.create_line(x-8, y+8, x+8, y+8, 
                                    fill='black', width=2, tags="player")
        
        # Имя над персонажем
        self.canvas.create_text(x, y-35, text=self.player_emoji, 
                                font=("Arial", 16), tags="player")
        self.canvas.create_text(x, y-50, text=self.player_name, 
                                font=("Arial", 8, "bold"), 
                                fill='#ffd700', tags="player")
    
    # ========== РИСОВАНИЕ ЛОКАЦИЙ ==========
    def draw_room(self):
        """Рисует комнату с персонажем"""
        self.canvas.delete("all")
        
        # Стены
        self.canvas.create_rectangle(30, 30, 920, 450, 
                                     fill='#2d2d44', outline='#444466', width=3)
        
        # Пол
        for i in range(20):
            x = 30 + i * 45
            self.canvas.create_rectangle(x, 380, x+22, 450, 
                                         fill='#3d3d55' if i%2==0 else '#35354d',
                                         outline='')
        
        # Светильник
        self.canvas.create_oval(400, 50, 550, 120, 
                                fill='#ffdd44', outline='#ffaa00', width=2)
        for i in range(8):
            angle = i * 45
            x1 = 475 + 60 * math.cos(math.radians(angle))
            y1 = 85 + 60 * math.sin(math.radians(angle))
            self.canvas.create_line(475, 85, x1, y1, 
                                    fill='#ffdd4466', width=1)
        
        # Дверь
        self.canvas.create_rectangle(780, 180, 870, 370, 
                                     fill='#8B4513', outline='#654321', width=3)
        self.canvas.create_oval(850, 250, 860, 270, 
                                fill='#ffd700', outline='#cc9900', width=2)
        self.canvas.create_text(825, 260, text="🚪", font=("Arial", 30))
        
        # Стол
        self.canvas.create_rectangle(120, 300, 350, 370, 
                                     fill='#5d3a1a', outline='#3d2a0a', width=2)
        self.canvas.create_rectangle(130, 270, 145, 300, fill='#5d3a1a')
        self.canvas.create_rectangle(325, 270, 340, 300, fill='#5d3a1a')
        
        # Предметы на столе
        self.canvas.create_oval(180, 310, 210, 340, 
                                fill='#66ccff', outline='#3399cc', width=2)
        self.canvas.create_rectangle(250, 320, 300, 345, 
                                      fill='#888899', outline='#666677', width=2)
        
        # Карта (если есть)
        if self.card:
            self.canvas.create_rectangle(200, 280, 300, 320, 
                                         fill='#ffd700', outline='#cc9900', width=3)
            self.canvas.create_text(250, 300, text="🗂️ КАРТА", 
                                    font=("Arial", 12, "bold"), fill='#000000')
        
        # Персонаж
        self.draw_player(self.player_x, self.player_y, self.walk_frame)
        
        # Название
        self.canvas.create_text(475, 55, text="🏚️ ЗАБРОШЕННАЯ ЛАБОРАТОРИЯ", 
                                font=("Arial", 16, "bold"), fill='#888899')
    
    def draw_electric(self):
        """Рисует электрощитовую"""
        self.canvas.delete("all")
        
        # Стены
        self.canvas.create_rectangle(30, 30, 920, 450, 
                                     fill='#1a2a1a', outline='#33aa33', width=3)
        
        # Пол
        for i in range(20):
            x = 30 + i * 45
            self.canvas.create_rectangle(x, 380, x+22, 450, 
                                         fill='#2a3a2a' if i%2==0 else '#223a22',
                                         outline='')
        
        # Щитки
        for i in range(3):
            x = 130 + i * 230
            self.canvas.create_rectangle(x, 150, x+180, 330, 
                                         fill='#333355', outline='#6666aa', width=2)
            self.canvas.create_text(x+90, 180, text=f"ЩИТ {i+1}", 
                                    font=("Arial", 12, "bold"), fill='#88ccff')
            
            # Лампочки
            colors = ['#ff4444', '#44ff44' if self.power else '#ffaa00', '#ffaa00']
            for j in range(3):
                y = 210 + j * 30
                self.canvas.create_oval(x+30+j*35, y, x+50+j*35, y+20, 
                                        fill=colors[j] if j < len(colors) else '#ffaa00',
                                        outline='#ffffff')
        
        # Рычаг
        self.canvas.create_rectangle(780, 200, 830, 350, 
                                     fill='#666677', outline='#888899', width=2)
        if self.power:
            self.canvas.create_rectangle(800, 180, 810, 200, 
                                         fill='#44ff44', outline='#33cc33', width=2)
            self.canvas.create_text(805, 280, text="⚡", font=("Arial", 30))
            self.canvas.create_text(805, 310, text="ВКЛ", 
                                    font=("Arial", 10, "bold"), fill='#44ff44')
        else:
            self.canvas.create_rectangle(800, 250, 810, 270, 
                                         fill='#ff4444', outline='#cc3333', width=2)
            self.canvas.create_text(805, 280, text="⚡", font=("Arial", 30))
        
        # Персонаж
        self.draw_player(self.player_x, self.player_y, self.walk_frame)
        
        # Название
        self.canvas.create_text(475, 55, text="⚡ ЭЛЕКТРОЩИТОВАЯ", 
                                font=("Arial", 16, "bold"), fill='#88ff88')
    
    def draw_reactor(self):
        """Рисует реакторную"""
        self.canvas.delete("all")
        
        # Стены
        self.canvas.create_rectangle(30, 30, 920, 450, 
                                     fill='#1a1a2a', outline='#44aaff', width=3)
        
        # Пол
        for i in range(20):
            x = 30 + i * 45
            self.canvas.create_rectangle(x, 380, x+22, 450, 
                                         fill='#2a2a3a' if i%2==0 else '#222a3a',
                                         outline='')
        
        # Реактор
        self.canvas.create_oval(350, 130, 600, 330, 
                                fill='#3355aa', outline='#44aaff', width=3)
        self.canvas.create_oval(390, 170, 560, 290, 
                                fill='#2255cc', outline='#66ccff', width=2)
        self.canvas.create_oval(430, 210, 520, 250, 
                                fill='#1166dd', outline='#88ddff', width=2)
        
        # Анимация реактора (пульсирующее свечение)
        pulse = int(150 + 50 * math.sin(time.time() * 2))
        self.canvas.create_oval(350, 130, 600, 330, 
                                fill=f'#44aaff{pulse:02x}', outline='', 
                                stipple='gray25')
        
        # Люк
        self.canvas.create_rectangle(730, 280, 830, 370, 
                                     fill='#333344', outline='#6666aa', width=2)
        self.canvas.create_text(780, 325, text="🕳️", font=("Arial", 40))
        
        # Персонаж
        self.draw_player(self.player_x, self.player_y, self.walk_frame)
        
        # Название
        self.canvas.create_text(475, 55, text="☢️ РЕАКТОРНАЯ", 
                                font=("Arial", 16, "bold"), fill='#44aaff')
    
    def draw_ending(self, ending_type):
        """Рисует финальную сцену"""
        self.canvas.delete("all")
        
        # Фон
        self.canvas.create_rectangle(0, 0, 950, 480, fill='#0a0a1a')
        
        if ending_type == "secret":
            self.canvas.create_text(475, 150, text="🕳️", font=("Arial", 80))
            self.canvas.create_text(475, 250, text="СЕКРЕТНЫЙ ТОННЕЛЬ", 
                                    font=("Arial", 30, "bold"), fill='#ffd700')
            self.canvas.create_text(475, 320, text="🏆 ВЫ СОВЕРШИЛИ ПОБЕГ! 🏆", 
                                    font=("Arial", 26, "bold"), fill='#ff6b6b')
            # Звёзды
            for i in range(20):
                x = random.randint(50, 900)
                y = random.randint(30, 430)
                self.canvas.create_oval(x, y, x+3, y+3, fill='#ffd700')
        
        elif ending_type == "best":
            self.canvas.create_text(475, 150, text="🌅", font=("Arial", 80))
            self.canvas.create_text(475, 280, text="🏆 ВЫ НА СВОБОДЕ! 🏆", 
                                    font=("Arial", 30, "bold"), fill='#ffd700')
            self.canvas.create_text(475, 350, text="ЛУЧШАЯ КОНЦОВКА", 
                                    font=("Arial", 22, "bold"), fill='#00ff88')
            # Солнечные лучи
            for i in range(12):
                angle = i * 30
                x = 475 + 200 * math.cos(math.radians(angle))
                y = 150 + 200 * math.sin(math.radians(angle))
                self.canvas.create_line(475, 150, x, y, 
                                        fill='#ffd70022', width=2)
        
        elif ending_type == "bad":
            self.canvas.create_text(475, 180, text="🌑", font=("Arial", 80))
            self.canvas.create_text(475, 320, text="😞 ПЛОХАЯ КОНЦОВКА", 
                                    font=("Arial", 28, "bold"), fill='#666677')
            self.canvas.create_text(475, 380, text="Тьма поглотила вас...", 
                                    font=("Arial", 16), fill='#444455')
        
        else:  # worst
            self.canvas.create_text(475, 150, text="⛓️", font=("Arial", 80))
            self.canvas.create_text(475, 280, text="☠️ ВЫ ЗАПЕРТЫ НАВЕЧНО", 
                                    font=("Arial", 26, "bold"), fill='#ff3333')
            self.canvas.create_text(475, 350, text="ХУДШАЯ КОНЦОВКА", 
                                    font=("Arial", 22, "bold"), fill='#ff4444')
            # Дрожащий эффект
            for i in range(5):
                x = 200 + i * 150
                self.canvas.create_rectangle(x, 380, x+10, 390, 
                                            fill='#333344', outline='')
    
    # ========== ЛОГИКА ИГРЫ ==========
    def update_inventory(self):
        """Обновляет отображение инвентаря"""
        items = []
        if self.card:
            items.append("🗂️ Карта")
        if self.power:
            items.append("⚡ Питание")
        
        if items:
            self.inventory_items.config(text=", ".join(items), fg='#00ff88')
        else:
            self.inventory_items.config(text="(пусто)", fg='#666677')
    
    def update_story(self, text, color='#ffffff'):
        """Обновляет текст истории"""
        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(1.0, text)
        self.story_text.config(state=tk.DISABLED, fg=color)
    
    def show_scene(self, step):
        self.step = step
        self.update_inventory()
        
        # Анимация ходьбы персонажа
        self.walk_frame += 1
        
        if step == 0:  # Старт
            self.draw_room()
            self.update_story(
                "🏚️ Вы приходите в сознание в заброшенной лаборатории...\n"
                "Голова раскалывается. Последнее, что вы помните - взрыв.\n"
                "Нужно срочно найти выход!",
                '#ffffff'
            )
            self.btn1.config(text="🔍 ОСМОТРЕТЬ КОМНАТУ")
            self.btn2.config(text="🚪 ОТКРЫТЬ ДВЕРЬ")
            self.btn2.pack(side=tk.LEFT, padx=20)
            self.btn1.pack(side=tk.LEFT, padx=20)
            self.restart_btn.pack_forget()
            self.status_bar.config(text="🔍 Исследуйте комнату...")
            self.hint_label.config(text="💡 Подсказка: Осмотрите комнату, возможно, там есть что-то полезное!")
            
        elif step == 1:  # Карта найдена
            self.draw_room()
            self.update_story(
                "✅ Вы нашли КАРТУ ДОСТУПА!\n"
                "Теперь нужно найти способ открыть главную дверь.\n\n"
                "Куда пойдёте?",
                '#00ff88'
            )
            self.btn1.config(text="⚡ В ЭЛЕКТРОЩИТОВУЮ")
            self.btn2.config(text="☢️ В ЛАБОРАТОРИЮ")
            self.status_bar.config(text="🗂️ Карта найдена! Выберите путь...")
            self.hint_label.config(text="💡 Подсказка: Для победы нужны карта и питание!")
            SoundMaker.success()
            
        elif step == 2:  # Дверь заперта
            self.draw_room()
            self.update_story(
                "🔒 Дверь заперта!\n"
                "Похоже, нужна карта доступа.\n"
                "Придётся исследовать лабораторию дальше...",
                '#ff6b6b'
            )
            self.btn1.config(text="🔍 ОСМОТРЕТЬ КОМНАТУ")
            self.btn2.pack_forget()
            self.status_bar.config(text="🔒 Дверь заперта! Ищите карту...")
            self.hint_label.config(text="💡 Подсказка: В комнате точно есть что-то полезное!")
            SoundMaker.fail()
            
        elif step == 3:  # Электрощитовая
            self.draw_electric()
            self.update_story(
                "⚡ Вы в ЭЛЕКТРОЩИТОВОЙ\n\n"
                "Старый пульт управления выглядит рабочим.\n"
                "Что делать?",
                '#88ff88'
            )
            self.btn1.config(text="🔌 ВКЛЮЧИТЬ ПИТАНИЕ")
            self.btn2.config(text="🚶 НЕ ТРОГАТЬ")
            self.btn2.pack(side=tk.LEFT, padx=20)
            self.status_bar.config(text="⚡ Включите питание или уходите...")
            self.hint_label.config(text="💡 Подсказка: Питание может пригодиться для открытия двери!")
            
        elif step == 4:  # Питание включено
            self.draw_electric()
            self.update_story(
                "💡 По всей лаборатории зажглись огни!\n\n"
                "✅ Питание восстановлено!\n"
                "Теперь можно попробовать открыть главную дверь.",
                '#00ff88'
            )
            self.btn1.config(text="🚪 ИДТИ К ВЫХОДУ")
            self.btn2.pack_forget()
            self.status_bar.config(text="💡 Питание включено! Идите к выходу!")
            self.hint_label.config(text="💡 Подсказка: Теперь у вас есть карта и питание - идите к выходу!")
            SoundMaker.success()
            
        elif step == 5:  # Лаборатория
            self.draw_reactor()
            self.update_story(
                "☢️ Вы в комнате с огромным реактором\n\n"
                "За пультом вы заметили странный ЛЮК в полу!\n"
                "Что делать?",
                '#44aaff'
            )
            self.btn1.config(text="🕳️ ИСПОЛЬЗОВАТЬ ПРОХОД")
            self.btn2.config(text="🔙 ВЕРНУТЬСЯ")
            self.btn2.pack(side=tk.LEFT, padx=20)
            self.status_bar.config(text="☢️ Реакторная лаборатория...")
            self.hint_label.config(text="💡 Подсказка: Люк ведёт в секретный тоннель...")
            
        elif step == 6:  # Секретная концовка
            self.draw_ending("secret")
            self.update_story(
                "🏆🏆🏆 СЕКРЕТНАЯ КОНЦОВКА! 🏆🏆🏆\n\n"
                "Вы нырнули в люк и оказались в подземном тоннеле!\n"
                "Через час вы вышли к старой дороге!\n\n"
                "🎉 ВЫ СОВЕРШИЛИ ИДЕАЛЬНЫЙ ПОБЕГ!",
                '#ffd700'
            )
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
            self.status_bar.config(text="🏆 СЕКРЕТНАЯ КОНЦОВКА! ПОЗДРАВЛЯЮ!")
            self.hint_label.config(text="🎉 Вы нашли секретный путь! Блестяще!")
            SoundMaker.win()
            self.attempts += 1
            self.attempts_label.config(text=f"🎮 Попыток: {self.attempts}")
            
        elif step == 7:  # Финальная концовка
            if self.card and self.power:
                self.draw_ending("best")
                self.update_story(
                    "🏆🏆🏆 ЛУЧШАЯ КОНЦОВКА! 🏆🏆🏆\n\n"
                    "✅ Карта доступа принята!\n"
                    "✅ Питание работает!\n"
                    "🔓 Дверь открылась...\n\n"
                    "🎉 Вы выбрались из лаборатории!\n"
                    "🎉 Поздравляем! Вы спаслись!",
                    '#00ff88'
                )
                self.status_bar.config(text="🏆 ЛУЧШАЯ КОНЦОВКА! ВЫ ПОБЕДИЛИ!")
                self.hint_label.config(text="🎉 Идеальное прохождение! Вы - герой!")
                SoundMaker.win()
                
            elif self.card and not self.power:
                self.draw_ending("bad")
                self.update_story(
                    "😞 ПЛОХАЯ КОНЦОВКА\n\n"
                    "✅ Карта доступа есть\n"
                    "❌ Но питания нет!\n"
                    "🚫 Дверь не открывается...\n\n"
                    "💀 Вы застряли в темноте навсегда.",
                    '#ff6b6b'
                )
                self.status_bar.config(text="😞 Плохая концовка... Попробуйте снова!")
                self.hint_label.config(text="💡 Совет: В следующий раз включите питание!")
                SoundMaker.fail()
                
            else:
                self.draw_ending("worst")
                self.update_story(
                    "☠️☠️☠️ ХУДШАЯ КОНЦОВКА ☠️☠️☠️\n\n"
                    "❌ У вас нет карты доступа!\n"
                    "❌ Питания нет!\n"
                    "🚫 Дверь заперта навсегда...\n\n"
                    "💀 Лаборатория стала вашей могилой.",
                    '#ff3333'
                )
                self.status_bar.config(text="☠️ Худшая концовка... Удачи в следующий раз!")
                self.hint_label.config(text="💡 Совет: Исследуйте всё и собирайте предметы!")
                SoundMaker.fail()
            
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
            self.attempts += 1
            self.attempts_label.config(text=f"🎮 Попыток: {self.attempts}")
        
        # Обновление персонажа
        self.root.after(100, self.animate_player)
    
    def animate_player(self):
        """Анимация персонажа"""
        self.walk_frame += 1
        if self.step < 6:
            self.draw_player(self.player_x, self.player_y, self.walk_frame)
            self.root.after(200, self.animate_player)
    
    # ========== ДЕЙСТВИЯ ==========
    def choice1(self):
        SoundMaker.click()
        
        if self.step == 0 or self.step == 2:
            self.card = True
            self.show_scene(1)
        elif self.step == 1:
            self.show_scene(3)
        elif self.step == 3:
            self.power = True
            self.show_scene(4)
        elif self.step == 4:
            self.show_scene(7)
        elif self.step == 5:
            self.show_scene(6)
    
    def choice2(self):
        SoundMaker.click()
        
        if self.step == 0:
            self.show_scene(2)
        elif self.step == 1:
            self.show_scene(5)
        elif self.step == 3:
            self.show_scene(7)
        elif self.step == 5:
            self.show_scene(7)
    
    def restart(self):
        SoundMaker.click()
        self.card = False
        self.power = False
        self.restart_btn.pack_forget()
        self.btn1.pack(side=tk.LEFT, padx=20)
        self.btn2.pack(side=tk.LEFT, padx=20)
        self.show_scene(0)
        self.status_bar.config(text="🔄 Игра перезапущена!")
        self.hint_label.config(text="💡 Подсказка: Исследуйте всё вокруг!")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    root = tk.Tk()
    game = SuperLabGame(root)
    
    # Центрирование окна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()