import tkinter as tk
from tkinter import messagebox
import random
import time
import os

# ========== ВСТРОЕННЫЕ ЗВУКИ ==========
try:
    import winsound
    SOUNDS = True
except:
    SOUNDS = False
    print("⚠️ Звуки не доступны (только для Windows)")

def play_sound(sound_type):
    """Воспроизводит звук"""
    if not SOUNDS:
        return
    
    try:
        if sound_type == "click":
            winsound.Beep(800, 50)
        elif sound_type == "success":
            winsound.Beep(523, 150)
            time.sleep(0.05)
            winsound.Beep(659, 150)
        elif sound_type == "fail":
            winsound.Beep(300, 300)
        elif sound_type == "win":
            for note in [523, 659, 784, 1047]:
                winsound.Beep(note, 100)
                time.sleep(0.05)
    except:
        pass

# ========== ИГРА ==========
class LabGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧪 ПОБЕГ ИЗ ЛАБОРАТОРИИ")
        self.root.geometry("800x650")
        self.root.configure(bg='#0a0a1a')
        
        # Игровые переменные
        self.card = False
        self.power = False
        self.step = 0
        
        # ===== ПЕРСОНАЖ =====
        self.player = "👨‍🔬"
        self.player_name = "Учёный"
        
        # ===== ВЕРХНЯЯ ПАНЕЛЬ =====
        top_frame = tk.Frame(root, bg='#0a0a1a')
        top_frame.pack(fill=tk.X, pady=10)
        
        # Имя персонажа
        tk.Label(
            top_frame,
            text=f"{self.player} {self.player_name}",
            font=("Arial", 18, "bold"),
            fg='#ffd700',
            bg='#0a0a1a'
        ).pack(side=tk.LEFT, padx=20)
        
        # Инвентарь
        self.inv_label = tk.Label(
            top_frame,
            text="🎒 Инвентарь: пусто",
            font=("Arial", 12),
            fg='#88ccff',
            bg='#0a0a1a'
        )
        self.inv_label.pack(side=tk.LEFT, padx=20)
        
        # ===== ХОЛСТ =====
        self.canvas = tk.Canvas(
            root,
            width=750,
            height=350,
            bg='#0a0a1a',
            highlightthickness=2,
            highlightcolor='#ffd700'
        )
        self.canvas.pack(pady=10)
        
        # ===== ТЕКСТ =====
        self.text_label = tk.Label(
            root,
            text="",
            font=("Comic Sans MS", 13),
            fg='#ffffff',
            bg='#0a0a1a',
            wraplength=700,
            justify=tk.CENTER
        )
        self.text_label.pack(pady=10)
        
        # ===== СТАТУС =====
        self.status = tk.Label(
            root,
            text="🔍 Исследуйте лабораторию...",
            font=("Arial", 10),
            fg='#666677',
            bg='#0a0a1a'
        )
        self.status.pack()
        
        # ===== КНОПКИ =====
        self.btn_frame = tk.Frame(root, bg='#0a0a1a')
        self.btn_frame.pack(pady=15)
        
        self.btn1 = tk.Button(
            self.btn_frame,
            text="ВЫБОР 1",
            font=("Arial", 12, "bold"),
            width=20,
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
            self.btn_frame,
            text="ВЫБОР 2",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            bg='#ff6b6b',
            fg='#000000',
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            command=self.choice2
        )
        self.btn2.pack(side=tk.LEFT, padx=15)
        
        # ===== КНОПКА ПЕРЕЗАПУСКА =====
        self.restart_btn = tk.Button(
            root,
            text="🔄 ИГРАТЬ ЗАНОВО",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            bg='#ffd93d',
            fg='#000000',
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            command=self.restart
        )
        
        # Запуск игры
        self.show_scene(0)
    
    def update_inventory(self):
        """Обновляет инвентарь"""
        items = []
        if self.card:
            items.append("🗂️ Карта")
        if self.power:
            items.append("⚡ Питание")
        
        if items:
            self.inv_label.config(text=f"🎒 Инвентарь: {', '.join(items)}", fg='#00ff88')
        else:
            self.inv_label.config(text="🎒 Инвентарь: пусто", fg='#88ccff')
    
    def draw_scene(self, scene_type):
        """Рисует сцену"""
        self.canvas.delete("all")
        
        if scene_type == "room":
            # Стены
            self.canvas.create_rectangle(50, 50, 700, 320, fill='#2d2d44', outline='#444466', width=3)
            # Пол
            self.canvas.create_rectangle(50, 260, 700, 320, fill='#3d3d55')
            # Дверь
            self.canvas.create_rectangle(580, 150, 650, 280, fill='#8B4513', outline='#654321', width=3)
            self.canvas.create_oval(630, 200, 640, 220, fill='#ffd700')
            self.canvas.create_text(615, 210, text="🚪", font=("Arial", 25))
            # Стол
            self.canvas.create_rectangle(100, 230, 250, 280, fill='#5d3a1a', outline='#3d2a0a')
            # Предметы
            self.canvas.create_oval(150, 240, 170, 260, fill='#66ccff')
            # Персонаж
            self.canvas.create_text(400, 290, text=self.player, font=("Arial", 35))
            # Название
            self.canvas.create_text(375, 75, text="🏚️ ЗАБРОШЕННАЯ ЛАБОРАТОРИЯ", 
                                    font=("Arial", 16, "bold"), fill='#888899')
            
        elif scene_type == "electric":
            # Стены
            self.canvas.create_rectangle(50, 50, 700, 320, fill='#1a2a1a', outline='#33aa33', width=3)
            # Щитки
            for i in range(3):
                x = 80 + i * 180
                self.canvas.create_rectangle(x, 130, x+150, 270, fill='#333355', outline='#6666aa', width=2)
                self.canvas.create_text(x+75, 200, text=f"ЩИТ {i+1}", font=("Arial", 12), fill='#88ccff')
                # Лампочки
                colors = ['#ff4444', '#44ff44' if self.power else '#ffaa00', '#ffaa00']
                for j in range(3):
                    self.canvas.create_oval(x+20+j*35, 150+j*30, x+40+j*35, 170+j*30, 
                                           fill=colors[j] if j < len(colors) else '#ffaa00')
            # Персонаж
            self.canvas.create_text(400, 290, text=self.player, font=("Arial", 35))
            # Название
            self.canvas.create_text(375, 75, text="⚡ ЭЛЕКТРОЩИТОВАЯ", 
                                    font=("Arial", 16, "bold"), fill='#88ff88')
            
        elif scene_type == "reactor":
            # Стены
            self.canvas.create_rectangle(50, 50, 700, 320, fill='#1a1a2a', outline='#44aaff', width=3)
            # Реактор
            self.canvas.create_oval(300, 130, 450, 270, fill='#3355aa', outline='#44aaff', width=3)
            self.canvas.create_text(375, 200, text="☢️", font=("Arial", 60))
            # Люк
            self.canvas.create_rectangle(550, 200, 630, 280, fill='#333344', outline='#6666aa', width=2)
            self.canvas.create_text(590, 240, text="🕳️", font=("Arial", 30))
            # Персонаж
            self.canvas.create_text(400, 290, text=self.player, font=("Arial", 35))
            # Название
            self.canvas.create_text(375, 75, text="☢️ РЕАКТОРНАЯ", 
                                    font=("Arial", 16, "bold"), fill='#44aaff')
    
    def draw_ending(self, ending_type):
        """Рисует финал"""
        self.canvas.delete("all")
        
        # Фон
        self.canvas.create_rectangle(0, 0, 750, 350, fill='#0a0a1a')
        
        if ending_type == "secret":
            self.canvas.create_text(375, 120, text="🕳️", font=("Arial", 70))
            self.canvas.create_text(375, 210, text="СЕКРЕТНАЯ КОНЦОВКА!", 
                                    font=("Arial", 24, "bold"), fill='#ffd700')
            self.canvas.create_text(375, 270, text="🏆 ВЫ ПОБЕДИЛИ! 🏆", 
                                    font=("Arial", 20, "bold"), fill='#ff6b6b')
            
        elif ending_type == "best":
            self.canvas.create_text(375, 130, text="🌅", font=("Arial", 70))
            self.canvas.create_text(375, 220, text="ЛУЧШАЯ КОНЦОВКА!", 
                                    font=("Arial", 24, "bold"), fill='#ffd700')
            self.canvas.create_text(375, 280, text="🎉 ВЫ НА СВОБОДЕ! 🎉", 
                                    font=("Arial", 20, "bold"), fill='#00ff88')
            
        elif ending_type == "bad":
            self.canvas.create_text(375, 140, text="🌑", font=("Arial", 70))
            self.canvas.create_text(375, 230, text="ПЛОХАЯ КОНЦОВКА", 
                                    font=("Arial", 24, "bold"), fill='#666677')
            self.canvas.create_text(375, 290, text="😞 Вы застряли в темноте...", 
                                    font=("Arial", 16), fill='#444455')
            
        else:  # worst
            self.canvas.create_text(375, 130, text="⛓️", font=("Arial", 70))
            self.canvas.create_text(375, 220, text="ХУДШАЯ КОНЦОВКА", 
                                    font=("Arial", 24, "bold"), fill='#ff3333')
            self.canvas.create_text(375, 280, text="☠️ ВЫ ЗАПЕРТЫ НАВЕЧНО", 
                                    font=("Arial", 18, "bold"), fill='#ff4444')
    
    def show_scene(self, step):
        self.step = step
        self.update_inventory()
        
        if step == 0:  # Старт
            self.draw_scene("room")
            self.text_label.config(
                text="🏚️ Вы в заброшенной лаборатории.\n"
                     "Нужно найти выход!",
                fg='#ffffff'
            )
            self.btn1.config(text="🔍 ОСМОТРЕТЬ")
            self.btn2.config(text="🚪 ОТКРЫТЬ ДВЕРЬ")
            self.btn2.pack(side=tk.LEFT, padx=15)
            self.btn1.pack(side=tk.LEFT, padx=15)
            self.restart_btn.pack_forget()
            self.status.config(text="🔍 Исследуйте комнату...")
            play_sound("click")
            
        elif step == 1:  # Карта найдена
            self.draw_scene("room")
            self.text_label.config(
                text="✅ Вы нашли КАРТУ ДОСТУПА!\n"
                     "Куда пойдёте?",
                fg='#00ff88'
            )
            self.btn1.config(text="⚡ В ЩИТОВУЮ")
            self.btn2.config(text="☢️ В ЛАБОРАТОРИЮ")
            self.status.config(text="🗂️ Карта найдена!")
            play_sound("success")
            
        elif step == 2:  # Дверь заперта
            self.draw_scene("room")
            self.text_label.config(
                text="🔒 Дверь заперта!\n"
                     "Нужна карта доступа!",
                fg='#ff6b6b'
            )
            self.btn1.config(text="🔍 ОСМОТРЕТЬ")
            self.btn2.pack_forget()
            self.status.config(text="🔒 Ищите карту...")
            play_sound("fail")
            
        elif step == 3:  # Электрощитовая
            self.draw_scene("electric")
            self.text_label.config(
                text="⚡ В электрощитовой.\n"
                     "Что делать?",
                fg='#88ff88'
            )
            self.btn1.config(text="🔌 ВКЛЮЧИТЬ")
            self.btn2.config(text="🚶 НЕ ТРОГАТЬ")
            self.btn2.pack(side=tk.LEFT, padx=15)
            self.status.config(text="⚡ Включите питание...")
            
        elif step == 4:  # Питание включено
            self.draw_scene("electric")
            self.text_label.config(
                text="💡 Питание восстановлено!\n"
                     "Теперь к выходу!",
                fg='#00ff88'
            )
            self.btn1.config(text="🚪 К ВЫХОДУ")
            self.btn2.pack_forget()
            self.status.config(text="💡 Питание включено!")
            play_sound("success")
            
        elif step == 5:  # Лаборатория
            self.draw_scene("reactor")
            self.text_label.config(
                text="☢️ Вы в реакторной.\n"
                     "Заметили ЛЮК в полу!",
                fg='#44aaff'
            )
            self.btn1.config(text="🕳️ В ЛЮК")
            self.btn2.config(text="🔙 НАЗАД")
            self.btn2.pack(side=tk.LEFT, padx=15)
            self.status.config(text="☢️ Реакторная...")
            
        elif step == 6:  # Секретная концовка
            self.draw_ending("secret")
            self.text_label.config(
                text="🏆 СЕКРЕТНАЯ КОНЦОВКА!\n"
                     "Вы сбежали через тайный проход!",
                fg='#ffd700'
            )
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
            self.status.config(text="🏆 ПОБЕДА!")
            play_sound("win")
            
        elif step == 7:  # Финал
            if self.card and self.power:
                self.draw_ending("best")
                self.text_label.config(
                    text="🏆 ЛУЧШАЯ КОНЦОВКА!\n"
                         "Карта + питание = СВОБОДА!",
                    fg='#00ff88'
                )
                play_sound("win")
                
            elif self.card and not self.power:
                self.draw_ending("bad")
                self.text_label.config(
                    text="😞 ПЛОХАЯ КОНЦОВКА\n"
                         "Карта есть, но нет питания.",
                    fg='#ff6b6b'
                )
                play_sound("fail")
                
            else:
                self.draw_ending("worst")
                self.text_label.config(
                    text="☠️ ХУДШАЯ КОНЦОВКА\n"
                         "Нет карты, нет питания!",
                    fg='#ff3333'
                )
                play_sound("fail")
            
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
            self.status.config(text="Игра окончена")
    
    def choice1(self):
        play_sound("click")
        
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
        play_sound("click")
        
        if self.step == 0:
            self.show_scene(2)
        elif self.step == 1:
            self.show_scene(5)
        elif self.step == 3:
            self.show_scene(7)
        elif self.step == 5:
            self.show_scene(7)
    
    def restart(self):
        play_sound("click")
        self.card = False
        self.power = False
        self.restart_btn.pack_forget()
        self.btn1.pack(side=tk.LEFT, padx=15)
        self.btn2.pack(side=tk.LEFT, padx=15)
        self.show_scene(0)
        self.status.config(text="🔄 Игра перезапущена!")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    root = tk.Tk()
    game = LabGame(root)
    root.mainloop()