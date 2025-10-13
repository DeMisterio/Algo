from setuptools import setup

APP = ['aiCalendar3betagen.py']
DATA_FILES = ['AlgoParser.py']  # Если есть дополнительные файлы, добавь их сюда
OPTIONS = {
    'argv_emulation': True,
    'packages': ['textblob', 'sklearn', 'numpy'],  # Only actual installed packages
    'includes': ['textblob', 'sklearn'],  # If needed, but often not necessary
    'excludes': ['packaging']
}

# Включаем дополнительные библиотеки


setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)