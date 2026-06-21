import tkinter as tk
from tkinter import messagebox
import random
import time

# ========== ЗВУКИ (встроенные) ==========
try:
    import winsound
    SOUND = True
except:
    SOUND = False

def sound_beep(freq, duration):
    if SOUND:
        try:
            winsound.Beep(freq, duration)
        except:
            pass

def sound_click():
    sound_beep(800, 30)

def sound_good():
    sound_beep(500, 100)
    time.sleep(0.05)
    sound_beep(700, 100)

def sound_bad():
    sound_beep(300, 300)

def sound_win():
    for f in [500, 600, 700, 800, 900]:
        sound_beep(f, 80)
        time.sleep(0.03)

# ========== ИГРА ==========
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("🔬 ПОБЕГ ИЗ ЛАБОРАТОРИИ")
        self.root.geometry("750x650")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # Переменные игры
        self.card = False
        self.power = False
        self.step = 0
        
        # Верхняя панель
        self.create_top_bar()
        
        # Холст для рисования
        self.canvas = tk.Canvas(
            root,
            width=700,
            height=350,
            bg='#16213e',
            highlightthickness=2,
            highlightcolor='#e94560'
        )
        self.canvas.pack(pady=10)
        
        # Текст
        self.text_label = tk.Label(
            root,
            text="",
            font=("Arial", 13),
            fg='#eeeeee',
            bg='#1a1a2e',
            wraplength=650,
            justify=tk.CENTER
        )
        self.text_label.pack(pady=10)
        
        # Кнопки
        self.btn_frame = tk.Frame(root, bg='#1a1a2e')
        self.btn_frame.pack(pady=15)
        
        self.btn1 = tk.Button(
            self.btn_frame,
            text="",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            bg='#e94560',
            fg='white',
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            command=self.choice1
        )
        self.btn1.pack(side=tk.LEFT, padx=10)
        
        self.btn2 = tk.Button(
            self.btn_frame,
            text="",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            bg='#533483',
            fg='white',
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            command=self.choice2
        )
        self.btn2.pack(side=tk.LEFT, padx=10)
        
        # Кнопка рестарта
        self.restart_btn = tk.Button(
            root,
            text="🔄 НАЧАТЬ ЗАНОВО",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            bg='#0f3460',
            fg='white',
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            command=self.restart
        )
        
        # Статус бар
        self.status = tk.Label(
            root,
            text="🔍 Добро пожаловать в лабораторию",
            font=("Arial", 10),
            fg='#888899',
            bg='#1a1a2e'
        )
        self.status.pack(pady=5)
        
        # Запуск
        self.show_scene(0)
    
    def create_top_bar(self):
        """Верхняя панель с инвентарём"""
        bar = tk.Frame(self.root, bg='#1a1a2e')
        bar.pack(fill=tk.X, pady=10, padx=20)
        
        # Название
        tk.Label(
            bar,
            text="🔬 ПОБЕГ ИЗ ЛАБОРАТОРИИ",
            font=("Arial", 16, "bold"),
            fg='#e94560',
            bg='#1a1a2e'
        ).pack(side=tk.LEFT)
        
        # Инвентарь
        self.inv_label = tk.Label(
            bar,
            text="🎒 Инвентарь: пусто",
            font=("Arial", 11),
            fg='#ffd93d',
            bg='#1a1a2e'
        )
        self.inv_label.pack(side=tk.RIGHT)
    
    def update_inventory(self):
        items = []
        if self.card:
            items.append("🗺️ Карта")
        if self.power:
            items.append("⚡ Питание")
        
        if items:
            self.inv_label.config(text=f"🎒 {', '.join(items)}")
        else:
            self.inv_label.config(text="🎒 Инвентарь: пусто")
    
    def draw_room(self):
        """Рисует комнату"""
        self.canvas.delete("all")
        
        # Стены
        self.canvas.create_rectangle(20, 20, 680, 330, fill='#2a2a4a', outline='#444466', width=2)
        
        # Пол
        for i in range(20):
            x = 20 + i * 33
            self.canvas.create_rectangle(x, 280, x+16, 330, 
                                         fill='#3a3a5a' if i%2==0 else '#2a2a4a',
                                         outline='')
        
        # Дверь справа
        self.canvas.create_rectangle(580, 160, 660, 280, 
                                     fill='#5d3a1a', outline='#3d2a0a', width=3)
        self.canvas.create_oval(640, 210, 650, 230, fill='#ffd700', outline='#cc9900')
        self.canvas.create_text(620, 220, text="🚪", font=("Arial", 20))
        
        # Стол
        self.canvas.create_rectangle(80, 250, 220, 280, 
                                     fill='#5d3a1a', outline='#3d2a0a')
        
        # Предметы на столе
        self.canvas.create_oval(120, 255, 140, 275, fill='#00d4ff', outline='#00aaff')
        self.canvas.create_rectangle(160, 260, 190, 275, fill='#888899', outline='#666677')
        
        # Карта (если есть)
        if self.card:
            self.canvas.create_rectangle(110, 235, 190, 260, 
                                         fill='#ffd700', outline='#cc9900', width=2)
            self.canvas.create_text(150, 248, text="🗺️", font=("Arial", 18))
        
        # Персонаж (круг с лицом)
        self.draw_character(400, 290)
        
        # Название
        self.canvas.create_text(350, 45, text="🏚️ ЛАБОРАТОРИЯ", 
                                font=("Arial", 14, "bold"), fill='#888899')
    
    def draw_electric(self):
        """Рисует щитовую"""
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(20, 20, 680, 330, fill='#1a2a1a', outline='#33aa33', width=2)
        
        # Щитки
        for i in range(3):
            x = 60 + i * 190
            self.canvas.create_rectangle(x, 100, x+160, 260, 
                                         fill='#2a2a4a', outline='#6666aa', width=2)
            
            # Индикаторы
            colors = ['#ff4444', '#44ff44' if self.power else '#ffaa00', '#ffaa00']
            for j in range(3):
                y = 130 + j * 35
                color = colors[j] if j < len(colors) else '#ffaa00'
                self.canvas.create_oval(x+20+j*40, y, x+40+j*40, y+20, 
                                       fill=color, outline='#ffffff')
            
            self.canvas.create_text(x+80, 115, text=f"ЩИТ {i+1}", 
                                   font=("Arial", 10, "bold"), fill='#88ccff')
        
        # Персонаж
        self.draw_character(400, 290)
        
        self.canvas.create_text(350, 45, text="⚡ ЭЛЕКТРОЩИТОВАЯ", 
                                font=("Arial", 14, "bold"), fill='#88ff88')
    
    def draw_reactor(self):
        """Рисует реактор"""
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(20, 20, 680, 330, fill='#1a1a2a', outline='#44aaff', width=2)
        
        # Реактор
        self.canvas.create_oval(280, 120, 420, 260, 
                                fill='#3355aa', outline='#44aaff', width=3)
        self.canvas.create_text(350, 190, text="☢️", font=("Arial", 50))
        
        # Люк
        self.canvas.create_rectangle(540, 200, 600, 270, 
                                     fill='#2a2a3a', outline='#6666aa', width=2)
        self.canvas.create_text(570, 235, text="🕳️", font=("Arial", 25))
        
        # Персонаж
        self.draw_character(400, 290)
        
        self.canvas.create_text(350, 45, text="☢️ РЕАКТОРНАЯ", 
                                font=("Arial", 14, "bold"), fill='#44aaff')
    
    def draw_ending(self, ending_type):
        """Рисует финал"""
        self.canvas.delete("all")
        
        bg_colors = {
            'secret': '#0a0a1a',
            'best': '#0a2a0a',
            'bad': '#1a0a0a',
            'worst': '#0a0a0a'
        }
        
        self.canvas.create_rectangle(0, 0, 700, 350, fill=bg_colors.get(ending_type, '#0a0a1a'))
        
        icons = {
            'secret': '🕳️',
            'best': '🌅',
            'worst': '⛓️'
        }
        
        icon = icons.get(ending_type, '💀')
        self.canvas.create_text(350, 150, text=icon, font=("Arial", 80))
        
        titles = {
            'secret': 'СЕКРЕТНАЯ КОНЦОВКА',
            'best': 'ЛУЧШАЯ КОНЦОВКА',
            'bad': 'ПЛОХАЯ КОНЦОВКА',
            'worst': 'ХУДШАЯ КОНЦОВКА'
        }
        
        color = '#ffd700' if ending_type in ['secret', 'best'] else '#ff6b6b'
        self.canvas.create_text(350, 260, text=titles.get(ending_type, 'КОНЕЦ'), 
                                font=("Arial", 20, "bold"), fill=color)
    
    def draw_character(self, x, y):
        """Рисует персонажа"""
        # Тень
        self.canvas.create_oval(x-20, y, x+20, y+10, fill='#00000044', outline='')
        
        # Тело
        self.canvas.create_oval(x-18, y-20, x+18, y+5, fill='#00d4ff', outline='#0088aa', width=2)
        
        # Глаза
        self.canvas.create_oval(x-10, y-12, x-5, y-6, fill='white', outline='black')
        self.canvas.create_oval(x+5, y-12, x+10, y-6, fill='white', outline='black')
        
        # Зрачки
        self.canvas.create_oval(x-8, y-10, x-6, y-8, fill='black')
        self.canvas.create_oval(x+6, y-10, x+8, y-8, fill='black')
        
        # Улыбка
        self.canvas.create_arc(x-8, y-4, x+8, y+6, 
                              start=0, extent=-180, 
                              style=tk.ARC, width=2, outline='black')
        
        # Имя
        self.canvas.create_text(x, y-35, text="👨‍🔬", font=("Arial", 16))
        self.canvas.create_text(x, y-48, text="Учёный", 
                               font=("Arial", 8, "bold"), fill='#88ccff')
    
    def show_scene(self, step):
        self.step = step
        self.update_inventory()
        
        if step == 0:  # Старт
            self.draw_room()
            self.text_label.config(
                text="🏚️ Вы очнулись в заброшенной лаборатории.\n"
                     "Вокруг темно. Нужно найти выход!",
                fg='#eeeeee'
            )
            self.btn1.config(text="🔍 ОСМОТРЕТЬ КОМНАТУ")
            self.btn2.config(text="🚪 ПОЙТИ К ДВЕРИ")
            self.btn2.pack(side=tk.LEFT, padx=10)
            self.btn1.pack(side=tk.LEFT, padx=10)
            self.restart_btn.pack_forget()
            self.status.config(text="🔍 Исследуйте комнату...")
            sound_click()
            
        elif step == 1:  # Карта найдена
            self.draw_room()
            self.text_label.config(
                text="✅ Вы нашли КАРТУ ДОСТУПА!\n\n"
                     "Теперь нужно восстановить питание.\n"
                     "Куда пойдёте?",
                fg='#00ff88'
            )
            self.btn1.config(text="⚡ В ЩИТОВУЮ")
            self.btn2.config(text="☢️ В РЕАКТОРНУЮ")
            self.status.config(text="🗺️ Карта найдена!")
            sound_good()
            
        elif step == 2:  # Дверь заперта
            self.draw_room()
            self.text_label.config(
                text="🔒 Дверь заперта!\n"
                     "Нужна карта доступа!",
                fg='#ff6b6b'
            )
            self.btn1.config(text="🔍 ОСМОТРЕТЬ КОМНАТУ")
            self.btn2.pack_forget()
            self.status.config(text="🔒 Ищите карту...")
            sound_bad()
            
        elif step == 3:  # Щитовая
            self.draw_electric()
            self.text_label.config(
                text="⚡ Вы в электрощитовой.\n"
                     "Включить питание?",
                fg='#88ff88'
            )
            self.btn1.config(text="🔌 ВКЛЮЧИТЬ")
            self.btn2.config(text="🚶 НЕ ТРОГАТЬ")
            self.btn2.pack(side=tk.LEFT, padx=10)
            self.status.config(text="⚡ Ваш выбор?")
            
        elif step == 4:  # Питание включено
            self.draw_electric()
            self.text_label.config(
                text="💡 Питание восстановлено!\n\n"
                     "Теперь можно открыть дверь!",
                fg='#00ff88'
            )
            self.btn1.config(text="🚪 ИДТИ К ДВЕРИ")
            self.btn2.pack_forget()
            self.status.config(text="💡 Питание есть!")
            sound_good()
            
        elif step == 5:  # Реакторная
            self.draw_reactor()
            self.text_label.config(
                text="☢️ Вы в реакторной.\n\n"
                     "Видите ЛЮК в полу!\n"
                     "Что делать?",
                fg='#44aaff'
            )
            self.btn1.config(text="🕳️ ЗАЛЕЗТЬ В ЛЮК")
            self.btn2.config(text="🔙 ВЕРНУТЬСЯ")
            self.btn2.pack(side=tk.LEFT, padx=10)
            self.status.config(text="☢️ Что выберете?")
            
        elif step == 6:  # Секретная концовка
            self.draw_ending('secret')
            self.text_label.config(
                text="🏆🏆🏆 СЕКРЕТНАЯ КОНЦОВКА! 🏆🏆🏆\n\n"
                     "Вы сбежали через тайный ход!\n"
                     "🎉 ПОЗДРАВЛЯЮ!",
                fg='#ffd700'
            )
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
            self.status.config(text="🏆 ПОБЕДА!")
            sound_win()
            
        elif step == 7:  # Финал
            if self.card and self.power:
                self.draw_ending('best')
                self.text_label.config(
                    text="🏆🏆🏆 ЛУЧШАЯ КОНЦОВКА! 🏆🏆🏆\n\n"
                         "✅ Карта и питание есть!\n"
                         "🔓 Дверь открылась!\n"
                         "🎉 ВЫ СВОБОДНЫ!",
                    fg='#00ff88'
                )
                sound_win()
                
            elif self.card and not self.power:
                self.draw_ending('bad')
                self.text_label.config(
                    text="😞 ПЛОХАЯ КОНЦОВКА\n\n"
                         "Карта есть, но нет питания.\n"
                         "Дверь не открывается...",
                    fg='#ff6b6b'
                )
                sound_bad()
                
            else:
                self.draw_ending('worst')
                self.text_label.config(
                    text="☠️ ХУДШАЯ КОНЦОВКА\n\n"
                         "Нет карты и питания.\n"
                         "Вы заперты навсегда...",
                    fg='#ff3333'
                )
                sound_bad()
            
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
            self.status.config(text="Игра окончена")
    
    def choice1(self):
        sound_click()
        
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
        sound_click()
        
        if self.step == 0:
            self.show_scene(2)
        elif self.step == 1:
            self.show_scene(5)
        elif self.step == 3:
            self.show_scene(7)
        elif self.step == 5:
            self.show_scene(7)
    
    def restart(self):
        sound_click()
        self.card = False
        self.power = False
        self.restart_btn.pack_forget()
        self.btn1.pack(side=tk.LEFT, padx=10)
        self.btn2.pack(side=tk.LEFT, padx=10)
        self.show_scene(0)
        self.status.config(text="🔄 Игра перезапущена!")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()