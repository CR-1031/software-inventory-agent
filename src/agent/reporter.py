import json
import platform
from datetime import datetime

class JsonReporter:
    def __init__(self):
        self.computer_name = platform.node()
        self.scan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_report(self, software_list):
        report = {
            "computer_name": self.computer_name,
            "scan_date": self.scan_date,
            "total_software": len(software_list),
            "software_list": [s.to_dict() for s in software_list]
        }
        return report

    def save_to_file(self, data, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
