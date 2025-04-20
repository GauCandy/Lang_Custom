from pathlib import Path
import json
import os
import random
import warnings
import sqlite3

def language_setup(base_path=None):
    """Khởi tạo thư mục, file ngôn ngữ và database SQLite, xóa sạch tất cả bảng trước khi lưu."""
    base_path = Path(base_path) if base_path else Path.cwd()
    language_dir = base_path / "import_language"
    db_dir = base_path / "data_language"
    db_path = db_dir / "DO_NOT_DELETE.db"
    default_lang_file = language_dir / "en.json"
    default_data = {
        "reply": {
            "text": {
                "greeting": "hello :D",
                "welcome": "hi :3"
            },
            "random": {
                "greetings": [
                    "hello :D",
                    "hi :3",
                    "hey there!"
                ]
            }
        },
        "error": {
            "text": {
                "not_found": "Resource not found",
                "invalid": "Invalid input"
            },
            "random": {
                "errors": [
                    "Oops, something went wrong!",
                    "Uh-oh, try again!"
                ]
            }
        }
    }

    # Tạo thư mục import_language nếu chưa tồn tại
    language_dir.mkdir(exist_ok=True)

    # Kiểm tra và tạo file en.json mặc định nếu không có file JSON nào
    json_files = list(language_dir.glob("*.json"))
    if not json_files:
        with open(default_lang_file, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4, ensure_ascii=False)
        json_files = [default_lang_file]

    # Tạo thư mục data_language nếu chưa tồn tại
    db_dir.mkdir(exist_ok=True)

    # Kết nối SQLite
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()

        # Xóa tất cả bảng trong database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        for table in tables:
            cursor.execute(f"DROP TABLE {table}")

        # Quét và xử lý từng file JSON
        for json_file in json_files:
            lang = json_file.stem  # Ví dụ: 'en', 'vi', 'jp'
            
            # Tạo bảng mới cho ngôn ngữ
            cursor.execute(f"""
                CREATE TABLE {lang} (
                    "group" TEXT NOT NULL,
                    type INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    value TEXT,
                    PRIMARY KEY ("group", type, name)
                )
            """)

            # Đọc dữ liệu từ file JSON
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                continue

            # Lưu dữ liệu vào bảng
            for group in data:
                # Lưu text
                for name, value in data[group].get("text", {}).items():
                    cursor.execute(f"""
                        INSERT INTO {lang} ("group", type, name, value)
                        VALUES (?, ?, ?, ?)
                    """, (group, 0, name, value))
                
                # Lưu random (lưu danh sách dưới dạng JSON string)
                for name, value in data[group].get("random", {}).items():
                    if isinstance(value, list):
                        cursor.execute(f"""
                            INSERT INTO {lang} ("group", type, name, value)
                            VALUES (?, ?, ?, ?)
                        """, (group, 1, name, json.dumps(value)))

        conn.commit()
    finally:
        conn.close()

def get(language="en", group=None, type=None, name=None):
    """Lấy dữ liệu từ database SQLite."""
    base_path = Path.cwd()
    db_path = base_path / "data_language" / "DO_NOT_DELETE.db"

    # Kiểm tra database tồn tại
    if not db_path.exists():
        return None

    # Kết nối SQLite
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()

        # Kiểm tra bảng ngôn ngữ tồn tại
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (language,))
        if not cursor.fetchone():
            return None

        # Kiểm tra type hợp lệ
        if type not in ["text", "random"]:
            warnings.warn(f"Invalid type: {type}. Must be 'text' or 'random'")
            return None

        type_value = 0 if type == "text" else 1

        # Truy vấn dữ liệu
        cursor.execute(f"""
            SELECT value FROM {language}
            WHERE "group" = ? AND type = ? AND name = ?
        """, (group, type_value, name))
        
        result = cursor.fetchone()
        if result is None:
            return None

        value = result[0]
        
        # Nếu type là random, parse JSON và chọn ngẫu nhiên
        if type == "random":
            try:
                value_list = json.loads(value)
                if not isinstance(value_list, list):
                    return None
                return random.choice(value_list)
            except json.JSONDecodeError:
                return None

        return value
    finally:
        conn.close()

def get_lang():
    """Trả về danh sách các ngôn ngữ hỗ trợ từ database."""
    base_path = Path.cwd()
    db_path = base_path / "data_language" / "DO_NOT_DELETE.db"

    if not db_path.exists():
        return []

    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        return tables
    except sqlite3.Error:
        return []
    finally:
        conn.close()