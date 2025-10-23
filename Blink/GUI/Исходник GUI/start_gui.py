import os
import sys

# Добавляем текущую директорию в путь для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from main_gui import main
    main()
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что все необходимые библиотеки установлены:")
    print("- tkinter (обычно входит в стандартную установку Python)")
    input("\nНажмите Enter для выхода...")
except Exception as e:
    print(f"Произошла ошибка: {e}")
    input("\nНажмите Enter для выхода...")
