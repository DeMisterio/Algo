import os
from pathlib import Path
import json
import shutil
import json
import os
import shutil
from pathlib import Path
from watchdog.utils.dirsnapshot import DirectorySnapshot

class BackUper():
    def __init__(self, Struct=None, Data=None, ignore_folder=None):
        self.Struct = Struct
        self.Data = Data 
        self.ignore_folder = ignore_folder or Path(__file__).parent.parent

    def safe_load_json(self, filepath):
        try:
            with open(filepath, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️ Ошибка загрузки JSON: {e}")
            config = {"version": 1.0}
            with open(filepath, "w") as file:
                json.dump(config, file, indent=4)
            return config

    def set_a_version(self):
        config_path = Path("config.json")
        if not config_path.exists():
            config = {'version': 1.0}
            with open(config_path, "w") as file:
                json.dump(config, file, indent=4)
            return 1.0
        else:
            try:
                config = self.safe_load_json("config.json")
                version = config.get("version", 0)
                version += 1
                config['version'] = version
                with open("config.json", "w") as file:
                    json.dump(config, file, indent=4)
                return version
            except Exception as e:
                print(f"⚠️ Ошибка изменения JSON: {e}")
                return 1.0
    def set_a_conclusion(self, conclusion):
        try:
            config = self.safe_load_json("config.json")
            version = config.get("version", 0)
            config['version' + version + '_UpdateInfo'] = conclusion
            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)
            return version
        except Exception as e:
            print(f"⚠️ Ошибка изменения JSON: {e}")
            return 1.0

    def create_BU_folder(self):
        print('BU_folder_created')
        version = int(self.set_a_version())
        BU_main_folder_name = f"{Path(__file__).parent.parent.parent.name}_v{version}"
        # Создаем папку бэкапа в той же директории, что и скрипт
        backup_path = Path(__file__).parent / BU_main_folder_name
        backup_path.mkdir(parents=True, exist_ok=True)
        return backup_path

    def _should_ignore(self, path):
        """Фильтр для игнорирования папки агента и .DS_Store файлов"""
        path_obj = Path(path)
        return (self.ignore_folder.name in path_obj.parts or 
                path_obj.name == '.DS_Store')

    def BackUpData(self, destination=None):
        """
        Копирует всё из текущей папки проекта в папку destination,
        используя тот же подход, что и в парсерах.
        """
        print('Back_Up_Started')
        
        # Определяем корневую папку проекта (родительская папка ignore_folder)
        project_root = self.ignore_folder.parent
        destination = Path(self.create_BU_folder())
        
        # Создаем снимок директории
        snapshot = DirectorySnapshot(str(project_root))
        
        # Копируем файлы и директории
        for path in sorted(snapshot.paths):
            if self._should_ignore(path) or Path(path) == project_root:
                continue
                
            try:
                rel_path = Path(path).relative_to(project_root)
                target_path = destination / rel_path
                
                if Path(path).is_dir():
                    target_path.mkdir(parents=True, exist_ok=True)
                else:
                    # Создаем родительские директории если нужно
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, target_path)
                    
            except Exception as e:
                print(f"Ошибка при копировании {path}: {e}")
        
        print(f'Back_Up_Completed to {destination}')
        return True


