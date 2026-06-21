import tkinter as tk
from tkinter import messagebox

class LabGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧪 Побег из лаборатории")
        self.root.geometry("700x550")
        self.root.configure(bg='#1a1a2e')
        
        self.card = False
        self.power = False
        self.step = 0
        
        # Заголовок
        self.title_label = tk.Label(
            root, 
            text="🧪 ПОБЕГ ИЗ ЗАБРОШЕННОЙ ЛАБОРАТОРИИ",
            font=("Arial", 18, "bold"),
            fg="#00ff88",
            bg='#1a1a2e'
        )
        self.title_label.pack(pady=20)
        
        # Текстовое поле для истории
        self.story_text = tk.Text(
            root,
            height=10,
            width=70,
            font=("Arial", 12),
            bg='#16213e',
            fg='#ffffff',
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.story_text.pack(pady=10, padx=20)
        self.story_text.config(state=tk.DISABLED)
        
        # Кнопки
        self.button_frame = tk.Frame(root, bg='#1a1a2e')
        self.button_frame.pack(pady=20)
        
        self.btn1 = tk.Button(
            self.button_frame,
            text="",
            font=("Arial", 12),
            width=25,
            bg='#00ff88',
            fg='#000000',
            relief=tk.FLAT,
            command=self.choice1
        )
        self.btn1.pack(side=tk.LEFT, padx=10)
        
        self.btn2 = tk.Button(
            self.button_frame,
            text="",
            font=("Arial", 12),
            width=25,
            bg='#ff6b6b',
            fg='#000000',
            relief=tk.FLAT,
            command=self.choice2
        )
        self.btn2.pack(side=tk.LEFT, padx=10)
        
        self.restart_btn = tk.Button(
            root,
            text="🔄 Играть заново",
            font=("Arial", 10),
            bg='#ffd93d',
            relief=tk.FLAT,
            command=self.restart
        )
        
        self.show_scene(0)
    
    def show_scene(self, step):
        self.step = step
        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete(1.0, tk.END)
        
        if step == 0:  # Старт
            self.story_text.insert(tk.END, "🏚️ Вы приходите в сознание в тёмной заброшенной лаборатории...\n\n")
            self.story_text.insert(tk.END, "Голова раскалывается. Последнее, что вы помните - взрыв.\n")
            self.story_text.insert(tk.END, "Нужно срочно найти выход!")
            self.btn1.config(text="🔍 Осмотреть комнату")
            self.btn2.config(text="🚪 Попытаться открыть дверь")
            
        elif step == 1:  # После осмотра
            self.story_text.insert(tk.END, "🔦 Вы обыскали комнату!\n\n")
            self.story_text.insert(tk.END, "✅ Вы нашли старую КАРТУ ДОСТУПА!\n")
            self.story_text.insert(tk.END, "Теперь нужно найти способ открыть главную дверь.\n\n")
            self.story_text.insert(tk.END, "Куда пойдёте?")
            self.btn1.config(text="⚡ В электрощитовую")
            self.btn2.config(text="☢️ В лабораторию")
            
        elif step == 2:  # Дверь заперта
            self.story_text.insert(tk.END, "🚫 Дверь заперта!\n\n")
            self.story_text.insert(tk.END, "Похоже, нужна карта доступа.\n")
            self.story_text.insert(tk.END, "Придётся исследовать лабораторию дальше...")
            self.btn1.config(text="🔍 Осмотреть комнату")
            self.btn2.config(text="")
            self.btn2.pack_forget()
            
        elif step == 3:  # Электрощитовая
            self.story_text.insert(tk.END, "⚡ Вы в ЭЛЕКТРОЩИТОВОЙ\n\n")
            self.story_text.insert(tk.END, "Старый пульт управления выглядит рабочим.\n")
            self.story_text.insert(tk.END, "Что делать?")
            self.btn1.config(text="🔌 Включить питание")
            self.btn2.config(text="🚶 Не трогать")
            
        elif step == 4:  # Питание включено
            self.story_text.insert(tk.END, "💡 По всей лаборатории зажглись огни!\n\n")
            self.story_text.insert(tk.END, "✅ Питание восстановлено!\n")
            self.story_text.insert(tk.END, "Теперь можно попробовать открыть главную дверь.")
            self.btn1.config(text="🚪 Идти к выходу")
            self.btn2.config(text="")
            self.btn2.pack_forget()
            
        elif step == 5:  # Лаборатория с реактором
            self.story_text.insert(tk.END, "☢️ Вы в комнате с огромным реактором\n\n")
            self.story_text.insert(tk.END, "За пультом вы заметили странный ЛЮК в полу!\n")
            self.story_text.insert(tk.END, "Что делать?")
            self.btn1.config(text="🕳️ Использовать проход")
            self.btn2.config(text="🔙 Вернуться")
            
        elif step == 6:  # Секретная концовка
            self.story_text.insert(tk.END, "🏆🏆🏆 СЕКРЕТНАЯ КОНЦОВКА! 🏆🏆🏆\n\n")
            self.story_text.insert(tk.END, "Вы нырнули в люк и оказались в подземном тоннеле...\n")
            self.story_text.insert(tk.END, "Через час вы вышли к старой дороге!\n\n")
            self.story_text.insert(tk.END, "🎉 ВЫ СОВЕРШИЛИ ПОБЕГ!\n")
            self.story_text.insert(tk.END, "🎉 Это ЛУЧШАЯ концовка!")
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
            
        elif step == 7:  # Финальная концовка (лучшая)
            if self.card and self.power:
                self.story_text.insert(tk.END, "🏆🏆🏆 ЛУЧШАЯ КОНЦОВКА! 🏆🏆🏆\n\n")
                self.story_text.insert(tk.END, "✅ Карта доступа принята!\n")
                self.story_text.insert(tk.END, "✅ Питание работает!\n")
                self.story_text.insert(tk.END, "🔓 Дверь открылась...\n\n")
                self.story_text.insert(tk.END, "🎉 Вы выбрались из лаборатории!\n")
                self.story_text.insert(tk.END, "🎉 Поздравляем! Вы спаслись!")
            elif self.card and not self.power:
                self.story_text.insert(tk.END, "😞 ПЛОХАЯ КОНЦОВКА\n\n")
                self.story_text.insert(tk.END, "✅ Карта доступа есть\n")
                self.story_text.insert(tk.END, "❌ Но питания нет!\n")
                self.story_text.insert(tk.END, "🚫 Дверь не открывается...\n\n")
                self.story_text.insert(tk.END, "💀 Вы застряли в темноте.")
            else:
                self.story_text.insert(tk.END, "☠️☠️☠️ ХУДШАЯ КОНЦОВКА ☠️☠️☠️\n\n")
                self.story_text.insert(tk.END, "❌ У вас нет карты доступа!\n")
                self.story_text.insert(tk.END, "❌ Питания нет!\n")
                self.story_text.insert(tk.END, "🚫 Дверь заперта навсегда...\n\n")
                self.story_text.insert(tk.END, "💀 Лаборатория стала вашей могилой.")
            
            self.btn1.pack_forget()
            self.btn2.pack_forget()
            self.restart_btn.pack(pady=10)
        
        self.story_text.config(state=tk.DISABLED)
    
    def choice1(self):
        if self.step == 0:
            self.card = True
            self.show_scene(1)
        elif self.step == 1:
            self.show_scene(3)
        elif self.step == 2:
            self.card = True
            self.show_scene(1)
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
        self.btn1.pack(side=tk.LEFT, padx=10)
        self.btn2.pack(side=tk.LEFT, padx=10)
        self.show_scene(0)

if __name__ == "__main__":
    root = tk.Tk()
    game = LabGame(root)
    root.mainloop()