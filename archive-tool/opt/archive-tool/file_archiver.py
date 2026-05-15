import os
import pathlib
import re
import shutil
import sys
import pwd
import datetime as dt
import grp
import config
import time

from lock import file_lock
from log_config import setup_logger

def group_exists(group_name):
    try:
        grp.getgrnam(group_name)
        return True
    except KeyError:
        return False


def is_valid_config():
    config_path = config.ARCHIVE_PATH
    config_folder = config.ARCHIVE_FOLDER
    if not isinstance(config_path, str):
        return False
    if not isinstance(config_folder, str):
        return False
    if not re.fullmatch(r'[A-Za-z0-9_-]+', config_folder):
        return False
    return True


def is_empty(folder):
    try:
        return not any(e for e in os.listdir(folder) if e not in config.EXCLUDED_FILES)
    except FileNotFoundError:
        return True


def create_archive_folder(my_group):
    timestamp = dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    unique_folder_name = f"{timestamp}_{my_group}_{config.ARCHIVE_FOLDER}"
    temp_folder = os.path.join(config.ARCHIVE_PATH, f"{unique_folder_name}.tmp")
    unique_archive_folder = os.path.join(config.ARCHIVE_PATH, f"{unique_folder_name}")
    os.makedirs(temp_folder, exist_ok=True)
    return unique_archive_folder, temp_folder


def delete_archived_files_from_home_dir(group_members, logger):
    for username in group_members:
        user = pwd.getpwnam(username)
        home = user.pw_dir
        for entry in os.listdir(home):
            path = os.path.join(home, entry)
            try:
                if os.path.isdir(path) and not os.path.islink(path):
                    shutil.rmtree(path)
                elif os.path.isfile(path) and not os.path.islink(
                        path) and not entry in config.EXCLUDED_FILES:
                    os.remove(path)
            except PermissionError:
                logger.error(f"Keine Berechtigung auf Verzeichnis '{home}'. Dateien von {username} wurden nicht verschoben.")

def ignore_func(dir, files):
    return {f for f in files if f in config.EXCLUDED_FILES}

def archive_files_from_group_members(group_name, logger):
    logger.info(f"Archivierungsprozess für Benutzergruppe '{group_name}' startet.")
    if not group_exists(group_name):
        logger.warning("Die Benutzergruppe existiert nicht. Es werden daher keine Dateien verschoben.")
        return
    if not is_valid_config():
        logger.error("Ungültige Konfiguration des Archivordners. Bitte in 'scripts/config.py' überprüfen.")
        return
    group = grp.getgrnam(group_name)
    group_members = group.gr_mem
    if not group_members:
        logger.warning(f"Die Gruppe '{group_name}' hat keine Benutzer. Es wurden daher keine Dateien verschoben.")
        return
    archive_folder_name, temp_folder = create_archive_folder(group_name)
    for username in group_members:
        user = pwd.getpwnam(username)
        archive_user_folder = os.path.join(temp_folder, username)
        home = user.pw_dir
        try:
            if is_empty(home):
                logger.info(f"Das Homeverzeichnis von '{username}' ist leer.")
            else:
                shutil.copytree(home, archive_user_folder, ignore=ignore_func)
                logger.info(f"Die Dateien von '{username}' wurden erfolgreich verschoben:")
        except PermissionError:
            logger.error(
                f"Keine Berechtigung auf Verzeichnis '{home}'. Dateien von {username} wurden nicht verschoben.")
    os.rename(temp_folder, archive_folder_name)
    delete_archived_files_from_home_dir(group_members, logger)
    if is_empty(archive_folder_name):
        shutil.rmtree(archive_folder_name)
        logger.info("Es wurden keine Dateien und Ordner verschoben.")
    else:
        logger.info(f"Die Dateien wurden in folgenden Ordner verschoben. {archive_folder_name}")
        logger.info("Archivierungsprozess beendet.")
    return


if __name__ == "__main__":
    logger = setup_logger()
    if len(sys.argv) > 1:
        group_name = sys.argv[1]
    else:
        logger.error("Prozess vorzeitig beendet. | Gruppenname fehlt als Parameter.|\n"
                     f"Beispiel: archive-tool <gruppen-name>\n{80 * '-'}")
        sys.exit(1)
    with file_lock(group_name, logger):
        archive_files_from_group_members(group_name, logger)