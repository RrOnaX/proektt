import tkinter as tk
from tkinter import font, messagebox
import random
import time
import math
import threading

# ========== ЗВУКИ (ВСТРОЕННЫЕ) ==========
try:
    import winsound
    SOUND = True
except:
    SOUND = False

def sound_effect(freq, duration):
    if SOUND:
        try:
            winsound.Beep(freq, duration)
        except:
            pass

def play_click():
    sound_effect(800, 30)

def play_success():
    for f in [523, 659, 784]:
        sound_effect(f, 100)
        time.sleep(0.05)

def play_fail():
    sound_effect(300, 400)

def play_win():
    for f in [523, 587, 659, 784, 880, 988, 1047]:
        sound_effect(f, 80)
        time.sleep(0.04)

# ========== ОСНОВНАЯ ИГРА ==========
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("🔬 ПОБЕГ ИЗ ЛАБОРАТОРИИ")
        self.root.geometry("900x700")
        self.root.configure(bg='#0a0e17')
        self.root.resizable(False, False)
        
        # Игровые состояния
        self.has_card = False
        self.has_power = False
        self.current_scene = 0
        self.gold = 0
        self.health = 100
        self.time = 0
        self.ending = None
        
        # ===== ВЕРХНЯЯ ПАНЕЛЬ =====
        self.create_header()
        
        # ===== ОСНОВНОЙ ХОЛСТ =====
        self.canvas = tk.Canvas(
            root,
            width=860,
            height=400,
            bg='#0a0e17',
            highlightthickness=2,
            highlightcolor='#00d4ff',
            relief=tk.FLAT
        )
        self.canvas.pack(pady=10)
        
        # ===== ТЕКСТОВАЯ ОБЛАСТЬ =====
        self.text_frame = tk.Frame(root, bg='#0a0e17')
        self.text_frame.pack(pady=8, fill=tk.X, padx=40)
        
        self.text_display = tk.Text(
            self.text_frame,
            height=3,
            font=("Segoe UI", 12),
            fg='#c8d6e5',
            bg='#16213e',
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=5,
            highlightthickness=1,
            highlightcolor='#00d4ff'
        )
        self.text_display.pack(fill=tk.X)
        self.text_display.config(state=tk.DISABLED)
        
        # ===== СТАТУС БАР =====
        self.status = tk.Label(
            root,
            text="🔍 Добро пожаловать в лабораторию",
            font=("Segoe UI", 10),
            fg='#8395a7',
            bg='#0a0e17'
        )
        self.status.pack(pady=5)
        
        # ===== КНОПКИ =====
        self.btn_frame = tk.Frame(root, bg='#0a0e17')
        self.btn_frame.pack(pady=15)
        
        self.btn1 = self.create_button("▶ ВЫБОР 1", '#00d4ff', self.choice1)
        self.btn1.pack(side=tk.LEFT, padx=15)
        
        self.btn2 = self.create_button("▶ ВЫБОР 2", '#ff6b6b', self.choice2)
        self.btn2.pack(side=tk.LEFT, padx=15)
        
        # ===== КНОПКА ПЕРЕЗАПУСКА =====
        self.restart_btn = self.create_button(
            "⟳ НОВАЯ ИГРА", 
            '#ffd93d', 
            self.restart,
            width=18
        )
        
        # ===== НИЖНИЙ БАР С ПОДСКАЗКАМИ =====
        self.hint = tk.Label(
            root,
            text="💡 Совет: Исследуйте каждую деталь",
            font=("Segoe UI", 9, "italic"),
            fg='#576574',
            bg='#0a0e17'
        )
        self.hint.pack(pady=5)
        
        # Запускаем игру
        self.show_scene(0)
        self.animate_ui()
    
    def create_header(self):
        """Создаёт верхнюю панель"""
        header = tk.Frame(self.root, bg='#0a0e17')
        header.pack(fill=tk.X, pady=8, padx=20)
        
        # Логотип
        tk.Label(
            header,
            text="🔬 ПОБЕГ ИЗ ЛАБОРАТОРИИ",
            font=("Segoe UI", 18, "bold"),
            fg='#00d4ff',
            bg='#0a0e17'
        ).pack(side=tk.LEFT)
        
        # Статистика
        stats = tk.Frame(header, bg='#0a0e17')
        stats.pack(side=tk.RIGHT)
        
        self.health_display = tk.Label(
            stats,
            text="❤️ 100",
            font=("Segoe UI", 11),
            fg='#ff6b6b',
            bg='#0a0e17'
        )
        self.health_display.pack(side=tk.LEFT, padx=10)
        
        self.inventory_display = tk.Label(
            stats,
            text="🎒 Пусто",
            font=("Segoe UI", 11),
            fg='#ffd93d',
            bg='#0a0e17'
        )
        self.inventory_display.pack(side=tk.LEFT, padx=10)
        
        self.time_display = tk.Label(
            stats,
            text="⏱ 0",
            font=("Segoe UI", 11),
            fg='#8395a7',
            bg='#0a0e17'
        )
        self.time_display.pack(side=tk.LEFT, padx=10)
    
    def create_button(self, text, color, command, width=20):
        """Создаёт стильную кнопку"""
        btn = tk.Button(
            self.btn_frame,
            text=text,
            font=("Segoe UI", 11, "bold"),
            width=width,
            height=2,
            bg=color,
            fg='#0a0e17',
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            command=command,
            activebackground='#ffffff',
            activeforeground='#0a0e17'
        )
        
        def on_enter(e):
            btn.config(bg='#ffffff', transform=True)
            play_click()
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn
    
    def update_stats(self):
        """Обновляет панель статистики"""
        # Инвентарь
        items = []
        if self.has_card:
            items.append("Карта")
        if self.has_power:
            items.append("⚡")
        
        if items:
            self.inventory_display.config(text=f"🎒 {', '.join(items)}", fg='#00d4ff')
        else:
            self.inventory_display.config(text="🎒 Пусто", fg='#8395a7')
        
        # Время
        self.time += 1
        self.time_display.config(text=f"⏱ {self.time}")
        
        # Здоровье (постепенное уменьшение в темноте)
        if not self.has_power and self.current_scene < 6:
            if self.time % 5 == 0 and self.health > 0:
                self.health -= 1
                self.health_display.config(text=f"❤️ {self.health}")
                if self.health <= 20:
                    self.health_display.config(fg='#ff0000')
                elif self.health <= 50:
                    self.health_display.config(fg='#ff6b6b')
    
    def set_text(self, text, color='#c8d6e5'):
        """Устанавливает текст"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, text)
        self.text_display.config(state=tk.DISABLED, fg=color)
    
    def set_status(self, text):
        """Устанавливает статус"""
        self.status.config(text=text)
    
    def set_hint(self, text):
        """Устанавливает подсказку"""
        self.hint.config(text=f"💡 {text}")
    
    # ===== ОТРИСОВКА СЦЕН =====
    def draw_room(self):
        """Рисует комнату"""
        self.canvas.delete("all")
        
        # Фон
        self.canvas.create_rectangle(0, 0, 860, 400, fill='#0f1a2e')
        
        # Стены
        self.canvas.create_rectangle(40, 40, 820, 350, fill='#1a2744', outline='#00d4ff33', width=2)
        
        # Свет (тусклый)
        for i in range(30):
            x = 430 + random.randint(-100, 100)
            y = 200 + random.randint(-80, 80)
            alpha = random.randint(10, 30)
            self.canvas.create_oval(x, y, x+5, y+5, fill=f'#ffff44{alpha:02x}', outline='')
        
        # Пол
        for i in range(30):
            x = 40 + i * 27
            self.canvas.create_rectangle(x, 330, x+13, 350, 
                                         fill='#2a3a5a' if i%2==0 else '#22304a',
                                         outline='')
        
        # Дверь
        self.canvas.create_rectangle(720, 180, 800, 330, 
                                     fill='#2a1a0a', outline='#4a3a2a', width=3)
        self.canvas.create_oval(785, 240, 795, 260, fill='#ffd700', outline='#cc9900')
        self.canvas.create_text(760, 255, text="🚪", font=("Segoe UI", 25))
        
        # Стол
        self.canvas.create_rectangle(100, 290, 280, 330, fill='#3a2a1a', outline='#5a4a3a')
        self.canvas.create_rectangle(110, 270, 130, 290, fill='#3a2a1a')
        self.canvas.create_rectangle(250, 270, 270, 290, fill='#3a2a1a')
        
        # Предметы на столе
        self.canvas.create_oval(160, 298, 185, 323, fill='#00d4ff44', outline='#00d4ff88', width=2)
        self.canvas.create_text(172, 310, text="📡", font=("Segoe UI", 20))
        
        # Карта (если есть)
        if self.has_card:
            self.canvas.create_rectangle(190, 275, 240, 310, 
                                         fill='#ffd700', outline='#cc9900', width=2)
            self.canvas.create_text(215, 292, text="🗺️", font=("Segoe UI", 22))
        
        # Персонаж (стилизованный)
        self.draw_character(450, 340)
        
        # Название
        self.canvas.create_text(430, 65, text="🏚️ ЗАБРОШЕННАЯ ЛАБОРАТОРИЯ", 
                                font=("Segoe UI", 16, "bold"), fill='#8395a7')
        
        # Эффект тумана
        self.canvas.create_rectangle(0, 340, 860, 400, fill='#0f1a2e', stipple='gray25')
    
    def draw_electric(self):
        """Рисует электрощитовую"""
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(0, 0, 860, 400, fill='#0a1a0a')
        self.canvas.create_rectangle(40, 40, 820, 350, fill='#0f2a0f', outline='#00ff8844', width=2)
        
        # Щитки
        for i in range(3):
            x = 60 + i * 250
            # Корпус
            self.canvas.create_rectangle(x, 100, x+220, 300, 
                                         fill='#1a2a3a', outline='#00d4ff33', width=2)
            # Панель
            self.canvas.create_rectangle(x+10, 110, x+210, 290, 
                                         fill='#0a1a2a', outline='#00d4ff22')
            
            # Лампочки
            for j in range(4):
                y = 130 + j * 40
                status = (i == 0 and self.has_power) or (i == 1 and self.has_power)
                color = '#00ff88' if (i == 0 and self.has_power) or (i == 1 and self.has_power) else '#ff4444'
                if i == 2:
                    color = '#ffaa00'
                
                self.canvas.create_oval(x+30+j*45, y, x+50+j*45, y+20, 
                                       fill=color, outline='#ffffff33')
                if color == '#00ff88':
                    # Эффект свечения
                    self.canvas.create_oval(x+30+j*45-10, y-10, x+50+j*45+10, y+30, 
                                           fill=f'{color}22', outline='')
            
            # Надпись
            names = ['🔋 ПИТАНИЕ', '⚡ РЕЗЕРВ', '🔌 РАСПРЕДЕЛ']
            self.canvas.create_text(x+110, 115, text=names[i], 
                                   font=("Segoe UI", 9, "bold"), fill='#8395a7')
        
        # Персонаж
        self.draw_character(430, 340)
        
        # Название
        self.canvas.create_text(430, 65, text="⚡ ЭЛЕКТРОЩИТОВАЯ", 
                                font=("Segoe UI", 16, "bold"), fill='#00ff88')
    
    def draw_reactor(self):
        """Рисует реакторную"""
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(0, 0, 860, 400, fill='#0a0a1a')
        self.canvas.create_rectangle(40, 40, 820, 350, fill='#0a1a2a', outline='#00d4ff44', width=2)
        
        # Реактор
        self.canvas.create_oval(320, 120, 540, 300, fill='#1a3a5a', outline='#00d4ff', width=3)
        self.canvas.create_oval(350, 150, 510, 270, fill='#0a2a4a', outline='#00d4ff88', width=2)
        self.canvas.create_oval(380, 180, 480, 240, fill='#0a1a3a', outline='#00d4ff44', width=1)
        
        # Анимация реактора
        pulse = int(100 + 50 * math.sin(time.time() * 2))
        self.canvas.create_oval(320, 120, 540, 300, 
                               fill=f'#00d4ff{pulse:02x}', outline='', stipple='gray25')
        
        # Радиация
        for i in range(8):
            angle = i * 45 + int(time.time() * 20) % 360
            x = 430 + 120 * math.cos(math.radians(angle))
            y = 210 + 120 * math.sin(math.radians(angle))
            self.canvas.create_line(430, 210, x, y, 
                                   fill='#00ff8844', width=1)
        
        # Люк
        self.canvas.create_rectangle(680, 230, 760, 330, 
                                     fill='#1a1a2a', outline='#00d4ff88', width=2)
        self.canvas.create_text(720, 280, text="🕳️", font=("Segoe UI", 35))
        
        # Персонаж
        self.draw_character(430, 340)
        
        # Название
        self.canvas.create_text(430, 65, text="☢️ РЕАКТОРНАЯ", 
                                font=("Segoe UI", 16, "bold"), fill='#00d4ff')
    
    def draw_ending(self, ending_type):
        """Рисует финальную сцену"""
        self.canvas.delete("all")
        
        # Фон
        colors = {
            'secret': ('#0a0a1a', '#ffd700'),
            'best': ('#0a2a0a', '#00ff88'),
            'bad': ('#0a0a0a', '#666677'),
            'worst': ('#1a0a0a', '#ff3333')
        }
        
        bg, color = colors.get(ending_type, ('#0a0a1a', '#ffffff'))
        self.canvas.create_rectangle(0, 0, 860, 400, fill=bg)
        
        # Иконка
        icons = {
            'secret': '🕳️',
            'best': '🌅',
            'bad': '🌑',
            'worst': '⛓️'
        }
        
        self.canvas.create_text(430, 140, text=icons.get(ending_type, '❓'), 
                               font=("Segoe UI", 80))
        
        # Текст
        titles = {
            'secret': 'СЕКРЕТНАЯ КОНЦОВКА',
            'best': 'ЛУЧШАЯ КОНЦОВКА',
            'bad': 'ПЛОХАЯ КОНЦОВКА',
            'worst': 'ХУДШАЯ КОНЦОВКА'
        }
        
        self.canvas.create_text(430, 250, text=titles.get(ending_type, 'КОНЕЦ'), 
                               font=("Segoe UI", 28, "bold"), fill=color)
        
        # Подзаголовок
        subtitles = {
            'secret': '🏆 Вы сбежали через тайный ход!',
            'best': '🎉 ВЫ НА СВОБОДЕ!',
            'bad': '😞 Вы застряли в темноте...',
            'worst': '☠️ Вы заперты навечно...'
        }
        
        self.canvas.create_text(430, 310, text=subtitles.get(ending_type, ''), 
                               font=("Segoe UI", 16), fill='#8395a7')
        
        # Звёзды для секретной концовки
        if ending_type == 'secret':
            for i in range(30):
                x = random.randint(20, 840)
                y = random.randint(20, 380)
                self.canvas.create_oval(x, y, x+3, y+3, fill='#ffd700')
    
    def draw_character(self, x, y):
        """Рисует персонажа"""
        # Тень
        self.canvas.create_oval(x-25, y, x+25, y+15, fill='#00000044', outline='')
        
        # Тело
        self.canvas.create_oval(x-20, y-25, x+20, y+5, fill='#00d4ff', outline='#0088aa', width=2)
        
        # Глаза
        self.canvas.create_oval(x-10, y-15, x-5, y-8, fill='white', outline='#0a0e17')
        self.canvas.create_oval(x+5, y-15, x+10, y-8, fill='white', outline='#0a0e17')
        
        # Зрачки
        self.canvas.create_oval(x-8, y-13, x-6, y-10, fill='#0a0e17')
        self.canvas.create_oval(x+6, y-13, x+8, y-10, fill='#0a0e17')
        
        # Улыбка
        self.canvas.create_arc(x-8, y-5, x+8, y+5, 
                              start=0, extent=-180, style=tk.ARC, 
                              width=2, outline='#0a0e17')
        
        # Очки
        self.canvas.create_oval(x-15, y-18, x-3, y-6, outline='#0088aa', width=1)
        self.canvas.create_oval(x+3, y-18, x+15, y-6, outline='#0088aa', width=1)
        self.canvas.create_line(x-3, y-12, x+3, y-12, fill='#0088aa')
        
        # Имя
        self.canvas.create_text(x, y-40, text="👨‍🔬 Учёный", 
                               font=("Segoe UI", 9, "bold"), fill='#00d4ff')
    
    # ===== ЛОГИКА СЦЕН =====
    def show_scene(self, scene):
        self.current_scene = scene
        self.update_stats()
        
        if scene == 0:  # Старт
            self.draw_room()
            self.set_text(
                "🏚️ Вы приходите в сознание в заброшенной лаборатории.\n"
                "Последнее, что вы помните - взрыв. Вокруг темно и холодно.\n"
                "Вам нужно найти выход из этого места!",
                '#c8d6e5'
            )
            self.set_status("🔍 Исследуйте комнату...")
            self.set_hint("Осмотрите комнату, возможно, найдёте что-то полезное")
            self.btn1.config(text="🔍 ОСМОТРЕТЬСЯ")
            self.btn2.config(text="🚪 ПОЙТИ К ДВЕРИ")
            self.btn2.pack(side=tk.LEFT, padx=15)
            self.btn1.pack(side=tk.LEFT, padx=15)
            self.restart_btn.pack_forget()
            play_click()
            
        elif scene == 1:  # Карта найдена
            self.draw_room()
            self.set_text(
                "✅ Отлично! Вы нашли старую КАРТУ ДОСТУПА под столом.\n"
                "Теперь вам нужно восстановить питание, чтобы открыть главную дверь.\n\n"
                "Куда направитесь?",
                '#00d4ff'
            )
            self.set_status("🗺️ Карта найдена! Выберите путь")
            self.set_hint("Для победы нужны карта и питание")
            self.btn1.config(text="⚡ В ЩИТОВУЮ")
            self.btn2.config(text="☢️ В РЕАКТОРНУЮ")
            play_success()
            
        elif scene == 2:  # Дверь заперта
            self.draw_room()
            self.set_text(
                "🔒 Дверь заперта! Требуется электронная карта доступа.\n"
                "Похоже, вам нужно найти карту в этой комнате.",
                '#ff6b6b'
            )
            self.set_status("🔒 Нужна карта доступа")
            self.set_hint("Обыщите комнату внимательнее")
            self.btn1.config(text="🔍 ОСМОТРЕТЬСЯ")
            self.btn2.pack_forget()
            play_fail()
            
        elif scene == 3:  # Электрощитовая
            self.draw_electric()
            self.set_text(
                "⚡ Вы в электрощитовой. Здесь пахнет озоном и старой проводкой.\n"
                "Пульт управления выглядит рабочим, но есть риск короткого замыкания.",
                '#00ff88'
            )
            self.set_status("⚡ Включить питание?")
            self.set_hint("Включение питания может открыть главную дверь")
            self.btn1.config(text="🔌 ВКЛЮЧИТЬ")
            self.btn2.config(text="🚶 УЙТИ")
            self.btn2.pack(side=tk.LEFT, padx=15)
            
        elif scene == 4:  # Питание включено
            self.draw_electric()
            self.set_text(
                "💡 По всей лаборатории зажглись огни! Питание восстановлено.\n"
                "Главная дверь теперь должна открыться.\n"
                "Скорее к выходу!",
                '#00ff88'
            )
            self.set_status("💡 Питание восстановлено!")
            self.set_hint("Идите к главной двери, пока не поздно")
            self.btn1.config(text="🚪 К ВЫХОДУ")
            self.btn2.pack_forget()
            play_success()
            
        elif scene == 5:  # Реакторная
            self.draw_reactor()
            self.set_text(
                "☢️ Вы в реакторной. Гудит оборудование.\n"
                "В углу вы замечаете странный ЛЮК в полу!\n"
                "Похоже, это секретный путь...",
                '#00d4ff'
            )
            self.set_status("☢️ Что делать?")
            self.set_hint("Люк может вести наружу или в ловушку")
            self.btn1.config(text="🕳️ В ЛЮК")
            self.btn2.config(text="🔙 ВЕРНУТЬСЯ")
            self.btn2.pack(side=tk.LEFT, padx=15)
            
        elif scene == 6:  # Секретная концовка
            self.draw_ending('secret')
            self.set_text(
                "🏆🏆🏆 СЕКРЕТНАЯ КОНЦОВКА! 🏆🏆🏆\n\n"
                "Вы нырнули в люк и оказались в секретном тоннеле!\n"
                "Через 15 минут вы вышли к старой дороге.\n"
                "Вас подобрала проезжающая машина.\n\n"
                "🎉 ИДЕАЛЬНЫЙ ПОБЕГ!",
                '#ffd700'
            )
            self.set_status("🏆 ПОБЕДА!")
            self.set_hint("Вы нашли лучший путь!")
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
            play_win()
            
        elif scene == 7:  # Финал
            if self.has_card and self.has_power:
                self.draw_ending('best')
                self.set_text(
                    "🏆🏆🏆 ЛУЧШАЯ КОНЦОВКА! 🏆🏆🏆\n\n"
                    "✅ Карта доступа принята!\n"
                    "✅ Питание работает!\n"
                    "🔓 Дверь открылась...\n\n"
                    "🎉 ВЫ СВОБОДНЫ! Поздравляем с побегом!",
                    '#00ff88'
                )
                self.set_status("🏆 ПОБЕДА!")
                self.set_hint("Идеальное прохождение!")
                play_win()
                
            elif self.has_card and not self.has_power:
                self.draw_ending('bad')
                self.set_text(
                    "😞 ПЛОХАЯ КОНЦОВКА\n\n"
                    "✅ Карта есть, но питания нет!\n"
                    "🚫 Дверь не открывается.\n"
                    "💀 Вы застряли в темноте...",
                    '#ff6b6b'
                )
                self.set_status("😞 Поражение")
                self.set_hint("В следующий раз включите питание!")
                play_fail()
                
            else:
                self.draw_ending('worst')
                self.set_text(
                    "☠️☠️☠️ ХУДШАЯ КОНЦОВКА ☠️☠️☠️\n\n"
                    "❌ Нет карты доступа!\n"
                    "❌ Нет питания!\n"
                    "🚫 Дверь заперта навсегда...\n"
                    "💀 Лаборатория стала вашей могилой.",
                    '#ff3333'
                )
                self.set_status("☠️ ПОРАЖЕНИЕ")
                self.set_hint("Нужно было искать карту и питание!")
                play_fail()
            
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
    
    # ===== ДЕЙСТВИЯ КНОПОК =====
    def choice1(self):
        play_click()
        
        if self.current_scene == 0 or self.current_scene == 2:
            self.has_card = True
            self.show_scene(1)
        elif self.current_scene == 1:
            self.show_scene(3)
        elif self.current_scene == 3:
            self.has_power = True
            self.show_scene(4)
        elif self.current_scene == 4:
            self.show_scene(7)
        elif self.current_scene == 5:
            self.show_scene(6)
    
    def choice2(self):
        play_click()
        
        if self.current_scene == 0:
            self.show_scene(2)
        elif self.current_scene == 1:
            self.show_scene(5)
        elif self.current_scene == 3:
            self.show_scene(7)
        elif self.current_scene == 5:
            self.show_scene(7)
    
    def restart(self):
        play_click()
        self.has_card = False
        self.has_power = False
        self.health = 100
        self.time = 0
        self.restart_btn.pack_forget()
        self.btn1.pack(side=tk.LEFT, padx=15)
        self.btn2.pack(side=tk.LEFT, padx=15)
        self.show_scene(0)
        self.set_status("🔄 Новая игра начата!")
        self.set_hint("Исследуйте лабораторию и найдите выход")
        self.health_display.config(text="❤️ 100", fg='#ff6b6b')
    
    def animate_ui(self):
        """Анимация интерфейса"""
        # Обновление времени
        if self.current_scene < 6:
            self.update_stats()
        
        # Перерисовка сцены с анимацией
        if self.current_scene == 5:  # Реактор с анимацией
            self.draw_reactor()
        
        # Запуск следующего кадра
        self.root.after(200, self.animate_ui)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()