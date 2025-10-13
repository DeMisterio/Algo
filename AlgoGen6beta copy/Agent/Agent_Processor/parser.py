import os
from pathlib import Path

class Parser:
    def __init__(self, agent_folder=None):
        # Папка, где лежит этот скрипт (агент)
        self.agent_folder = agent_folder or Path(__file__).parent.parent
        # Родительская папка агента — корень для сканирования
        self.project_root = self.agent_folder.parent 
        # Имя папки агента, которую нужно игнорировать
        self.ignore_folder_name = self.agent_folder.name
        self.Structure = ""
        self.Data = ""

    def _should_ignore(self, path: Path) -> bool:
        try:
            path = path.resolve()
            # Игнорируем папку агента и всё её содержимое
            if self.ignore_folder_name in path.parts:
                return True
            # Игнорируем всё, что вне project_root
            if self.project_root not in path.parents and path != self.project_root:
                return True
            return False
        except Exception:
            return True

    def parseStruct(self) -> str:
        from pathlib import Path
        from watchdog.utils.dirsnapshot import DirectorySnapshot
        
        snapshot = DirectorySnapshot(str(self.project_root))
        structure_lines = []
        
        # Фильтр для игнорирования папки агента и .DS_Store файлов
        def should_ignore(path):
            path_obj = Path(path)
            return (self.agent_folder.name in path_obj.parts or 
                    path_obj.name == '.DS_Store' or
                    path_obj == self.project_root)

        for path in sorted(snapshot.paths):
            if should_ignore(path):
                continue
                
            rel_path = Path(path).relative_to(self.project_root)
            indent = "    " * (len(rel_path.parents) - 1)
            
            if Path(path).is_dir():
                structure_lines.append(f"{indent}Dir: {rel_path.name}")
            else:
                structure_lines.append(f"{indent}File: {rel_path.name}")
        
        self.Structure = "\n".join(structure_lines)
        return self.Structure

    def parseData(self) -> str:
        from pathlib import Path
        from watchdog.utils.dirsnapshot import DirectorySnapshot
        
        snapshot = DirectorySnapshot(str(self.project_root))
        structure_lines = []
        
        # Фильтр для игнорирования папки агента и .DS_Store файлов
        def should_ignore(path):
            path_obj = Path(path)
            return (self.agent_folder.name in path_obj.parts or 
                    path_obj.name == '.DS_Store' or
                    path_obj == self.project_root)

        for path in sorted(snapshot.paths):
            if should_ignore(path):
                continue
                
            rel_path = Path(path).relative_to(self.project_root)
            indent = "    " * (len(rel_path.parents) - 1)
            
            if Path(path).is_dir():
                structure_lines.append(f"{indent}Dir: {rel_path.name}")
            else:
                structure_lines.append(f"{indent}File: {rel_path.name}")
                # Если текстовый файл, добавляем содержимое
                try:
                    ext = Path(path).suffix.lower()
                    # Список бинарных расширений
                    binary_extensions = {
                        ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".ico",
                        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv",
                        ".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a",
                        ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", 
                        ".exe", ".dll", ".so", ".bin"
                    }
                    
                    if ext not in binary_extensions:
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        # Отступ для содержимого файла
                        content_indent = "    " * len(rel_path.parents)
                        for line in content.splitlines():
                            structure_lines.append(f"{content_indent}{line}")
                    else:
                        content_indent = "    " * len(rel_path.parents)
                        structure_lines.append(f"{content_indent}[binary file]")
                except Exception:
                    content_indent = "    " * len(rel_path.parents)
                    structure_lines.append(f"{content_indent}[unreadable]")
        
        self.Data = "\n".join(structure_lines)
        return self.Data

    def save_structure(self, filepath="Project_struct.txt"):
        if self.Structure:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(self.Structure)
            except Exception:
                pass

    def save_data(self, filepath="Project_data.txt"):
        if self.Data:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(self.Data)
            except Exception:
                pass


sst = Parser()
print(sst.parseData())