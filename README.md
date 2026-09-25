# Zapret Downloader

Программа для автоматической установки и обновления [zapret-discord-youtube](https://github.com/Flowseal/zapret-discord-youtube) от [Flowseal](https://github.com/Flowseal).

## 📖 О проекте

**Zapret Downloader** — это удобная утилита, которая избавляет от необходимости вручную скачивать и обновлять сборку `zapret-discord-youtube`. Программа сама проверяет наличие новых версий, скачивает их и устанавливает в нужную папку.

### Что она делает

- 🔍 Проверяет актуальную версию `zapret-discord-youtube` на GitHub.
- ⬇️ Автоматически скачивает последний релиз.
- 📦 Распаковывает архив в указанную директорию.
- 🔄 Позволяет обновлять уже установленную версию одной командой.
- 🖥️ Работает на Windows.

## 🙏 Благодарности

Этот проект **не является самостоятельной разработкой** в части самого инструмента обхода блокировок. Вся основная работа проделана автором оригинального проекта.

- **Оригинальный проект:** [zapret-discord-youtube](https://github.com/Flowseal/zapret-discord-youtube)
- **Автор:** [Flowseal](https://github.com/Flowseal)
- **Лицензия оригинала:** [Указать лицензию, например MIT]

Огромная благодарность Flowseal за создание и поддержку `zapret-discord-youtube`. Без его труда этот проект был бы невозможен.

## 🚀 Установка и использование

### Требования

- Windows 10/11
- Python 3.8+ (если запускаете из исходников)
- Права администратора (для работы `zapret`)

### Запуск из исходников

```bash
git clone https://github.com/egogo-1/zapret-downloader.git
cd zapret-downloader
python zapret_downloader.py
pip install requests
