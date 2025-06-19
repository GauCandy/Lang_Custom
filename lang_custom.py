import json
import random
import sqlite3
from pathlib import Path
import shutil
import aiosqlite
import warnings
import inspect
import linecache
import difflib

warnings.filterwarnings('always', category=UserWarning, append=True)

DB_PATH = Path.cwd() / "_data_language" / "DO_NOT_DELETE.db"

# Lưu trữ các giá trị mặc định
_DEFAULTS = {
    "language": None,
    "group": None,
    "type": None
}

def ensure_default_language():
    workspace_folder = Path.cwd()
    lang_dir = workspace_folder / "_data_language"
    lang_dir.mkdir(exist_ok=True)
    json_files = list(lang_dir.glob("*.json"))
    if not json_files:
        source_path = Path(__file__).parent / "en.json"
        target_path = lang_dir / "en.json"
        if source_path.exists():
            shutil.copy(source_path, target_path)
        else:
            raise FileNotFoundError(f"Không tìm thấy file en.json mẫu tại {source_path}")

def language_setup():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
    lang_dir = Path.cwd() / "_data_language"
    for json_file in lang_dir.glob("*.json"):
        lang_name = json_file.stem
        try:
            create_table(cursor, lang_name)
            load_json_to_table(cursor, lang_name, json_file)
        except (json.JSONDecodeError, ValueError):
            continue
    conn.commit()
    conn.close()

def create_table(cursor, lang_name):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {lang_name} (
            "group" TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('text', 'random')),
            name TEXT NOT NULL,
            idx INTEGER DEFAULT NULL,
            value TEXT NOT NULL,
            PRIMARY KEY ("group", type, name, idx)
        )
    """)

def load_json_to_table(cursor, lang_name, json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"JSON root in {json_file} must be an object")
    for group, group_data in data.items():
        if not isinstance(group_data, dict):
            raise ValueError(f"Group '{group}' in {json_file} must be an object")
        for type_name, type_data in group_data.items():
            if type_name not in ['text', 'random']:
                continue
            if not isinstance(type_data, dict):
                raise ValueError(f"Type '{type_name}' in group '{group}' in {json_file} must be an object")
            for name, value in type_data.items():
                if type_name == 'text':
                    if not isinstance(value, str):
                        raise ValueError(f"Text value for '{name}' in group '{group}' in {json_file} must be a string")
                    cursor.execute(f"""
                        INSERT INTO {lang_name} ("group", type, name, idx, value)
                        VALUES (?, ?, ?, ?, ?)
                    """, (group, type_name, name, None, value))
                elif type_name == 'random':
                    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
                        raise ValueError(f"Random value for '{name}' in group '{group}' in {json_file} must be a list of strings")
                    for idx, val in enumerate(value):
                        cursor.execute(f"""
                            INSERT INTO {lang_name} ("group", type, name, idx, value)
                            VALUES (?, ?, ?, ?, ?)
                        """, (group, type_name, name, idx, val))

async def reload():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("BEGIN EXCLUSIVE TRANSACTION")
        async with db.execute("SELECT name FROM sqlite_master WHERE type='table';") as cursor:
            tables = await cursor.fetchall()
        for table in tables:
            await db.execute(f"DROP TABLE IF EXISTS {table[0]}")
        lang_dir = Path.cwd() / "_data_language"
        for json_file in lang_dir.glob("*.json"):
            lang_name = json_file.stem
            await db.execute(f"""
                CREATE TABLE {lang_name} (
                    "group" TEXT NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('text', 'random')),
                    name TEXT NOT NULL,
                    idx INTEGER DEFAULT NULL,
                    value TEXT NOT NULL,
                    PRIMARY KEY ("group", type, name, idx)
                )
            """)
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    continue
                for group, group_data in data.items():
                    if not isinstance(group_data, dict):
                        continue
                    for type_name, type_data in group_data.items():
                        if type_name not in ['text', 'random']:
                            continue
                        if not isinstance(type_data, dict):
                            continue
                        for name, value in type_data.items():
                            if type_name == 'text':
                                if not isinstance(value, str):
                                    continue
                                await db.execute(f"""
                                    INSERT INTO {lang_name} ("group", type, name, idx, value)
                                    VALUES (?, ?, ?, ?, ?)
                                """, (group, type_name, name, None, value))
                            elif type_name == 'random':
                                if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
                                    continue
                                for idx, val in enumerate(value):
                                    await db.execute(f"""
                                        INSERT INTO {lang_name} ("group", type, name, idx, value)
                                        VALUES (?, ?, ?, ?, ?)
                                    """, (group, type_name, name, idx, val))
            except (json.JSONDecodeError, ValueError):
                continue
        await db.commit()

async def reload_language(language):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("BEGIN EXCLUSIVE TRANSACTION")
        await db.execute(f"DROP TABLE IF EXISTS {language}")
        await db.execute(f"""
            CREATE TABLE {language} (
                "group" TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('text', 'random')),
                name TEXT NOT NULL,
                idx INTEGER DEFAULT NULL,
                value TEXT NOT NULL,
                PRIMARY KEY ("group", type, name, idx)
            )
        """)
        json_file = Path.cwd() / "_data_language" / f"{language}.json"
        try:
            if json_file.exists():
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    await db.rollback()
                    return
                for group, group_data in data.items():
                    if not isinstance(group_data, dict):
                        continue
                    for type_name, type_data in group_data.items():
                        if type_name not in ['text', 'random']:
                            continue
                        if not isinstance(type_data, dict):
                            continue
                        for name, value in type_data.items():
                            if type_name == 'text':
                                if not isinstance(value, str):
                                    continue
                                await db.execute(f"""
                                    INSERT INTO {language} ("group", type, name, idx, value)
                                    VALUES (?, ?, ?, ?, ?)
                                """, (group, type_name, name, None, value))
                            elif type_name == 'random':
                                if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
                                    continue
                                for idx, val in enumerate(value):
                                    await db.execute(f"""
                                        INSERT INTO {language} ("group", type, name, idx, value)
                                        VALUES (?, ?, ?, ?, ?)
                                    """, (group, type_name, name, idx, val))
            else:
                frame = inspect.currentframe().f_back
                filename = Path(frame.f_code.co_filename).name
                lineno = frame.f_lineno
                warnings.warn(f"JSON file {json_file} does not exist, table {language} created but empty at {filename}:{lineno}", UserWarning, stacklevel=2)
        except (json.JSONDecodeError, ValueError):
            await db.rollback()
            return
        await db.commit()

async def get_lang():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT name FROM sqlite_master WHERE type='table';") as cursor:
            tables = await cursor.fetchall()
            return [table[0] for table in tables]

async def has_language(language):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (language,)) as cursor:
            return bool(await cursor.fetchone())

async def default(language=None, group=None, type=None):
    """
    Thiết lập các giá trị mặc định cho language, group, và type.
    Các giá trị None sẽ giữ nguyên giá trị mặc định hiện tại.

    Args:
        language (str, optional): Ngôn ngữ mặc định (ví dụ: 'vi').
        group (str, optional): Nhóm mặc định (ví dụ: 'tos').
        type (str, optional): Loại mặc định (ví dụ: 'text').

    Returns:
        None
    """
    if language is not None:
        _DEFAULTS["language"] = language
    if group is not None:
        _DEFAULTS["group"] = group
    if type is not None:
        _DEFAULTS["type"] = type

async def get(language=None, group=None, type=None, name=None):
    """
    Lấy giá trị ngôn ngữ từ cơ sở dữ liệu, sử dụng giá trị mặc định nếu không cung cấp.

    Args:
        language (str, optional): Ngôn ngữ (ví dụ: 'vi'). Nếu None, dùng giá trị mặc định.
        group (str, optional): Nhóm (ví dụ: 'tos'). Nếu None, dùng giá trị mặc định.
        type (str, optional): Loại ('text' hoặc 'random'). Nếu None, dùng giá trị mặc định.
        name (str, optional): Tên giá trị (ví dụ: 'accept'). Bắt buộc nếu không có giá trị mặc định.

    Returns:
        str or None: Giá trị ngôn ngữ hoặc None nếu không tìm thấy.

    Raises:
        UserWarning: Nếu thiếu tham số cần thiết hoặc dữ liệu không tồn tại.
    """
    params = {
        "language": language if language is not None else _DEFAULTS["language"],
        "group": group if group is not None else _DEFAULTS["group"],
        "type": type if type is not None else _DEFAULTS["type"],
        "name": name
    }

    if params["language"] is None:
        warnings.warn("Thiếu tham số 'language' và không có giá trị mặc định", UserWarning, stacklevel=2)
        return None
    if params["group"] is None:
        warnings.warn("Thiếu tham số 'group' và không có giá trị mặc định", UserWarning, stacklevel=2)
        return None
    if params["type"] is None:
        warnings.warn("Thiếu tham số 'type' và không có giá trị mặc định", UserWarning, stacklevel=2)
        return None
    if params["name"] is None:
        warnings.warn("Thiếu tham số 'name'. Phải cung cấp 'name' để lấy giá trị", UserWarning, stacklevel=2)
        return None

    async with aiosqlite.connect(DB_PATH) as db:
        frame = inspect.currentframe().f_back
        filename = Path(frame.f_code.co_filename).name
        lineno = frame.f_lineno
        line = linecache.getline(filename, lineno).rstrip('\n')

        async with db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (params["language"],)) as cursor:
            table_exists = await cursor.fetchone()
        if not table_exists:
            message = f"No data found for language '{params['language']}'"
            warnings.warn(message, UserWarning, stacklevel=2)
            return None

        if params["type"] not in ['text', 'random']:
            message = f"Invalid type: '{params['type']}' (must be 'text' or 'random')"
            warnings.warn(message, UserWarning, stacklevel=2)
            return None

        async with db.execute(f"SELECT DISTINCT \"group\" FROM {params['language']}") as cursor:
            groups = [row[0] for row in await cursor.fetchall()]
        if params["group"] not in groups:
            similar_groups = difflib.get_close_matches(params["group"], groups, n=1, cutoff=0.6)
            if similar_groups:
                suggestion = f". Did you mean '{similar_groups[0]}'?"
            else:
                suggestion = ""
            message = f"No data found for group '{params['group']}' in language '{params['language']}'{suggestion}"
            warnings.warn(message, UserWarning, stacklevel=2)
            return None

        async with db.execute(f"""
            SELECT name FROM {params['language']}
            WHERE "group" = ? AND type = ?
        """, (params["group"], params["type"])) as cursor:
            names = [row[0] for row in await cursor.fetchall()]
        if params["name"] not in names:
            similar_names = difflib.get_close_matches(params["name"], names, n=1, cutoff=0.6)
            if similar_names:
                suggestion = f". Did you mean '{similar_names[0]}'?"
            else:
                suggestion = ""
            message = f"No data found for name '{params['name']}' with group '{params['group']}' and type '{params['type']}' in language '{params['language']}'{suggestion}"
            warnings.warn(message, UserWarning, stacklevel=2)
            return None

        query = f"""
            SELECT value FROM {params['language']}
            WHERE "group" = ? AND type = ? AND name = ?
            {"AND idx IS NULL" if params["type"] == "text" else ""}
        """
        async with db.execute(query, (params["group"], params["type"], params["name"])) as cursor:
            rows = await cursor.fetchall()
            return rows[0][0] if params["type"] == "text" else random.choice([r[0] for r in rows])

async def batch(language=None, group=None, type=None, names=None):
    """
    Lấy nhiều giá trị ngôn ngữ cùng lúc dựa trên danh sách names, sử dụng giá trị mặc định nếu không cung cấp.

    Args:
        language (str, optional): Ngôn ngữ (ví dụ: 'vi'). Nếu None, dùng giá trị mặc định.
        group (str, optional): Nhóm (ví dụ: 'tos'). Nếu None, dùng giá trị mặc định.
        type (str, optional): Loại ('text' hoặc 'random'). Nếu None, dùng giá trị mặc định.
        names (list, optional): Danh sách tên giá trị (ví dụ: ['123', '124', '125']). Bắt buộc.

    Returns:
        dict: Dictionary với key là name và value là giá trị ngôn ngữ hoặc chuỗi rỗng nếu không tìm thấy.

    Raises:
        UserWarning: Nếu thiếu tham số cần thiết hoặc dữ liệu không tồn tại.
    """
    params = {
        "language": language if language is not None else _DEFAULTS["language"],
        "group": group if group is not None else _DEFAULTS["group"],
        "type": type if type is not None else _DEFAULTS["type"],
        "names": names
    }

    if params["language"] is None:
        warnings.warn("Thiếu tham số 'language' và không có giá trị mặc định", UserWarning, stacklevel=2)
        return {}
    if params["group"] is None:
        warnings.warn("Thiếu tham số 'group' và không có giá trị mặc định", UserWarning, stacklevel=2)
        return {}
    if params["type"] is None:
        warnings.warn("Thiếu tham số 'type' và không có giá trị mặc định", UserWarning, stacklevel=2)
        return {}
    if not params["names"] or not isinstance(params["names"], list):
        warnings.warn("Thiếu hoặc tham số 'names' không hợp lệ. Phải cung cấp danh sách names", UserWarning, stacklevel=2)
        return {}

    result = {name: "" for name in params["names"]}  # Khởi tạo dictionary với giá trị rỗng

    async with aiosqlite.connect(DB_PATH) as db:
        frame = inspect.currentframe().f_back
        filename = Path(frame.f_code.co_filename).name
        lineno = frame.f_lineno

        # Kiểm tra bảng ngôn ngữ
        async with db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (params["language"],)) as cursor:
            table_exists = await cursor.fetchone()
        if not table_exists:
            message = f"No data found for language '{params['language']}'"
            warnings.warn(message, UserWarning, stacklevel=2)
            return result

        # Kiểm tra type hợp lệ
        if params["type"] not in ['text', 'random']:
            message = f"Invalid type: '{params['type']}' (must be 'text' or 'random')"
            warnings.warn(message, UserWarning, stacklevel=2)
            return result

        # Kiểm tra group
        async with db.execute(f"SELECT DISTINCT \"group\" FROM {params['language']}") as cursor:
            groups = [row[0] for row in await cursor.fetchall()]
        if params["group"] not in groups:
            similar_groups = difflib.get_close_matches(params["group"], groups, n=1, cutoff=0.6)
            if similar_groups:
                suggestion = f". Did you mean '{similar_groups[0]}'?"
            else:
                suggestion = ""
            message = f"No data found for group '{params['group']}' in language '{params['language']}'{suggestion}"
            warnings.warn(message, UserWarning, stacklevel=2)
            return result

        # Truy vấn tất cả names trong một truy vấn
        placeholders = ",".join("?" for _ in params["names"])
        query = f"""
            SELECT name, value FROM {params['language']}
            WHERE "group" = ? AND type = ? AND name IN ({placeholders})
            {"AND idx IS NULL" if params["type"] == "text" else ""}
        """
        async with db.execute(query, [params["group"], params["type"]] + params["names"]) as cursor:
            rows = await cursor.fetchall()
            if params["type"] == "text":
                for name, value in rows:
                    result[name] = value
            else:
                # Nhóm các giá trị theo name cho type="random"
                random_values = {}
                for name, value in rows:
                    if name not in random_values:
                        random_values[name] = []
                    random_values[name].append(value)
                for name in random_values:
                    result[name] = random.choice(random_values[name]) if random_values[name] else ""

        # Kiểm tra các name không tìm thấy
        for name in params["names"]:
            if result[name] == "":
                similar_names = difflib.get_close_matches(name, 
                    [n async for n in (await db.execute(f"SELECT name FROM {params['language']} WHERE \"group\" = ? AND type = ?", 
                    (params["group"], params["type"]))).fetchall()], n=1, cutoff=0.6)
                suggestion = f". Did you mean '{similar_names[0][0]}'?" if similar_names else ""
                message = f"No data found for name '{name}' with group '{params['group']}' and type '{params['type']}' in language '{params['language']}'{suggestion}"
                warnings.warn(message, UserWarning, stacklevel=2)

    return result

ensure_default_language()
language_setup()