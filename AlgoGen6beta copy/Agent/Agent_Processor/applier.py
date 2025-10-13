from pathlib import Path

class ProjectBuilder:
    def __init__(self, agent_folder=None):
        # Родительская папка агента — корень для сканирования
        self.agent_folder = Path(agent_folder) if agent_folder else Path(__file__).parent.parent
        self.project_root = self.agent_folder.parent

    def build_from_template(self, template: str):
        lines = template.splitlines()
        stack = [(self.project_root, -1)]  # (путь, уровень отступа)
        file_path = None
        file_content = []
        base_indent = None  # для сохранения правильных отступов

        def save_file():
            nonlocal file_path, file_content, base_indent
            if file_path:
                if file_content:
                    # Убираем только базовый отступ
                    adjusted = []
                    for l in file_content:
                        if l.strip():
                            adjusted.append(l[base_indent:] if base_indent is not None and len(l) >= base_indent else l)
                        else:
                            adjusted.append("")
                    file_path.write_text("\n".join(adjusted), encoding="utf-8")
                else:
                    file_path.write_text("", encoding="utf-8")
            file_path, file_content, base_indent = None, [], None

        for line in lines:
            if not line.strip():
                if file_path:
                    file_content.append("")
                continue

            indent = len(line) - len(line.lstrip(" "))
            stripped = line.strip()

            # --- Новый каталог ---
            if stripped.startswith("Dir:"):
                save_file()
                dirname = stripped.split(":", 1)[1].strip()
                while stack and stack[-1][1] >= indent:
                    stack.pop()
                parent_dir = stack[-1][0]
                current_dir = parent_dir / dirname
                current_dir.mkdir(parents=True, exist_ok=True)
                stack.append((current_dir, indent))

            # --- Новый файл ---
            elif stripped.startswith("File:"):
                save_file()
                filename = stripped.split(":", 1)[1].strip()
                while stack and stack[-1][1] >= indent:
                    stack.pop()
                parent_dir = stack[-1][0]
                file_path = parent_dir / filename

            # --- Контент файла ---
            else:
                if file_path:
                    if base_indent is None and line.strip():
                        base_indent = len(line) - len(line.lstrip(" "))
                    file_content.append(line)

        save_file()
        print(f"✅ Структура успешно собрана в: {self.project_root}")