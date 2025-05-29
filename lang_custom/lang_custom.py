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

async def get(language, group, type, name):
    async with aiosqlite.connect(DB_PATH) as db:
        frame = inspect.currentframe().f_back
        filename = Path(frame.f_code.co_filename).name
        lineno = frame.f_lineno
        line = linecache.getline(filename, lineno).rstrip('\n')

        async with db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (language,)) as cursor:
            table_exists = await cursor.fetchone()
        if not table_exists:
            message = f"No data found for language '{language}'"
            warnings.warn(message, UserWarning, stacklevel=2)
            return None

        if type not in ['text', 'random']:
            message = f"Invalid type: '{type}' (must be 'text' or 'random')"
            warnings.warn(message, UserWarning, stacklevel=2)
            return None

        async with db.execute(f"SELECT DISTINCT \"group\" FROM {language}") as cursor:
            groups = [row[0] for row in await cursor.fetchall()]
        if group not in groups:
            similar_groups = difflib.get_close_matches(group, groups, n=1, cutoff=0.6)
            if similar_groups:
                suggestion = f". Did you mean '{similar_groups[0]}'?"
            else:
                suggestion = ""
            message = f"No data found for group '{group}' in language '{language}'{suggestion}"
            warnings.warn(message, UserWarning, stacklevel=2)
            return None

        async with db.execute(f"""
            SELECT name FROM {language}
            WHERE "group" = ? AND type = ?
        """, (group, type)) as cursor:
            names = [row[0] for row in await cursor.fetchall()]
        if name not in names:
            similar_names = difflib.get_close_matches(name, names, n=1, cutoff=0.6)
            if similar_names:
                suggestion = f". Did you mean '{similar_names[0]}'?"
            else:
                suggestion = ""
            message = f"No data found for name '{name}' with group '{group}' and type '{type}' in language '{language}'{suggestion}"
            warnings.warn(message, UserWarning, stacklevel=2)
            return None

        query = f"""
            SELECT value FROM {language}
            WHERE "group" = ? AND type = ? AND name = ?
            {"AND idx IS NULL" if type == "text" else ""}
        """
        async with db.execute(query, (group, type, name)) as cursor:
            rows = await cursor.fetchall()
            return rows[0][0] if type == "text" else random.choice([r[0] for r in rows])

ensure_default_language()
language_setup()