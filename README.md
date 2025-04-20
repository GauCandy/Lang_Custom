# Lang Custom v1.1.1

**Lang Custom** is a Python library designed to manage and load translations from JSON files, powered by **SQLite** for blazing-fast performance and reduced memory usage. Say goodbye to messy JSON parsing and hello to a standardized, headache-free language system!

## Why Lang Custom?

Lang Custom was born to simplify multilingual support for bots and applications. Managing translations can be chaotic without a proper system—scattered JSON files, inconsistent parsing, and no standardization. This library brings order with a clean API, SQLite-backed storage, and customizable language files. Whether you're building a small bot or a large-scale app, Lang Custom makes language management reliable and efficient.

## Installation

Install the library using pip:
```sh
pip install lang_custom
```

**Note**: This version is **not backward compatible** with v1.0.14 or earlier due to major changes in the API and database integration. Upgrade with caution!

## Usage Guide

### 1. Import the library
```python
import lang_custom
```

### 2. Initialize the database
Call `language_setup()` in your main script to set up the SQLite database and load data from JSON files in the `import_language/` directory:
```python
lang_custom.language_setup()
```

This creates:
- `import_language/` directory with a default `en.json` if no JSON files exist.
- `data_language/DO_NOT_DELETE.db` with tables for each language (e.g., `en`, `vi`).
- Clears all existing tables and reloads data from JSON files.

**Important**: 
- Only call `language_setup()` once in your main script. Sub-modules can use `get()` or `get_lang()` without re-initializing.
- **Do not delete** the `data_language/` directory or `DO_NOT_DELETE.db` file, especially while your bot or application is running, as this will cause data loss and errors.

### 3. Get the list of supported languages
To see available languages (based on JSON files or SQLite tables):
```python
languages = lang_custom.get_lang()
print(languages)  # Example: ['en', 'vi', 'jp']
```

### 4. Retrieve language data
Use `get(language, group, type, name)` to fetch data from SQLite:
- `language`: Name of the language (e.g., `"en"`, `"vi"`).
- `group`: Data group in the JSON structure (e.g., `"reply"`, `"error"`).
- `type`: `"text"` for a fixed string or `"random"` for a random item from a list.
- `name`: Key within the group (e.g., `"greeting"`, `"greetings"`).

Examples:
```python
# Get a fixed text
text = lang_custom.get(language="en", group="error", type="text", name="not_found")
print(text)  # Output: Resource not found

# Get a random text from a list
random_text = lang_custom.get(language="en", group="reply", type="random", name="greetings")
print(random_text)  # Output: hello :D or hi :3 or hey there!
```

If `language`, `group`, or `name` doesn’t exist, or if `type` is invalid (not `"text"` or `"random"`), it returns `None`. Invalid `type` also triggers a console warning:
```
lang_custom/language_loader.py:XXX: UserWarning: Invalid type: test. Must be 'text' or 'random'
```

### 5. File structure
Language files are stored in `import_language/` (user-added translations). Example `import_language/en.json`:
```json
{
    "reply": {
        "text": {
            "greeting": "hello :D",
            "welcome": "hi :3"
        },
        "random": {
            "greetings": ["hello :D", "hi :3", "hey there!"]
        }
    },
    "error": {
        "text": {
            "not_found": "Resource not found",
            "invalid": "Invalid input"
        },
        "random": {
            "errors": ["Oops, something went wrong!", "Uh-oh, try again!"]
        }
    }
}
```

Add your own JSON files (e.g., `vi.json`, `jp.json`) to `import_language/` with the same structure. Run `language_setup()` to load them into SQLite.

## Performance Benefits
- **SQLite Storage**: Language data is stored in `data_language/DO_NOT_DELETE.db`, reducing memory usage compared to parsing JSON files repeatedly.
- **Fast Queries**: SQLite queries are faster than JSON parsing, especially for large datasets or frequent access.
- **Single Initialization**: `language_setup()` loads data once, and sub-modules query the database directly.

## Compatibility
**v1.1.1 is not backward compatible** with v1.0.14 or earlier due to:
- New SQLite-based architecture.
- Replaced `lang()`, `group()`, `get_text()`, `random_text()` with `get()`.
- Removed caching mechanism (SQLite handles performance).

Update your code to use the new API. Check the [Usage Guide](#usage-guide) for details.

## Important Notes
- **Do not delete** the `data_language/` directory or `DO_NOT_DELETE.db` file while your bot or application is running. This file contains all language data, and deleting it will cause your application to fail.
- If you need to reset the database, call `language_setup()` again, but be aware it will clear and reload all data from JSON files.

## Feedback & Issues
Found a bug or have feedback? Reach out to me:
[Discord me](https://discord.gg/pGcSyr2bcY)

Thank you for using Lang Custom! 🚀

![Thank you](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)

---

# Lang Custom v1.1.1 (Vietnamese)

**Lang Custom** là một thư viện Python giúp quản lý và tải bản dịch từ các tệp JSON, sử dụng **SQLite** để đạt hiệu suất cao và giảm tiêu tốn bộ nhớ. Tạm biệt việc parse JSON lằng nhằng và chào đón một hệ thống ngôn ngữ chuẩn hóa, không còn đau đầu!

## Tại sao dùng Lang Custom?

Lang Custom ra đời để đơn giản hóa hỗ trợ đa ngôn ngữ cho bot và ứng dụng. Quản lý bản dịch có thể trở nên hỗn loạn nếu không có hệ thống chuẩn—tệp JSON rải rác, parse không đồng nhất, không có tiêu chuẩn. Thư viện này mang lại trật tự với API rõ ràng, lưu trữ bằng SQLite, và các tệp ngôn ngữ tùy chỉnh. Dù bạn xây dựng bot nhỏ hay ứng dụng lớn, Lang Custom giúp quản lý ngôn ngữ đáng tin cậy và hiệu quả.

## Cài đặt

Cài đặt thư viện bằng pip:
```sh
pip install lang_custom
```

**Lưu ý**: Phiên bản này **không tương thích ngược** với v1.0.14 hoặc cũ hơn do thay đổi lớn trong API và tích hợp database. Hãy cẩn thận khi nâng cấp!

## Hướng dẫn sử dụng

### 1. Nhập thư viện
```python
import lang_custom
```

### 2. Khởi tạo database
Gọi `language_setup()` trong script chính để thiết lập database SQLite và tải dữ liệu từ tệp JSON trong thư mục `import_language/`:
```python
lang_custom.language_setup()
```

Hàm này:
- Tạo thư mục `import_language/` và tệp `en.json` mặc định nếu không có tệp JSON nào.
- Tạo `data_language/DO_NOT_DELETE.db` với bảng cho mỗi ngôn ngữ (ví dụ: `en`, `vi`).
- Xóa sạch tất cả bảng hiện có và tải lại dữ liệu từ tệp JSON.

**Quan trọng**:
- Chỉ gọi `language_setup()` một lần trong script chính. Các module con có thể dùng `get()` hoặc `get_lang()` mà không cần khởi tạo lại.
- **Không xóa** thư mục `data_language/` hoặc tệp `DO_NOT_DELETE.db`, đặc biệt khi bot hoặc ứng dụng đang chạy, vì sẽ gây mất dữ liệu và lỗi.

### 3. Lấy danh sách ngôn ngữ hỗ trợ
Để xem các ngôn ngữ có sẵn (dựa trên tệp JSON hoặc bảng SQLite):
```python
languages = lang_custom.get_lang()
print(languages)  # Ví dụ: ['en', 'vi', 'jp']
```

### 4. Lấy dữ liệu ngôn ngữ
Dùng `get(language, group, type, name)` để lấy dữ liệu từ SQLite:
- `language`: Tên ngôn ngữ (ví dụ: `"en"`, `"vi"`).
- `group`: Nhóm dữ liệu trong cấu trúc JSON (ví dụ: `"reply"`, `"error"`).
- `type`: `"text"` cho chuỗi cố định hoặc `"random"` cho chọn ngẫu nhiên từ danh sách.
- `name`: Khóa trong nhóm (ví dụ: `"greeting"`, `"greetings"`).

Ví dụ:
```python
# Lấy chuỗi cố định
text = lang_custom.get(language="en", group="error", type="text", name="not_found")
print(text)  # Output: Resource not found

# Lấy chuỗi ngẫu nhiên từ danh sách
random_text = lang_custom.get(language="en", group="reply", type="random", name="greetings")
print(random_text)  # Output: hello :D hoặc hi :3 hoặc hey there!
```

Nếu `language`, `group`, hoặc `name` không tồn tại, hoặc `type` không hợp lệ (không phải `"text"` hoặc `"random"`), hàm trả về `None`. `type` sai sẽ hiện cảnh báo trên console:
```
lang_custom/language_loader.py:XXX: UserWarning: Invalid type: test. Must be 'text' or 'random'
```

### 5. Cấu trúc tệp
Tệp ngôn ngữ được lưu trong `import_language/` (bản dịch do người dùng thêm). Ví dụ `import_language/en.json`:
```json
{
    "reply": {
        "text": {
            "greeting": "hello :D",
            "welcome": "hi :3"
        },
        "random": {
            "greetings": ["hello :D", "hi :3", "hey there!"]
        }
    },
    "error": {
        "text": {
            "not_found": "Resource not found",
            "invalid": "Invalid input"
        },
        "random": {
            "errors": ["Oops, something went wrong!", "Uh-oh, try again!"]
        }
    }
}
```

Thêm tệp JSON của bạn (ví dụ: `vi.json`, `jp.json`) vào `import_language/` với cấu trúc tương tự. Chạy `language_setup()` để tải chúng vào SQLite.

## Lợi ích hiệu suất
- **Lưu trữ SQLite**: Dữ liệu ngôn ngữ được lưu trong `data_language/DO_NOT_DELETE.db`, giảm sử dụng bộ nhớ so với parse JSON liên tục.
- **Truy vấn nhanh**: Truy vấn SQLite nhanh hơn parse JSON, đặc biệt với dữ liệu lớn hoặc truy cập thường xuyên.
- **Khởi tạo một lần**: `language_setup()` tải dữ liệu một lần, các module con truy vấn database trực tiếp.

## Tương thích
**v1.1.1 không tương thích ngược** với v1.0.14 hoặc cũ hơn do:
- Kiến trúc mới dựa trên SQLite.
- Thay `lang()`, `group()`, `get_text()`, `random_text()` bằng `get()`.
- Bỏ cơ chế cache (SQLite đảm nhiệm hiệu suất).

Cập nhật mã của bạn theo [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng).

## Lưu ý quan trọng
- **Không xóa** thư mục `data_language/` hoặc tệp `DO_NOT_DELETE.db` khi bot hoặc ứng dụng đang chạy. Tệp này chứa toàn bộ dữ liệu ngôn ngữ, và xóa nó sẽ khiến ứng dụng lỗi.
- Nếu cần reset database, gọi lại `language_setup()`, nhưng lưu ý hàm này sẽ xóa và tải lại toàn bộ dữ liệu từ tệp JSON.

## Phản hồi & Báo lỗi
Gặp lỗi hoặc có ý kiến? Liên hệ tôi:
[Discord me](https://discord.gg/pGcSyr2bcY)

Cảm ơn bạn đã sử dụng Lang Custom! 🚀

![Cảm ơn](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)