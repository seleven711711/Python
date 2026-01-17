import os
import time
import sqlite3
import subprocess
import sys
import json

# Настройка путей
def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DB_PATH = os.path.join(os.path.dirname(__file__), 'rename_queue.db')
LOCK_FILE = os.path.join(os.path.dirname(__file__), 'worker.lock')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    # Используем новую таблицу tasks с JSON полем files
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, 
            task_dir TEXT, 
            files TEXT, 
            commit_msg TEXT,
            unique_key TEXT UNIQUE ON CONFLICT REPLACE
        )
    ''')
    return conn

def run_git(args, cwd):
    flags = 0x08000000 if os.name == 'nt' else 0
    try:
        subprocess.run(['git'] + args, cwd=cwd, capture_output=True, check=False, creationflags=flags)
    except Exception:
        pass

def process_queue():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, task_dir, files, commit_msg FROM tasks")
        rows = cursor.fetchall()
        
        if not rows:
            conn.close()
            return False

        for row in rows:
            row_id, task_dir, files_json, commit_msg = row
            try:
                files = json.loads(files_json) # [{'base': '...', 'target': '...'}, ...]
            except:
                # Corrupt data, delete
                cursor.execute("DELETE FROM tasks WHERE id=?", (row_id,))
                conn.commit()
                continue
            
            # 1. Resolving paths
            resolved_moves = []
            
            for f in files:
                base_name = f['base']
                target_name = f['target']
                
                target_path = os.path.join(task_dir, target_name)
                current_path = None
                
                if os.path.exists(target_path):
                    current_path = target_path
                else:
                    for prefix in ['', '+', '-']:
                        p = os.path.join(task_dir, prefix + base_name)
                        if os.path.exists(p):
                            current_path = p
                            break
                
                if not current_path:
                    # File not found. Skip it.
                    continue
                    
                resolved_moves.append((current_path, target_path))

            if not resolved_moves:
                # No files found at all. Delete task.
                cursor.execute("DELETE FROM tasks WHERE id=?", (row_id,))
                conn.commit()
                continue
            
            # 2. Check & Rename Phase (Atomic-like)
            completed_renames = []
            abort = False
            
            for src, dst in resolved_moves:
                if src == dst:
                    continue
                
                try:
                    # If target exists (and it's not src), remove it (cleanup old garbage)
                    if os.path.exists(dst):
                         try: os.remove(dst)
                         except: pass

                    os.rename(src, dst)
                    completed_renames.append((src, dst))
                except OSError:
                    # File Locked! Abort everything.
                    abort = True
                    break
                except Exception:
                    abort = True
                    break
            
            if abort:
                # Rollback!
                for src, dst in reversed(completed_renames):
                    try:
                        # Rename dst back to src
                        if os.path.exists(dst):
                            os.rename(dst, src)
                    except:
                        pass
                # Do NOT delete from queue. Wait for next cycle.
                continue

            # 3. Git Phase (Success)
            # Add all target paths (even those that didn't need rename)
            # We add all 'target_path' from resolved_moves just in case
            to_add = set()
            for src, dst in resolved_moves:
                to_add.add(dst)
            
            if to_add:
                for path in to_add:
                    run_git(['add', path], repo_root())
                run_git(['commit', '-m', commit_msg], repo_root())
            
            cursor.execute("DELETE FROM tasks WHERE id=?", (row_id,))
            conn.commit()
                
        conn.close()
        return True
    except Exception:
        return False

def main():
    f_lock = open(LOCK_FILE, 'w')
    try:
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(f_lock.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.lockf(f_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (IOError, OSError):
        return

    idle_count = 0
    while True:
        worked = process_queue()
        
        if worked:
            idle_count = 0
            time.sleep(1)
        else:
            idle_count += 1
            time.sleep(2)
            
        if idle_count > 30:
            break
            
    try:
        f_lock.close()
        os.remove(LOCK_FILE)
    except:
        pass

if __name__ == "__main__":
    main()
