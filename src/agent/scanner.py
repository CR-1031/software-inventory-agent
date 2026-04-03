import winreg
from datetime import datetime

class Software:
    def __init__(self, name="", version="", publisher="", install_date=""):
        self.name = name
        self.version = version
        self.publisher = publisher
        self.install_date = install_date

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "publisher": self.publisher,
            "install_date": self.install_date
        }

    def is_valid(self):
        return self.name != ""


class RegistryScanner:
    def __init__(self, include_32bit=True):
        self.include_32bit = include_32bit

    def scan(self):
        software_list = []
        
        # Основной раздел 64-bit
        software_list += self.scan_hive(winreg.HKEY_LOCAL_MACHINE, 
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        
        # 32-bit приложения на 64-bit системе
        if self.include_32bit:
            software_list += self.scan_hive(winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
        
        return software_list

    def scan_hive(self, hive, subkey):
        software_list = []
        try:
            key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
            num_subkeys = winreg.QueryInfoKey(key)[0]
            
            for i in range(num_subkeys):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey_path = f"{subkey}\\{subkey_name}"
                    software = self.read_software_from_key(hive, subkey_path, subkey_name)
                    if software and software.is_valid():
                        software_list.append(software)
                except Exception:
                    continue
                    
            winreg.CloseKey(key)
        except Exception:
            pass
        
        return software_list

    def read_software_from_key(self, hive, subkey_path, subkey_name):
        try:
            key = winreg.OpenKey(hive, subkey_path, 0, winreg.KEY_READ)
            
            name = ""
            version = ""
            publisher = ""
            install_date = ""
            
            try:
                name = winreg.QueryValueEx(key, "DisplayName")[0]
            except:
                name = subkey_name
            
            try:
                version = winreg.QueryValueEx(key, "DisplayVersion")[0]
            except:
                pass
            
            try:
                publisher = winreg.QueryValueEx(key, "Publisher")[0]
            except:
                pass
            
            try:
                install_date = winreg.QueryValueEx(key, "InstallDate")[0]
            except:
                pass
            
            winreg.CloseKey(key)
            
            return Software(name, version, publisher, install_date)
        except Exception:
            return None
