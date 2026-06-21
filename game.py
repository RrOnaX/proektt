import tkinter as tk
from tkinter import font
import random

class LabGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧪 ПОБЕГ ИЗ ЗАБРОШЕННОЙ ЛАБОРАТОРИИ")
        self.root.geometry("900x700")
        self.root.configure(bg='#0a0a1a')
        
        self.card = False
        self.power = False
        self.step = 0
        
        # Создание холста для рисования
        self.canvas = tk.Canvas(
            root,
            width=900,
            height=500,
            bg='#0a0a1a',
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Фрейм для текста
        self.text_frame = tk.Frame(root, bg='#0a0a1a')
        self.text_frame.pack(pady=10, fill=tk.X, padx=50)
        
        self.story_label = tk.Label(
            self.text_frame,
            text="",
            font=("Comic Sans MS", 14),
            fg='#ffffff',
            bg='#0a0a1a',
            wraplength=800,
            justify=tk.CENTER
        )
        self.story_label.pack()
        
        # Фрейм для кнопок
        self.button_frame = tk.Frame(root, bg='#0a0a1a')
        self.button_frame.pack(pady=20)
        
        # Стильные кнопки
        self.btn1 = tk.Button(
            self.button_frame,
            text="",
            font=("Comic Sans MS", 13, "bold"),
            width=25,
            height=2,
            bg='#00ff88',
            fg='#000000',
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            command=self.choice1
        )
        self.btn1.pack(side=tk.LEFT, padx=15)
        
        self.btn2 = tk.Button(
            self.button_frame,
            text="",
            font=("Comic Sans MS", 13, "bold"),
            width=25,
            height=2,
            bg='#ff6b6b',
            fg='#000000',
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            command=self.choice2
        )
        self.btn2.pack(side=tk.LEFT, padx=15)
        
        # Кнопка перезапуска
        self.restart_btn = tk.Button(
            root,
            text="🔄 НАЧАТЬ ЗАНОВО",
            font=("Comic Sans MS", 14, "bold"),
            bg='#ffd93d',
            fg='#000000',
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            command=self.restart,
            width=20,
            height=2
        )
        
        # Запуск игры
        self.show_scene(0)
    
    def draw_room(self):
        """Рисует комнату"""
        self.canvas.delete("all")
        
        # Стены
        self.canvas.create_rectangle(50, 50, 850, 450, fill='#2d2d44', outline='#444466', width=3)
        
        # Пол
        self.canvas.create_rectangle(50, 350, 850, 450, fill='#3d3d55', outline='')
        
        # Светильник
        self.canvas.create_oval(400, 80, 500, 130, fill='#ffdd44', outline='#ffaa00', width=2)
        self.canvas.create_line(450, 130, 450, 200, fill='#888899', width=3)
        
        # Дверь
        self.canvas.create_rectangle(700, 200, 780, 350, fill='#8B4513', outline='#654321', width=3)
        self.canvas.create_oval(760, 260, 770, 280, fill='#ffd700', outline='#cc9900', width=2)
        self.canvas.create_text(740, 275, text="🚪", font=("Arial", 30))
        
        # Стол
        self.canvas.create_rectangle(150, 300, 350, 350, fill='#5d3a1a', outline='#3d2a0a', width=2)
        self.canvas.create_rectangle(160, 260, 170, 300, fill='#5d3a1a')
        self.canvas.create_rectangle(330, 260, 340, 300, fill='#5d3a1a')
        
        # Предметы на столе
        self.canvas.create_oval(200, 280, 230, 310, fill='#66ccff', outline='#3399cc', width=2)
        self.canvas.create_rectangle(260, 290, 300, 310, fill='#888899', outline='#666677', width=2)
        
        # Тень
        self.canvas.create_text(450, 400, text="🏚️ ЗАБРОШЕННАЯ ЛАБОРАТОРИЯ", 
                                font=("Arial", 16, "bold"), fill='#888899')
    
    def draw_corridor(self):
        """Рисует коридор"""
        self.canvas.delete("all")
        
        # Стены
        self.canvas.create_rectangle(0, 0, 900, 500, fill='#1a1a2e')
        
        # Перспектива коридора
        points = [450, 450, 100, 100, 800, 100]
        self.canvas.create_polygon(points, fill='#2a2a44', outline='#444466', width=2)
        
        # Свет
        self.canvas.create_oval(350, 80, 550, 200, fill='#ffdd44', outline='#ffaa00', width=2)
        self.canvas.create_text(450, 150, text="💡", font=("Arial", 40))
        
        # Дверь в конце
        self.canvas.create_rectangle(380, 180, 520, 300, fill='#8B4513', outline='#654321', width=3)
        self.canvas.create_oval(500, 240, 510, 260, fill='#ffd700')
        
        self.canvas.create_text(450, 350, text="🚪 ВЫХОД", font=("Arial", 18, "bold"), fill='#ffd700')
    
    def draw_electric(self):
        """Рисует электрощитовую"""
        self.canvas.delete("all")
        
        # Стены
        self.canvas.create_rectangle(50, 50, 850, 450, fill='#1a2a1a', outline='#33aa33', width=2)
        
        # Электрические щитки
        for i in range(3):
            x = 150 + i * 200
            self.canvas.create_rectangle(x, 150, x+150, 300, fill='#333355', outline='#6666aa', width=2)
            self.canvas.create_text(x+75, 170, text=f"ЩИТ {i+1}", font=("Arial", 12), fill='#88ccff')
            
            # Лампочки
            colors = ['#ff4444', '#44ff44', '#ffaa00']
            for j in range(3):
                self.canvas.create_oval(x+30+j*35, 200, x+50+j*35, 220, fill=colors[j], outline='#ffffff')
        
        # Рычаг
        self.canvas.create_rectangle(700, 200, 750, 350, fill='#666677', outline='#888899', width=2)
        self.canvas.create_rectangle(720, 180, 730, 200, fill='#ff4444', outline='#cc3333', width=2)
        self.canvas.create_text(725, 280, text="⚡", font=("Arial", 30))
        
        self.canvas.create_text(450, 400, text="⚡ ЭЛЕКТРОЩИТОВАЯ", 
                                font=("Arial", 16, "bold"), fill='#88ff88')
    
    def draw_reactor(self):
        """Рисует лабораторию с реактором"""
        self.canvas.delete("all")
        
        # Стены
        self.canvas.create_rectangle(50, 50, 850, 450, fill='#1a1a2a', outline='#44aaff', width=2)
        
        # Реактор
        self.canvas.create_oval(350, 150, 550, 350, fill='#3355aa', outline='#44aaff', width=3)
        self.canvas.create_oval(380, 180, 520, 320, fill='#2255cc', outline='#66ccff', width=2)
        self.canvas.create_oval(410, 210, 490, 290, fill='#1166dd', outline='#88ddff', width=2)
        self.canvas.create_text(450, 250, text="☢️", font=("Arial", 50))
        
        # Свечение
        for i in range(3):
            x = 350 + i * 100
            self.canvas.create_oval(x-20, 350, x+20, 390, fill='#44ff44', outline='#44ff44', width=0)
        
        # Люк
        self.canvas.create_rectangle(680, 300, 780, 380, fill='#333344', outline='#6666aa', width=2)
        self.canvas.create_text(730, 340, text="🕳️", font=("Arial", 30))
        
        self.canvas.create_text(450, 420, text="☢️ РЕАКТОРНАЯ", 
                                font=("Arial", 16, "bold"), fill='#44aaff')
    
    def draw_ending(self, ending_type):
        """Рисует финальную сцену"""
        self.canvas.delete("all")
        
        # Фон
        self.canvas.create_rectangle(0, 0, 900, 500, fill='#0a0a1a')
        
        if ending_type == "secret":
            # Секретная концовка - тоннель
            self.canvas.create_oval(200, 200, 700, 400, fill='#1a1a2a', outline='#333355', width=3)
            self.canvas.create_text(450, 250, text="🕳️", font=("Arial", 80))
            self.canvas.create_text(450, 350, text="СЕКРЕТНЫЙ ТОННЕЛЬ", 
                                    font=("Arial", 20, "bold"), fill='#ffd700')
            self.canvas.create_text(450, 400, text="🏆 ВЫ СБЕЖАЛИ! 🏆", 
                                    font=("Arial", 24, "bold"), fill='#ff6b6b')
        
        elif ending_type == "best":
            # Лучшая концовка - свобода
            self.canvas.create_rectangle(0, 0, 900, 500, fill='#0a2a0a')
            self.canvas.create_text(450, 150, text="🌅", font=("Arial", 80))
            self.canvas.create_text(450, 280, text="ВЫ НА СВОБОДЕ!", 
                                    font=("Arial", 30, "bold"), fill='#ffd700')
            self.canvas.create_text(450, 350, text="🏆 ЛУЧШАЯ КОНЦОВКА", 
                                    font=("Arial", 22, "bold"), fill='#00ff88')
        
        elif ending_type == "bad":
            # Плохая концовка - темнота
            self.canvas.create_rectangle(0, 0, 900, 500, fill='#000000')
            self.canvas.create_text(450, 200, text="🌑", font=("Arial", 80))
            self.canvas.create_text(450, 320, text="ТЬМА ПОГЛОТИЛА ВАС...", 
                                    font=("Arial", 26, "bold"), fill='#666677')
            self.canvas.create_text(450, 380, text="😞 ПЛОХАЯ КОНЦОВКА", 
                                    font=("Arial", 20, "bold"), fill='#ff6b6b')
        
        else:  # worst
            # Худшая концовка - заперт
            self.canvas.create_rectangle(0, 0, 900, 500, fill='#1a0a0a')
            self.canvas.create_text(450, 150, text="⛓️", font=("Arial", 80))
            self.canvas.create_text(450, 280, text="ВЫ ЗАПЕРТЫ НАВЕЧНО", 
                                    font=("Arial", 26, "bold"), fill='#ff3333')
            self.canvas.create_text(450, 350, text="☠️ ХУДШАЯ КОНЦОВКА", 
                                    font=("Arial", 20, "bold"), fill='#ff4444')
    
    def show_scene(self, step):
        self.step = step
        
        if step == 0:  # Старт
            self.draw_room()
            self.story_label.config(
                text="🏚️ Вы приходите в сознание в заброшенной лаборатории...\n"
                     "Голова раскалывается. Последнее, что вы помните - взрыв.\n"
                     "Нужно срочно найти выход!",
                fg='#ffffff'
            )
            self.btn1.config(text="🔍 ОСМОТРЕТЬ КОМНАТУ")
            self.btn2.config(text="🚪 ОТКРЫТЬ ДВЕРЬ")
            self.btn2.pack(side=tk.LEFT, padx=15)
            self.btn1.pack(side=tk.LEFT, padx=15)
            self.restart_btn.pack_forget()
            
        elif step == 1:  # Карта найдена
            self.draw_room()
            self.canvas.create_text(200, 290, text="🗂️ КАРТА!", 
                                   font=("Arial", 16, "bold"), fill='#ffd700')
            self.story_label.config(
                text="✅ Вы нашли КАРТУ ДОСТУПА!\n"
                     "Теперь нужно найти способ открыть главную дверь.\n\n"
                     "Куда пойдёте?",
                fg='#00ff88'
            )
            self.btn1.config(text="⚡ В ЭЛЕКТРОЩИТОВУЮ")
            self.btn2.config(text="☢️ В ЛАБОРАТОРИЮ")
            
        elif step == 2:  # Дверь заперта
            self.draw_room()
            self.canvas.create_text(740, 250, text="🔒", font=("Arial", 40))
            self.story_label.config(
                text="🔒 Дверь заперта!\n"
                     "Похоже, нужна карта доступа.\n"
                     "Придётся исследовать лабораторию дальше...",
                fg='#ff6b6b'
            )
            self.btn1.config(text="🔍 ОСМОТРЕТЬ КОМНАТУ")
            self.btn2.pack_forget()
            
        elif step == 3:  # Электрощитовая
            self.draw_electric()
            self.story_label.config(
                text="⚡ Вы в ЭЛЕКТРОЩИТОВОЙ\n\n"
                     "Старый пульт управления выглядит рабочим.\n"
                     "Что делать?",
                fg='#88ff88'
            )
            self.btn1.config(text="🔌 ВКЛЮЧИТЬ ПИТАНИЕ")
            self.btn2.config(text="🚶 НЕ ТРОГАТЬ")
            self.btn2.pack(side=tk.LEFT, padx=15)
            
        elif step == 4:  # Питание включено
            self.draw_electric()
            self.canvas.create_text(450, 100, text="💡 ПИТАНИЕ ВКЛЮЧЕНО!", 
                                   font=("Arial", 18, "bold"), fill='#00ff88')
            self.story_label.config(
                text="💡 По всей лаборатории зажглись огни!\n\n"
                     "✅ Питание восстановлено!\n"
                     "Теперь можно попробовать открыть главную дверь.",
                fg='#00ff88'
            )
            self.btn1.config(text="🚪 ИДТИ К ВЫХОДУ")
            self.btn2.pack_forget()
            
        elif step == 5:  # Лаборатория
            self.draw_reactor()
            self.story_label.config(
                text="☢️ Вы в комнате с огромным реактором\n\n"
                     "За пультом вы заметили странный ЛЮК в полу!\n"
                     "Что делать?",
                fg='#44aaff'
            )
            self.btn1.config(text="🕳️ ИСПОЛЬЗОВАТЬ ПРОХОД")
            self.btn2.config(text="🔙 ВЕРНУТЬСЯ")
            self.btn2.pack(side=tk.LEFT, padx=15)
            
        elif step == 6:  # Секретная концовка
            self.draw_ending("secret")
            self.story_label.config(
                text="🏆🏆🏆 СЕКРЕТНАЯ КОНЦОВКА! 🏆🏆🏆\n\n"
                     "Вы нырнули в люк и оказались в подземном тоннеле!\n"
                     "Через час вы вышли к старой дороге!\n\n"
                     "🎉 ВЫ СОВЕРШИЛИ ИДЕАЛЬНЫЙ ПОБЕГ!",
                fg='#ffd700'
            )
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
            
        elif step == 7:  # Финальная концовка
            if self.card and self.power:
                self.draw_ending("best")
                self.story_label.config(
                    text="🏆🏆🏆 ЛУЧШАЯ КОНЦОВКА! 🏆🏆🏆\n\n"
                         "✅ Карта доступа принята!\n"
                         "✅ Питание работает!\n"
                         "🔓 Дверь открылась...\n\n"
                         "🎉 Вы выбрались из лаборатории!\n"
                         "🎉 Поздравляем! Вы спаслись!",
                    fg='#00ff88'
                )
            elif self.card and not self.power:
                self.draw_ending("bad")
                self.story_label.config(
                    text="😞 ПЛОХАЯ КОНЦОВКА\n\n"
                         "✅ Карта доступа есть\n"
                         "❌ Но питания нет!\n"
                         "🚫 Дверь не открывается...\n\n"
                         "💀 Вы застряли в темноте навсегда.",
                    fg='#ff6b6b'
                )
            else:
                self.draw_ending("worst")
                self.story_label.config(
                    text="☠️☠️☠️ ХУДШАЯ КОНЦОВКА ☠️☠️☠️\n\n"
                         "❌ У вас нет карты доступа!\n"
                         "❌ Питания нет!\n"
                         "🚫 Дверь заперта навсегда...\n\n"
                         "💀 Лаборатория стала вашей могилой.",
                    fg='#ff3333'
                )
            
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
    
    def choice1(self):
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
        if self.step == 0:
            self.show_scene(2)
        elif self.step == 1:
            self.show_scene(5)
        elif self.step == 3:
            self.show_scene(7)
        elif self.step == 5:
            self.show_scene(7)
    
    def restart(self):
        self.card = False
        self.power = False
        self.restart_btn.pack_forget()
        self.btn1.pack(side=tk.LEFT, padx=15)
        self.btn2.pack(side=tk.LEFT, padx=15)
        self.show_scene(0)

if __name__ == "__main__":
    root = tk.Tk()
    game = LabGame(root)
    root.mainloop()