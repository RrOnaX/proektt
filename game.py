import os
import sys

def clear_screen():
    """Очистка экрана для разных ОС"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color_code):
    """Цветной вывод в консоль"""
    print(f"\033[{color_code}m{text}\033[0m")

def print_slow(text, delay=0.03):
    """Эффект печатающегося текста"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        import time
        time.sleep(delay)
    print()

def game():
    clear_screen()
    print_colored("="*50, "96")
    print_colored("   🧪 ПОБЕГ ИЗ ЗАБРОШЕННОЙ ЛАБОРАТОРИИ   ", "93")
    print_colored("="*50, "96")
    print()
    
    card = False
    power = False
    
    # ПЕРВЫЙ ВЫБОР
    print_slow("Вы приходите в сознание в темной лаборатории...")
    print_slow("Голова раскалывается. Последнее, что вы помните - взрыв.")
    print()
    print_colored("1 - Осмотреть комнату", "92")
    print_colored("2 - Попытаться открыть дверь", "91")
    print()
    
    while True:
        choice = input("👉 Ваш выбор (1 или 2): ")
        if choice in ["1", "2"]:
            break
        print_colored("❌ Введите 1 или 2!", "91")
    
    if choice == "1":
        card = True
        print_slow("🔍 Вы обыскали комнату и нашли старую карту доступа!", 0.05)
        print_colored("✅ Карта доступа получена!", "92")
    else:
        print_slow("🚪 Дверь заперта. Без карты доступа её не открыть.", 0.05)
        print_colored("❌ Придется искать другой путь.", "91")
    
    print()
    input("Нажмите Enter чтобы продолжить...")
    clear_screen()
    
    # ВТОРОЙ ВЫБОР
    print_colored("📍 Куда пойдете?", "93")
    print_colored("1 - Пойти в электрощитовую", "92")
    print_colored("2 - Пойти в лабораторию с реактором", "91")
    print()
    
    while True:
        choice = input("👉 Ваш выбор (1 или 2): ")
        if choice in ["1", "2"]:
            break
        print_colored("❌ Введите 1 или 2!", "91")
    
    if choice == "1":
        clear_screen()
        print_colored("⚡ ЭЛЕКТРОЩИТОВАЯ", "93")
        print_slow("Вы вошли в комнату, уставленную старыми щитками.")
        print_slow("Пульт управления выглядит рабочим.")
        print()
        print_colored("1 - Включить питание", "92")
        print_colored("2 - Не трогать оборудование", "91")
        print()
        
        while True:
            choice = input("👉 Ваш выбор (1 или 2): ")
            if choice in ["1", "2"]:
                break
            print_colored("❌ Введите 1 или 2!", "91")
        
        if choice == "1":
            power = True
            print_slow("🔌 Вы дернули рычаг. По всей лаборатории зажглись огни!", 0.05)
            print_colored("✅ Питание восстановлено!", "92")
        else:
            print_slow("Вы решили не рисковать и покинули щитовую.", 0.05)
            print_colored("⚠️ В лаборатории осталось темно.", "93")
    
    else:
        clear_screen()
        print_colored("☢️ ЛАБОРАТОРИЯ", "93")
        print_slow("Вы зашли в комнату с огромным реактором.")
        print_slow("За пультом вы заметили странный люк в полу.")
        print()
        print_colored("1 - Использовать секретный проход", "92")
        print_colored("2 - Вернуться назад", "91")
        print()
        
        while True:
            choice = input("👉 Ваш выбор (1 или 2): ")
            if choice in ["1", "2"]:
                break
            print_colored("❌ Введите 1 или 2!", "91")
        
        if choice == "1":
            clear_screen()
            print_colored("="*50, "96")
            print_colored("   🏆 СЕКРЕТНАЯ КОНЦОВКА!   ", "93")
            print_colored("="*50, "96")
            print()
            print_slow("Вы нырнули в люк и оказались в подземном тоннеле...", 0.05)
            print_slow("Через час вы вышли к старой дороге и были спасены.", 0.05)
            print()
            print_colored("🎉 Вы нашли тайный выход из лаборатории!", "92")
            print_colored("🎉 Это лучшая концовка!", "93")
            return
    
    # ФИНАЛ
    clear_screen()
    print_colored("="*50, "96")
    print_colored("   🚪 ВЫХОД ИЗ ЛАБОРАТОРИИ   ", "93")
    print_colored("="*50, "96")
    print()
    
    if card and power:
        print_slow("✅ Карта доступа принята.", 0.05)
        print_slow("✅ Питание работает.", 0.05)
        print_slow("🔓 Дверь открылась...", 0.05)
        print()
        print_colored("="*50, "92")
        print_colored("   🏆 ЛУЧШАЯ КОНЦОВКА!   ", "93")
        print_colored("="*50, "92")
        print_slow("Вы выбрались из лаборатории и добрались до города.", 0.05)
        print_slow("В новостях сказали, что лаборатория взорвалась через час.", 0.05)
        print_colored("🎉 Поздравляем! Вы спаслись!", "92")
    
    elif card:
        print_slow("✅ Карта доступа принята.", 0.05)
        print_slow("❌ Но питание не работает, двери заблокированы.", 0.05)
        print()
        print_colored("="*50, "91")
        print_colored("   😞 ПЛОХАЯ КОНЦОВКА   ", "93")
        print_colored("="*50, "91")
        print_slow("Вы остались заперты в темной лаборатории.", 0.05)
        print_slow("Через несколько часов вы слышите странный звук...", 0.05)
        print_colored("💀 Игра окончена.", "91")
    
    else:
        print_slow("🚪 Дверь заперта.", 0.05)
        print_slow("❌ У вас нет карты доступа.", 0.05)
        print()
        print_colored("="*50, "91")
        print_colored("   ☠️ ХУДШАЯ КОНЦОВКА   ", "93")
        print_colored("="*50, "91")
        print_slow("Вы не смогли выбраться.", 0.05)
        print_slow("Лаборатория погрузилась во тьму навсегда...", 0.05)
        print_colored("💀 Игра окончена.", "91")

if __name__ == "__main__":
    while True:
        game()
        print()
        play_again = input("🔄 Хотите сыграть еще раз? (да/нет): ").lower()
        if play_again not in ["да", "yes", "д", "y"]:
            print_colored("👋 Спасибо за игру!", "93")
            break
        clear_screen()