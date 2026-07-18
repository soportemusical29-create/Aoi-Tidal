try:
    import warnings
    import requests
    import socket
    import asyncio
    import pproxy
    import threading
    import re
    from lxml import html
    import socks
    import os
    from packaging import version
    import io
    import logging
    import string
    import sys
    import zipfile
    
    # Suppress asyncio "Task was destroyed but it is pending" warnings
    # These occur during normal proxy relay switching and are harmless
    warnings.filterwarnings("ignore", message=".*Task was destroyed but it is pending.*")
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="asyncio")
    
    # Also suppress via logging
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    
    # On Windows, use ProactorEventLoop and suppress its warnings
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    import win32process
    import win32gui
    import win32con
    import time
    import subprocess
    from datetime import datetime, timedelta
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    from requests.exceptions import ProxyError, RequestException
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
    from flask import Flask, render_template, request, redirect, url_for, jsonify
    from flask_sqlalchemy import SQLAlchemy
    from requests.exceptions import RequestException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.action_chains import ActionChains
    import re
    from url_writer import url_writer
    import shutil
    import tempfile
    import atexit
    import signal
    import psutil
    from colorama import init, Fore
    import uuid
    from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
    from comtypes import CLSCTX_ALL
    import pythoncom
    import json
    from websocket import create_connection
    import queue

    from Crypto.Cipher import AES
    import base64
    import secrets
    import base64
    from pathlib import Path
    from tkinter import filedialog, messagebox
    import hmac
    import requests
    import random
    import string
    import hashlib
    from functools import wraps
    from ConsoleLogger import add_log
    import ConsoleLogger
    import UtilsService
    import selenium.webdriver.remote.webelement

    # When running as PyInstaller exe, help patchright find its driver (must bundle with --collect-all patchright)
    if getattr(sys, 'frozen', False):
        _meipass = getattr(sys, '_MEIPASS', None)
        if _meipass:
            for _sub in ('package', 'driver', os.path.join('driver', 'package')):
                _d = os.path.join(_meipass, 'patchright', _sub.replace('/', os.sep))
                if os.path.isdir(_d):
                    os.environ['PATH'] = os.path.abspath(_d) + os.pathsep + os.environ.get('PATH', '')

    from requests.exceptions import ProxyError, RequestException
    from patchright.async_api import async_playwright
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.action_chains import ActionChains

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)

    project_dir_old = os.getenv('APPDATA')
    project_dir2 = os.path.join(project_dir_old, 'Aoi')
    if not os.path.exists(project_dir2):
        os.makedirs(project_dir2, exist_ok=True)
    project_dir = os.path.join(project_dir_old, 'Aoi', 'Tidal')
    if not os.path.exists(project_dir):
        os.makedirs(project_dir, exist_ok=True)

    def _find_chrome_executable():
        """Find Google Chrome executable. Run at launch so compiled exe finds Chrome on current machine. Returns path or None."""
        if sys.platform != 'win32':
            if sys.platform == 'darwin':
                p = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                return p if os.path.isfile(p) else None
            for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'):
                try:
                    path = shutil.which(name)
                    if path:
                        return path
                except Exception:
                    pass
            return None
        # Windows: try registry first (works from compiled exe and respects machine's install)
        try:
            import winreg
            for root, key_path in [
                (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'),
                (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'),
                (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome'),
                (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome'),
            ]:
                try:
                    key = winreg.OpenKey(root, key_path, 0, winreg.KEY_READ)
                    path = None
                    try:
                        if 'App Paths' in key_path:
                            path, _ = winreg.QueryValueEx(key, None)
                        else:
                            try:
                                path, _ = winreg.QueryValueEx(key, 'InstallLocation')
                                if path:
                                    path = os.path.join(path.rstrip(os.sep), 'Application', 'chrome.exe')
                            except Exception:
                                try:
                                    path, _ = winreg.QueryValueEx(key, 'DisplayIcon')
                                    if path and ',' in path:
                                        path = path.split(',')[0].strip()
                                except Exception:
                                    path = None
                        winreg.CloseKey(key)
                        if path:
                            path = os.path.normpath(os.path.expandvars(path))
                            if os.path.isfile(path):
                                return path
                    except Exception:
                        try:
                            winreg.CloseKey(key)
                        except Exception:
                            pass
                except (OSError, FileNotFoundError):
                    pass
        except ImportError:
            pass
        # Hardcoded paths (expand env so it works when env is minimal in compiled exe)
        pf = os.environ.get('PROGRAMFILES', 'C:\\Program Files')
        pf86 = os.environ.get('ProgramFiles(x86)', os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'))
        localappdata = os.environ.get('LOCALAPPDATA', os.path.expandvars('%LOCALAPPDATA%'))
        if not localappdata or localappdata == '%LOCALAPPDATA%':
            localappdata = os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local')
        candidates = [
            os.path.join(pf, 'Google', 'Chrome', 'Application', 'chrome.exe'),
            os.path.join(pf86, 'Google', 'Chrome', 'Application', 'chrome.exe'),
            os.path.join(localappdata, 'Google', 'Chrome', 'Application', 'chrome.exe'),
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        ]
        for path in candidates:
            try:
                path = os.path.normpath(path)
                if path and os.path.isfile(path):
                    return path
            except Exception:
                pass
        return None

    def _get_chrome_version():
        """Detect installed Chrome version by reading chrome.exe file version."""
        try:
            chrome_path = _find_chrome_executable()
            if chrome_path and os.path.isfile(chrome_path):
                import win32api
                info = win32api.GetFileVersionInfo(chrome_path, "\\")
                ms = info['FileVersionMS']
                ls = info['FileVersionLS']
                v1 = (ms >> 16) & 0xffff
                v2 = ms & 0xffff
                v3 = (ls >> 16) & 0xffff
                return f"{v1}.{v2}.{v3}"
        except Exception:
            pass
        try:
            import subprocess
            chrome_path = _find_chrome_executable()
            if chrome_path and os.path.isfile(chrome_path):
                out = subprocess.check_output([chrome_path, '--version'], stderr=subprocess.STDOUT, timeout=5).decode('utf-8', errors='replace')
                import re
                m = re.search(r'(\d+\.\d+\.\d+)', out)
                if m:
                    return m.group(1)
        except Exception:
            pass
        return None

    PATCHRIGHT_CHROME_EXECUTABLE = _find_chrome_executable()

    files = os.path.join(project_dir_old, 'Aoi', 'Tidal', 'Files')
    if not os.path.exists(files):
        os.makedirs(files, exist_ok=True)

    init()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(project_dir, "Files", "batches.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        return response

    db = SQLAlchemy(app)

    Bot_name = "Aoi Tidal"
    global_bot_name = "Tidal"  # IHeartRadio, YouTube Music, Apple Music, Deezer, Napster
    Bot_version = "1.0.1"
    backend_state = 'Initializing...'
    akey = '15c797c3984e3057c40e70871335a11e'.encode('utf-8')


    def generate_secret_key(length=64):
        return base64.urlsafe_b64encode(secrets.token_bytes(length)).decode()


    class PortManager:
        def __init__(self, port_range=(30001, 65535)):
            """
            Initialize the PortManager with a range of ports to scan.
            Defaults to the range of 30001 to 65535.
            """
            self.lock = threading.Lock()
            self.in_use_ports = []
            self.port_range = port_range

        def add_port(self, port):
            """Add a port to the list of in-use ports."""
            with self.lock:
                if port not in self.in_use_ports:
                    self.in_use_ports.append(port)
                    return True  # Successfully added
                else:
                    return False  # Port already in use

        def remove_port(self, port):
            """Remove a port from the list of in-use ports."""
            with self.lock:
                if port in self.in_use_ports:
                    self.in_use_ports.remove(port)
                    return True  # Successfully removed
                else:
                    return False  # Port not in the list

        def get_in_use_ports(self):
            """Retrieve a copy of the current in-use ports."""
            with self.lock:
                return list(self.in_use_ports)  # Return a copy of the list

        def is_port_free(self, port):
            """Check if a port is free on the local machine."""
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Set a timeout for the connection attempt
                try:
                    s.bind(("", port))  # Try to bind to the port
                    return True  # Port is free
                except OSError:
                    return False  # Port is in use

        def use_free_port(self):
            """
            Find and use a free port within the defined range.
            Returns a random free port if successful, or None if no free port is found.
            """
            with self.lock:
                # Generate a shuffled list of ports within the range
                available_ports = list(range(self.port_range[0], self.port_range[1] + 1))
                random.shuffle(available_ports)

                for port in available_ports:
                    if port not in self.in_use_ports and self.is_port_free(port):
                        self.in_use_ports.append(port)
                        return port  # Return the free port

                return None  # No free port found


    class AccountManager:
        def __init__(self, project_dir):
            self.project_dir = project_dir
            self.sessions_dir = os.path.join(project_dir, 'Files', 'Sessions')
            # Uses global used_accounts set and lock for thread safety across all threads

        def get_session_folder_for_email(self, email):
            """
            Get the session folder path for a given email.
            E.g., 'emlkobe5@gmail.com' -> 'emlkobe5_tidal_desktop_session'
            """
            username = email.split('@')[0]
            session_name = f"{username}_tidal_desktop_session"
            return os.path.join(self.sessions_dir, session_name)

        def get_accounts_with_sessions(self):
            """
            Get list of account strings that have existing session folders.
            Returns list of (account_string, session_folder_path) tuples.
            """
            accounts_with_sessions = []
            if not os.path.exists(self.sessions_dir):
                return accounts_with_sessions
            
            # Get all session folders
            existing_sessions = set()
            for folder_name in os.listdir(self.sessions_dir):
                if folder_name.endswith('_tidal_desktop_session'):
                    existing_sessions.add(folder_name)
            
            # Check which accounts have matching session folders
            for account_string in worker_loaded_accounts:
                email = account_string.split(':')[0]
                username = email.split('@')[0]
                session_name = f"{username}_tidal_desktop_session"
                if session_name in existing_sessions:
                    session_path = os.path.join(self.sessions_dir, session_name)
                    accounts_with_sessions.append((account_string, session_path))
            
            return accounts_with_sessions

        def get_free_account(self, stay_logged_in, thread_number):
            """
            Get a free account for the thread.
            
            If stay_logged_in=True: prioritize accounts with existing session folders.
            If stay_logged_in=False: get random account and delete its session folder.

            Args:
                stay_logged_in (bool): Whether to reuse existing sessions.
                thread_number (int): The thread identifier.

            Returns:
                tuple: (email, password, account_string, session_folder) of the account to use.
            """
            if stay_logged_in:
                # First, try to find an account with an existing session folder
                accounts_with_sessions = self.get_accounts_with_sessions()
                random.shuffle(accounts_with_sessions)  # Randomize to distribute load
                
                for account_string, session_folder in accounts_with_sessions:
                    with used_accounts_lock:
                        if account_string not in used_accounts:
                            used_accounts.add(account_string)
                            email, password = account_string.split(":", 1)
                            print_log("INFO", "blue", thread_number, f"Reusing session for account: {email}")
                            return email, password, account_string, session_folder
            
            # No existing session found (or stay_logged_in=False), get a fresh account
            try:
                account_string = get_random_account()
                email, password = account_string.split(":", 1)
                session_folder = self.get_session_folder_for_email(email)
                
                # If stay_logged_in=False, delete the session folder if it exists
                if not stay_logged_in and os.path.exists(session_folder):
                    shutil.rmtree(session_folder)
                    print_log("INFO", "blue", thread_number, f"Deleted old session for: {email}")
                
                # Ensure the session folder exists
                os.makedirs(session_folder, exist_ok=True)
                
                print_log("INFO", "blue", thread_number, f"Using fresh account: {email}:{password}")
                return email, password, account_string, session_folder
            except Exception as e:
                print_log("ERR.", "red", thread_number, f"Failed to get account: {e}")
                raise

        def release_account(self, account_string):
            """
            Remove the account from the used accounts set.

            Args:
                account_string (str): The account string (email:password).
            """
            release_account(account_string)  # Use the global release_account function


    class Batch(db.Model):
        id = db.Column(db.String(50), primary_key=True)
        type = db.Column(db.String(50), nullable=False)
        name = db.Column(db.String(50), nullable=False)
        content = db.Column(db.Text, nullable=False)

        def __repr__(self):
            return f'<Batch {self.name}>'


    class StreamRecord(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        timestamp = db.Column(db.DateTime, nullable=False)
        streams_done = db.Column(db.Integer, nullable=False)
        artist_name = db.Column(db.String(100), nullable=False)
        song_name = db.Column(db.String(100), nullable=False)
        current_playtime = db.Column(db.Integer, nullable=False)

        def __repr__(self):
            return f'<StreamRecord {self.timestamp} - {self.streams_done}>'

    class Link(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        link = db.Column(db.String(255), unique=True, nullable=False)
        artist_name = db.Column(db.String(100), nullable=False)
        album_name = db.Column(db.String(100), nullable=False)
        song_count = db.Column(db.Integer, nullable=False)
        time_read = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self):
            return f'<Link {self.link}>'


    original_socket = socket.socket

    worker_bot_running = False
    worker_threads = {}
    worker_tidal_executable_path = None
    worker_widevine_folder = None
    worker_streams_done = 0
    worker_threads_running = 0
    worker_successful_logins = 0
    worker_unsuccessful_logins = 0
    worker_song_likes = 0
    worker_album_likes = 0
    worker_follows_done = 0
    worker_proxy_errors = 0
    worker_bot_errors = 0

    worker_thread_logging_in = False
    login_semaphore = threading.Semaphore(1)  # Only 1 thread can login at a time
    worker_login_batch_count = 0
    worker_login_batch_timestamp = None
    worker_login_batch_max = 0  # Random 8-11, set per batch

    previous_streams_per_month = None
    current_streams_per_month = 0

    worker_loaded_accounts = []
    worker_loaded_link = []
    worker_loaded_proxies = []
    worker_loaded_login_proxies = []  # Proxies for login (residential)
    worker_loaded_streaming_proxies = []  # Proxies for streaming (datacenter)

    config_threads_to_start = 0
    config_thread_start_delay = 30  # Delay in seconds between starting threads
    config_optimize_tidal_app = False
    config_streams_to_do = 0
    config_album_likes_rate = 0
    config_song_likes_rate = 0
    config_follows_rate = 0
    config_playtime_type = ''
    config_playtime_seconds = ''
    config_playtime_percentage = ''
    config_use_proxies = False
    config_use_dual_proxies = False  # Use separate login and streaming proxies
    config_proxyless_login = False  # Login without proxy, then switch to streaming proxy
    config_links_batch_id = ''
    config_proxies_batch_id = ''
    config_login_proxies_batch_id = ''  # Residential proxies for login
    config_streaming_proxies_batch_id = ''  # Datacenter proxies for streaming
    config_ppa = ''
    config_stay_logged_in = False
    config_accounts_batch_id = ''
    config_use_webhook = False
    config_webhook_name = ''
    config_webhook_url = ''
    config_webhook_interval = 0
    config_shuffle_perc = 0
    config_search_links_perc = 0

    config_hide_tidal_app = False
    config_mute_tidal_app = False
    config_streaming_quality_to_low = False

    settings_capsolver_api_key = None

    start_time = time.time()
    used_accounts = set()
    used_accounts_lock = threading.Lock()
    streaming_proxy_usage = {}  # Dict tracking usage count per proxy
    streaming_proxy_usage_lock = threading.Lock()
    stop_flags = {}
    
    # Global AccountManager instance (shared across all threads)
    global_account_manager = None

    stream_data_queue = []
    stream_data_lock = threading.Lock()


    def verify_token(token):
        try:
            # Decrypt the token using the key
            decrypted_data = decrypt_data(token, akey)
            if decrypted_data != "Decryption failed":
                # Further checks like expiration, or matching the user credentials can be added here
                return True
            else:
                return False
        except Exception as e:
            # print(f"Token verification failed: {str(e)}")
            return False


    def require_token(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]

            if not token or not verify_token(token):
                return jsonify({"message": "Unauthorized"}), 401

            return f(*args, **kwargs)

        return decorated_function


    def save_stream_data():
        while True:
            time.sleep(10)
            records_to_save = []
            with stream_data_lock:
                if len(stream_data_queue) != 0:
                    records_to_save = stream_data_queue[:]
                    stream_data_queue.clear()
            if records_to_save:
                with app.app_context():
                    for record in records_to_save:
                        new_record = StreamRecord(
                            timestamp=record['timestamp'],
                            streams_done=record['streams_done'],
                            artist_name=record['artist_name'],
                            song_name=record['song_name'],
                            current_playtime=record['current_playtime']
                        )
                        db.session.add(new_record)
                    db.session.commit()


    # Start the consumer thread
    consumer_thread = threading.Thread(target=save_stream_data)
    consumer_thread.start()


    def send_stream_data_to_consumer(timestamp, streams_done, artist_name, song_name, current_playtime):
        stream_data = {
            'timestamp': timestamp,
            'streams_done': streams_done,
            'artist_name': artist_name,
            'song_name': song_name,
            'current_playtime': current_playtime
        }
        with stream_data_lock:
            stream_data_queue.append(stream_data)


    def load_used_accounts():
        sessions_folder = os.path.join(project_dir, 'Files', 'Sessions')
        if os.path.exists(sessions_folder):
            for session_dir in os.listdir(sessions_folder):
                account_file_path = os.path.join(sessions_folder, session_dir, 'account.txt')
                if os.path.isfile(account_file_path):
                    with open(account_file_path, 'r') as file:
                        account = file.read().strip()
                        used_accounts.add(account)


    def save_account_to_file(port, account):
        session_folder = os.path.join(project_dir, 'Files', 'Sessions', str(port))
        if not os.path.exists(session_folder):
            os.makedirs(session_folder, exist_ok=True)
        account_file_path = os.path.join(session_folder, 'account.txt')
        with open(account_file_path, 'w') as file:
            file.write(account)

    def kill_tidal_process(tidal_instance):
        try:
            if tidal_instance is None:
                return "No tidal instance provided."
            # Try to terminate gracefully first
            tidal_instance.terminate()
            try:
                tidal_instance.wait(timeout=5)  # Wait for process to die
            except:
                pass
            # If still alive, force kill
            if tidal_instance.poll() is None:
                tidal_instance.kill()
                try:
                    tidal_instance.wait(timeout=5)
                except:
                    pass
            return "Process terminated successfully."
        except psutil.NoSuchProcess:
            return "No such process found."
        except psutil.TimeoutExpired:
            return "Failed to terminate the process within the timeout."
        except Exception as e:
            return f"An error occurred: {e}"


    def bring_tidal_window_to_front(pid=None, title_substring="TIDAL", prefer_login=True):
        """
        Bring TIDAL window to the foreground on Windows.
        
        Args:
            pid: Process ID of TIDAL instance (optional, will search by title if not provided)
            title_substring: Window title to search for (default: "TIDAL")
            prefer_login: If True, prefer the login window over main window
        
        Returns:
            True if window was found and brought to front, False otherwise
        """
        import ctypes
        from ctypes import wintypes
        
        # Windows API constants
        SW_RESTORE = 9
        HWND_TOPMOST = -1
        HWND_NOTOPMOST = -2
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_SHOWWINDOW = 0x0040
        
        user32 = ctypes.windll.user32
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        
        def get_window_text(hwnd):
            length = user32.GetWindowTextLengthW(hwnd) + 1
            buffer = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(hwnd, buffer, length)
            return buffer.value
        
        def get_window_pid(hwnd):
            window_pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
            return window_pid.value
        
        def is_window_visible(hwnd):
            return user32.IsWindowVisible(hwnd)
        
        # Find matching windows
        windows = []
        
        def enum_callback(hwnd, _):
            if is_window_visible(hwnd):
                title = get_window_text(hwnd)
                window_pid = get_window_pid(hwnd)
                
                # Match by PID if provided, otherwise by title
                if pid is not None:
                    if window_pid == pid:
                        windows.append({'hwnd': hwnd, 'title': title, 'pid': window_pid})
                elif title and title_substring.lower() in title.lower():
                    windows.append({'hwnd': hwnd, 'title': title, 'pid': window_pid})
            return True
        
        user32.EnumWindows(EnumWindowsProc(enum_callback), 0)
        
        # Also check for login windows if prefer_login is True
        if prefer_login and pid is None:
            def enum_login_callback(hwnd, _):
                if is_window_visible(hwnd):
                    title = get_window_text(hwnd)
                    if title and 'login' in title.lower():
                        window_pid = get_window_pid(hwnd)
                        windows.insert(0, {'hwnd': hwnd, 'title': title, 'pid': window_pid})
                return True
            user32.EnumWindows(EnumWindowsProc(enum_login_callback), 0)
        
        if not windows:
            return False
        
        # Bring the first matching window to front
        target = windows[0]
        hwnd = target['hwnd']
        
        # Restore if minimized
        user32.ShowWindow(hwnd, SW_RESTORE)
        time.sleep(0.05)
        
        # SetForegroundWindow
        user32.SetForegroundWindow(hwnd)
        
        # Use SetWindowPos with TOPMOST flag temporarily for reliability
        user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
        time.sleep(0.02)
        user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
        
        # Simulate Alt key press to bypass Windows foreground restrictions
        user32.keybd_event(0x12, 0, 0, 0)  # Alt key down
        user32.keybd_event(0x12, 0, 2, 0)  # Alt key up
        time.sleep(0.02)
        user32.SetForegroundWindow(hwnd)
        
        user32.BringWindowToTop(hwnd)
        
        return True


    def get_running_time():
        elapsed_time = time.time() - start_time
        days, remainder = divmod(elapsed_time, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(days)} days, {int(hours):02}:{int(minutes):02}:{int(seconds):02}"


    def encrypt_data(data, key):
        """Encrypt data with AES encryption using EAX mode for confidentiality and authenticity."""
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return base64.b64encode(nonce + tag + ciphertext).decode('utf-8')


    def decrypt_data(enc_data, key):
        """Decrypt data with AES encryption, handling potential errors in decryption."""
        try:
            # Decode the data strictly, this raises an exception if there are issues
            enc_data_bytes = base64.b64decode(enc_data, validate=True)
            nonce, tag, ciphertext = enc_data_bytes[:16], enc_data_bytes[16:32], enc_data_bytes[32:]
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.decode('utf-8')
        except (ValueError, KeyError, base64.binascii.Error) as e:
            return "Decryption failed"


    unhashed_token = ""
    crbrstoken = None


    # Function to create a JWT token
    def create_token(info):
        email, password = str(info).split(':')
        data = json.dumps({"username": email,
                           "password": password})
        global unhashed_token
        global akey
        unhashed_token = encrypt_data(data, akey)
        # print(f"created unhashed token: {unhashed_token}")
        # Correct way to create HMAC object
        '''hmac_obj = hmac.new(SECRET_KEY.encode(), unhashed_token.encode(), hashlib.sha256)
        hmac_digest = hmac_obj.hexdigest()
        encoded_token = base64.urlsafe_b64encode(hmac_digest.encode()).decode()
        print(f"created hashed token: {encoded_token}")'''

        return unhashed_token


    @app.route('/')
    def home():
        return "Welcome to the Aoi Tidal API"

    @app.route('/get_log', methods=['GET'])
    def get_log_req():
        return jsonify(ConsoleLogger.log_array)

    @app.route('/save_settings', methods=['POST'])
    @require_token
    def save_settings():
        try:
            settings_data = request.json
            global settings_capsolver_api_key
            settings_capsolver_api_key = settings_data.get('apiKey')
            settings_file_path = os.path.join(project_dir, 'Files', 'settings.json')
            with open(settings_file_path, 'w') as settings_file:
                json.dump(settings_data, settings_file, indent=4)

            return jsonify({"message": "Settings saved successfully"}), 200

        except Exception as e:
            return jsonify({"error": f"Failed to save settings: {str(e)}"}), 500


    @app.route('/load_settings', methods=['GET'])
    @require_token
    def load_settings():
        try:
            settings_file_path = os.path.join(project_dir, 'Files', 'settings.json')
            if os.path.exists(settings_file_path):
                with open(settings_file_path, 'r') as settings_file:
                    settings_data = json.load(settings_file)
                    global settings_capsolver_api_key
                    settings_capsolver_api_key = settings_data.get('apiKey')
                return jsonify(settings_data), 200
            else:
                return jsonify({"error": "Settings file not found"}), 404

        except Exception as e:
            return jsonify({"error": f"Failed to load settings: {str(e)}"}), 500


    @app.route('/check_cred', methods=['POST'])
    def check_cred():
        try:
            credentials_file = os.path.join(project_dir, 'Files', 'credentials.json')

            if Path(credentials_file).is_file():
                # print(credentials_file + " is true")
                with open(credentials_file, 'r') as f:
                    credentials_object = json.load(f)

                username = credentials_object.get("username")
                password = credentials_object.get("password")

                if username and password:
                    token = create_token(username + ":" + password)
                    return jsonify({"success": True, "message": "Successfully logged in!", "token": token}), 200
                else:
                    # print("returning  not logged in 2")
                    return jsonify({"success": False, "message": "Invalid credentials in the file"}), 400
            else:
                return jsonify({"success": False, "message": "Credentials file not found"}), 404
        except Exception as e:
            # Log the exception instead of printing
            # print(str(e))
            return jsonify({"success": False, "message": "Internal server error"}), 500


    @app.route('/register', methods=['POST'])
    def register():
        username = request.json.get('username')
        password = request.json.get('password')
        if not username or not password:
            return jsonify({"success": False, "message": "Username and password required"}), 400
        token = create_token(username + ":" + password)
        return jsonify({"success": True, "message": "Successfully Registered!", "token": token})


    @app.route('/login', methods=['POST'])
    def login():
        username = request.json.get('username')
        password = request.json.get('password')
        stayloggedin = request.json.get('stayloggedin')
        if str(stayloggedin).lower().__contains__("true"):
            creds = {
                "username": username,
                "password": password
            }
            creds_obj = json.dumps(creds, indent=2)
            json_path = os.path.join(project_dir, 'Files', 'credentials.json')
            with open(json_path, "w") as outfile:
                outfile.write(creds_obj)
        token = create_token(username + ":" + password)
        return jsonify({"success": True, "message": "Successfully logged in!", "token": token})


    @app.route('/check_token', methods=['POST'])
    def check_token():
        # Get the token from the request
        auth_token = request.headers.get('Authorization')

        if not auth_token:
            return jsonify({"message": "Unauthorized"}), 401

        if verify_token(auth_token):
            return jsonify({"message": "Token is valid"}), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401


    @app.route('/delete_batch', methods=['POST'])
    @require_token
    def delete_batch():
        batch_data = request.json
        batch_type = batch_data.get('type')
        batch_id = batch_data.get('id')

        if not batch_type or not batch_id:
            return jsonify({"error": "Batch type and id are required"}), 400

        batch = Batch.query.filter_by(id=batch_id, type=batch_type).first()
        if batch:
            db.session.delete(batch)
            db.session.commit()
            return jsonify({"message": f"Batch {batch_id} deleted successfully"}), 200
        else:
            return jsonify({"error": "Batch not found"}), 404


    @app.route('/update_batch', methods=['POST'])
    @require_token
    def update_batch():
        batch_data = request.json
        batch_type = batch_data.get('type')
        batch_id = batch_data.get('id')
        batch_name = batch_data.get('name')
        batch_content = batch_data.get('content')

        if not batch_type or not batch_id or not batch_name or not batch_content:
            return jsonify({"error": "Batch type, id, name, and content are required"}), 400

        batch = Batch.query.filter_by(id=batch_id, type=batch_type).first()
        if batch:
            batch.name = batch_name
            batch.content = batch_content
        else:
            batch = Batch(id=batch_id, type=batch_type, name=batch_name, content=batch_content)
            db.session.add(batch)
        db.session.commit()

        return jsonify({"message": f"Batch {batch_name} updated successfully"}), 200


    @app.route('/add_batch', methods=['POST'])
    @require_token
    def add_batch():
        batch_data = request.json
        batch_type = batch_data.get('type')
        batch_name = batch_data.get('name')
        batch_content = batch_data.get('content')

        if not batch_type or not batch_name or not batch_content:
            return jsonify({"error": "Batch type, name, and content are required"}), 400

        batch_id = str(uuid.uuid4())
        batch = Batch(id=batch_id, type=batch_type, name=batch_name, content=batch_content)
        db.session.add(batch)
        db.session.commit()

        return jsonify({"message": f"Batch {batch_name} added successfully", "id": batch_id}), 201


    @app.route('/get_batches', methods=['GET'])
    @require_token
    def get_batches():
        batch_type = request.args.get('type')
        if not batch_type:
            return jsonify({"error": "Batch type is required"}), 400

        batches = Batch.query.filter_by(type=batch_type).all()
        batch_list = [{"type": batch.type, "id": batch.id, "name": batch.name, "content": batch.content} for batch in batches]

        return jsonify({"batches": batch_list})


    @app.route('/logout_all_accounts', methods=['POST'])
    @require_token
    def logout_all_accounts():
        global used_accounts
        with used_accounts_lock:
            used_accounts.clear()
        try:
            sessions_dir = os.path.join(project_dir, 'Files', 'Sessions')
            if os.path.exists(sessions_dir):
                for item in os.listdir(sessions_dir):
                    item_path = os.path.join(sessions_dir, item)
                    try:
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                    except Exception:
                        pass
        except Exception:
            pass
        return jsonify({"message": "All accounts logged out successfully"})


    @app.route('/run_optimizer', methods=['POST'])
    @require_token
    def run_optimizer():
        import subprocess
        ps_commands = [
            'Write-Host "Limpiando cache de memoria..."',
            'Write-Host "Optimizando memoria..."',
            'Write-Host "Cerrando procesos que consumen mucha RAM..."',
            'Get-Process | Where-Object { $_.WorkingSet64 -gt 500MB -and $_.ProcessName -notmatch "^(System|Idle|svchost|csrss|winlogon|services|lsass|spoolsv|conhost|RuntimeBroker|ShellExperienceHost|SearchIndexer|SearchUI|sihost|taskhostw)$" } | ForEach-Object { Write-Host "  Cerrando $($_.ProcessName) ($( [math]::Round($_.WorkingSet64/1MB) ) MB)"; Stop-Process $_.Id -Force -ErrorAction SilentlyContinue }',
            'Write-Host "Optimizando prioridad de procesos..."',
            'Write-Host "Eliminando archivos temporales del usuario..."',
            r'Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Write-Host "Eliminando archivos temporales del sistema..."',
            r'Remove-Item -Path "$env:SystemRoot\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Write-Host "Eliminando archivos TIDAL de usuarios..."',
            r'Remove-Item -Path "$env:LOCALAPPDATA\TIDAL\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Write-Host "Eliminando archivos Temp Adicionales de Navegacion..."',
            r'Remove-Item -Path "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache\*" -Recurse -Force -ErrorAction SilentlyContinue',
            r'Remove-Item -Path "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache\*" -Recurse -Force -ErrorAction SilentlyContinue',
            r'Remove-Item -Path "$env:LOCALAPPDATA\BraveSoftware\*\User Data\Default\Cache\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Write-Host "Limpiando cache de Windows Update..."',
            'Stop-Service wuauserv -Force -ErrorAction SilentlyContinue; ' + r'Remove-Item -Path "$env:SystemRoot\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue; ' + 'Start-Service wuauserv -ErrorAction SilentlyContinue',
            'Write-Host "Limpiando cache de DNS..."',
            'ipconfig /flushdns',
            'Write-Host "Vaciando la Papelera de Reciclaje..."',
            'Clear-RecycleBin -Force -ErrorAction SilentlyContinue',
            'Write-Host "Optimizando el disco..."',
            'Write-Host "Limpiando cache de iconos..."',
            'ie4uinit.exe -ClearIconCache -ErrorAction SilentlyContinue',
            'Write-Host "=============================="',
            'Write-Host "Optimizacion completada. El equipo esta mas eficiente."',
            'Write-Host "=============================="',
        ]
        script = "; ".join(ps_commands)
        try:
            result = subprocess.run(
                ["powershell", "-Command", script],
                capture_output=True, text=True, timeout=120
            )
            output = result.stdout + result.stderr
            return jsonify({"message": "Optimizacion completada", "output": output})
        except subprocess.TimeoutExpired:
            return jsonify({"message": "Optimizacion timeout", "output": ""})
        except Exception as e:
            return jsonify({"message": f"Error: {e}", "output": ""}), 500


    @app.route('/save_config', methods=['POST'])
    @require_token
    def save_config():
        config_data = request.json
        config_name = config_data.get("config_name")
        if not config_name:
            return jsonify({"error": "Config name is required"}), 400

        config_path = os.path.join(project_dir, 'Files', 'Configs', f'{config_name}.json')
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)

        return jsonify({"message": f"Config {config_name} saved successfully"}), 201


    def stop_thread(thread_number):
        # Signal the thread to stop
        stop_flags[thread_number] = True

        # Wait for the thread to stop
        if thread_number in worker_threads:
            worker_threads[thread_number]["thread"].join()

        # Clean up thread resources
        if thread_number in worker_threads:
            worker_threads.pop(thread_number, None)
        global worker_threads_running
        worker_threads_running -= 1
        stop_flags.pop(thread_number, None)


    @app.route('/restart_thread', methods=['POST'])
    @require_token
    def restart_thread():
        data = request.json
        thread_number = data.get('thread_number')
        # Retrieve the port used by the thread
        port = int(data.get('port'))

        if not thread_number:
            return jsonify({"message": "Thread number is required"}), 400

        update_thread_status(thread_number, 'Restarting', None, False, False, True, False, True, None)
        # Stop the existing thread
        if thread_number in worker_threads:
            stop_thread(thread_number)

        kill_tidal_process(tidal_instance)

        worker_thread = threading.Thread(target=thread_function, args=(thread_number, port,))
        worker_threads[thread_number] = {
            "thread": worker_thread,
            "status": "Starting",
            "proxy": "/",
            "logins": 0,
            "streams": 0,
            "likes": 0,
            "follows": 0,
            "errors": 0,
            "controls": "restart",
            "port": port,
            "pid": "/"
        }
        worker_thread.start()

        return jsonify({"message": f"Thread {thread_number} restarted successfully"}), 200


    @app.route('/view_thread', methods=['POST'])
    @require_token
    def view_thread():
        data = request.json
        port = data.get('pid')

        if not port:
            return jsonify({"message": "Port is required"}), 400

        try:
            executable_path = os.path.join(project_dir, 'Files', 'manage.exe')
            command = [executable_path, '--port', str(port), '--action', 'show']  # Add the action argument as needed

            # Use subprocess to call the executable
            subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)

            return jsonify({"message": "ok"}), 200
        except Exception as e:
            return jsonify({"message": f"Error bringing browser window to foreground: {e}"}), 500


    @app.route('/start_bot', methods=['POST'])
    @require_token
    def start_stop_bot():
        print('got start bot request')
        global worker_bot_running
        if worker_bot_running is False:
            try:
                data = request.json
                config_name = data.get('config_name')
                if not config_name:
                    return jsonify({"message": "Config name is required"}), 400

                config_path = os.path.join(os.path.join(project_dir, 'Files', 'Configs'), f"{config_name}.json")
                if not os.path.exists(config_path):
                    ConsoleLogger.log_array.append(f"Config {config_name} not found")
                    return jsonify({"message": f"Config {config_name} not found"}), 404

                with open(config_path, 'r') as config_file:
                    config_data = json.load(config_file)

                global config_threads_to_start
                global config_thread_start_delay
                global config_optimize_tidal_app
                global config_streams_to_do
                global config_album_likes_rate
                global config_song_likes_rate
                global config_follows_rate
                global config_playtime_type
                global config_playtime_seconds
                global config_playtime_percentage
                global config_use_proxies
                global config_use_dual_proxies
                global config_proxyless_login
                global config_links_batch_id
                global config_proxies_batch_id
                global config_login_proxies_batch_id
                global config_streaming_proxies_batch_id
                global config_ppa
                global config_stay_logged_in
                global config_accounts_batch_id
                global config_use_webhook
                global config_webhook_name
                global config_webhook_url
                global config_webhook_interval
                global config_shuffle_perc  # Add this line
                global config_search_links_perc
                global config_hide_tidal_app
                global config_mute_tidal_app
                global config_streaming_quality_to_low

                config_threads_to_start = int(config_data.get('threads_to_start'))
                config_thread_start_delay = int(config_data.get('thread_start_delay', 30))
                config_optimize_tidal_app = config_data.get('optimize_tidal_app')
                config_streams_to_do = int(config_data.get('streams_to_do'))
                config_album_likes_rate = int(config_data.get('album_likes_rate', 0))
                config_song_likes_rate = int(config_data.get('song_likes_rate', 0))
                config_follows_rate = int(config_data.get('follows_rate', 0))
                config_playtime_type = config_data.get('playtime_type')
                config_playtime_seconds = config_data.get('playtime_seconds')
                config_playtime_percentage = config_data.get('playtime_percentage')
                config_use_proxies = str(config_data.get('use_proxies'))
                config_use_dual_proxies = str(config_data.get('use_dual_proxies', 'false'))
                config_proxyless_login = str(config_data.get('proxyless_login', 'false'))
                config_links_batch_id = config_data.get('links_batch_id')
                config_proxies_batch_id = config_data.get('proxies_batch_id')
                config_login_proxies_batch_id = config_data.get('login_proxies_batch_id', '')
                config_streaming_proxies_batch_id = config_data.get('streaming_proxies_batch_id', '')
                config_accounts_batch_id = config_data.get('accounts_batch_id')
                config_ppa = config_data.get('ppa')
                config_stay_logged_in = config_data.get('stay_logged_in')
                config_shuffle_perc = int(config_data.get('shuffle_perc'))  # Add this line
                config_search_links_perc = int(config_data.get('search_links_perc'))

                config_hide_tidal_app = str(config_data.get('config_hide_tidal_app'))
                config_mute_tidal_app = str(config_data.get('config_mute_tidal_app'))
                config_streaming_quality_to_low = str(config_data.get('streaming_quality_to_low', 'false'))

                webhook_config = config_data.get('webhook', {})
                config_use_webhook = str(webhook_config.get('use'))
                config_webhook_name = webhook_config.get('name')
                config_webhook_url = webhook_config.get('url')
                config_webhook_interval = webhook_config.get('interval')

                global worker_loaded_accounts
                global worker_loaded_proxies
                global worker_loaded_login_proxies
                global worker_loaded_streaming_proxies
                global worker_loaded_link

                with app.app_context():
                    batch = Batch.query.filter_by(id=config_accounts_batch_id, type='accounts').first()
                    if not batch:
                        ConsoleLogger.log_array.append("Account batch not found")
                        raise Exception("Account batch not found")
                    accounts = batch.content.splitlines()
                    available_accounts = [account for account in accounts if account not in used_accounts]
                    if not available_accounts:
                        ConsoleLogger.log_array.append('No available accounts left.')
                        raise Exception("No available accounts left.")
                    worker_loaded_accounts = available_accounts
                
                # Initialize global account manager
                global global_account_manager
                global_account_manager = AccountManager(project_dir)
                ConsoleLogger.log_array.append(f"Loaded {len(worker_loaded_accounts)} accounts")

                if config_use_proxies.lower().__contains__('true'):
                    with app.app_context():
                        batch = Batch.query.filter_by(id=config_proxies_batch_id, type='proxies').first()
                        if not batch:
                            ConsoleLogger.log_array.append("Proxy batch not found")
                            raise Exception("Proxy batch not found")
                        proxies = batch.content.splitlines()
                        worker_loaded_proxies = proxies

                # Load dual proxies (login + streaming) if enabled
                if config_use_dual_proxies.lower().__contains__('true'):
                    with app.app_context():
                        # Load login proxies (residential)
                        login_batch = Batch.query.filter_by(id=config_login_proxies_batch_id, type='proxies').first()
                        if not login_batch:
                            ConsoleLogger.log_array.append("Login proxy batch not found")
                            raise Exception("Login proxy batch not found")
                        worker_loaded_login_proxies = login_batch.content.splitlines()
                        ConsoleLogger.log_array.append(f"Loaded {len(worker_loaded_login_proxies)} login proxies")

                        # Load streaming proxies (datacenter)
                        streaming_batch = Batch.query.filter_by(id=config_streaming_proxies_batch_id, type='proxies').first()
                        if not streaming_batch:
                            ConsoleLogger.log_array.append("Streaming proxy batch not found")
                            raise Exception("Streaming proxy batch not found")
                        worker_loaded_streaming_proxies = streaming_batch.content.splitlines()
                        ConsoleLogger.log_array.append(f"Loaded {len(worker_loaded_streaming_proxies)} streaming proxies")

                # Load streaming proxies for proxyless login mode (login without proxy, then use streaming proxy)
                if config_proxyless_login.lower().__contains__('true'):
                    with app.app_context():
                        # Load streaming proxies (datacenter)
                        streaming_batch = Batch.query.filter_by(id=config_streaming_proxies_batch_id, type='proxies').first()
                        if not streaming_batch:
                            ConsoleLogger.log_array.append("Streaming proxy batch not found for proxyless login mode")
                            raise Exception("Streaming proxy batch not found")
                        worker_loaded_streaming_proxies = streaming_batch.content.splitlines()
                        ConsoleLogger.log_array.append(f"Loaded {len(worker_loaded_streaming_proxies)} streaming proxies for proxyless login")

                with app.app_context():
                    batch = Batch.query.filter_by(id=config_links_batch_id, type='links').first()
                    if not batch:
                        ConsoleLogger.log_array.append("Link batch not found")
                        raise Exception("Link batch not found")
                    links = batch.content.splitlines()
                    worker_loaded_link = links

                if config_use_webhook == 'True':
                    webhook_thread = threading.Thread(target=send_discord_webhook,
                                                      args=(int(config_webhook_interval), config_webhook_url))
                    webhook_thread.daemon = True
                    webhook_thread.start()

                worker_bot_running = True
                bot_thread = threading.Thread(target=main_function, args=(config_data,))
                bot_thread.start()
                return jsonify({"message": f"Bot started with config {config_name}"}), 200
            except Exception as e:
                return jsonify({"message": f"Failed to load config: {e}"}), 400

        else:
            for thread_number in list(worker_threads.keys()):
                stop_flags[thread_number] = True

                # Attempt to stop all threads
            for thread_info in worker_threads.values():
                thread = thread_info["thread"]
                if thread.is_alive():
                    try:
                        thread._stop()
                    except Exception as e:
                        print(f"Error stopping thread: {e}")

                # Clear worker threads
            worker_threads.clear()
            worker_threads.clear()
            worker_bot_running = False
            ConsoleLogger.log_array.clear()
            ConsoleLogger.log_array.append('Aoi Tidal 1.0.0 - [Console Logs]')
            ConsoleLogger.log_array.append('<---------------------------------------->')
            ConsoleLogger.log_array.append(' ')
            return jsonify({"message": f"Bot stopped"}), 200


    @app.route('/get_worker_threads', methods=['GET'])
    @require_token
    def get_worker_threads():
        global worker_threads
        worker_threads_serializable = {
            key: {
                "thread_number": key,  # Include the thread number
                "status": value["status"],
                "proxy": value["proxy"],
                "logins": value["logins"],
                "streams": value["streams"],
                "likes": value["likes"],
                "follows": value["follows"],
                "errors": value["errors"],
                "controls": value["controls"],
                "pid": value["pid"],
                "port": value["port"]
            }
            for key, value in worker_threads.items()
        }
        return jsonify(list(worker_threads_serializable.values()))


    @app.route('/get_worker_stats', methods=['GET'])
    @require_token
    def get_worker_stats():
        global worker_streams_done
        global worker_threads_running
        global worker_successful_logins
        global worker_unsuccessful_logins
        global worker_song_likes
        global worker_album_likes
        global worker_follows_done
        global worker_proxy_errors
        global worker_bot_errors
        return jsonify({
            "worker_streams_done": worker_streams_done,
            "worker_threads_running": worker_threads_running,
            "worker_successful_logins": worker_successful_logins,
            "worker_unsuccessful_logins": worker_unsuccessful_logins,
            "worker_song_likes": worker_song_likes,
            "worker_album_likes": worker_album_likes,
            "worker_follows_done": worker_follows_done,
            "worker_proxy_errors": worker_proxy_errors,
            "worker_bot_errors": worker_bot_errors
        })

    @app.route('/get_config', methods=['GET'])
    @require_token
    def get_config():
        config_name = request.args.get('name')
        config_path = os.path.join(project_dir, 'Files', 'Configs', f'{config_name}.json')

        if not os.path.exists(config_path):
            return jsonify({"error": "Config not found"}), 404

        with open(config_path, 'r') as file:
            config_data = json.load(file)

        return jsonify(config_data)

    @app.route('/get_configs', methods=['GET'])
    @require_token
    def get_configs():
        config_path = os.path.join(project_dir, 'Files', 'Configs')
        configs = [f.split('.')[0] for f in os.listdir(config_path) if f.endswith('.json')]
        return jsonify({"configs": configs})


    @app.route('/get_streams_done', methods=['GET'])
    @require_token
    def get_streams_done():
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        if not start_date_str or not end_date_str:
            return jsonify({"error": "Start date and end date are required"}), 400

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        streams = StreamRecord.query.filter(StreamRecord.timestamp >= start_date,
                                            StreamRecord.timestamp <= end_date).all()
        streams_list = [
            {"timestamp": stream.timestamp.strftime('%Y-%m-%d %H:%M:%S'), "streams_done": stream.streams_done} for
            stream in streams]

        return jsonify({"streams": streams_list})


    def get_time():
        t = time.localtime()
        return time.strftime("%H:%M:%S", t)


    COLORS = {
        "white": Fore.WHITE,
        "magenta": Fore.MAGENTA,
        "light_green": Fore.LIGHTGREEN_EX,
        "dark_green": Fore.GREEN,
        "green": Fore.GREEN,
        "light_red": Fore.LIGHTRED_EX,
        "dark_red": Fore.RED,
        "red": Fore.RED,
        "yellow": Fore.YELLOW,
        "blue": Fore.LIGHTBLUE_EX,
        "gray": Fore.LIGHTBLACK_EX,
    }


    def print_log(type, color, thread, message):
        current_time = datetime.now().strftime("[%H:%M:%S]")
        color_code = COLORS.get(color.lower(), Fore.WHITE)
        if thread is None or thread == "Main":
            thread_str = "Main"
        else:
            thread_str = f"{thread:03d}"
        add_log(type, thread_str, message)
        #print(f"{current_time}|Thread {thread_str} {color_code} [{type}] {Fore.WHITE} - {message}")


    def send_discord_webhook(interval, url):
        while True:
            try:
                global previous_streams_per_month
                global current_streams_per_month
                global worker_threads_running
                global worker_successful_logins
                global worker_unsuccessful_logins
                global worker_streams_done
                global worker_song_likes
                global worker_album_likes
                global worker_follows_done
                global worker_bot_errors
                cpu_usage = psutil.cpu_percent(1)
                ram_usage = psutil.virtual_memory()[2]
                elapsed_time = time.time() - start_time
                streams_per_second = worker_streams_done / elapsed_time if elapsed_time > 0 else 0
                streams_per_hour = streams_per_second * 3600
                streams_per_day = streams_per_hour * 24
                streams_per_month = streams_per_day * 30

                if previous_streams_per_month is not None:
                    if streams_per_month > previous_streams_per_month:
                        trend_emoji = "📈"  # Up
                    elif streams_per_month < previous_streams_per_month:
                        trend_emoji = "📉"  # Down
                    else:
                        trend_emoji = "⚖️"  # Steady
                else:
                    trend_emoji = "🔄"  # Initial value

                previous_streams_per_month = current_streams_per_month
                current_streams_per_month = streams_per_month

                payload = {
                    "content": "",
                    "tts": False,
                    "embeds": [
                        {
                            "id": 10674342,
                            "description": f"**Machine Name:** {config_webhook_name} \n[CPU: {cpu_usage}% | RAM {ram_usage}%]",
                            "color": 6313836,
                            "fields": [
                                {
                                    "id": 564153579,
                                    "name": "Threads running:",
                                    "value": str(worker_threads_running),
                                    "inline": True
                                },
                                {
                                    "id": 445057359,
                                    "name": "Successful Logins:",
                                    "value": str(worker_successful_logins),
                                    "inline": True
                                },
                                {
                                    "id": 955958044,
                                    "name": "Unsuccessful Logins:",
                                    "value": str(worker_unsuccessful_logins),
                                    "inline": True
                                },
                                {
                                    "id": 53898218,
                                    "name": "Streams:",
                                    "value": str(worker_streams_done),
                                    "inline": True
                                },
                                {
                                    "id": 711494525,
                                    "name": "Song Likes:",
                                    "value": str(worker_song_likes),
                                    "inline": True
                                },
                                {
                                    "id": 970976981,
                                    "name": "Album Likes:",
                                    "value": str(worker_album_likes),
                                    "inline": True
                                },
                                {
                                    "id": 513764591,
                                    "name": "Followers:",
                                    "value": str(worker_follows_done),
                                    "inline": True
                                },
                                {
                                    "id": 17774328,
                                    "name": "Errors:",
                                    "value": str(worker_bot_errors),
                                    "inline": True
                                },
                                {
                                    "id": 970976989,
                                    "name": "Time running:",
                                    "value": get_running_time(),
                                    "inline": True
                                },
                                {
                                    "id": 7793137,
                                    "name": "Streams Per Hour:",
                                    "value": f"{streams_per_hour:,.0f}".replace(',', '.'),
                                    "inline": True
                                },
                                {
                                    "id": 7793138,
                                    "name": "Streams Per Day:",
                                    "value": f"{streams_per_day:,.0f}".replace(',', '.'),
                                    "inline": True
                                },
                                {
                                    "id": 7793139,
                                    "name": "Streams Per Month:",
                                    "value": f"{streams_per_month:,.0f}".replace(',', '.'),
                                    "inline": True
                                },
                                {
                                    "id": "stream_trend",
                                    "name": "Streaming Trend",
                                    "value": trend_emoji,
                                    "inline": True
                                }
                            ],
                            "image": {
                                "url": "https://i.ibb.co/pv5DVpQ/statswebhook.png"
                            },
                            "footer": {
                                "text": "Aoi | Tidal v1.0.0"
                            }
                        }
                    ],
                    "components": [],
                    "actions": {},
                    "username": "Aoi Tidal",
                    "avatar_url": ""
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                requests.post(url, headers=headers, data=json.dumps(payload))
                time.sleep(interval * 60)  # Convert interval from minutes to seconds
            except:
                pass

    def patch_chromedriver(executable_path=None):
        """Patches the ChromeDriver binary to make it undetectable.

        Args:
            executable_path: A full file path to the chromedriver executable.
                             If None, it will default to 'chromedriver.exe' in the current directory.

        Returns:
            bool: True if the patching was successful, False otherwise.
        """
        exe_name = "chromedriver.exe"
        executable_path = executable_path or os.path.join(os.getcwd(), exe_name)

        def gen_random_cdc():
            cdc = random.choices(string.ascii_lowercase, k=26)
            cdc[-6:-4] = map(str.upper, cdc[-6:-4])
            cdc[2] = cdc[0]
            cdc[3] = "_"
            return "".join(cdc).encode()

        def is_binary_patched(executable_path):
            with io.open(executable_path, "rb") as fh:
                if re.search(
                        b"window.cdc_adoQpoasnfa76pfcZLmcfl_"
                        b"(Array|Promise|Symbol|Object|Proxy|JSON)",
                        fh.read()
                ):
                    return False
            return True

        def patch_exe(executable_path):
            """Patches the ChromeDriver binary"""
            def gen_js_whitespaces(match):
                return b"\n" * len(match.group())

            def gen_call_function_js_cache_name(match):
                rep_len = len(match.group()) - 3
                ran_len = random.randint(6, rep_len)
                bb = b"'" + bytes(str().join(random.choices(
                    population=string.ascii_letters, k=ran_len
                )), 'ascii') + b"';" + (b"\n" * (rep_len - ran_len))
                return bb

            with io.open(executable_path, "r+b") as fh:
                file_bin = fh.read()
                file_bin = re.sub(
                    b"window\\.cdc_[a-zA-Z0-9]{22}_"
                    b"(Array|Promise|Symbol|Object|Proxy|JSON)"
                    b" = window\\.(Array|Promise|Symbol|Object|Proxy|JSON);",
                    gen_js_whitespaces,
                    file_bin,
                )
                file_bin = re.sub(
                    b"window\\.cdc_[a-zA-Z0-9]{22}_"
                    b"(Array|Promise|Symbol|Object|Proxy|JSON) \\|\\|",
                    gen_js_whitespaces,
                    file_bin,
                )
                file_bin = re.sub(
                    b"'\\$cdc_[a-zA-Z0-9]{22}_';",
                    gen_call_function_js_cache_name,
                    file_bin,
                )
                fh.seek(0)
                fh.write(file_bin)
            return True

        if not os.path.exists(executable_path):
            raise FileNotFoundError(f"ChromeDriver not found at {executable_path}")

        if is_binary_patched(executable_path):
            return patch_exe(executable_path)
        else:
            return False
    def update_thread_status(thread_number, status=None, proxy=None, increment_logins=False, increment_streams=False,
                             increment_likes=False, increment_follows=False, increment_errors=False, pid=None):
        global worker_threads
        global worker_successful_logins
        global worker_streams_done
        global worker_song_likes
        global worker_follows_done
        global worker_bot_errors
        if thread_number in worker_threads:
            thread = worker_threads[thread_number]
            if status:
                thread["status"] = status
            if proxy:
                thread["proxy"] = proxy
            if increment_logins:
                thread["logins"] += 1
            if increment_streams:
                thread["streams"] += 1
            if increment_likes:
                thread["likes"] += 1
            if increment_follows:
                thread["follows"] += 1
            if increment_errors:
                thread["errors"] += 1
            if pid:
                thread["pid"] = pid





    def check_http_https(proxy):
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        url = "https://ipinfo.io/ip"
        try:
            response = requests.get(url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                return "HTTP/HTTPS", "Working"
            else:
                return None, f"Failed with status code {response.status_code}"
        except requests.exceptions.ProxyError as e:
            return None, "Proxy error: Possibly wrong credentials or unauthorized IP"
        except requests.exceptions.RequestException as e:
            return None, f"Request error: {str(e)}"
        return None, "Unknown error"


    def check_socks5(proxy_ip, proxy_port, username=None, password=None):
        if username and password:
            proxy_url = f"socks5://{username}:{password}@{proxy_ip}:{proxy_port}"
        else:
            proxy_url = f"socks5://{proxy_ip}:{proxy_port}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        url = "http://ipinfo.io/ip"
        try:
            response = requests.get(url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                return "SOCKS5", "Working"
            else:
                return None, f"Failed with status code {response.status_code}"
        except ProxyError as e:
            if "authentication failed" in str(e):
                return None, "Authentication failed: Possibly wrong credentials"
            else:
                return None, f"Proxy error: {str(e)}"
        except RequestException as e:
            return None, f"Request error: {str(e)}"
        return None, "Unknown error"


    def determine_proxy_protocol(proxy):
        parts = proxy.split(":")
        if len(parts) == 2:
            proxy_ip, proxy_port = parts
            proxy_port = int(proxy_port)
            username = None
            password = None
            proxy_http_https = f"http://{proxy_ip}:{proxy_port}"
        elif len(parts) == 4:
            proxy_ip, proxy_port, username, password = parts
            proxy_port = int(proxy_port)
            proxy_http_https = f"http://{username}:{password}@{proxy_ip}:{proxy_port}"
        else:
            return "Invalid proxy format", "N/A"

        # Check HTTP/HTTPS

        protocol, status = check_http_https(proxy_http_https)

        if protocol:
            return protocol, status

        # Check SOCKS5
        protocol, status = check_socks5(proxy_ip, proxy_port, username, password)
        if protocol:
            return protocol, status

        return None, "Failed to determine protocol"


    def request_with_proxy(url, proxy, max_retries=3, delay=1, timeout=5):
        proxy_dict = {
            'http': proxy,
            'https': proxy
        }
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, proxies=proxy_dict, timeout=timeout)
                if response.status_code == 200:
                    return response
                last_error = f"Status code: {response.status_code}"
            except RequestException as e:
                last_error = str(e)[:100]  # Truncate long errors

            if attempt < max_retries:
                time.sleep(delay)
        # Optionally log the final error for debugging
        # print(f"[DEBUG] Proxy verification failed: {last_error}")
        return None


    def start_proxy_server(proxyline, protocol, proxy_server_port):
        def start_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        parts = proxyline.split(':')
        if len(parts) != 4:
            raise ValueError("Invalid proxy format. Must be ip:port:username:password")

        if protocol == "HTTP/HTTPS":
            formatted_proxy = f"http://{parts[0]}:{parts[1]}#{parts[2]}:{parts[3]}"
        elif protocol == "SOCKS5":
            formatted_proxy = f"socks5://{parts[0]}:{parts[1]}#{parts[2]}:{parts[3]}"
        else:
            return None, None, None

        # Check if port is available before trying to bind
        def is_port_available(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    s.bind(('127.0.0.1', port))
                    return True
                except OSError:
                    return False

        # Wait up to 5 seconds for port to become available
        for _ in range(10):
            if is_port_available(proxy_server_port):
                break
            time.sleep(0.5)
        else:
            # Port still not available after waiting
            return None, None, None

        try:
            remote_server = pproxy.Connection(formatted_proxy)
            server = pproxy.Server(f'http://:{proxy_server_port}')

            # Reset socket to original before creating the event loop
            socket.socket = original_socket
            proxy_asyncio_loop = asyncio.new_event_loop()
            proxy_server_thread = threading.Thread(target=start_loop, args=(proxy_asyncio_loop,), daemon=True)
            proxy_server_thread.start()

            # Schedule the server start and wait for it
            future = asyncio.run_coroutine_threadsafe(server.start_server({'rserver': [remote_server]}), proxy_asyncio_loop)
            try:
                # Wait up to 5 seconds for server to start
                future.result(timeout=5)
            except asyncio.TimeoutError:
                # Server is still starting, continue with verification
                pass
            except Exception as start_error:
                # Server failed to start (e.g., port in use)
                try:
                    proxy_asyncio_loop.call_soon_threadsafe(proxy_asyncio_loop.stop)
                    proxy_server_thread.join(timeout=2)
                except:
                    pass
                return None, None, None

            # Give the server a moment to fully initialize
            time.sleep(0.5)

            proxy = f"http://localhost:{proxy_server_port}"
            url = "http://ipinfo.io/ip"

            # Quick verification with reduced retries to avoid long hangs
            # 3 retries with 5 second timeout = max 18 seconds
            response = request_with_proxy(url, proxy, max_retries=3, delay=0.5)

            if response:
                return proxy_asyncio_loop, proxy_server_thread, proxy
            else:
                # Stop the proxy server and return None to signal failure
                try:
                    proxy_asyncio_loop.call_soon_threadsafe(proxy_asyncio_loop.stop)
                    proxy_server_thread.join(timeout=2)
                    # Give OS time to release the port
                    time.sleep(0.5)
                except Exception:
                    pass
                return None, None, None
        except Exception as e:
            # If anything fails during setup, clean up and return None
            try:
                if 'proxy_asyncio_loop' in dir() and proxy_asyncio_loop:
                    proxy_asyncio_loop.call_soon_threadsafe(proxy_asyncio_loop.stop)
                if 'proxy_server_thread' in dir() and proxy_server_thread:
                    proxy_server_thread.join(timeout=2)
                    time.sleep(0.5)
            except Exception:
                pass
            return None, None, None


    class DynamicProxyRelay:
        """
        A dynamic proxy relay that can switch between direct mode and upstream proxy mode
        without restarting. Tidal connects to this relay and never needs to restart.
        
        Uses a simple HTTP CONNECT proxy for direct mode, then pproxy for upstream mode.
        """
        def __init__(self, local_port):
            self.local_port = local_port
            self.loop = None
            self.thread = None
            self.server = None
            self.direct_server = None
            self.current_mode = None  # 'direct' or 'proxy'
            self.current_upstream = None
            self.lock = threading.Lock()

        def _start_loop(self, loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        def _stop_server(self):
            """Stop the current proxy server and clean up all pending tasks"""
            with self.lock:
                if self.loop is not None:
                    try:
                        # Create an async cleanup function
                        async def cleanup_async():
                            try:
                                # Close direct server if running
                                if self.direct_server is not None:
                                    self.direct_server.close()
                                    try:
                                        await self.direct_server.wait_closed()
                                    except:
                                        pass
                                
                                # Cancel all pending tasks
                                tasks = [t for t in asyncio.all_tasks(self.loop) 
                                        if t is not asyncio.current_task()]
                                for task in tasks:
                                    task.cancel()
                                
                                # Wait for all tasks to be cancelled
                                if tasks:
                                    await asyncio.gather(*tasks, return_exceptions=True)
                            except:
                                pass
                        
                        # Schedule cleanup
                        future = asyncio.run_coroutine_threadsafe(cleanup_async(), self.loop)
                        try:
                            future.result(timeout=3)  # Wait up to 3 seconds for cleanup
                        except:
                            pass
                        
                        # Now stop the loop
                        self.loop.call_soon_threadsafe(self.loop.stop)
                        
                        if self.thread:
                            self.thread.join(timeout=5)
                        
                        # Give some time for cleanup
                        time.sleep(0.2)
                        
                        try:
                            if not self.loop.is_closed():
                                self.loop.close()
                        except:
                            pass
                    except Exception as e:
                        pass
                    finally:
                        self.loop = None
                        self.thread = None
                        self.server = None
                        self.direct_server = None

        async def _handle_direct_client(self, reader, writer):
            """Handle a client connection in direct mode (transparent proxy)"""
            try:
                # Read the first line to get the request
                first_line = await asyncio.wait_for(reader.readline(), timeout=30)
                if not first_line:
                    writer.close()
                    return
                
                first_line_str = first_line.decode('utf-8', errors='ignore').strip()
                
                # Check if it's a CONNECT request (HTTPS)
                if first_line_str.startswith('CONNECT'):
                    # CONNECT host:port HTTP/1.1
                    parts = first_line_str.split()
                    if len(parts) >= 2:
                        host_port = parts[1]
                        if ':' in host_port:
                            host, port = host_port.rsplit(':', 1)
                            port = int(port)
                        else:
                            host = host_port
                            port = 443
                        
                        # Read headers until empty line
                        while True:
                            line = await asyncio.wait_for(reader.readline(), timeout=10)
                            if line == b'\r\n' or line == b'\n' or not line:
                                break
                        
                        # Connect to target
                        try:
                            target_reader, target_writer = await asyncio.wait_for(
                                asyncio.open_connection(host, port), timeout=30
                            )
                            # Send 200 Connection Established
                            writer.write(b'HTTP/1.1 200 Connection Established\r\n\r\n')
                            await writer.drain()
                            
                            # Relay data bidirectionally
                            await self._relay_data(reader, writer, target_reader, target_writer)
                        except Exception as e:
                            writer.write(b'HTTP/1.1 502 Bad Gateway\r\n\r\n')
                            await writer.drain()
                else:
                    # Regular HTTP request
                    # Parse the request line: GET http://host/path HTTP/1.1
                    parts = first_line_str.split()
                    if len(parts) >= 2:
                        method = parts[0]
                        url = parts[1]
                        
                        # Parse URL to get host
                        if url.startswith('http://'):
                            url = url[7:]
                            slash_idx = url.find('/')
                            if slash_idx != -1:
                                host_port = url[:slash_idx]
                                path = url[slash_idx:]
                            else:
                                host_port = url
                                path = '/'
                            
                            if ':' in host_port:
                                host, port = host_port.rsplit(':', 1)
                                port = int(port)
                            else:
                                host = host_port
                                port = 80
                            
                            # Read remaining headers
                            headers = []
                            while True:
                                line = await asyncio.wait_for(reader.readline(), timeout=10)
                                if line == b'\r\n' or line == b'\n' or not line:
                                    break
                                headers.append(line)
                            
                            # Connect to target and forward request
                            try:
                                target_reader, target_writer = await asyncio.wait_for(
                                    asyncio.open_connection(host, port), timeout=30
                                )
                                
                                # Send modified request (with path only, not full URL)
                                new_first_line = f"{method} {path} HTTP/1.1\r\n".encode()
                                target_writer.write(new_first_line)
                                for header in headers:
                                    target_writer.write(header)
                                target_writer.write(b'\r\n')
                                await target_writer.drain()
                                
                                # Relay response back
                                while True:
                                    data = await asyncio.wait_for(target_reader.read(8192), timeout=60)
                                    if not data:
                                        break
                                    writer.write(data)
                                    await writer.drain()
                                
                                target_writer.close()
                            except Exception as e:
                                writer.write(b'HTTP/1.1 502 Bad Gateway\r\n\r\n')
                                await writer.drain()
            except Exception as e:
                pass
            finally:
                try:
                    writer.close()
                except:
                    pass

        async def _relay_data(self, client_reader, client_writer, target_reader, target_writer):
            """Relay data between client and target bidirectionally"""
            async def forward(src, dst):
                try:
                    while True:
                        data = await asyncio.wait_for(src.read(8192), timeout=300)
                        if not data:
                            break
                        dst.write(data)
                        await dst.drain()
                except:
                    pass

            await asyncio.gather(
                forward(client_reader, target_writer),
                forward(target_reader, client_writer),
                return_exceptions=True
            )
            
            try:
                target_writer.close()
            except:
                pass

        async def _start_direct_server(self):
            """Start the direct proxy server"""
            self.direct_server = await asyncio.start_server(
                self._handle_direct_client,
                '127.0.0.1',
                self.local_port
            )

        def start_direct(self):
            """
            Start relay in direct mode (no upstream proxy).
            Tidal connects to this local proxy which passes requests directly to the internet.
            """
            self._stop_server()
            
            # Reset socket to original before creating the event loop
            socket.socket = original_socket
            self.loop = asyncio.new_event_loop()
            self.thread = threading.Thread(target=self._start_loop, args=(self.loop,))
            self.thread.start()

            # Start the direct proxy server
            asyncio.run_coroutine_threadsafe(self._start_direct_server(), self.loop)

            self.current_mode = 'direct'
            self.current_upstream = None
            
            # Wait a moment for server to start
            time.sleep(1)
            
            return f"http://localhost:{self.local_port}"

        def switch_to_proxy(self, proxyline, protocol):
            """
            Switch relay to route through an upstream proxy.
            Returns the upstream proxy info for logging.
            """
            self._stop_server()
            
            # Wait for port to be released
            time.sleep(1)
            
            # Parse proxy line
            parts = proxyline.split(':')
            if len(parts) == 4:
                # Format: host:port:user:pass
                if protocol == "HTTP/HTTPS":
                    formatted_proxy = f"http://{parts[0]}:{parts[1]}#{parts[2]}:{parts[3]}"
                elif protocol == "SOCKS5":
                    formatted_proxy = f"socks5://{parts[0]}:{parts[1]}#{parts[2]}:{parts[3]}"
                else:
                    raise ValueError(f"Unknown protocol: {protocol}")
            elif len(parts) == 2:
                # Format: host:port (no auth)
                formatted_proxy = f"http://{parts[0]}:{parts[1]}"
            else:
                raise ValueError("Invalid proxy format")

            # Reset socket to original before creating the event loop
            socket.socket = original_socket
            self.loop = asyncio.new_event_loop()
            self.thread = threading.Thread(target=self._start_loop, args=(self.loop,))
            self.thread.start()

            # Start server with upstream proxy
            remote_server = pproxy.Connection(formatted_proxy)
            self.server = pproxy.Server(f'http://:{self.local_port}')
            asyncio.run_coroutine_threadsafe(
                self.server.start_server({'rserver': [remote_server]}), 
                self.loop
            )

            self.current_mode = 'proxy'
            self.current_upstream = proxyline
            
            # Wait a moment and verify
            time.sleep(1)
            
            # Verify the proxy is working
            proxy_url = f"http://localhost:{self.local_port}"
            url = "http://ipinfo.io/ip"
            response = request_with_proxy(url, proxy_url, max_retries=3)
            
            if response:
                return True, response.text.strip()
            else:
                return False, None

        def stop(self):
            """Stop the relay completely"""
            self._stop_server()
            self.current_mode = None
            self.current_upstream = None

        def get_local_proxy(self):
            """Get the local proxy URL that Tidal should connect to"""
            return f"http://localhost:{self.local_port}"


    def find_widevine_folder():
        """
        Locate the WidevineCdm folder in the AppData/Roaming/TIDAL directory.

        Returns:
            str: Path to the WidevineCdm folder if found, or None if not found.
        """
        # Get the path for the Roaming AppData
        roaming_appdata_directory = os.getenv('APPDATA')

        if not roaming_appdata_directory:
            raise EnvironmentError("APPDATA environment variable is not set.")

        # Construct the expected path
        widevine_path = os.path.join(roaming_appdata_directory, 'TIDAL', 'WidevineCdm')

        # Check if the folder exists
        if os.path.exists(widevine_path):
            return widevine_path

        return None


    def find_tidal_exe(min_version="2.40.0"):
        local_appdata_directory = os.getenv('LOCALAPPDATA')
        roaming_appdata_directory = os.getenv('APPDATA')

        if not local_appdata_directory or not roaming_appdata_directory:
            raise EnvironmentError("AppData environment variables are not set.")

        potential_paths = [
            os.path.join(local_appdata_directory, 'TIDAL'),
            os.path.join(roaming_appdata_directory, 'TIDAL')
        ]

        '''# Force check for version 2.38.6 first
        forced_version = "2.38.6"
        for base_path in potential_paths:
            if os.path.exists(base_path):
                forced_path = os.path.join(base_path, f'app-{forced_version}', 'TIDAL.exe')
                if os.path.isfile(forced_path):
                    print(f"Found forced Tidal version: {forced_version}")
                    return forced_path'''

        latest_exe = None
        latest_version = None

        for base_path in potential_paths:
            if os.path.exists(base_path):
                for root, dirs, files in os.walk(base_path):
                    for dir_name in dirs:
                        if dir_name.startswith('app-'):
                            folder_version = dir_name[4:]
                            full_version_path = os.path.join(root, dir_name, 'TIDAL.exe')

                            if os.path.isfile(full_version_path):
                                if version.parse(folder_version) >= version.parse(min_version):
                                    if (latest_version is None or
                                            version.parse(folder_version) > version.parse(latest_version)):
                                        latest_version = folder_version
                                        latest_exe = full_version_path
        print(f"Latest Tidal executable: {latest_exe}")
        print(f"Latest Tidal version: {latest_version}")
        return latest_exe

    def compare_versions(current_version, target_version):
        """
        Compare two version strings to check if the current version is below the target version.
        """
        current_version_parts = list(map(int, current_version.split('.')))
        target_version_parts = list(map(int, target_version.split('.')))

        # Compare each part of the version
        for curr, target in zip(current_version_parts, target_version_parts):
            if curr < target:
                return True
            elif curr > target:
                return False

        # If all parts are equal, then current_version is not below target_version
        return False


    def download_tidal_exe():
        url = "https://download.tidal.com/desktop/TIDALSetup.exe"
        #url = ""
        filename = "TIDALSetup.exe"
        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)

        # Run the executable
        subprocess.run([filename], check=True)


    def ensure_chromedriver(url, target_dir):
        chromedriver_path = os.path.join(target_dir, 'chromedriver.exe')

        def get_chromedriver_version(chromedriver_path):
            try:
                # Run chromedriver and capture the output
                output = subprocess.check_output([chromedriver_path, '--version'], stderr=subprocess.STDOUT).decode('utf-8')
                # Extract version number from the output
                version_line = output.splitlines()[0]
                # Assuming version format like: "ChromeDriver 122.0.6261.94 (commit...)"
                version = version_line.split()[1]
                return version
            except Exception as e:
                print_log('ERROR', 'red', 'Main', f"Failed to get ChromeDriver version: {e}")
                return None

        # Check if chromedriver.exe already exists
        if os.path.isfile(chromedriver_path):
            installed_version = get_chromedriver_version(chromedriver_path)
            target_version = url.split('/')[-3]
            if installed_version != target_version:
                print_log('INFO', 'blue', 'Main', f"Installed ChromeDriver version {installed_version} is outdated (target: {target_version}), redownloading...")
                try:
                    os.remove(chromedriver_path)  # Remove the outdated version
                except OSError:
                    pass
            else:
                print_log('INFO', 'blue', 'Main', f"Found ChromeDriver version {installed_version}, no need to redownload.")
                return

        # Proceed to download if chromedriver doesn't exist or is outdated
        print_log('INFO', 'blue', 'Main', "Chromedriver not found or outdated, downloading and extracting...")
        # Download the zip file
        response = requests.get(url)
        zip_filename = os.path.join(target_dir, 'chromedriver.zip')
        with open(zip_filename, 'wb') as file:
            file.write(response.content)

        # Extract the zip file
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(target_dir)

        # Move chromedriver.exe to the desired directory
        extracted_dir = os.path.join(target_dir, 'chromedriver-win64')
        shutil.move(os.path.join(extracted_dir, 'chromedriver.exe'), target_dir)

        # Clean up the extracted folder and zip file
        os.remove(zip_filename)
        shutil.rmtree(extracted_dir)

        print_log('INFO', 'blue', 'Main', 'Chromedriver downloaded and extracted successfully.')


    def force_delete_sessions():
        session_folder = os.path.join(project_dir, 'Files', 'Sessions')

        if not os.path.exists(session_folder):
            # print(f"The path {session_folder} does not exist.")
            return

        for item in os.listdir(session_folder):
            item_path = os.path.join(session_folder, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    # print(f"Deleted folder: {item_path}")
                else:
                    os.remove(item_path)
                    # print(f"Deleted file: {item_path}")
            except Exception as e:
                pass
                # print(f"Failed to delete {item_path}. Reason: {e}")


    def initialize():
        files_dir = os.path.join(project_dir, 'Files')
        if not os.path.exists(files_dir):
            os.makedirs(files_dir, exist_ok=True)

        configs_dir = os.path.join(files_dir, 'Configs')
        if not os.path.exists(configs_dir):
            os.makedirs(configs_dir, exist_ok=True)

        tidal_app_dir = os.path.join(files_dir, 'tidal_app')
        if not os.path.exists(tidal_app_dir):
            os.makedirs(tidal_app_dir, exist_ok=True)

        sessions_dir = os.path.join(files_dir, 'Sessions')
        if not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir, exist_ok=True)

        logs_dir = os.path.join(files_dir, 'Logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir, exist_ok=True)

        global worker_tidal_executable_path
        worker_tidal_executable_path = find_tidal_exe()
        if worker_tidal_executable_path:
            print_log('INFO', 'blue', 'Main', 'Found Tidal Client!')
        else:
            download_tidal_exe()
            # After downloading, find the exe path again
            worker_tidal_executable_path = find_tidal_exe()
            if worker_tidal_executable_path:
                print_log('INFO', 'blue', 'Main', 'Tidal Client installed and found!')
            else:
                print_log('ERR.', 'red', 'Main', 'Failed to find Tidal Client after installation!')
                raise Exception("Tidal executable not found after installation")

        global worker_widevine_folder
        worker_widevine_folder = find_widevine_folder()

        view_path = os.path.join(files_dir, 'manage.exe')
        if not os.path.isfile(view_path):
            print_log('WARN', 'yellow', 'Main', 'manage.exe not found - window show functionality will be limited')

        # Use hardcoded ChromeDriver 148 (stable, known working)
        chromedriver_url = "https://storage.googleapis.com/chrome-for-testing-public/148.0.7778.218/win64/chromedriver-win64.zip"
        print_log('INFO', 'blue', 'Main', 'Using ChromeDriver 148.0.7778.218 (hardcoded)')
        ensure_chromedriver(chromedriver_url, files_dir)
        patch_chromedriver(os.path.join(files_dir, 'chromedriver.exe'))
        print_log('INFO', 'blue', 'Main', 'Patched Chromedriver!')

        print_log('INFO', 'blue', 'Main', 'Checking url_writer installation (registry)...')
        url_writer.check_installation()
        if url_writer.is_installed:
            print_log('INFO', 'blue', 'Main', 'url_writer: already registered')
        else:
            print_log('WARN', 'yellow', 'Main', 'url_writer: not installed — login URL capture (urls.txt) may not work; run as Administrator and/or check network.')

        # Create the database tables
        with app.app_context():
            db.create_all()
        settings_file_path = os.path.join(project_dir, 'Files', 'settings.json')
        if os.path.exists(settings_file_path):
            with open(settings_file_path, 'r') as settings_file:
                settings_data = json.load(settings_file)
                global settings_capsolver_api_key
                settings_capsolver_api_key = settings_data.get('apiKey')
        print_log('INFO', 'blue', 'Main', f'CapSolver API Key: {settings_capsolver_api_key}')
        load_used_accounts()
        global backend_state
        backend_state = 'Ready!'

    initialize()

    def clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, remove_folder, tidal_instance):
        user_data_dir = session_folder

        try:
            if driver:
                driver.quit()
        except:
            pass
        if tidal_instance:
            kill_tidal_process(tidal_instance)
        
        if str(config_stay_logged_in).lower().__contains__('false'):
            if remove_folder is True:
                for i in range(5):
                    try:
                        shutil.rmtree(user_data_dir)
                        break
                    except:
                        time.sleep(1)
        if proxy_asyncio_loop is not None:
            try:
                if proxy_asyncio_loop and proxy_server_thread:
                    proxy_asyncio_loop.call_soon_threadsafe(proxy_asyncio_loop.stop)
                    proxy_server_thread.join(timeout=5)  # Add timeout to prevent hanging
                    # Give the OS time to release the socket
                    time.sleep(1)
            except:
                pass

        return True

    # force_delete_sessions()
    def start_tidal_old(port, thread_number, local_proxyline):
        while True:
            session_folder = os.path.join(project_dir, 'Files', 'Sessions', str(port))
            if not os.path.exists(session_folder):
                os.makedirs(session_folder, exist_ok=True)
            # options.set_preference("intl.accept_languages", locale_code)
            # Start the executable
            process = subprocess.Popen([r"C:\Users\rezq\AppData\Local\TIDAL\app-2.38.6\TIDAL.exe"])

            if local_proxyline is None:
                tidal_instance = subprocess.Popen([f'{worker_tidal_executable_path} --remote-allow-origins=http://localhost:{port} --remote-debugging-port={port} --user-data-dir="{session_folder}" '],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
            else:
                tidal_instance = subprocess.Popen([f'{worker_tidal_executable_path} --remote-allow-origins=http://localhost:{port} --remote-debugging-port={port} --user-data-dir="{session_folder}" --proxy-server={local_proxyline} '],
                    # --disable-blink-features=AutomationControlled --disable-dev-shm-usage --disable-background-timer-throttling --disable-backgrounding-occluded-windows --process-per-site --enable-low-end-device-mode --disable-renderer-backgrounding --disable-gpu --memory-pressure-off --disable-web-security --mute-audio
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
            if tidal_instance.poll() is not None:
                raise RuntimeError("Tidal instance exited unexpectedly")
            # Wait for the Tidal instance to be fully started
            timeout = 60  # Timeout in seconds
            poll_interval = 1  # Polling interval in seconds
            start_time = time.time()
            launched = False
            while time.time() - start_time < timeout:
                local_debugging_url = f"http://localhost:{port}/json"
                try:
                    response = requests.get(local_debugging_url)
                    if response.status_code == 200:
                        if 'https://desktop.tidal.com/service-worker.js' in str(response.text):
                            print_log("INFO", "blue", thread_number,
                                      f'Tidal Instance launched and ready to be connected!')
                            launched = True
                            break
                except:
                    pass

                time.sleep(poll_interval)

            if launched is False:
                print_log("EXC.", "yellow", thread_number, f'Failed to launch tidal instance')
                msg = kill_process_on_port(port)
                print_log("INFO", "blue", thread_number, msg)

                for i in range(5):
                    try:
                        shutil.rmtree(user_data_dir)
                        break
                    except:
                        time.sleep(1)
                return None
            else:
                break
        return tidal_instance

    def start_tidal(thread_number, local_proxyline, session_folder, driver_instance_port):
        timeout = 10  # Timeout in seconds
        poll_interval = 1  # Polling interval in seconds

        # Ensure the session folder exists
        os.makedirs(session_folder, exist_ok=True)

        # Path to the WidevineCdm folder in the session directory
        session_widevine_folder = os.path.join(session_folder, 'WidevineCdm')

        # Check if the WidevineCdm folder exists and has subfolders
        # Only copy if worker_widevine_folder exists (it may not exist on fresh Tidal installs)
        if worker_widevine_folder is not None and os.path.exists(worker_widevine_folder):
            if not os.path.exists(session_widevine_folder) or not any(
                    os.path.isdir(os.path.join(session_widevine_folder, subfolder))
                    for subfolder in os.listdir(session_widevine_folder)
            ):
                # If not, copy the entire worker_widevine_folder to the session folder
                if os.path.exists(session_widevine_folder):
                    shutil.rmtree(session_widevine_folder)  # Remove the existing folder if it's incomplete
                shutil.copytree(worker_widevine_folder, session_widevine_folder)
                #print(f"Copied WidevineCdm to {session_widevine_folder}")

        '''tidal_instance = subprocess.Popen(
            f'{worker_tidal_executable_path} --remote-allow-origins=http://localhost:{port} --remote-debugging-port={port} --user-data-dir="{session_folder}" --proxy-server={local_proxyline} ',
            # --disable-blink-features=AutomationControlled --disable-dev-shm-usage --disable-background-timer-throttling --disable-backgrounding-occluded-windows --process-per-site --enable-low-end-device-mode --disable-renderer-backgrounding --disable-gpu --memory-pressure-off --disable-web-security --mute-audio
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )'''

        tidal_command = [
            worker_tidal_executable_path,
            f'--remote-allow-origins=http://localhost:{driver_instance_port}',
            f'--remote-debugging-port={driver_instance_port}',
            f'--user-data-dir={session_folder}',
            '--no-sandbox',
            '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding',
            '--disable-blink-features=AutomationControlled'
        ]

        if local_proxyline:
            tidal_command.append(f'--proxy-server={local_proxyline}')

        tidal_instance = subprocess.Popen(
            tidal_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


        launched = False
        for i in range(30):
            local_debugging_url = f"http://localhost:{driver_instance_port}/json"
            try:
                response = requests.get(local_debugging_url)
                if response.status_code == 200 and 'https://desktop.tidal.com/service-worker.js' in response.text:
                    launched = True
                    break
            except Exception as e:
                pass

            time.sleep(poll_interval)

        if launched:
            return tidal_instance
        return None


    def start_driver(port, thread_number):
        options = Options()
        options.debugger_address = f"localhost:{port}"
        # Use WebDriverManager to manage the ChromeDriver
        service = Service(executable_path=project_dir + "/Files/chromedriver.exe")

        # Wait for the Chrome instance to be fully initialized
        for attempt in range(10):
            try:
                driver = webdriver.Chrome(service=service, options=options)
                print_log("INFO", "blue", thread_number, f'Successfully connected to Tidal instance on port: {port}')
                return driver, service, options
            except Exception as e:
                print_log("ERR.", "red", thread_number,
                          f'Attempt {attempt + 1}: Failed to connect to Tidal instance on port: {port} with error: {e}')
                time.sleep(2)  # Wait for 2 seconds before retrying

        return None, None, f"Failed to connect to Tidal instance on port: {port} after multiple attempts"




    def random_wait(min_seconds=1, max_seconds=3):
        time.sleep(random.uniform(min_seconds, max_seconds))


    def human_type(element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))  # Random delay between keystrokes


    def is_captcha_present(driver):
        driver.implicitly_wait(5)
        try:
            # Assuming that the iframe has a unique part of the URL that can be used to identify it
            iframe = driver.find_element(By.XPATH, '//iframe[contains(@src, "captcha-delivery")]')
            driver.implicitly_wait(30)
            return True
        except NoSuchElementException:
            driver.implicitly_wait(30)
            return False


    def check_logged_in(thread_number, driver):
        case = False
        for i in range(10):
            '''# Check if offline dialog is showing and click refresh if needed
            try:
                offline_dialog = driver.find_element(By.ID, "OFFLINE_STARTUP")
                if offline_dialog.is_displayed():
                    print_log("INFO", "yellow", f"Thread {thread_number}", "Offline dialog detected, clicking refresh...")
                    refresh_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-test="dialog-offline-startup-refresh-button"]')
                    refresh_btn.click()
                    time.sleep(10)  # Wait for page to reload
            except:
                pass  # Dialog not present, continue normally'''
            try:
                # Check if the login button exists
                login_button = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, 'login-button'))
                )
                case = False
                break
            except:
                pass
            try:
                # Check if the login button exists
                login_button = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="isLoggedIn"]'))
                )
                case = True
                break
            except:
                pass

        return case


    def random_mouse_movements(driver, duration=10):
        end_time = time.time() + duration
        actions = ActionChains(driver)

        # Get the dimensions of the browser window
        window_size = driver.get_window_size()
        window_width = window_size['width']
        window_height = window_size['height']

        while time.time() < end_time:
            # Generate random coordinates within the browser window
            x_offset = random.randint(0, window_width - 1)
            y_offset = random.randint(0, window_height - 1)

            # Perform the move action
            actions.move_by_offset(x_offset, y_offset).perform()
            time.sleep(random.uniform(0.1, 0.5))  # Random sleep time to simulate natural movement

            # Reset the actions to avoid cumulative offsets
            actions = ActionChains(driver)


    def solve_captcha(driver, thread_number, port, proxy):
        # List of user agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        ]

        # Function to get the WebSocket debugger URL
        def get_websocket_debugger_url():
            for i in range(20):
                local_debugging_url = f"http://localhost:{port}/json"
                response = requests.get(local_debugging_url)
                if response.status_code == 200:
                    tabs = response.json()
                    for tab in tabs:
                        if 'geo.captcha-delivery.com' in tab.get('title', ''):
                            return tab['url']
                time.sleep(1)
            return None

        # Function to check if the IP is banned
        def is_ip_banned(url):
            if 't=bv' in str(url):
                return True
            else:
                return False

        # Function to create the task
        def create_task(captcha_url, user_agent, proxy):
            print_log("INFO", "blue", thread_number,
                      f"Creating new Captcha Solving task with proxy {proxy}")
            api_url = "https://api.capsolver.com/createTask"
            headers = {
                "Content-Type": "application/json"
            }
            payload = {
                "clientKey": str(settings_capsolver_api_key),  # Replace with your actual API key
                "task": {
                    "type": "DatadomeSliderTask",
                    "websiteURL": "https://login.tidal.com",
                    "captchaUrl": captcha_url,
                    "userAgent": user_agent,
                    "proxy": proxy
                }
            }
            response = requests.post(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                print_log("INFO", "blue", thread_number,
                          f"Created new Captcha Solving task: {response_data.get('taskId')}")
                return response_data.get('taskId')
            else:
                print_log("ERR.", "red", thread_number,
                          f'Failed to created new Captcha Solving task: {response.text}')
                return None

        # Function to get the task result
        def get_task_result(task_id):
            api_url = "https://api.capsolver.com/getTaskResult"
            headers = {
                "Content-Type": "application/json"
            }
            payload = {
                "clientKey": str(settings_capsolver_api_key),
                "taskId": task_id
            }
            while True:
                response = requests.post(api_url, headers=headers, json=payload)
                if response.status_code == 200:
                    response_data = response.json()
                    if response_data.get('status') == 'ready':
                        return True, response_data.get('solution')
                    else:
                        if response_data.get('status') == 'failed':
                            return False, response_data
                else:
                    print_log("ERR.", "red", thread_number,
                              f"Failed to get captcha task result. Status code: {response.status_code}")
                time.sleep(5)  # Wait for 5 seconds before checking the status again

        websocket_debugger_url = get_websocket_debugger_url()
        if websocket_debugger_url:
            captcha_url = websocket_debugger_url
            if captcha_url:
                if is_ip_banned(captcha_url):
                    print_log("EXC.", "yellow", thread_number, f"Cant solve captcha because, Proxy ip is banned!")
                    return False
                else:
                    print_log("INFO", "blue", thread_number, f"Proxy IP is not banned, trying to solve Captcha now!")
                    attempts = 0
                    while True:
                        if attempts == 5:
                            return False
                        user_agent = random.choice(user_agents)  # Randomly select a user agent
                        task_id = create_task(captcha_url, user_agent, proxy)
                        attempts += 1
                        if task_id:
                            solved = None
                            error = None
                            while True:
                                solution, msg = get_task_result(task_id)
                                if solution is False:
                                    print_log("EXC.", "yellow", thread_number,
                                              f"Captcha Task failed because: {msg.get('errorDescription')}")
                                    if 'Proxy IP banned' in str(msg.get('errorDescription')):
                                        print_log("INFO", "blue", thread_number,
                                                  f"Resubmitted Captcha solving task, attempt {attempts}/5")
                                        solved = False
                                        error = True
                                        break
                                    else:
                                        solved = False
                                        error = False
                                        break
                                elif solution is True:
                                    print_log("SUCC", "green", thread_number,
                                              f"Captcha Solving Task completed successfully.")
                                    new_cookie_str = msg.get('cookie')
                                    new_cookie_parts = new_cookie_str.split('; ')
                                    new_cookie_dict = {}

                                    for part in new_cookie_parts:
                                        if '=' in part:
                                            key, value = part.split('=', 1)
                                            new_cookie_dict[key] = value

                                    new_cookie = {
                                        'name': 'datadome',
                                        'value': new_cookie_dict['datadome'],
                                        'domain': '.tidal.com',
                                        'path': '/',
                                        'secure': True,
                                        'httpOnly': False,
                                        'sameSite': 'Lax',
                                        'expiry': int(time.time()) + int(
                                            new_cookie_dict.get('Max-Age')) if 'Max-Age' in new_cookie_dict else None
                                    }
                                    driver.add_cookie(new_cookie)
                                    solved = True
                                    error = False
                                    break

                            if solved is True:
                                return True
                            elif solved is False and error is False:
                                return False
                            elif solved is False and error is True:
                                pass
                            else:
                                print("unhandled case a captcha solving loop")
                                return False
            else:
                print("Unable to retrieve the captcha URL.")
        else:
            print("Unable to find the WebSocket debugger URL.")


    class WebElement(selenium.webdriver.remote.webelement.WebElement):
        def __init__(self, parent, id_):
            super().__init__(parent, id_)

        def uc_click(
                self,
                driver: WebDriver,
                selector: str = None,
                delay: int = 0,  # milliseconds
                reconnect_time: float = 0.5,
        ):
            """
            Click using a JS delayed click if delay>0, otherwise direct JS click.
            selector: CSS selector string for JS click.
            """
            if selector and delay > 0:
                # Safely quote the selector for JS
                quoted = json.dumps(selector)
                js = (
                    f"setTimeout(function() {{ "
                    f"document.querySelector({quoted}).click(); "
                    f"}}, {int(delay)});"
                )
                driver.execute_script(js)
            else:
                # Fallback to a direct JS click on the element itself
                driver.execute_script("arguments[0].click();", self)

            # give the page a moment to react
            time.sleep(reconnect_time)

    # Utility function to wrap found element
    def find_uc_element(driver, by, value):
        elem = driver.find_element(by, value)
        return WebElement(elem.parent, elem.id)

    def delayed_load_url(driver: WebDriver, url: str, delay: int = 5000):
        """
        Load a URL after a specified delay.
        :param driver: WebDriver instance
        :param url: The URL to load
        :param delay: Delay in milliseconds before loading the URL
        """
        script = f'setTimeout(function() {{ window.location.href = "{url}"; }}, {delay});'
        driver.execute_script(script)

    def get_tidal_login_url_from_temp(thread_number, timeout=60, tracking_udid=None):
        """
        Wait for url_writer to capture the Tidal login URL and read it from urls.txt in temp.
        Same workflow as Spotify: url_writer writes the URL to %TEMP%\\urls.txt when the app
        opens the login page. Returns the URL string or None on timeout.

        If tracking_udid is provided, only returns a URL that contains this UUID (so we use
        the login URL tied to our session). Otherwise returns the first non-empty URL found.
        """
        urls_file = os.path.join(tempfile.gettempdir(), "urls.txt")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if os.path.exists(urls_file):
                    with open(urls_file, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    if content:
                        # If we have a trackingUdid, only accept URL that contains it
                        if tracking_udid and tracking_udid not in content:
                            time.sleep(0.2)
                            continue
                        try:
                            with open(urls_file, 'w', encoding='utf-8') as f:
                                f.write('')
                        except Exception:
                            pass
                        print_log("INFO", "blue", thread_number, "Captured login URL from url_writer (urls.txt)")
                        return content
            except Exception as e:
                print_log("WARN", "yellow", thread_number, f"Error reading urls.txt: {e}")
            time.sleep(0.2)
        print_log("WARN", "yellow", thread_number, f"Timeout ({timeout}s) waiting for login URL in urls.txt")
        return None

    def get_tracking_udid_from_page(driver):
        """
        Extract trackingUdid (UUID) from Tidal app localStorage.
        Looks for keys starting with 'AuthDB/' and extracts the 36-char UUID.
        Same logic as: getTrackingUuid() from AuthDB/<uuid> in localStorage.
        """
        try:
            script = """
            (function() {
                var uuid = null;
                for (var i = 0; i < localStorage.length; i++) {
                    var key = localStorage.key(i);
                    if (key && key.indexOf('AuthDB/') === 0) {
                        var match = key.match(/AuthDB\\/([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/i);
                        if (match && match[1]) {
                            uuid = match[1];
                            break;
                        }
                    }
                }
                return uuid;
            })();
            """
            result = driver.execute_script(script)
            return result if result else None
        except Exception:
            return None

    def _solve_captcha_capsolver_for_browser(captcha_url, thread_number, print_log_fn, proxy_for_task=None):
        """
        Solve DataDome captcha via Capsolver API (no driver/port). Returns (True, cookie_dict) or (False, None).
        cookie_dict is ready for driver.add_cookie() with domain .tidal.com.
        """
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        ]
        if not captcha_url or "captcha-delivery" not in captcha_url:
            return False, None
        if "t=bv" in captcha_url:
            print_log_fn("EXC.", "yellow", thread_number, "Captcha: proxy IP is banned (t=bv)")
            return False, None
        api_key = settings_capsolver_api_key if settings_capsolver_api_key else ""
        if not api_key:
            print_log_fn("ERR.", "red", thread_number, "CapSolver API key not set")
            return False, None
        for attempt in range(5):
            payload_create = {
                "clientKey": api_key,
                "task": {
                    "type": "DatadomeSliderTask",
                    "websiteURL": "https://login.tidal.com",
                    "captchaUrl": captcha_url,
                    "userAgent": random.choice(user_agents),
                    "proxy": proxy_for_task or ""
                }
            }
            try:
                r = requests.post("https://api.capsolver.com/createTask", json=payload_create, timeout=30)
                data = r.json() if r.status_code == 200 else {}
                task_id = data.get("taskId")
            except Exception as e:
                print_log_fn("ERR.", "red", thread_number, f"CapSolver createTask error: {e}")
                return False, None
            if not task_id:
                continue
            for _ in range(60):
                time.sleep(2)
                try:
                    r2 = requests.post("https://api.capsolver.com/getTaskResult", json={"clientKey": api_key, "taskId": task_id}, timeout=30)
                    data2 = r2.json() if r2.status_code == 200 else {}
                except Exception:
                    continue
                if data2.get("status") == "ready":
                    sol = data2.get("solution") or {}
                    cookie_str = sol.get("cookie") or ""
                    if not cookie_str or "datadome=" not in cookie_str:
                        return False, None
                    parts = cookie_str.split("; ")
                    parsed = {}
                    for part in parts:
                        if "=" in part:
                            k, v = part.split("=", 1)
                            parsed[k.strip()] = v.strip()
                    datadome_val = parsed.get("datadome", "")
                    if not datadome_val:
                        return False, None
                    print_log_fn("SUCC", "green", thread_number, "Captcha solved via CapSolver")
                    return True, {
                        "name": "datadome",
                        "value": datadome_val,
                        "domain": ".tidal.com",
                        "path": "/",
                        "secure": True,
                        "httpOnly": False,
                        "sameSite": "Lax",
                    }
                if data2.get("status") == "failed":
                    err = data2.get("errorDescription", "")
                    if "Proxy IP banned" in str(err):
                        break
                    print_log_fn("EXC.", "yellow", thread_number, f"Captcha task failed: {err}")
                    return False, None
        return False, None

    async def _login_tidal_with_patchright_async(thread_number, login_url, email, password, proxy_string, mute, print_log_fn):
        """Run Tidal login flow in a separate Chrome via patchright (email → continue → password → login)."""
        context = None
        try:
            session_path = os.path.join(project_dir, 'Files', 'Sessions', f'pr_login_{thread_number}_{email.replace("@", "_").replace(".", "_")}')
            os.makedirs(session_path, exist_ok=True)
            proxy_url = proxy_string if proxy_string and proxy_string != "/" else None
            proxy_dict = None
            if proxy_url:
                from urllib.parse import urlparse
                parsed = urlparse(proxy_url)
                if parsed.username or parsed.password:
                    default_port = 1080 if (parsed.scheme or "").startswith("socks") else (443 if (parsed.scheme or "") == "https" else 80)
                    proxy_dict = {"server": f"{parsed.scheme or 'http'}://{parsed.hostname}:{parsed.port or default_port}", "username": parsed.username, "password": parsed.password}
                else:
                    proxy_dict = {"server": proxy_url}
            delay = random.uniform(0.2, 0.8)
            await asyncio.sleep(delay)

            # Resolve Chrome at launch time (critical for compiled exe: runs on target machine)
            chrome_path = _find_chrome_executable()
            if not chrome_path:
                print_log_fn("ERR.", "red", thread_number, "Google Chrome not found. Install Chrome from https://www.google.com/chrome/ to use login.")
                return False, "Google Chrome not found. Please install Chrome to use login."
            print_log_fn("INFO", "blue", thread_number, f"Using Chrome: {chrome_path}")

            async with async_playwright() as p:
                launch_kw = dict(
                    user_data_dir=session_path,
                    headless=False,
                    no_viewport=True,
                    proxy=proxy_dict,
                    locale='en-US',
                    args=(["--mute-audio", "--lang=en-US"] if mute else ["--lang=en-US"]) + ["--disable-gpu", "--disable-software-rasterizer", "--no-sandbox"],
                    executable_path=chrome_path,
                )
                context = await p.chromium.launch_persistent_context(**launch_kw)
                page = context.pages[0] if context.pages else await context.new_page()
                await page.goto(login_url, timeout=90000, wait_until="domcontentloaded")
                await asyncio.sleep(15)

                # Detect DataDome/captcha-delivery captcha (full page or iframe)
                for captcha_round in range(3):
                    captcha_url = None
                    try:
                        current_url = page.url or ""
                        if "captcha-delivery" in current_url or "geo.captcha-delivery.com" in current_url:
                            captcha_url = current_url
                        if not captcha_url:
                            try:
                                iframe_loc = page.locator('iframe[src*="captcha-delivery"]')
                                if await iframe_loc.count() > 0:
                                    captcha_url = await iframe_loc.first.get_attribute("src")
                            except Exception:
                                pass
                    except Exception:
                        pass
                    if not captcha_url:
                        break
                    print_log_fn("INFO", "blue", thread_number, "DataDome/captcha-delivery captcha detected, solving via CapSolver...")
                    solved, cookie_dict = _solve_captcha_capsolver_for_browser(
                        captcha_url, thread_number, print_log_fn, proxy_for_task=None
                    )
                    if not solved or not cookie_dict:
                        return False, "Captcha solve failed"
                    try:
                        await page.goto("https://login.tidal.com/", timeout=30000, wait_until="domcontentloaded")
                        await asyncio.sleep(1)
                        if isinstance(cookie_dict, dict) and "name" in cookie_dict and "value" in cookie_dict:
                            cookie_list = [{"name": cookie_dict["name"], "value": cookie_dict["value"], "domain": "login.tidal.com", "path": "/"}]
                        elif isinstance(cookie_dict, list):
                            cookie_list = [{"name": c["name"], "value": c["value"], "domain": "login.tidal.com", "path": "/"} for c in cookie_dict if isinstance(c, dict) and "name" in c and "value" in c]
                        else:
                            cookie_list = [dict(cookie_dict, **{"domain": "login.tidal.com", "path": "/"})]
                        await context.add_cookies(cookie_list)
                        await page.goto(login_url, timeout=90000, wait_until="domcontentloaded")
                        await asyncio.sleep(2)
                    except Exception as e:
                        print_log_fn("WARN", "yellow", thread_number, f"After captcha solve: {e}")
                        return False, "Captcha cookie apply failed"

                print_log_fn("INFO", "cyan", thread_number, "STEP: cookie consent")
                try:
                    cookie_btn = page.locator('#onetrust-accept-btn-handler').first
                    await cookie_btn.wait_for(state='visible', timeout=5000)
                    await cookie_btn.click()
                    await asyncio.sleep(1)
                except Exception:
                    pass
                print_log_fn("INFO", "cyan", thread_number, "STEP: email field")
                email_field = page.locator('#email').first
                try:
                    await email_field.wait_for(state='visible', timeout=5000)
                except Exception:
                    for sel in ['input[type="email"]', 'input[name="email"]', 'input[name="username"]', 'input[autocomplete="username"]']:
                        email_field = page.locator(sel).first
                        try:
                            await email_field.wait_for(state='visible', timeout=3000)
                            break
                        except Exception:
                            pass
                email_remembered = False
                if not await email_field.count():
                    print_log_fn("INFO", "yellow", thread_number, "Email field not found — TIDAL may have remembered it, trying to clear session")
                    try:
                        await page.goto("https://login.tidal.com/logout", wait_until="domcontentloaded", timeout=10000)
                        await asyncio.sleep(1)
                    except Exception:
                        pass
                    try:
                        await page.evaluate("() => { localStorage.clear(); document.cookie.split(';').forEach(c => { document.cookie = c.trim().split('=')[0] + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/'; }); }")
                    except Exception:
                        pass
                    email_enc = requests.utils.quote(email)
                    try:
                        await page.goto(f"https://login.tidal.com/login?email={email_enc}&lang=en", wait_until="networkidle", timeout=20000)
                        await asyncio.sleep(3)
                    except Exception as nav_e:
                        print_log_fn("WARN", "yellow", thread_number, f"Direct navigation failed: {nav_e}")
                    for _r in range(20):
                        ef = page.locator('#email').first
                        if await ef.count() and await ef.is_visible():
                            email_field = ef
                            print_log_fn("INFO", "blue", thread_number, "Email field appeared after session clear")
                            break
                        pf = page.locator('#password').first
                        if await pf.count() and await pf.is_visible():
                            password_field = pf
                            pwd_visible = True
                            email_remembered = True
                            print_log_fn("INFO", "blue", thread_number, "Password field visible after session clear (email remembered)")
                            break
                        await asyncio.sleep(0.5)
                if not email_remembered:
                    await email_field.fill(email)
                    await asyncio.sleep(random.uniform(0.5, 1.2))
                    print_log_fn("INFO", "cyan", thread_number, "STEP: continue button")
                    login_btn = page.locator("button[ui-test-id='check-user-continue-button']").first
                    try:
                        await login_btn.wait_for(state='visible', timeout=5000)
                    except Exception:
                        for sel in ['button:has-text("Continue")', 'button:has-text("continue")', 'button[type="submit"]']:
                            login_btn = page.locator(sel).first
                            try:
                                await login_btn.wait_for(state='visible', timeout=3000)
                                break
                            except Exception:
                                pass
                    try:
                        await login_btn.wait_for(state='visible', timeout=15000)
                    except Exception:
                        pass
                    if not await login_btn.count():
                        return False, "Continue button not found"
                    print_log_fn("INFO", "cyan", thread_number, "STEP: clicking continue")
                    await login_btn.click()
                    print_log_fn("INFO", "cyan", thread_number, "STEP: after click - wait for navigation")
                    try:
                        await page.wait_for_url("**/auth/**", timeout=5000)
                        print_log_fn("INFO", "blue", thread_number, "Page navigated to auth URL")
                    except Exception:
                        pass
                    try:
                        await page.wait_for_load_state("networkidle", timeout=8000)
                    except Exception:
                        pass
                    await asyncio.sleep(2)
                print_log_fn("INFO", "cyan", thread_number, "STEP: checking URL")
                try:
                    url_now = page.url
                    print_log_fn("INFO", "blue", thread_number, f"URL after Continue: {url_now}")
                    print_log_fn("INFO", "cyan", thread_number, "STEP: getting HTML")
                    html_snippet = await asyncio.wait_for(page.content(), timeout=5)
                    print_log_fn("INFO", "blue", thread_number, f"HTML snippet: {html_snippet[:400]}")
                except asyncio.TimeoutError:
                    print_log_fn("WARN", "yellow", thread_number, "page.content() timed out (5s)")
                except Exception as e:
                    print_log_fn("WARN", "yellow", thread_number, f"page.content error: {e}")
                print_log_fn("INFO", "cyan", thread_number, "STEP: dump all input fields")
                try:
                    all_inputs = await page.evaluate("""() => {
                        const inputs = document.querySelectorAll('input');
                        return Array.from(inputs).map(i => ({id: i.id, name: i.name, type: i.type, placeholder: i.placeholder, autocomplete: i.autocomplete, visible: i.offsetParent !== null}));
                    }""")
                    print_log_fn("INFO", "blue", thread_number, f"Input fields: {all_inputs}")
                except Exception as e:
                    print_log_fn("WARN", "yellow", thread_number, f"Input dump error: {e}")

                # Check for DataDome CAPTCHA on the authorize page (may appear as iframe or full redirect)
                for captcha_round in range(3):
                    captcha_url = None
                    try:
                        cur = page.url or ""
                        if "captcha-delivery" in cur or "geo.captcha-delivery.com" in cur:
                            captcha_url = cur
                        if not captcha_url:
                            try:
                                iframe_loc = page.locator('iframe[src*="captcha-delivery"]')
                                if await iframe_loc.count() > 0:
                                    captcha_url = await iframe_loc.first.get_attribute("src")
                            except Exception:
                                pass
                    except Exception:
                        pass
                    if not captcha_url:
                        break
                    if "t=bv" in captcha_url:
                        print_log_fn("EXC.", "red", thread_number, "CAPTCHA: IP baneada por DataDome (t=bv). Usa proxies residenciales o cambia tu IP.")
                        return False, "IP is banned by DataDome (t=bv) - use residential proxies or change IP"
                    print_log_fn("INFO", "blue", thread_number, "DataDome CAPTCHA detected on authorize page, solving via CapSolver...")
                    solved, cookie_dict = _solve_captcha_capsolver_for_browser(
                        captcha_url, thread_number, print_log_fn, proxy_for_task=None
                    )
                    if not solved or not cookie_dict:
                        return False, "Captcha solve failed on authorize page"
                    try:
                        await page.goto("https://login.tidal.com/", timeout=30000, wait_until="domcontentloaded")
                        await asyncio.sleep(1)
                        if isinstance(cookie_dict, dict) and "name" in cookie_dict and "value" in cookie_dict:
                            cookie_list = [{"name": cookie_dict["name"], "value": cookie_dict["value"], "domain": "login.tidal.com", "path": "/"}]
                        elif isinstance(cookie_dict, list):
                            cookie_list = [{"name": c["name"], "value": c["value"], "domain": "login.tidal.com", "path": "/"} for c in cookie_dict if isinstance(c, dict) and "name" in c and "value" in c]
                        else:
                            cookie_list = [dict(cookie_dict, **{"domain": "login.tidal.com", "path": "/"})]
                        await context.add_cookies(cookie_list)
                        await page.goto(login_url, timeout=90000, wait_until="domcontentloaded")
                        await asyncio.sleep(2)
                    except Exception as e:
                        print_log_fn("WARN", "yellow", thread_number, f"After captcha solve on authorize: {e}")
                        return False, "Captcha cookie apply failed on authorize page"

                print_log_fn("INFO", "cyan", thread_number, "STEP: check for confirm identity / password field")
                confirmed = False
                yes_continue_selectors = [
                    'button:has-text("Yes, continue")',
                    'button:has-text("Sí, continuar")',
                    'button:has-text("continuar")',
                    'button:has-text("continue")',
                    'text=Sí, continuar',
                    'text=Yes, continue',
                    '[data-test*="confirm-identity"]',
                ]
                for sel_yes in yes_continue_selectors:
                    try:
                        yes_btn = page.locator(sel_yes).first
                        await yes_btn.wait_for(state='visible', timeout=1500)
                        await yes_btn.click()
                        print_log_fn("INFO", "blue", thread_number, f"Clicked '{sel_yes}' on confirm identity page")
                        await asyncio.sleep(2)
                        confirmed = True
                        break
                    except Exception:
                        pass
                if not confirmed:
                    print_log_fn("INFO", "yellow", thread_number, "No selector matched 'Yes, continue', trying JS broad search")
                    try:
                        js_clicked = await page.evaluate("""() => {
                            const btns = document.querySelectorAll('button, a, div[role="button"]');
                            for (const el of btns) {
                                const t = (el.textContent || '').toLowerCase().trim();
                                if (t.includes('continue') || t.includes('continuar') || t.includes('sí') || t.includes('yes')) {
                                    el.click();
                                    return {text: el.textContent.trim().slice(0, 40), tag: el.tagName, class: el.className};
                                }
                            }
                            return null;
                        }""")
                        if js_clicked:
                            print_log_fn("INFO", "blue", thread_number, f"JS clicked confirm identity button: {js_clicked}")
                            await asyncio.sleep(2)
                            confirmed = True
                    except Exception as e:
                        print_log_fn("WARN", "yellow", thread_number, f"JS broad search error: {e}")
                if not email_remembered:
                    pwd_visible = False
                password_field = page.locator('#password').first
                try:
                    await password_field.wait_for(state='visible', timeout=3000)
                    pwd_visible = True
                except Exception:
                    for sel in ['input[type="password"]', 'input[name="password"]', 'input[autocomplete="current-password"]', 'input[data-test*="password"]', '[data-test="password-input"]']:
                        password_field = page.locator(sel).first
                        try:
                            await password_field.wait_for(state='visible', timeout=2000)
                            pwd_visible = True
                            break
                        except Exception:
                            pass
                if not pwd_visible:
                    print_log_fn("INFO", "cyan", thread_number, "STEP: password not visible, dump all visible buttons/links")
                    try:
                        visible_els = await page.evaluate("""() => {
                            const all = document.querySelectorAll('button, a, span, [role="button"], [role="tab"], input, label, h1, h2, p');
                            return Array.from(all).filter(el => el.offsetParent !== null).map(el => ({
                                tag: el.tagName,
                                type: el.type || '',
                                text: (el.textContent || '').trim().slice(0, 60),
                                id: el.id,
                                'data-test': el.getAttribute('data-test') || '',
                                'aria-label': el.getAttribute('aria-label') || '',
                                href: el.href || ''
                            }));
                        }""")
                        print_log_fn("INFO", "blue", thread_number, f"Visible elements: {visible_els[:30]}")
                    except Exception as e:
                        print_log_fn("WARN", "yellow", thread_number, f"Dump error: {e}")
                    print_log_fn("INFO", "cyan", thread_number, "STEP: try to find any 'password' text on page")
                    pwd_found_js = await page.evaluate("""() => {
                        const body = document.body.innerText || '';
                        const lines = body.split('\\n').filter(l => l.toLowerCase().includes('password') || l.toLowerCase().includes('contrase') || l.toLowerCase().includes('sign in'));
                        return lines.slice(0, 10);
                    }""")
                    print_log_fn("INFO", "blue", thread_number, f"Text containing password/signin: {pwd_found_js}")
                    print_log_fn("INFO", "cyan", thread_number, "STEP: look for option link")
                    pwd_option_selectors = [
                        '[data-test*="password-tab"]',
                        'button:has-text("Use password")', 'a:has-text("Use password")',
                        'button:has-text("Sign in with password")', 'a:has-text("Sign in with password")',
                        'button:has-text("Log in with password")', 'a:has-text("Log in with password")',
                        'button:has-text("Usar contraseña")',
                        'a:has-text("Usar contraseña")',
                        'button:has-text("Iniciar sesión con contraseña")',
                        '[role="tab"]:has-text("Password")',
                        '[role="tab"]:has-text("Contraseña")',
                        'button:has-text("contraseña")', 'a:has-text("contraseña")',
                        'a:has-text("Password")',
                        'button:has-text("password"):has-text("Log")',
                        'a:has-text("Sign in with password")',
                        '[data-test*="sign-in-with-password"]',
                        '[data-test*="login-with-password"]',
                        'a:has-text("Sign in")',
                        'button:has-text("Sign in")',
                    ]
                    found_option = False
                    for sel in pwd_option_selectors:
                        pwd_switch = page.locator(sel).first
                        try:
                            await pwd_switch.wait_for(state='visible', timeout=1500)
                            await pwd_switch.click()
                            print_log_fn("INFO", "blue", thread_number, f"Clicked password option (match: {sel})")
                            await asyncio.sleep(1)
                            found_option = True
                            break
                        except Exception:
                            pass
                    if not found_option:
                        print_log_fn("INFO", "yellow", thread_number, "No password option found in DOM, trying JS broad search")
                        try:
                            clicked = await page.evaluate("""() => {
                                const allEls = document.querySelectorAll('button, a, span, div[role="button"]');
                                for (const el of allEls) {
                                    const t = (el.textContent || '').toLowerCase().trim();
                                    if (t.includes('use password') || t.includes('sign in with password') || t.includes('log in with password') || t.includes('contraseña') || t === 'password' || t === 'contraseña' || t === 'sign in' || t.includes('iniciar ses')) {
                                        el.click();
                                        return {text: el.textContent.trim(), tag: el.tagName};
                                    }
                                }
                                return null;
                            }""")
                            if clicked:
                                print_log_fn("INFO", "blue", thread_number, f"JS clicked element: {clicked}")
                                await asyncio.sleep(2)
                                found_option = True
                            else:
                                print_log_fn("INFO", "yellow", thread_number, "No password/Sign-in link at all. Navigating to tidal.com/login directly")
                                try:
                                    email_enc = requests.utils.quote(email)
                                    await page.goto(f"https://login.tidal.com/login?email={email_enc}&lang=en", wait_until="networkidle", timeout=15000)
                                    await asyncio.sleep(3)
                                    new_url = page.url
                                    print_log_fn("INFO", "blue", thread_number, f"After direct navigation URL: {new_url}")
                                    visible_els2 = await page.evaluate("""() => {
                                        const all = document.querySelectorAll('button, a, input');
                                        return Array.from(all).filter(el => el.offsetParent !== null).map(el => ({
                                            tag: el.tagName, type: el.type || '', text: (el.textContent || '').trim().slice(0, 40), id: el.id, name: el.name,
                                            'data-test': el.getAttribute('data-test') || '', autocomplete: el.getAttribute('autocomplete') || ''
                                        }));
                                    }""")
                                    print_log_fn("INFO", "blue", thread_number, f"Login page elements: {visible_els2[:20]}")
                                except Exception as nav_e:
                                    print_log_fn("WARN", "yellow", thread_number, f"Direct navigation failed: {nav_e}")
                        except Exception as e:
                            print_log_fn("WARN", "yellow", thread_number, f"JS fallback error: {e}")
                    for _ in range(20):
                        password_field = page.locator('#password').first
                        if await password_field.count() and await password_field.is_visible():
                            break
                        await asyncio.sleep(0.5)
                    pwd_found = await password_field.count() and await password_field.is_visible()
                    if not pwd_found:
                        for sel in ['input[type="password"]', 'input[name="password"]', 'input[autocomplete="current-password"]', '[data-test="password-input"]', 'input[data-test*="password"]', 'input[placeholder*="Contrase"]', 'input[placeholder*="password"]']:
                            password_field = page.locator(sel).first
                            try:
                                await password_field.wait_for(state='visible', timeout=3000)
                                if await password_field.count():
                                    pwd_found = True
                                    break
                            except Exception:
                                pass
                    if not pwd_found:
                        print_log_fn("INFO", "yellow", thread_number, "Password field not found after option, dumping page content")
                        try:
                            html_now = await asyncio.wait_for(page.content(), timeout=5)
                            print_log_fn("INFO", "blue", thread_number, f"Full HTML snippet: {html_now[:600]}")
                            err_text = await page.evaluate("""() => {
                                const errs = document.querySelectorAll('[class*="error"], [class*="alert"], [class*="message"], [role="alert"]');
                                return Array.from(errs).map(e => e.textContent.trim()).filter(Boolean);
                            }""")
                            print_log_fn("INFO", "blue", thread_number, f"Error elements: {err_text}")
                        except Exception as dump_e:
                            print_log_fn("WARN", "yellow", thread_number, f"Dump failed: {dump_e}")
                        print_log_fn("INFO", "yellow", thread_number, "Navigating to clean login page")
                        try:
                            email_enc = requests.utils.quote(email)
                            await page.goto(f"https://login.tidal.com/login?email={email_enc}&lang=en", wait_until="networkidle", timeout=20000)
                            await asyncio.sleep(3)
                            print_log_fn("INFO", "blue", thread_number, f"Clean login URL: {page.url}")
                            for _ in range(20):
                                password_field = page.locator('#password').first
                                if await password_field.count() and await password_field.is_visible():
                                    pwd_found = True
                                    break
                                await asyncio.sleep(0.5)
                            if not pwd_found:
                                for sel in ['input[type="password"]', 'input[name="password"]', 'input[autocomplete="current-password"]', '[data-test="password-input"]', 'input[data-test*="password"]']:
                                    password_field = page.locator(sel).first
                                    try:
                                        await password_field.wait_for(state='visible', timeout=3000)
                                        if await password_field.count():
                                            pwd_found = True
                                            break
                                    except Exception:
                                        pass
                        except Exception as nav_e:
                            print_log_fn("WARN", "yellow", thread_number, f"Clean login nav failed: {nav_e}")
                if not await password_field.count():
                    return False, "Password field not found"
                await password_field.fill(password)
                await asyncio.sleep(random.uniform(0.5, 1.2))
                login_submit_btn = page.locator('[ui-test-id="login-user-login-button"]').first
                try:
                    await login_submit_btn.wait_for(state='visible', timeout=5000)
                except Exception:
                    for sel in ['button:has-text("Log in")', 'button:has-text("log in")', 'button:has-text("Sign in")', 'button:has-text("Iniciar sesión")', 'button:has-text("Continuar")', 'button:has-text("Entrar")', 'button[type="submit"]']:
                        login_submit_btn = page.locator(sel).first
                        try:
                            await login_submit_btn.wait_for(state='visible', timeout=3000)
                            break
                        except Exception:
                            pass
                try:
                    await login_submit_btn.wait_for(state='visible', timeout=10000)
                except Exception:
                    pass
                if not await login_submit_btn.count():
                    return False, "Login submit button not found"
                await login_submit_btn.click()
                print_log_fn("INFO", "blue", thread_number, "Clicked login button")

                await asyncio.sleep(3)
                current_url = page.url or ""
                if "login.tidal.com" in current_url and "success" not in current_url:
                    yes_continue_selectors = [
                        'button:has-text("Sí, continuar")',
                        'button:has-text("continuar")',
                        'button:has-text("continue")',
                        'text=Sí, continuar',
                        'text=Yes, continue',
                        '[data-test*="confirm-identity"]',
                    ]
                    for sel_yes in yes_continue_selectors:
                        try:
                            yes_btn = page.locator(sel_yes).first
                            await yes_btn.wait_for(state='visible', timeout=2000)
                            await yes_btn.click()
                            print_log_fn("INFO", "blue", thread_number, f"Clicked '{sel_yes}' after login")
                            await asyncio.sleep(3)
                            break
                        except Exception:
                            pass
                    try:
                        js_clicked = await page.evaluate("""() => {
                            const btns = document.querySelectorAll('button, a, div[role="button"]');
                            for (const el of btns) {
                                const t = (el.textContent || '').toLowerCase().trim();
                                if (t.includes('continue') || t.includes('continuar') || t.includes('sí') || t.includes('yes')) {
                                    el.click();
                                    return el.textContent.trim().slice(0, 40);
                                }
                            }
                            return null;
                        }""")
                        if js_clicked:
                            print_log_fn("INFO", "blue", thread_number, f"JS clicked 'Yes, continue' after login: {js_clicked}")
                            await asyncio.sleep(3)
                    except Exception:
                        pass

                for _ in range(45):
                    try:
                        current_url = page.url or ""
                        if "login.tidal.com/success" in current_url:
                            import re
                            code_value = None
                            state_value = "na"
                            for _extract in range(5):
                                try:
                                    raw = await page.evaluate("""
                                        () => {
                                            try {
                                                var d = window.__NUXT__ && window.__NUXT__.data && window.__NUXT__.data[0];
                                                var url = (d && d.successRedirectUrl) ? d.successRedirectUrl : null;
                                                if (!url) return null;
                                                var m = url.match(/[?&]code=([^&]+)/);
                                                var s = (url.match(/[?&]state=([^&]+)/) || [])[1];
                                                return m ? JSON.stringify({code: m[1], state: s || 'na'}) : null;
                                            } catch (e) { return null; }
                                        }
                                    """)
                                    if raw and isinstance(raw, str):
                                        try:
                                            o = json.loads(raw)
                                            if o.get("code"):
                                                code_value = o["code"]
                                                state_value = o.get("state") or "na"
                                                break
                                        except Exception:
                                            pass
                                except Exception:
                                    pass
                                if not code_value:
                                    html = await page.evaluate("() => document.documentElement.outerHTML") or ""
                                    if html:
                                        m = re.search(r'login(?:/|\\u002F)auth\?code=(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)', html)
                                        if m:
                                            code_value = m.group(1).strip()
                                        if not code_value:
                                            m = re.search(r'code=(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)', html)
                                            if m:
                                                code_value = m.group(1)
                                        if code_value:
                                            m2 = re.search(r'state=([A-Za-z0-9_.-]+)', html)
                                            if m2:
                                                state_value = m2.group(1).strip()
                                        if code_value:
                                            break
                                if not code_value:
                                    scripts = await page.evaluate("() => Array.from(document.querySelectorAll('script')).map(s => s.textContent).join('\\n');")
                                    if scripts and isinstance(scripts, str):
                                        m = re.search(r'code=(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*)', scripts)
                                        if m:
                                            code_value = m.group(1)
                                            break
                                await asyncio.sleep(0.25)
                            if code_value:
                                tidal_auth_uri = f"tidal://login/auth?code={code_value}&state={state_value}"
                                print_log_fn("INFO", "blue", thread_number, f"Captured tidal://login/auth URL (code length {len(code_value)})")
                                return True, tidal_auth_uri
                            print_log_fn("WARN", "yellow", thread_number, "Success page seen but code not extracted yet, retrying...")
                        if "login.tidal.com" in current_url:
                            try:
                                err = page.locator('[data-test="notification-message"]').first
                                if await err.count() > 0:
                                    err_text = await err.text_content()
                                    if err_text and "Unable to log in" in err_text:
                                        return False, "Unable to log in (proxy/session)"
                            except Exception:
                                pass
                            try:
                                reg_form = page.locator('#registration-first-step').first
                                if await reg_form.count() > 0:
                                    print_log_fn("INFO", "yellow", thread_number, "Registration form shown after login – account not valid")
                                    return False, "Account not valid (registration form shown)"
                            except Exception:
                                pass
                            try:
                                new_pwd = page.locator('input#new-password[placeholder*="Create your password"], input[name="new-password"]').first
                                if await new_pwd.count() > 0:
                                    print_log_fn("INFO", "yellow", thread_number, "Create password field shown – account not valid")
                                    return False, "Account not valid (create account form shown)"
                            except Exception:
                                pass
                    except Exception:
                        pass
                    await asyncio.sleep(1)
                print_log_fn("ERR.", "red", thread_number, "Login timeout (no success redirect)")
                return False, "Login timeout (no success redirect)"
        except Exception as e:
            print_log_fn("ERR.", "red", thread_number, f'Error occurred in login function: {str(e)}')
            return False, str(e)
        finally:
            if context:
                try:
                    await context.close()
                except Exception:
                    pass

    def login_tidal_with_patchright(thread_number, login_url, email, password, proxy_string, mute, print_log_fn):
        """Sync wrapper: run Tidal patchright login and return (success, reason)."""
        try:
            return asyncio.run(_login_tidal_with_patchright_async(
                thread_number, login_url, email, password, proxy_string, mute, print_log_fn
            ))
        except Exception as e:
            return False, str(e)

    def login_account(thread_number, driver, tidal_instance, proxy, service, options, email, password, driver_instance_port, tidal_instance_port, account_manager):
        try:
            for login_attempt in range(3):
                update_thread_status(thread_number, 'Logging in', None, False, False, False, False, False, None)
                driver.implicitly_wait(1)
                random_wait(2, 4)
                for i in range(5):
                    try:
                        #driver.find_element(By.ID, 'onetrust-reject-all-handler').click()
                        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
                        break
                    except:
                        pass
                driver.implicitly_wait(40)
                main_window = driver.current_window_handle
                new_window_detected = False
                random_wait(2, 4)
                # Web-login flow: get trackingUdid from Tidal app localStorage first (AuthDB/<uuid>)
                tracking_udid = get_tracking_udid_from_page(driver)
                if tracking_udid:
                    print_log("INFO", "blue", thread_number, f"Captured trackingUdid (AuthDB): {tracking_udid}")
                elem = find_uc_element(driver, By.CSS_SELECTOR, '[data-test="login-button"]')
                elem.uc_click(driver,
                              selector='[data-test="login-button"]',
                              delay=5000)
                
                # Then get login URL from url_writer (urls.txt); URL contains this uuid
                print_log("INFO", "blue", thread_number, "Waiting for login URL from url_writer (urls.txt)...")
                login_url = get_tidal_login_url_from_temp(thread_number, timeout=50, tracking_udid=tracking_udid)
                if login_url:
                    # Use patchright Chrome for login (same pattern as Spotify login_with_chrome)
                    mute_login = str(config_mute_tidal_app).lower().__contains__('true')
                    print_log("INFO", "blue", thread_number, "Opening login in patchright Chrome...")
                    success, reason = login_tidal_with_patchright(
                        thread_number, login_url, email, password, proxy, mute_login, print_log
                    )
                    if not success:
                        print_log("ERR.", "red", thread_number, f"patchright login failed: {reason}")
                        if login_attempt < 2:
                            print_log("INFO", "blue", thread_number, f"Retrying login (attempt {login_attempt+2}/3)...")
                            continue
                        return driver, False, False, reason or "patchright login failed"
                    # Route the login callback to this Tidal desktop instance so the right app receives the auth code.
                    if success and reason and isinstance(reason, str) and reason.strip().lower().startswith("tidal://"):
                        try:
                            tidal_uri = reason.strip()
                            if "://" in tidal_uri:
                                path_query = tidal_uri.split("://", 1)[1].strip()
                            else:
                                path_query = tidal_uri.strip()
                            if path_query.startswith("/"):
                                path_query = path_query[1:]

                            try:
                                current = driver.current_url or ""
                                if "desktop.stage.tidal.com" in current:
                                    base = "https://desktop.stage.tidal.com"
                                else:
                                    base = "https://desktop.tidal.com"
                            except Exception:
                                base = "https://desktop.tidal.com"
                            callback_url = f"{base.rstrip('/')}/{path_query}"

                            driver.set_page_load_timeout(10)
                            try:
                                driver.get(callback_url)
                                print_log("INFO", "blue", thread_number, "Routed login callback to desktop.tidal.com")
                            except Exception:
                                pass
                            driver.set_page_load_timeout(300)
                            time.sleep(2)

                            try:
                                driver.get("https://desktop.tidal.com/browse")
                                print_log("INFO", "blue", thread_number, "Navigated Tidal app to home page")
                            except Exception:
                                try:
                                    driver.execute_script("window.location.href = 'https://desktop.tidal.com/browse'")
                                except Exception:
                                    pass
                            time.sleep(3)

                            page_text = ""
                            try:
                                page_text = driver.page_source or ""
                            except Exception:
                                pass
                            error_detected = "no ha sido posible" in page_text.lower() or "unable to log in" in page_text.lower() or "try again" in page_text.lower() or "not possible" in page_text.lower()
                            if error_detected:
                                print_log("WARN", "yellow", thread_number, "Login error detected in Tidal app after callback")
                                if login_attempt < 2:
                                    print_log("INFO", "blue", thread_number, f"Retrying login (attempt {login_attempt+2}/3)...")
                                    continue
                                else:
                                    print_log("ERR.", "red", thread_number, "Login failed after 3 attempts")
                                    return driver, False, False, "Login failed after callback (error in Tidal app)"
                        except Exception as e:
                            print_log("WARN", "yellow", thread_number, f"Could not route auth to Tidal app: {e}")

                return driver, False, True, None
        except Exception as e:
            global worker_bot_errors
            worker_bot_errors += 1
            print_log("ERR.", "red", thread_number, f'Error occurred in login function: {str(e)}')
            update_thread_status(thread_number, None, None, False, False, False, False, True, None)
            return driver, True, False, False


    # Sentinel: account check hit Access Denied (proxy blocked); caller should try different proxy and re-check
    ACC_TYPE_PROXY_BLOCKED = "PROXY_BLOCKED"

    def check_account_type(thread_number, driver, driver_instance_port):
        try:
            logged_in = check_logged_in(thread_number, driver)
            if not logged_in:
                return False
            # Reset implicit wait to 0 for fast checks
            driver.implicitly_wait(0)
            
            try:
                artist_picker = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="artist-category-container"]'))
                )
                clicked_numbers2 = set()
                for i in range(3):
                    # Generate a random number that has not been clicked yet
                    while True:
                        num = random.randint(2, 11)
                        if num not in clicked_numbers2:
                            break
                    driver.find_element(By.XPATH, f'//div[2]/div[{num}]').click()
                    clicked_numbers2.add(num)
                    time.sleep(random.randint(1, 3))

                time.sleep(4)
                driver.find_element(By.CSS_SELECTOR, '[data-test="finish-artist-picker"]').click()
            except:
                pass

            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys(',').key_up(Keys.CONTROL).perform()

            executable_path = os.path.join(project_dir, 'Files', 'manage.exe')
            try:
                command = [executable_path, '--port', str(driver_instance_port), '--action', 'show']
                subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass

            # If proxy is blocked, CDN returns Access Denied XML; signal caller to retry with different proxy
            time.sleep(1.5)
            try:
                page_source = (driver.page_source or '') if hasattr(driver, 'page_source') else ''
                if '<Code>AccessDenied</Code>' in page_source or ('Access Denied' in page_source and 'Error' in page_source):
                    print_log("WARN", "yellow", thread_number, 'Proxy blocked (Access Denied) during account check – will retry with different proxy')
                    return ACC_TYPE_PROXY_BLOCKED
            except Exception:
                pass

            try:
                modal = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ReactModal__Content"))
                )
                close_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "modalHeader")]//button'))
                )
                close_button.click()
            except:
                pass

            try:
                #wait for this element to be visible data-test="settings-page"
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="settings-page"]'))
                )
            except:
                try:
                    page_source = (driver.page_source or '') if hasattr(driver, 'page_source') else ''
                    if '<Code>AccessDenied</Code>' in page_source or ('Access Denied' in page_source and 'Error' in page_source):
                        print_log("WARN", "yellow", thread_number, 'Proxy blocked (Access Denied) during account check – will retry with different proxy')
                        return ACC_TYPE_PROXY_BLOCKED
                except Exception:
                    pass
                try:
                    modal = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "ReactModal__Content"))
                    )
                    close_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "modalHeader")]//button'))
                    )
                    close_button.click()
                except:
                    pass
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).send_keys(',').key_up(Keys.CONTROL).perform()
                #wait for this element to be visible data-test="settings-page"
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="settings-page"]'))
                )

            try:
                modal = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ReactModal__Content"))
                )
                close_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "modalHeader")]//button'))
                )
                close_button.click()
            except:
                pass

            if str(config_streaming_quality_to_low).lower().__contains__('true'):
                try:
                    driver.find_element(By.CSS_SELECTOR, '[data-test="audio-quality-low"]').click()
                except:
                    pass
            else:
                try:
                    driver.find_element(By.CSS_SELECTOR, '[data-test="audio-quality-high"]').click()
                except:
                    pass
            
            try:
                driver.find_element(By.CSS_SELECTOR, '[data-test="settings-tab--account"]').click()
            except:
                try:
                    driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/account"]').click()
                except:
                    try:
                        modal = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "ReactModal__Content"))
                        )
                        close_button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "modalHeader")]//button'))
                        )
                        close_button.click()
                    except:
                        pass
                    try:
                        driver.find_element(By.CSS_SELECTOR, '[data-test="settings-tab--account"]').click()
                    except:
                        driver.find_element(By.CSS_SELECTOR, 'a[href="/settings/account"]').click()

            manage_subscription_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="https://account.tidal.com/"]'))
            )

            # Scroll into view if necessary
            driver.execute_script("arguments[0].scrollIntoView();", manage_subscription_link)
            subscription_info_div = manage_subscription_link.find_element(By.XPATH, './ancestor::div[1]/preceding-sibling::div')
            subscription_name = subscription_info_div.find_element(By.XPATH, './span[2]')
            combined_text = str(subscription_name.text)
            account_type = "Unknown"
            if "TIDAL + DJ Extension" in combined_text:
                account_type = "HiFi + DJ Extension"
            elif "TIDAL +" in combined_text:
                account_type = "TIDAL +"
            elif "TIDAL Intro" in combined_text:
                account_type = "TIDAL Intro"
            elif "TIDAL" in combined_text:
                account_type = "TIDAL Individual"
            try:
                driver.find_element(By.CSS_SELECTOR, '[data-test="sidebar-logo"]').click()
            except:
                pass
            print_log('INFO', "green", thread_number, f'Account type: {account_type}')

            return account_type
        except Exception as e:
            print_log("ERR.", "red", thread_number, f'Error occurred in check account function: {str(e)}')
            global worker_bot_errors
            worker_bot_errors += 1
            update_thread_status(thread_number, None, None, False, False, False, False, True, None)
            return None

    def scrape_link_infos(thread_number, driver, link_o, driver_instance_port):
        try:
            with app.app_context():
                existing_link = Link.query.filter_by(link=link_o).first()

                if existing_link:
                    return existing_link.artist_name, existing_link.album_name, existing_link.song_count

                driver.get(link_o)
                executable_path = os.path.join(project_dir, 'Files', 'manage.exe')
                try:
                    command = [executable_path, '--port', str(driver_instance_port), '--action', 'show']
                    subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
                except:
                    pass
                title_element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'h2[data-test="title"]'))
                )
                title_text = title_element.text
                artist_text = ""
                for sel in [
                    '[data-test-module-type="ALBUM_HEADER"] [data-test="grid-item-detail-text-title-artist"]',
                    '[data-test="grid-item-detail-text-title-artist"]',
                    '[data-test="artist-link"]',
                    '[data-test="album-header-artist"]',
                ]:
                    try:
                        artist_text = driver.find_element(By.CSS_SELECTOR, sel).text
                        break
                    except:
                        pass
                song_count = 1
                for sel in [
                    '[data-test-module-type="ALBUM_HEADER"] [data-test="grid-item-meta-item-count"]',
                    '[data-test="grid-item-meta-item-count"]',
                    '[data-test="track-count"]',
                ]:
                    try:
                        el = driver.find_element(By.CSS_SELECTOR, sel)
                        m = re.search(r'\d+', el.text)
                        if m:
                            song_count = int(m.group())
                        break
                    except:
                        pass
                new_link = Link(
                    link=link_o,
                    artist_name=artist_text,
                    album_name=title_text,
                    song_count=song_count,
                    time_read=datetime.utcnow()
                )
                db.session.add(new_link)
                db.session.commit()
                driver.back()
                return new_link.artist_name, new_link.album_name, new_link.song_count
        except Exception as e:
            print_log("ERR.", "red", thread_number, f'Failed to scrape Link details: {str(e)}')
            return None, None, 0

    def load_link(thread_number, driver, driver_instance_port):
        try:
            # Reset implicit wait to 0 for fast checks
            driver.implicitly_wait(0)
            
            '''# Check if offline dialog is showing and click refresh if needed
            try:
                driver.find_element(By.ID, "OFFLINE_STARTUP")
                print_log("INFO", "yellow", thread_number, "Offline dialog detected, clicking refresh...")
                driver.find_element(By.CSS_SELECTOR, 'button[data-test="dialog-offline-startup-refresh-button"]').click()
                time.sleep(3)  # Wait for page to reload
            except:
                pass  # Dialog not present, continue normally'''

            artist_name = None
            link = get_random_link()
            # Convert any tidal link format to desktop.tidal.com format
            # Supports: https://listen.tidal.com/album/123, https://tidal.com/album/123/u, etc.
            album_match = re.search(r'/album/(\d+)', link)
            if album_match:
                album_id = album_match.group(1)
                link = f'https://desktop.tidal.com/album/{album_id}'



            update_thread_status(thread_number, 'Loading link', None, False, False, False, False, False, None)
            if not str(link).__contains__('playlist'):
                artist_name, album_name, song_count = scrape_link_infos(thread_number, driver, link, driver_instance_port)
            
            executable_path = os.path.join(project_dir, 'Files', 'manage.exe')
            try:
                command = [executable_path, '--port', str(driver_instance_port), '--action', 'show']
                subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
            
            if str(config_optimize_tidal_app).lower().__contains__('false'):
                try:
                    element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.ID, 'sidebar'))
                    )
                except:
                    pass

            if random.randrange(100) < int(config_search_links_perc): #
                search_input = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="search-popover-search-field"]'))
                )
                actions = ActionChains(driver)
                actions.move_to_element(search_input).click().perform()
                search_input.clear()
                if str(link).__contains__('playlist'):
                    search_input.send_keys(link)
                    search_input.send_keys(Keys.RETURN)
                else:
                    #<a class="_link_222030a _disableUnderline_8e517ad" data-test="search-results-top-hit-373248804-link" draggable="false" href="/album/373248804" rel="noreferrer" target="_self"><span class="_visuallyHidden_af361da">album</span></a>
                    if artist_name is not None:
                        search_input.send_keys(f'{album_name} {artist_name}')
                        search_input.send_keys(Keys.RETURN)

                        found = False
                        for i in range(15):
                            try:
                                # If "no results" shows up, bail early
                                WebDriverWait(driver, 1).until(
                                    EC.presence_of_element_located(
                                        (By.CSS_SELECTOR, '[data-test="search-results-empty"]'))
                                )
                                break
                            except:
                                pass

                            try:
                                WebDriverWait(driver, 1).until(
                                    #data-test=""
                                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="search-results-top"]'))
                                )
                                found = True
                                break
                            except:
                                pass

                        if not found:
                            print_log("EXC.", "yellow", thread_number,
                                      f'Failed to load link: {link}, no search results found.')
                            return False, 0, None

                        # Instead of clicking the span wrapper, click its sibling <a data-test="…-link">:
                        link_locator = (
                            By.CSS_SELECTOR,
                            'a[data-test^="search-results-top-hit"][data-test$="-link"]'
                        )
                        result_link = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(link_locator)
                        )

                        # Scroll into view to avoid overlays
                        driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});",
                            result_link
                        )

                        # Click it (JS fallback if Selenium's click is intercepted)
                        try:
                            result_link.click()
                        except Exception:
                            driver.execute_script("arguments[0].click();", result_link)

                    else:
                        search_input.send_keys(link)
                        search_input.send_keys(Keys.RETURN)
            else:
                driver.get(link)

            try:
                page_not_found = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="page-not-found"]'))
                )
                print_log("EXC.", "yellow", thread_number, f'Failed to load link: {str(link)}, Not found.')
                return False, 0, None
            except:
                pass

            title_element = None
            for title_sel in ['h2[data-test="title"]', 'h1[data-test="title"]', '[data-test="title"]', 'h1']:
                try:
                    title_element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, title_sel))
                    )
                    break
                except:
                    pass
            if not title_element:
                notification_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.notification--hckxF[data-test="notification"]'))
                )
                if notification_element.is_displayed():
                    notification_text = notification_element.text
                    if "nicht mehr verfügbar" in notification_text:
                        print_log("EXC.", "yellow", thread_number, f'Failed to load link: {str(link)}, Not found.')
                        return False, 0, None
                for title_sel in ['h2[data-test="title"]', 'h1[data-test="title"]', '[data-test="title"]', 'h1']:
                    try:
                        title_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, title_sel))
                        )
                        break
                    except:
                        pass
            if not title_element:
                print_log("ERR.", "yellow", thread_number, f'Could not find title element for link: {link}')
                return False, 0, None


            def add_to_playlist():
                driver.find_element(By.CSS_SELECTOR, '[data-test="show-context-menu-button"]').click() #
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, '[data-test="add-to-playlist"]').click()
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, 'button[data-test="sub-menu-item-recent-playlist-0"]').click()

                driver.implicitly_wait(1)
                while True:
                    try:
                        driver.find_element(By.CSS_SELECTOR, '[data-test="confirm"]').click()
                        break
                    except:
                        pass
                    try:
                        title_element = WebDriverWait(driver, 1).until(
                            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[4]/div/div/button'))
                        )
                        print(f'Added to playlist | {len(links_list)}')
                        break
                    except:
                        pass


                load_link(thread_number, driver, driver_instance_port)


            if str(config_optimize_tidal_app).lower().__contains__('true'):
                script = """
                        var stylesheets = document.styleSheets;
                        for (var i = 0; i < stylesheets.length; i++) {
                            try {
                                stylesheets[i].disabled = true;
                            } catch (e) {}
                        }
                        // Remove element by data-test ID
                        var sidebarWrapper = document.querySelector('[data-test="main-layout-sidebar-wrapper"]');
                        if (sidebarWrapper) {
                            sidebarWrapper.remove();
                        }

                        // Remove image element with specific classes
                        var coverArtImages = document.querySelectorAll('img[data-test="cover-art"]');
                        coverArtImages.forEach(function(image) {
                            image.remove();
                        });

                        const cellImages = document.querySelectorAll('[class*="cellImage"]');
                        cellImages.forEach(element => {
                            element.remove();
                        });

                        const svgElements = document.querySelectorAll('svg');
                        svgElements.forEach(element => {
                            element.remove();
                        });

                        const fullscreenElements = document.querySelectorAll('[class*="fullscreen"]');
                        fullscreenElements.forEach(element => {
                            element.remove();
                        });

                        // Add CSS to body
                        document.body.style.webkitAppRegion = 'drag';
                        """
                try:
                    driver.execute_script(script)
                except:
                    pass

            title_text = title_element.text
            artist_text = ""
            for sel in [
                '[data-test-module-type="ALBUM_HEADER"] [data-test="grid-item-detail-text-title-artist"]',
                '[data-test="grid-item-detail-text-title-artist"]',
                '[data-test="artist-link"]',
                '[data-test="album-header-artist"]',
            ]:
                try:
                    artist_text = driver.find_element(By.CSS_SELECTOR, sel).text
                    break
                except:
                    pass
            song_count = 1
            for sel in [
                '[data-test-module-type="ALBUM_HEADER"] [data-test="grid-item-meta-item-count"]',
                '[data-test="grid-item-meta-item-count"]',
                '[data-test="track-count"]',
            ]:
                try:
                    el = driver.find_element(By.CSS_SELECTOR, sel)
                    m = re.search(r'\d+', el.text)
                    if m:
                        song_count = int(m.group())
                    break
                except:
                    pass

            if song_count == 1:
                print_log("SUCC", "gray", thread_number,
                          f'Loaded new link {title_text} by {artist_text} with {song_count} song')
            else:
                print_log("SUCC", "gray", thread_number,
                          f'Loaded new link {title_text} by {artist_text} with {song_count} songs')

            if random.randrange(100) < int(config_album_likes_rate):
                favorite_btn = driver.find_element(By.CSS_SELECTOR, '[data-test="favorite-button"]')
                if favorite_btn.get_attribute('aria-checked') != 'true':
                    favorite_btn.click()
                    global worker_album_likes
                    worker_album_likes += 1
                    update_thread_status(thread_number, None, None, False, False, True, False, False, None)

            play_by_shuffle = False
            if random.randrange(100) < int(config_shuffle_perc):
                play_by_shuffle = True
                shufflebtn = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="shuffle-all"]'))
                )
                driver.execute_script("arguments[0].click();", shufflebtn)
            else:
                playbtn = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="play-all"]'))
                )
                driver.execute_script("arguments[0].click();", playbtn)



            started_playing = True
            def check_song_starts_playing():
                driver.implicitly_wait(5)
                current_time_element_old = driver.find_element(By.CSS_SELECTOR, 'time[data-test="current-time"]').text
                driver.implicitly_wait(1)
                for i in range(15):
                    driver.implicitly_wait(1)
                    try:
                        notification = driver.find_element(By.CSS_SELECTOR, 'time[data-test="current-time"]').text
                        if "paus" in str(notification):
                            return False, 0, 'in-use'
                    except:
                        pass


                    current_time_element = driver.find_element(By.CSS_SELECTOR, 'time[data-test="current-time"]').text

                    # Check if the time has changed, indicating that the song is playing
                    if current_time_element_old != current_time_element:
                        break
                    else:
                        current_time_element_old = current_time_element
                        time.sleep(1)  # Wait for 1 second before checking again
                else:
                    print_log("EXC.", "yellow", thread_number, 'Song did not start playing within 30 seconds')
                    started_playing = False

            check_song_starts_playing()
            if started_playing is False:
                close_upsell(driver)
                if play_by_shuffle is True:
                    shufflebtn = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="shuffle-all"]'))
                    )
                    driver.execute_script("arguments[0].click();", shufflebtn)
                else:
                    playbtn = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="play-all"]'))
                    )
                    driver.execute_script("arguments[0].click();", playbtn)
                check_song_starts_playing()
            
            close_upsell(driver)
            repeat_btn = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="repeat"]'))
                    )
            data_type = repeat_btn.get_attribute("data-type")
            if data_type == "button__repeatSingle":
                clicks = 2
            elif data_type == "button__repeatOff":
                clicks = 1
            else:
                clicks = 0  # Or handle as needed

            # Click the button required number of times
            for _ in range(clicks):
                driver.execute_script("arguments[0].click();", repeat_btn)
                time.sleep(0.5)  # Slight delay to allow UI to update

            return True, song_count, None
        except Exception as e:
            '''# Check if offline dialog is showing and click refresh if needed
            try:
                driver.find_element(By.ID, "OFFLINE_STARTUP")
                print_log("INFO", "yellow", f"Thread {thread_number}", "Offline dialog detected, clicking refresh...")
                driver.find_element(By.CSS_SELECTOR, 'button[data-test="dialog-offline-startup-refresh-button"]').click()
                time.sleep(3)  # Wait for page to reload
            except:
                pass  # Dialog not present, continue normally'''
            print_log("ERR.", "red", thread_number, f'Error occurred in Load link function: {str(e)}')
            if str(e).__contains__('Message: Stacktrace: GetHandleVerifier '):
                return False, 0, 'restart'
            global worker_bot_errors
            worker_bot_errors += 1
            update_thread_status(thread_number, None, None, False, False, False, False, True, None)
            return False, 0, None


    def close_upsell(driver):
        try:
            upsell = driver.find_element(By.CSS_SELECTOR, 'dialog[data-test="dialog"][id="UPSELL"]')
            if upsell.is_displayed():
                close_btn = upsell.find_element(By.CSS_SELECTOR, 'button[data-test="dialog-close-button"], button[aria-label*="Close"], button.close')
                driver.execute_script("arguments[0].click();", close_btn)
                time.sleep(1)
        except:
            pass

    def play_songs(thread_number, driver, song_count, ppa):
        try:
            driver.implicitly_wait(20)
            update_thread_status(thread_number, 'Streaming', None, False, False, False, False, False, None)
            close_upsell(driver)
            track_title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="footer-track-title"]'))
            )
            track_title_text = track_title_element.text

            # Locate the second element and get its text
            artist_name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="grid-item-detail-text-title-artist"]'))
            )
            artist_name_text = artist_name_element.text

            if random.randrange(100) < int(config_song_likes_rate):
                favorite_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="footer-favorite-button"]'))
                )
                favorite_button.click()
                print_log("SUCC", "gray", thread_number, f"Liked Song {track_title_text} by {artist_name_text}")
                global worker_song_likes
                worker_song_likes += 1
                update_thread_status(thread_number, None, None, False, False, True, False, False, None)

            if str(config_playtime_type).lower().__contains__('seconds'):
                playtime1, playtime2 = map(int, str(config_playtime_seconds).split('-'))

                finalplaytime = playtime1 if playtime1 == playtime2 else random.randrange(playtime1, playtime2)

                for _ in range(finalplaytime):
                    driver.implicitly_wait(0)
                    try:
                        notification = driver.find_element(By.CSS_SELECTOR, 'time[data-test="current-time"]').text
                        if "paus" in str(notification):
                            return False, False, 'in-use'
                    except:
                        pass
                    time.sleep(1)
            else:
                percentage1, percentage2 = map(int, str(config_playtime_percentage).split('-'))

                percentage = percentage1 if percentage1 == percentage2 else random.randrange(percentage1, percentage2)

                def get_time_in_seconds(time_str):
                    minutes, seconds = map(int, time_str.split(':'))
                    return minutes * 60 + seconds

                try:
                    current_time_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'time[data-test="current-time"]'))
                    )
                    duration_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'time[data-test="duration"]'))
                    )

                    current_time_text = current_time_element.text
                    duration_text = duration_element.text
                    # print(f'current time: {current_time_text}/{duration_text}')

                    current_time_seconds = get_time_in_seconds(current_time_text)
                    duration_seconds = get_time_in_seconds(duration_text)

                    wait_time = int((duration_seconds * percentage / 100) - current_time_seconds)
                    if wait_time > 0:
                        # print(f"Waiting for {wait_time} seconds...")
                        for _ in range(wait_time):
                            driver.implicitly_wait(0)
                            try:
                                notification = driver.find_element(By.CSS_SELECTOR, 'time[data-test="current-time"]').text
                                if "paus" in str(notification):
                                    return False, False, 'in-use'
                            except:
                                pass
                            time.sleep(1)
                        # print("done now")
                    else:
                        pass
                        # print("The current time is already beyond the specified percentage of the song duration.")

                except TimeoutException:
                    print("Elements not found within the timeout period.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            driver.implicitly_wait(10)
            current_time_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'time[data-test="current-time"]'))
            ).text
            duration_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'time[data-test="duration"]'))
            ).text
            print_log("SUCC", "green", thread_number,
                      f"Streamed {track_title_text} by {artist_name_text} for {current_time_text}/{duration_text} | PPA: {ppa}")
            if song_count != 1:
                try:
                    upsell = driver.find_element(By.CSS_SELECTOR, 'dialog[data-test="dialog"][id="UPSELL"]')
                    if upsell.is_displayed():
                        close_btn = upsell.find_element(By.CSS_SELECTOR, 'button[data-test="dialog-close-button"], button[aria-label*="Close"], button.close')
                        driver.execute_script("arguments[0].click();", close_btn)
                        time.sleep(1)
                except:
                    pass
                nextBtn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next"]'))
                )
                driver.execute_script("arguments[0].click();", nextBtn)

            timestamp = datetime.now()
            send_stream_data_to_consumer(timestamp, 1, artist_name_text, track_title_text, current_time_text)

            update_thread_status(thread_number, None, None, False, True, False, False, False, None)
            return False, True, ''
        except Exception as e:
            global worker_bot_errors
            worker_bot_errors += 1
            print_log("ERR.", "red", thread_number, f'Error occurred in play song function: {str(e)}')
            update_thread_status(thread_number, None, None, False, False, False, False, True, None)
            if 'getattribute' in str(e).lower():
                return False, False, str(e)
            elif 'no such element' in str(e).lower():
                return False, False, str(e)
            elif 'is not clickable at point' in str(e).lower():
                return False, False, str(e)


            return True, False, str(e)


    def get_random_proxy():
        proxy = random.choice(worker_loaded_proxies)
        return proxy

    def get_random_login_proxy():
        """Get a random login proxy (typically residential for bypassing auth detection)"""
        proxy = random.choice(worker_loaded_login_proxies)
        return proxy

    def get_random_streaming_proxy():
        """Get a streaming proxy, preferring unused ones, or the least used if all are in use."""
        with streaming_proxy_usage_lock:
            if not worker_loaded_streaming_proxies:
                print_log("EXC.", "red", "Main", "No streaming proxies loaded! Check your proxy batch config.")
                return None
            # Find proxies with 0 usage (not in use)
            available_proxies = [p for p in worker_loaded_streaming_proxies if streaming_proxy_usage.get(p, 0) == 0]
            
            if available_proxies:
                # Pick a random unused proxy
                proxy = random.choice(available_proxies)
            else:
                # All proxies are in use - pick the least used one
                min_usage = min(streaming_proxy_usage.get(p, 0) for p in worker_loaded_streaming_proxies)
                least_used = [p for p in worker_loaded_streaming_proxies if streaming_proxy_usage.get(p, 0) == min_usage]
                proxy = random.choice(least_used)
                print_log("INFO", "yellow", "Main", f"All streaming proxies in use - reusing least used proxy (usage: {min_usage})")
            
            # Increment usage count
            streaming_proxy_usage[proxy] = streaming_proxy_usage.get(proxy, 0) + 1
            return proxy

    def release_streaming_proxy(proxy):
        """Release a streaming proxy by decrementing its usage count."""
        with streaming_proxy_usage_lock:
            if proxy in streaming_proxy_usage:
                streaming_proxy_usage[proxy] = max(0, streaming_proxy_usage[proxy] - 1)
                print_log("INFO", "blue", "Main", f"Released streaming proxy: {proxy.split(':')[0]} (usage now: {streaming_proxy_usage[proxy]})")


    def get_random_account():
        """Get a random account that is not already in use by another thread."""
        with used_accounts_lock:
            # Filter out accounts that are already in use
            available_accounts = [acc for acc in worker_loaded_accounts if acc not in used_accounts]
            if not available_accounts:
                raise Exception("No available accounts left - all accounts are in use by other threads")
            account = random.choice(available_accounts)
            used_accounts.add(account)
            return account
    
    def release_account(account):
        """Release an account so it can be used by another thread."""
        with used_accounts_lock:
            if account in used_accounts:
                used_accounts.discard(account)
                email = account.split(":")[0] if ":" in account else account
                print_log("INFO", "green", None, f"Released account: {email}")


    def get_random_link():
        link = random.choice(worker_loaded_link)
        return link


    def get_hwnd_for_pid(pid):
        def callback(hwnd, hwnds):
            tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
            if current_pid == pid and win32gui.IsWindowVisible(hwnd):
                hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds[0] if hwnds else None

    def mute_executable(pid):
        try:
            hwnd = get_hwnd_for_pid(pid)
            if hwnd:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
                win32gui.SetForegroundWindow(hwnd)
            else:
                print("Window not found.")
        except:
            pass

    def get_used_accounts(project_dir):
        """
        Go through all folders in the 'Sessions' directory, check if 'account.txt' exists
        and contains valid email:password combinations, and return a list of accounts.

        Args:
            project_dir (str): The base project directory.

        Returns:
            list: A list of valid email:password pairs.
        """
        used_accounts = []  # To store accounts found in the Sessions folder
        sessions_dir = os.path.join(project_dir, 'Files', 'Sessions')  # Path to Sessions folder

        # Iterate through all subdirectories in the Sessions folder
        for folder_name in os.listdir(sessions_dir):
            folder_path = os.path.join(sessions_dir, folder_name)

            # Check if it's a directory
            if os.path.isdir(folder_path):
                # Construct the path to account.txt
                account_file = os.path.join(folder_path, 'account.txt')

                # Check if the account.txt file exists
                if os.path.exists(account_file):
                    # Read the file and extract email:password pairs
                    with open(account_file, 'r') as file:
                        for line in file:
                            line = line.strip()  # Remove any extra whitespace
                            if ":" in line:  # Check if it contains an email:password separator
                                email, password = line.split(":", 1)  # Split on the first ':'
                                used_accounts.append((email, password))  # Add the account to the list

        return used_accounts

    def thread_function(thread_number):
        while True:
            try:
                print_log("INFO", "blue", thread_number, f'Started thread {thread_number}')
                while not stop_flags.get(thread_number, False):
                    local_proxyline = None
                    proxy_asyncio_loop = None
                    proxy_server_thread = None
                    proxy = '/'
                    Account = None
                    driver = None
                    service = None
                    options = None
                    tidal_instance = None
                    protocol = None
                    current_account_string = None  # Track the account in use for this thread
                    current_streaming_proxy = None  # Track the streaming proxy in use for this thread
                    tidal_launch_failed = False  # Flag to track if Tidal failed to launch
                    port_manager = PortManager()
                    if str(config_stay_logged_in).lower().__contains__('true'):
                        stay_logged_in = True
                    else:
                        stay_logged_in = False


                    while True:
                        tidal_instance_port = port_manager.use_free_port()
                        driver_instance_port = port_manager.use_free_port()
                        proxy_server_port = port_manager.use_free_port()

                        # Use global account manager (shared across all threads)
                        account_manager = global_account_manager

                        acc_type = None  # set by check_account_type; None if login failed before check

                        print_log("INFO", "blue", thread_number, f'Thread started with free ports [{tidal_instance_port}, {driver_instance_port}, {proxy_server_port}]')
                        def set_proxy(max_attempts=10):
                            for attempt in range(max_attempts):
                                proxy = get_random_proxy()  # Replace this with your proxy
                                protocol, msg = determine_proxy_protocol(proxy)
                                if protocol is None:
                                    print_log("EXC.", "yellow", thread_number, f'Failed to check proxy protocol for proxy {proxy} (attempt {attempt+1}/{max_attempts})')
                                    continue
                                else:
                                    print_log("INFO", "blue", thread_number, f'Proxy Protocol for {proxy} is {protocol}')
                                
                                parts = proxy.split(":")
                                if len(parts) != 2:
                                    proxy_asyncio_loop, proxy_server_thread, local_proxyline = start_proxy_server(proxy, protocol, proxy_server_port)
                                    if local_proxyline is None:
                                        print_log("EXC.", "yellow", thread_number, f'Failed to start proxy server for {proxy}, trying another... (attempt {attempt+1}/{max_attempts})')
                                        continue
                                    return True, proxy_asyncio_loop, proxy_server_thread, local_proxyline, proxy
                                else:
                                    local_proxyline = f'http://{proxy}'
                                    return True, None, None, local_proxyline, proxy
                            # All attempts failed
                            print_log("ERR.", "red", thread_number, f'Failed to set up proxy after {max_attempts} attempts')
                            return False, None, None, None, None

                        def set_login_proxy(max_attempts=10):
                            """Set up a login proxy (residential) for authentication"""
                            for attempt in range(max_attempts):
                                proxy = get_random_login_proxy()
                                protocol, msg = determine_proxy_protocol(proxy)
                                if protocol is None:
                                    print_log("EXC.", "yellow", thread_number, f'Failed to check login proxy protocol for {proxy} (attempt {attempt+1}/{max_attempts})')
                                    continue
                                else:
                                    print_log("INFO", "blue", thread_number, f'Login Proxy Protocol for {proxy} is {protocol}')
                                
                                parts = proxy.split(":")
                                if len(parts) != 2:
                                    proxy_asyncio_loop, proxy_server_thread, local_proxyline = start_proxy_server(proxy, protocol, proxy_server_port)
                                    if local_proxyline is None:
                                        print_log("EXC.", "yellow", thread_number, f'Failed to start proxy server for {proxy}, trying another... (attempt {attempt+1}/{max_attempts})')
                                        continue
                                    return True, proxy_asyncio_loop, proxy_server_thread, local_proxyline, proxy
                                else:
                                    local_proxyline = f'http://{proxy}'
                                    return True, None, None, local_proxyline, proxy
                            # All attempts failed
                            print_log("ERR.", "red", thread_number, f'Failed to set up login proxy after {max_attempts} attempts')
                            return False, None, None, None, None

                        def set_streaming_proxy(port=None, max_attempts=10):
                            """Set up a streaming proxy (datacenter) for playback"""
                            use_port = port if port is not None else proxy_server_port
                            for attempt in range(max_attempts):
                                proxy = get_random_streaming_proxy()
                                protocol, msg = determine_proxy_protocol(proxy)
                                if protocol is None:
                                    print_log("EXC.", "yellow", thread_number, f'Failed to check streaming proxy protocol for {proxy} (attempt {attempt+1}/{max_attempts})')
                                    continue
                                else:
                                    print_log("INFO", "blue", thread_number, f'Streaming Proxy Protocol for {proxy} is {protocol}')
                                
                                parts = proxy.split(":")
                                if len(parts) != 2:
                                    proxy_asyncio_loop, proxy_server_thread, local_proxyline = start_proxy_server(proxy, protocol, use_port)
                                    if local_proxyline is None:
                                        print_log("EXC.", "yellow", thread_number, f'Failed to start proxy server for {proxy}, trying another... (attempt {attempt+1}/{max_attempts})')
                                        continue
                                    return True, proxy_asyncio_loop, proxy_server_thread, local_proxyline, proxy
                                else:
                                    local_proxyline = f'http://{proxy}'
                                    return True, None, None, local_proxyline, proxy
                            # All attempts failed
                            print_log("ERR.", "red", thread_number, f'Failed to set up streaming proxy after {max_attempts} attempts')
                            return False, None, None, None, None

                        # Determine which proxy mode to use
                        use_dual_proxies = str(config_use_dual_proxies).lower().__contains__('true')
                        use_proxyless_login = str(config_proxyless_login).lower().__contains__('true')

                        # Dynamic proxy relay for seamless proxy switching
                        dynamic_relay = None

                        if use_proxyless_login:
                            # Login via relay in direct mode (no upstream), will switch to streaming proxy after login
                            print_log("INFO", "blue", thread_number, 'Using proxyless login mode: relay in direct mode for authentication')
                            dynamic_relay = DynamicProxyRelay(proxy_server_port)
                            local_proxyline = dynamic_relay.start_direct()
                            proxy = 'proxyless (direct relay)'
                        elif use_dual_proxies:
                            # Use login proxy via relay, will switch to streaming proxy after login
                            print_log("INFO", "blue", thread_number, 'Using dual proxy mode: relay with login proxy for authentication')
                            dynamic_relay = DynamicProxyRelay(proxy_server_port)
                            
                            # Get login proxy and its protocol
                            login_proxy = get_random_login_proxy()
                            login_protocol, msg = determine_proxy_protocol(login_proxy)
                            if login_protocol is None:
                                print_log("EXC.", "yellow", thread_number, f'Failed to check login proxy protocol for {login_proxy}')
                                # Release ports before continuing
                                port_manager.remove_port(tidal_instance_port)
                                port_manager.remove_port(driver_instance_port)
                                port_manager.remove_port(proxy_server_port)
                                continue
                            print_log("INFO", "blue", thread_number, f'Login Proxy Protocol for {login_proxy} is {login_protocol}')
                            
                            # Start relay with login proxy
                            success, relay_ip = dynamic_relay.switch_to_proxy(login_proxy, login_protocol)
                            if not success:
                                print_log("ERR.", "red", thread_number, f'Failed to start relay with login proxy {login_proxy}')
                                dynamic_relay.stop()
                                # Release ports before continuing
                                port_manager.remove_port(tidal_instance_port)
                                port_manager.remove_port(driver_instance_port)
                                port_manager.remove_port(proxy_server_port)
                                continue
                            
                            local_proxyline = dynamic_relay.get_local_proxy()
                            proxy = login_proxy
                        elif str(config_use_proxies).lower().__contains__('true'):
                            success, proxy_asyncio_loop, proxy_server_thread, local_proxyline, proxy = set_proxy()
                            if not success:
                                print_log("ERR.", "red", thread_number, 'All proxies failed, retrying thread...')
                                # Release ports before continuing
                                port_manager.remove_port(tidal_instance_port)
                                port_manager.remove_port(driver_instance_port)
                                port_manager.remove_port(proxy_server_port)
                                time.sleep(5)  # Brief cooldown before retry
                                continue


                        update_thread_status(thread_number, 'Starting', proxy, False, False, False, False, False, None)
                        email, password, current_account_string, session_folder = account_manager.get_free_account(stay_logged_in, thread_number)
                        attempts = 0
                        max_attempts = 3
                        while attempts < max_attempts:
                            attempts += 1
                            tidal_instance = start_tidal(thread_number, local_proxyline, session_folder, driver_instance_port)
                            if tidal_instance is None:
                                print_log("EXC.", "yellow", thread_number, f'Failed to launch Tidal instance (Attempt {attempts}/{max_attempts})')
                                clean_driver_and_tidal(thread_number, None, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, False, tidal_instance)
                                # Wait for port to be released before retrying
                                time.sleep(2)
                                
                                # Handle retry with different proxy based on mode
                                if use_dual_proxies and dynamic_relay is not None:
                                    # Switch relay to a different login proxy
                                    new_login_proxy = get_random_login_proxy()
                                    new_login_protocol, msg = determine_proxy_protocol(new_login_proxy)
                                    if new_login_protocol is not None:
                                        print_log("INFO", "blue", thread_number, f'Switching relay to different login proxy: {new_login_proxy}')
                                        success, relay_ip = dynamic_relay.switch_to_proxy(new_login_proxy, new_login_protocol)
                                        if success:
                                            proxy = new_login_proxy
                                            print_log("INFO", "blue", thread_number, f'Relay switched to new login proxy')
                                        else:
                                            print_log("WARN", "yellow", thread_number, f'Failed to switch relay to new login proxy')
                                    else:
                                        print_log("WARN", "yellow", thread_number, f'Failed to check new login proxy protocol')
                                elif use_proxyless_login and dynamic_relay is not None:
                                    # Proxyless mode - relay is in direct mode, no switch needed
                                    print_log("INFO", "blue", thread_number, 'Retrying Tidal launch (proxyless mode, relay unchanged)')
                                elif str(config_use_proxies).lower().__contains__('true'):
                                    # Regular proxy mode - switch to different proxy
                                    success, proxy_asyncio_loop, proxy_server_thread, local_proxyline, proxy = set_proxy()
                                    if not success:
                                        print_log("WARN", "yellow", thread_number, f'Failed to set up new proxy, continuing with next attempt')
                            else:
                                print_log("INFO", "blue", thread_number, 'Tidal Instance launched and ready to be connected!')
                                break
                        else:
                            print_log("ERR.", "red", thread_number, f"Tidal failed to launch after {max_attempts} attempts, cleaning folder!")
                            clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                            tidal_launch_failed = True
                            # Release account before breaking since we're exiting the while True loop
                            if current_account_string is not None:
                                release_account(current_account_string)
                                current_account_string = None
                            # Stop dynamic relay if it was used
                            if dynamic_relay is not None:
                                try:
                                    dynamic_relay.stop()
                                except:
                                    pass
                            break

                        update_thread_status(thread_number, 'Started', None, False, False, False, False, False, tidal_instance.pid)

                        driver, service, options = start_driver(driver_instance_port, thread_number)
                        if driver is None:
                            print_log("ERR.", "red", thread_number, f'Failed to start driver: {options}')
                            clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                            tidal_launch_failed = True
                            # Release account before breaking since we're exiting the while True loop
                            if current_account_string is not None:
                                release_account(current_account_string)
                                current_account_string = None
                            # Stop dynamic relay if it was used
                            if dynamic_relay is not None:
                                try:
                                    dynamic_relay.stop()
                                except:
                                    pass
                            break
                        else:
                            break
                    #input(f"Done with driver setup, press enter to continue | {driver_instance_port}")
                    
                    # If Tidal/driver failed to launch, skip rest and retry
                    if tidal_launch_failed:
                        if dynamic_relay:
                            dynamic_relay.stop()
                        # Release account before retrying
                        if current_account_string is not None:
                            release_account(current_account_string)
                            current_account_string = None
                        continue
                    

                    if str(config_hide_tidal_app).lower().__contains__('true'):
                        executable_path = os.path.join(project_dir, 'Files', 'manage.exe')
                        try:
                            command = [executable_path, '--port', str(driver_instance_port), '--action', 'hide']
                            subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
                        except:
                            pass

                    logged_in_before = False
                    if str(config_stay_logged_in).lower().__contains__('true'):
                        login_result = check_logged_in(thread_number, driver)
                        if login_result is True:
                            print_log("INFO", "green", thread_number, f'Account is still logged in.')
                            logged_in_before = True

                            # If proxyless login or dual proxies enabled and already logged in, switch to streaming proxy immediately
                            if use_proxyless_login or use_dual_proxies:
                                print_log("INFO", "blue", thread_number, 'Already logged in, switching to streaming proxy...')

                                # Close the current driver
                                try:
                                    driver.quit()
                                except:
                                    pass

                                # Kill the tidal instance (but keep session folder!)
                                kill_tidal_process(tidal_instance)

                                # Stop the login proxy server completely (only if dual proxies mode)
                                if use_dual_proxies and proxy_asyncio_loop is not None:
                                    try:
                                        proxy_asyncio_loop.call_soon_threadsafe(proxy_asyncio_loop.stop)
                                        proxy_server_thread.join(timeout=10)
                                        proxy_asyncio_loop.close()
                                        print_log("INFO", "blue", thread_number, 'Login proxy server stopped.')
                                    except Exception as e:
                                        print_log("WARN", "yellow", thread_number, f'Error stopping login proxy: {e}')
                                    finally:
                                        proxy_asyncio_loop = None
                                        proxy_server_thread = None
                                    # Release the old proxy port
                                    port_manager.remove_port(proxy_server_port)

                                # Get a port for streaming proxy
                                streaming_proxy_port = port_manager.use_free_port()
                                print_log("INFO", "blue", thread_number, f'Using port {streaming_proxy_port} for streaming proxy')

                                # Wait a moment for cleanup
                                time.sleep(2)

                                # Start streaming proxy with new port
                                set, proxy_asyncio_loop, proxy_server_thread, local_proxyline, proxy = set_streaming_proxy(streaming_proxy_port)
                                current_streaming_proxy = proxy  # Track for cleanup

                                # Restart tidal with streaming proxy
                                tidal_instance = start_tidal(thread_number, local_proxyline, session_folder, driver_instance_port)
                                if tidal_instance is None:
                                    print_log("ERR.", "red", thread_number, 'Failed to restart Tidal with streaming proxy!')
                                    clean_driver_and_tidal(thread_number, None, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    # Release account before exiting
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    break

                                # Reconnect the driver
                                driver, service, options = start_driver(driver_instance_port, thread_number)
                                if driver is None:
                                    print_log("ERR.", "red", thread_number, 'Failed to reconnect driver after proxy switch!')
                                    clean_driver_and_tidal(thread_number, None, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    # Release account before exiting
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    break

                                print_log("INFO", "green", thread_number, f'Switched to streaming proxy: {proxy}')
                                
                                # Update UI status with new streaming proxy
                                update_thread_status(thread_number, 'Streaming', proxy, False, False, False, False, False, tidal_instance.pid if tidal_instance else None)

                                # Verify still logged in
                                time.sleep(3)
                                login_result = check_logged_in(thread_number, driver)
                                if not login_result:
                                    print_log("ERR.", "red", thread_number, 'Session lost after proxy switch!')
                                    logged_in_before = False

                            acc_type = check_account_type(thread_number, driver, driver_instance_port)
                            # Already-logged-in path: no relay to cycle, use default if proxy blocked
                            if acc_type == ACC_TYPE_PROXY_BLOCKED:
                                acc_type = "TIDAL Individual"
                            if acc_type is None:
                                acc_type = "TIDAL Individual"
                            if acc_type is False:
                                login_result = False
                                # Intro detected while already logged in: clean up and remove session to avoid reuse loop
                                print_log("INFO", "blue", thread_number, "TIDAL Intro detected (already logged in) – removing session and cleaning up")
                                clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                try:
                                    if session_folder and os.path.exists(session_folder):
                                        shutil.rmtree(session_folder)
                                        print_log("INFO", "blue", thread_number, "Removed Intro account session folder")
                                except Exception as e:
                                    print_log("WARN", "yellow", thread_number, f"Could not remove Intro session folder: {e}")
                                if current_account_string is not None:
                                    release_account(current_account_string)
                                    current_account_string = None
                                if dynamic_relay is not None:
                                    try:
                                        dynamic_relay.stop()
                                    except:
                                        pass
                        else:
                            print_log("ERR.", "red", thread_number, f'Account is logged out!')


                    if logged_in_before is False:
                        # Pass local_proxyline (relay or http://ip:port) so the login browser uses a supported proxy.
                        # Chrome does not support proxy auth in --proxy-server; raw ip:port:user:pass causes ERR_NO_SUPPORTED_PROXIES.
                        # Stagger login attempts so not all threads hit Tidal at the same time (DataDome will ban the IP)
                        stagger = random.uniform(3, 15)
                        print_log("INFO", "cyan", thread_number, f"Waiting {stagger:.1f}s stagger + login semaphore...")
                        time.sleep(stagger)
                        login_semaphore.acquire()
                        try:
                            # Batch login limiter: after 8-11 logins, wait 7-11 minutes before next batch
                            global worker_login_batch_count, worker_login_batch_timestamp, worker_login_batch_max
                            if worker_login_batch_max == 0:
                                worker_login_batch_max = 5
                                worker_login_batch_timestamp = time.time()
                            if worker_login_batch_count >= worker_login_batch_max:
                                elapsed = time.time() - worker_login_batch_timestamp
                                wait_minutes = random.randint(7, 10)
                                wait_seconds = max(0, wait_minutes * 60 - elapsed)
                                print_log("INFO", "yellow", thread_number, f"Batch limit {worker_login_batch_max} reached, waiting {wait_seconds/60:.1f} min before next batch...")
                                time.sleep(wait_seconds)
                                worker_login_batch_count = 0
                                worker_login_batch_max = 5
                                worker_login_batch_timestamp = time.time()
                            driver, login_account_fatal_error, login_result, login_return_msg = login_account(thread_number, driver, tidal_instance, local_proxyline, service, options, email, password, driver_instance_port, tidal_instance_port, account_manager)
                            if login_result:
                                worker_login_batch_count += 1
                                print_log("INFO", "green", thread_number, f"Login batch: {worker_login_batch_count}/{worker_login_batch_max}")
                        finally:
                            login_semaphore.release()

                    if login_result is True:
                        #worker_thread_logging_in = False

                        # Handle proxy switching after login
                        if logged_in_before is False:
                            
                            # DUAL PROXIES MODE: Seamless relay switch (NO Tidal restart!)
                            if use_dual_proxies and dynamic_relay is not None:
                                print_log("INFO", "blue", thread_number, 'Login successful! Switching relay to streaming proxy...')

                                # Get streaming proxy and its protocol - retry with different proxies if protocol check fails
                                max_protocol_check_attempts = 5
                                streaming_protocol = None
                                for protocol_attempt in range(max_protocol_check_attempts):
                                    streaming_proxy = get_random_streaming_proxy()
                                    if streaming_proxy is None:
                                        print_log("ERR.", "red", thread_number, "No streaming proxies available — check your proxy batch")
                                        clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                        if dynamic_relay:
                                            dynamic_relay.stop()
                                        if current_account_string is not None:
                                            release_account(current_account_string)
                                            current_account_string = None
                                        break
                                    current_streaming_proxy = streaming_proxy  # Track for cleanup
                                    streaming_protocol, msg = determine_proxy_protocol(streaming_proxy)
                                    if streaming_protocol is None:
                                        print_log("EXC.", "yellow", thread_number, f'Failed to check streaming proxy protocol for {streaming_proxy} (attempt {protocol_attempt + 1}/{max_protocol_check_attempts})')
                                        # Release this proxy and try another
                                        if current_streaming_proxy is not None:
                                            release_streaming_proxy(current_streaming_proxy)
                                            current_streaming_proxy = None
                                        if protocol_attempt < max_protocol_check_attempts - 1:
                                            continue
                                    else:
                                        break
                                
                                if streaming_protocol is None:
                                    print_log("ERR.", "red", thread_number, f'All streaming proxy protocol checks failed!')
                                    clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    if dynamic_relay:
                                        dynamic_relay.stop()
                                    # Release account before exiting
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    break
                                
                                print_log("INFO", "blue", thread_number, f'Streaming Proxy Protocol for {streaming_proxy} is {streaming_protocol}')

                                # Switch the relay to streaming proxy - Tidal stays running!
                                print_log("INFO", "blue", thread_number, 'Switching relay upstream to streaming proxy (no Tidal restart)...')
                                success, relay_ip = dynamic_relay.switch_to_proxy(streaming_proxy, streaming_protocol)
                                
                                if success:
                                    print_log("SUCC", "green", thread_number, f'Relay switched to streaming proxy: {streaming_proxy}')
                                    print_log("INFO", "blue", thread_number, f'New IP via relay: {relay_ip}')
                                    proxy = streaming_proxy
                                    # Update thread status with new proxy
                                    update_thread_status(thread_number, None, streaming_proxy, False, False, False, False, False, None)
                                else:
                                    print_log("ERR.", "red", thread_number, f'Failed to switch relay to streaming proxy!')
                                    clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    if dynamic_relay:
                                        dynamic_relay.stop()
                                    # Release account before exiting
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    break

                                # Brief wait for relay to stabilize
                                time.sleep(2)
                                
                                # Navigate to home to trigger new requests through the streaming proxy
                                # Retry with different streaming proxies if CDN blocks the proxy
                                max_streaming_proxy_attempts = 3
                                streaming_proxy_success = False
                                
                                for streaming_attempt in range(max_streaming_proxy_attempts):
                                    try:
                                        driver.get("https://desktop.tidal.com/home")
                                        time.sleep(3)
                                        
                                        # Check for Access Denied error (CDN blocking proxy)
                                        page_source = driver.page_source
                                        if '<Code>AccessDenied</Code>' in page_source or 'Access Denied' in page_source:
                                            print_log("WARN", "yellow", thread_number, f'Streaming proxy blocked by CDN (attempt {streaming_attempt + 1}/{max_streaming_proxy_attempts})')
                                            
                                            if streaming_attempt < max_streaming_proxy_attempts - 1:
                                                # Release the old streaming proxy before getting a new one
                                                if current_streaming_proxy is not None:
                                                    release_streaming_proxy(current_streaming_proxy)
                                                # Try a different streaming proxy
                                                streaming_proxy = get_random_streaming_proxy()
                                                current_streaming_proxy = streaming_proxy  # Track new proxy
                                                streaming_protocol, msg = determine_proxy_protocol(streaming_proxy)
                                                if streaming_protocol:
                                                    print_log("INFO", "blue", thread_number, f'Trying different streaming proxy: {streaming_proxy}')
                                                    success, relay_ip = dynamic_relay.switch_to_proxy(streaming_proxy, streaming_protocol)
                                                    if success:
                                                        print_log("INFO", "blue", thread_number, f'Switched to new streaming proxy, retrying...')
                                                        time.sleep(2)
                                                        continue
                                            
                                            # All attempts failed
                                            print_log("ERR.", "red", thread_number, f'All streaming proxies blocked by CDN!')
                                            break
                                        else:
                                            # No Access Denied - proxy works
                                            streaming_proxy_success = True
                                            break
                                            
                                    except Exception as e:
                                        print_log("WARN", "yellow", thread_number, f'Error navigating to home: {e}')
                                        break
                                
                                if not streaming_proxy_success:
                                    print_log("ERR.", "red", thread_number, 'Failed to find working streaming proxy!')
                                    clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    if dynamic_relay:
                                        dynamic_relay.stop()
                                    # Release account before exiting
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    break

                                # Verify we're still logged in (should be since we didn't restart Tidal)
                                print_log("INFO", "blue", thread_number, 'Verifying session after relay switch...')
                                still_logged_in = check_logged_in(thread_number, driver)
                                if not still_logged_in:
                                    print_log("ERR.", "red", thread_number, 'Session lost after relay switch!')
                                    clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    if dynamic_relay:
                                        dynamic_relay.stop()
                                    # Release account before exiting
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    break
                                else:
                                    print_log("SUCC", "green", thread_number, 'Session verified - still logged in after relay switch!')

                            # PROXYLESS MODE: Seamless relay switch from direct to upstream (NO Tidal restart!)
                            elif use_proxyless_login and dynamic_relay is not None:
                                print_log("INFO", "blue", thread_number, 'Login successful! Switching relay from direct to streaming proxy...')

                                # Get streaming proxy and its protocol - retry with different proxies if protocol check fails
                                max_protocol_check_attempts = 5
                                streaming_protocol = None
                                for protocol_attempt in range(max_protocol_check_attempts):
                                    streaming_proxy = get_random_streaming_proxy()
                                    if streaming_proxy is None:
                                        print_log("ERR.", "red", thread_number, "No streaming proxies available — check your proxy batch")
                                        clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                        if dynamic_relay:
                                            dynamic_relay.stop()
                                        if current_account_string is not None:
                                            release_account(current_account_string)
                                            current_account_string = None
                                        break
                                    current_streaming_proxy = streaming_proxy  # Track for cleanup
                                    streaming_protocol, msg = determine_proxy_protocol(streaming_proxy)
                                    if streaming_protocol is None:
                                        print_log("EXC.", "yellow", thread_number, f'Failed to check streaming proxy protocol for {streaming_proxy} (attempt {protocol_attempt + 1}/{max_protocol_check_attempts})')
                                        # Release this proxy and try another
                                        if current_streaming_proxy is not None:
                                            release_streaming_proxy(current_streaming_proxy)
                                            current_streaming_proxy = None
                                        if protocol_attempt < max_protocol_check_attempts - 1:
                                            continue
                                    else:
                                        break
                                
                                if streaming_protocol is None:
                                    print_log("ERR.", "red", thread_number, f'All streaming proxy protocol checks failed!')
                                    clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    if dynamic_relay:
                                        dynamic_relay.stop()
                                    # Release account before exiting
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    break
                                
                                print_log("INFO", "blue", thread_number, f'Streaming Proxy Protocol for {streaming_proxy} is {streaming_protocol}')

                                # Switch the relay from direct to streaming proxy - Tidal stays running!
                                print_log("INFO", "blue", thread_number, 'Switching relay from direct to streaming proxy (no Tidal restart)...')
                                success, relay_ip = dynamic_relay.switch_to_proxy(streaming_proxy, streaming_protocol)
                                
                                if success:
                                    print_log("SUCC", "green", thread_number, f'Relay switched to streaming proxy: {streaming_proxy}')
                                    print_log("INFO", "blue", thread_number, f'New IP via relay: {relay_ip}')
                                    proxy = streaming_proxy
                                    # Update thread status with new proxy
                                    update_thread_status(thread_number, None, streaming_proxy, False, False, False, False, False, None)
                                else:
                                    print_log("ERR.", "red", thread_number, f'Failed to switch relay to streaming proxy!')
                                    clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    if dynamic_relay:
                                        dynamic_relay.stop()
                                    # Release account before exiting
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    break

                                # Brief wait for relay to stabilize
                                time.sleep(2)
                                streaming_proxy_success = True
                                
                                # Navigate to home to trigger new requests through the streaming proxy
                                # Retry with different streaming proxies if CDN blocks the proxy
                                max_streaming_proxy_attempts = 3
                                streaming_proxy_success = False
                                
                                for streaming_attempt in range(max_streaming_proxy_attempts):
                                    try:
                                        driver.get("https://desktop.tidal.com/home")
                                        time.sleep(3)
                                        
                                        # Check for Access Denied error (CDN blocking proxy)
                                        page_source = driver.page_source
                                        if '<Code>AccessDenied</Code>' in page_source or 'Access Denied' in page_source:
                                            print_log("WARN", "yellow", thread_number, f'Streaming proxy blocked by CDN (attempt {streaming_attempt + 1}/{max_streaming_proxy_attempts})')
                                            
                                            if streaming_attempt < max_streaming_proxy_attempts - 1:
                                                # Release the old streaming proxy before getting a new one
                                                if current_streaming_proxy is not None:
                                                    release_streaming_proxy(current_streaming_proxy)
                                                # Try a different streaming proxy
                                                streaming_proxy = get_random_streaming_proxy()
                                                current_streaming_proxy = streaming_proxy  # Track new proxy
                                                streaming_protocol, msg = determine_proxy_protocol(streaming_proxy)
                                                if streaming_protocol:
                                                    print_log("INFO", "blue", thread_number, f'Trying different streaming proxy: {streaming_proxy}')
                                                    success, relay_ip = dynamic_relay.switch_to_proxy(streaming_proxy, streaming_protocol)
                                                    if success:
                                                        print_log("INFO", "blue", thread_number, f'Switched to new streaming proxy, retrying...')
                                                        time.sleep(2)
                                                        continue
                                            
                                            # All attempts failed
                                            print_log("ERR.", "red", thread_number, f'All streaming proxies blocked by CDN!')
                                            break
                                        else:
                                            # No Access Denied - proxy works
                                            streaming_proxy_success = True
                                            break
                                            
                                    except Exception as e:
                                        print_log("WARN", "yellow", thread_number, f'Error navigating to home: {e}')
                                        break
                                
                                if not streaming_proxy_success:
                                    print_log("ERR.", "red", thread_number, 'Failed to find working streaming proxy!')
                                    clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    if dynamic_relay:
                                        dynamic_relay.stop()
                                    # Release account before exiting
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    break

                                # Verify we're still logged in (should be since we didn't restart Tidal)
                                print_log("INFO", "blue", thread_number, 'Verifying session after relay switch...')
                                still_logged_in = check_logged_in(thread_number, driver)
                                if not still_logged_in:
                                    print_log("ERR.", "red", thread_number, 'Session lost after relay switch!')
                                    clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    if dynamic_relay:
                                        dynamic_relay.stop()
                                    # Release account before exiting
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    break
                                else:
                                    print_log("SUCC", "green", thread_number, 'Session verified - still logged in after relay switch!')

                        if logged_in_before is False:
                            acc_type = check_account_type(thread_number, driver, driver_instance_port)
                        if acc_type is False:
                            logged_in = False
                        elif acc_type is not None:
                            logged_in = True
                        elif logged_in_before is True:
                            logged_in = True
                        else:
                            # acc_type still None: login failed or check never ran
                            logged_in = False
                        ppa_parts = str(config_ppa).split('-')
                        if len(ppa_parts) == 2:
                            ppa1, ppa2 = ppa_parts
                            if int(ppa1) == int(ppa2):
                                ppa = int(ppa1)
                            else:
                                ppa = random.randrange(int(ppa1), int(ppa2))
                        else:
                            ppa = int(ppa_parts[0]) if ppa_parts[0] else 5
                        while logged_in is True:
                            if stop_flags.get(thread_number, False):
                                # Release account and proxy when stopping
                                if current_account_string is not None:
                                    release_account(current_account_string)
                                    current_account_string = None
                                if current_streaming_proxy is not None:
                                    release_streaming_proxy(current_streaming_proxy)
                                    current_streaming_proxy = None
                                break
                            loadlink_result, song_count, msg = load_link(thread_number, driver, driver_instance_port)
                            if msg == 'restart':
                                print_log("ERR.", "red", thread_number, f'Driver crashed because of system resources, cleaning up and restarting!')
                                # Clean up driver AND Tidal instance properly
                                rsp = clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                # Stop dynamic relay if it was used
                                if dynamic_relay is not None:
                                    try:
                                        dynamic_relay.stop()
                                    except:
                                        pass
                                # Release account and proxy before breaking
                                if current_account_string is not None:
                                    release_account(current_account_string)
                                    current_account_string = None
                                if current_streaming_proxy is not None:
                                    release_streaming_proxy(current_streaming_proxy)
                                    current_streaming_proxy = None
                                break
                            if str(config_mute_tidal_app).lower().__contains__('true'):
                                mute_executable(tidal_instance.pid)
                            if loadlink_result is True:
                                for song in range(song_count):
                                    if stop_flags.get(thread_number, False):
                                        break
                                    play_song_fatal_error, play_song_result, play_song_msg = play_songs(thread_number, driver, song_count, ppa)
                                    if play_song_result is True:
                                        ppa -= 1
                                        if ppa == 0:
                                            if str(stay_logged_in).lower().__contains__('false'):
                                                logged_in = False
                                        global worker_streams_done
                                        worker_streams_done += 1
                                    else:
                                        if play_song_msg == 'in-use':
                                            rsp = clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop,
                                                                         proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                            # Stop dynamic relay if it was used
                                            if dynamic_relay is not None:
                                                try:
                                                    dynamic_relay.stop()
                                                except:
                                                    pass
                                            # Release account and streaming proxy
                                            if current_account_string is not None:
                                                release_account(current_account_string)
                                                current_account_string = None
                                            if current_streaming_proxy is not None:
                                                release_streaming_proxy(current_streaming_proxy)
                                                current_streaming_proxy = None
                                            logged_in = False
                                            break
                                        elif play_song_fatal_error is True:
                                            rsp = clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop,
                                                                         proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                            # Stop dynamic relay if it was used
                                            if dynamic_relay is not None:
                                                try:
                                                    dynamic_relay.stop()
                                                except:
                                                    pass
                                            # Release account and streaming proxy
                                            if current_account_string is not None:
                                                release_account(current_account_string)
                                                current_account_string = None
                                            if current_streaming_proxy is not None:
                                                release_streaming_proxy(current_streaming_proxy)
                                                current_streaming_proxy = None
                                            logged_in = False
                                            break
                                        else:
                                            # Other errors - still need to clean up!
                                            rsp = clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop,
                                                                         proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                            # Stop dynamic relay if it was used
                                            if dynamic_relay is not None:
                                                try:
                                                    dynamic_relay.stop()
                                                except:
                                                    pass
                                            # Release account and streaming proxy
                                            if current_account_string is not None:
                                                release_account(current_account_string)
                                                current_account_string = None
                                            if current_streaming_proxy is not None:
                                                release_streaming_proxy(current_streaming_proxy)
                                                current_streaming_proxy = None
                                            logged_in = False
                                            break
                            else:
                                if msg == 'in-use':
                                    pass
                                login_result = check_logged_in(thread_number, driver)
                                if login_result is False:
                                    print_log("ERR.", "red", thread_number, f'Account is logged out!')
                                    # Clean up driver and Tidal instance BEFORE releasing account
                                    rsp = clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                                    # Stop dynamic relay if it was used
                                    if dynamic_relay is not None:
                                        try:
                                            dynamic_relay.stop()
                                        except:
                                            pass
                                    # Release account before breaking
                                    if current_account_string is not None:
                                        release_account(current_account_string)
                                        current_account_string = None
                                    # Release streaming proxy before breaking
                                    if current_streaming_proxy is not None:
                                        release_streaming_proxy(current_streaming_proxy)
                                        current_streaming_proxy = None
                                    logged_in = False
                                    break
                    else:
                        # logged_in is False (e.g. TIDAL Intro) – clean up and remove session so we don't get stuck in reuse loop
                        #worker_thread_logging_in = True
                        rsp = clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                        # If account was TIDAL Intro, remove session folder so next time we don't reuse "already logged in" Intro state
                        if acc_type is False:
                            try:
                                if session_folder and os.path.exists(session_folder):
                                    shutil.rmtree(session_folder)
                                    print_log("INFO", "blue", thread_number, "Removed Intro account session folder")
                            except Exception as e:
                                print_log("WARN", "yellow", thread_number, f"Could not remove Intro session folder: {e}")
                        # Release account before retrying with a new one
                        if current_account_string is not None:
                            release_account(current_account_string)
                            current_account_string = None
                        # Stop dynamic relay if it was used
                        if dynamic_relay is not None:
                            try:
                                dynamic_relay.stop()
                            except:
                                pass


                # Release the account and streaming proxy so another thread can use them
                if current_account_string is not None:
                    release_account(current_account_string)
                    current_account_string = None
                if current_streaming_proxy is not None:
                    release_streaming_proxy(current_streaming_proxy)
                    current_streaming_proxy = None
                
                rsp = clean_driver_and_tidal(thread_number, driver, proxy_asyncio_loop, proxy_server_thread, session_folder, driver_instance_port, True, tidal_instance)
                # Stop dynamic relay if it was used
                if dynamic_relay is not None:
                    try:
                        dynamic_relay.stop()
                    except:
                        pass
                update_thread_status(thread_number, 'Stopped', None, False, False, False, False, False, None)
                time.sleep(10)
            except Exception as e:
                print_log("ERR.", "red", thread_number, f'Fail in thread: {str(e)}')
                # Release account and streaming proxy on exception
                try:
                    if current_account_string is not None:
                        release_account(current_account_string)
                        current_account_string = None
                except:
                    pass
                try:
                    if current_streaming_proxy is not None:
                        release_streaming_proxy(current_streaming_proxy)
                        current_streaming_proxy = None
                except:
                    pass
                # Stop dynamic relay on exception
                try:
                    if dynamic_relay is not None:
                        dynamic_relay.stop()
                except:
                    pass
                # Prevent infinite spin loop on repeated failures (e.g. all accounts in use)
                time.sleep(30)
            if stop_flags.get(thread_number, False):
                break


    def main_function(config_data):
        threads_to_start = config_threads_to_start
        for i in range(threads_to_start):
            global worker_threads_running
            worker_threads_running += 1
            num = i + 1

            worker_thread = threading.Thread(target=thread_function, args=(num,))
            worker_threads[num] = {
                "thread": worker_thread,
                "status": "starting",
                "proxy": "/",
                "logins": 0,
                "streams": 0,
                "likes": 0,
                "follows": 0,
                "errors": 0,
                "controls": "restart",
                "port": 9999,
                "pid": "/"
            }
            worker_thread.start()
            time.sleep(config_thread_start_delay)
        input()


    def cleanup():
        try:
            print("Cleaning up...")
            for proc in psutil.process_iter(['pid', 'name']):
                if str(proc.info['name']).lower() == 'tidal.exe' or str(proc.info['name']).lower() == 'tidal' or str(proc.info['name']).lower() == 'tidalplayer.exe' or str(proc.info['name']).lower() == 'tidalplayer' or str(proc.info['name']).lower() == 'chromedriver.exe' or str(proc.info['name']).lower() == 'chromedriver':
                    proc.kill()

            print("All Tidal.exe processes have been terminated.")
        except:
            pass


    atexit.register(cleanup)


    def signal_handler(sig, frame):
        cleanup()
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


    @app.route('/backend', methods=['POST'])
    def backend_ready():
        if backend_state != 'Ready!':
            return jsonify({"ready": False, "message": backend_state})
        else:
            return jsonify({"ready": True, "message": "Ready to launch!"})


    if __name__ == '__main__':
        cleanup()
        app.run(port=8111, debug=False)
except Exception as e:
    try:
        messagebox.showerror("Backend error", str(e))
    except:
        print(f"Backend error: {e}")
