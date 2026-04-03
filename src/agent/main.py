import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner import RegistryScanner
from reporter import JsonReporter
from logger import AppLogger

def main():
    parser = argparse.ArgumentParser(description="Агент инвентаризации ПО")
    parser.add_argument("--scan", action="store_true", help="Запустить сканирование")
    parser.add_argument("--output", type=str, help="Сохранить отчет в файл")
    parser.add_argument("--send", type=str, help="Отправить отчет на сервер")
    
    args = parser.parse_args()
    
    logger = AppLogger()
    
    if args.scan:
        logger.info("Начало сканирования")
        
        scanner = RegistryScanner()
        software_list = scanner.scan()
        
        logger.info(f"Найдено {len(software_list)} программ")
        
        reporter = JsonReporter()
        report = reporter.generate_report(software_list)
        
        # Вывод в консоль
        print(f"\nИмя компьютера: {report['computer_name']}")
        print(f"Дата сканирования: {report['scan_date']}")
        print(f"Всего программ: {report['total_software']}")
        print("\nСписок ПО:")
        for i, sw in enumerate(report['software_list'][:20], 1):
            print(f"  {i}. {sw['name']} - {sw['version']} ({sw['publisher']})")
        
        if len(report['software_list']) > 20:
            print(f"  ... и еще {len(report['software_list']) - 20} программ")
        
        # Сохранение в файл
        if args.output:
            reporter.save_to_file(report, args.output)
            logger.info(f"Отчет сохранен в {args.output}")
        
        logger.info("Сканирование завершено")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
