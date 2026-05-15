import fcntl
from contextlib import contextmanager
import sys



@contextmanager
def file_lock(group_name, logger):
    lock_fd = open(f"/var/lock/{group_name}.lock", "w")
    locked = False
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        locked = True
        logger.info("Lock erfolgreich gesetzt.")
        yield
    except BlockingIOError:
        logger.warning(
            f"Prozess vorzeitig beendet.|\n"
            f"Ein anderer Archivierungsprozess für die Gruppe ‘{group_name}‘ läuft bereits."
            f"\n{80 * '-'}")
        sys.exit(1)
    finally:
        if locked:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
                logger.info(f"Lock freigegeben.\n{80 * '-'}")
            except Exception:
                logger.warning(f"Das Lock konnte nicht freigegeben werden.\n{80 * '-'}")
            lock_fd.close()
