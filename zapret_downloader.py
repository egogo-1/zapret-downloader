import os
import shutil
import subprocess
import zipfile
import requests
from pathlib import Path

script_dir = Path(__file__).resolve().parent
zapret_dir = script_dir / "zapret"
lists_dir = zapret_dir / "lists"

URL = "https://api.github.com/repos/Flowseal/zapret-discord-youtube/releases/latest"
release = requests.get(URL).json()
latest_version = release["tag_name"]


# ---------- версия ----------
def get_local_version() -> str | None:
    if not zapret_dir.exists():
        return None
    for bat in zapret_dir.rglob("service.bat"):
        with open(bat, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "LOCAL_VERSION" in line:
                    return line.split("=", 1)[1].strip().strip('"')
    return None


# ---------- выключение ----------
def stop_zapret():
    """Останавливает службу zapret и убивает связанные процессы."""
    print("Остановка zapret...")

    # 1. Остановить службу (если установлена через service.bat)
    subprocess.run(
        ["sc", "stop", "zapret"],
        capture_output=True, text=True, shell=True
    )
    subprocess.run(
        ["sc", "stop", "WinDivert"],
        capture_output=True, text=True, shell=True
    )

    # 2. Убить процессы, которые могут держать файлы
    for proc in ("winws.exe", "WinDivert.exe", "service.bat"):
        subprocess.run(
            ["taskkill", "/F", "/IM", proc],
            capture_output=True, text=True, shell=True
        )

    # 3. Небольшая пауза, чтобы Windows отпустила файлы
    import time
    time.sleep(1)


# ---------- удаление ----------
def clean_zapret(keep: str = "lists"):
    """Удаляет всё в zapret_dir, кроме папки keep."""
    if not zapret_dir.exists():
        return

    print(f"Очистка {zapret_dir} (сохраняю {keep}/)...")
    for item in zapret_dir.iterdir():
        if item.name == keep:
            continue
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        else:
            try:
                item.unlink()
            except PermissionError:
                print(f"  Не удалось удалить {item} — файл занят")
                raise


# ---------- скачивание ----------
def download_zapret():
    zapret_dir.mkdir(parents=True, exist_ok=True)

    for asset in release["assets"]:
        if asset["name"].endswith(".zip"):
            download_url = asset["browser_download_url"]
            zip_path = script_dir / asset["name"]

            print(f"Скачивание {asset['name']}...")
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            print("Распаковка...")
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(zapret_dir)

            zip_path.unlink()
            print("Готово.")
            return
    raise RuntimeError("В релизе не найден .zip-файл")


# ---------- основной сценарий ----------
def update():
    local = get_local_version()
    if local == latest_version:
        print(f"Уже актуальная версия: {local}")
        return

    print(f"Обновление {local} → {latest_version}")

    stop_zapret()          # 1. выключить
    clean_zapret()         # 2. удалить всё, кроме lists
    download_zapret()      # 3. скачать и распаковать


if __name__ == "__main__":
    update()