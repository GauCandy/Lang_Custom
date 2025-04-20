# Lang Custom v1.1.0

**Lang Custom** is a Python library designed to manage and load translations from JSON files, now powered by **SQLite** for blazing-fast performance and reduced memory usage. Say goodbye to messy JSON parsing and hello to a standardized, headache-free language system!

## Why did I create Lang Custom?

One day, I decided to make my bot support multiple languages. I scoured the internet for translation libraries, but most were... well, *not great*. So, I set out to create my own language files with customizable tones.

At first, managing JSON files seemed simple. But without a proper library, things got **chaotic**. Every code segment loaded language data differently—especially when AI tools like ChatGPT got involved. No standard, no consistency. Looking at my old code, I could only say: **"It's a miracle it didn't crash :v"**

I was never sure if my code worked as intended, and every change felt like playing Russian roulette. Some parts worked, others broke due to inconsistent handling. So, I created **Lang Custom**—a library that makes language management easy, consistent, and *actually reliable*.

With **v1.1.0**, we’ve taken it to the next level by integrating **SQLite** to store language data, making it perfect for large-scale bots or applications. No more loading JSON files into memory every time—query a database and save your RAM!

## Installation

Install the library using pip:
```sh
pip install lang_custom
```

**Note**: This version is **not backward compatible** with v1.0.14 or earlier due to major changes in the API and database integration. Upgrade with caution!

## What's New in v1.1.0

- **SQLite Backend**: Language data is now stored in an SQLite database (`lang_custom/database/language.db`) instead of being parsed from JSON files every time. This reduces memory usage and speeds up data retrieval, especially for large bots.
- **New API**:
  - `language_setup()`: Initializes the SQLite database, clears all existing tables, and loads data from JSON files in `import_language/`.
  - `get(language, group, type, name)`: Retrieves data from SQLite. `type` can be `"text"` (fixed string) or `"random"` (random choice from a list).
  - `get_lang()`: Returns a list of supported languages (e.g., `['en', 'vi', 'jp']`).
- **Improved Error Handling**: Returns `None` for invalid `language`, `group`, or `name`. Warns on console for invalid `type` (must be `"text"` or `"random"`).
- **Breaking Changes**: Old methods like `lang()`, `group()`, `get_text()`, and `random_text()` are gone. Update your code to use the new `get()` API.

## Usage Guide

### 1. Import the library
```python
import lang_custom
```

### 2. Initialize the database
Before using the library, call `language_setup()` in your main script to set up the SQLite database and load data from JSON files in the `import_language/` directory:
```python
lang_custom.language_setup()
```

This creates:
- `import_language/` directory with a default `en.json` if no JSON files exist.
- `lang_custom/database/language.db` with tables for each language (e.g., `en`, `vi`).
- Clears all existing tables and reloads data from JSON files.

**Note**: Call `language_setup()` only once in your main script. Sub-modules can use `get()` or `get_lang()` without re-initializing.

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
- **SQLite Storage**: Language data is stored in `lang_custom/database/language.db`, reducing memory usage compared to parsing JSON files repeatedly.
- **Fast Queries**: SQLite queries are faster than JSON parsing, especially for large datasets or frequent access.
- **Single Initialization**: `language_setup()` loads data once, and sub-modules query the database directly.

## Compatibility
**v1.1.0 is not backward compatible** with v1.1.0 or earlier due to:
- New SQLite-based architecture.
- Replaced `lang()`, `group()`, `get_text()`, `random_text()` with `get()`.
- Removed caching mechanism (SQLite handles performance).

Update your code to use the new API. Check the [Usage Guide](#usage-guide) for details.

## Feedback & Issues
Found a bug or have feedback? Reach out to me:
[Discord me](https://discord.gg/pGcSyr2bcY)

Thank you for using Lang Custom! 🚀

![Thank you](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)

---

# Lang Custom v1.1.0 (Vietnamese)

**Lang Custom** là một thư viện Python giúp quản lý và tải bản dịch từ các tệp JSON, giờ đây sử dụng **SQLite** để đạt hiệu suất cao và giảm tiêu tốn bộ nhớ. Tạm biệt việc parse JSON lằng nhằng và chào đón một hệ thống ngôn ngữ chuẩn hóa, không còn đau đầu!

## Tại sao tôi tạo ra Lang Custom?

Một ngày nọ, tôi muốn bot của mình hỗ trợ nhiều ngôn ngữ. Tôi đã tìm kiếm các thư viện dịch thuật, nhưng phần lớn đều... *tệ vl*. Thế là tôi quyết định tự tạo các tệp ngôn ngữ với ngữ điệu tùy chỉnh.

Ban đầu, quản lý tệp JSON có vẻ dễ. Nhưng không có thư viện chuẩn, mọi thứ trở nên **hỗn loạn**. Mỗi đoạn mã tải dữ liệu ngôn ngữ theo cách riêng—đặc biệt khi dùng AI như ChatGPT hỗ trợ. Chẳng có tiêu chuẩn chung nào. Nhìn lại mã cũ, tôi chỉ biết thốt lên: **"Tởm vl, nó không crash cũng hay đấy :v"**

Tôi không chắc mã của mình có chạy đúng không, và mỗi lần chỉnh sửa là một lần chơi "may rủi". Một số phần chạy tốt, nhưng phần khác có thể lỗi do xử lý không đồng nhất. Vì thế, tôi tạo ra **Lang Custom**—thư viện giúp quản lý ngôn ngữ dễ dàng, nhất quán, và *thực sự đáng tin*.

Với **v1.1.0**, chúng tôi nâng cấp bằng cách tích hợp **SQLite** để lưu dữ liệu ngôn ngữ, lý tưởng cho bot hoặc ứng dụng lớn. Không còn load JSON vào RAM nữa—truy vấn database và tiết kiệm tài nguyên!

## Cài đặt

Cài đặt thư viện bằng pip:
```sh
pip install lang_custom
```

**Lưu ý**: Phiên bản này **không tương thích ngược** với v1.0.14 hoặc cũ hơn do thay đổi lớn trong API và tích hợp database. Hãy cẩn thận khi nâng cấp!

## Có gì mới trong v1.1.0

- **Backend SQLite**: Dữ liệu ngôn ngữ được lưu trong database SQLite (`lang_custom/database/language.db`) thay vì parse từ JSON mỗi lần. Giảm sử dụng bộ nhớ và tăng tốc truy xuất, đặc biệt cho bot lớn.
- **API mới**:
  - `language_setup()`: Khởi tạo database SQLite, xóa sạch tất cả bảng và tải dữ liệu từ tệp JSON trong `import_language/`.
  - `get(language, group, type, name)`: Lấy dữ liệu từ SQLite. `type` là `"text"` (chuỗi cố định) hoặc `"random"` (chọn ngẫu nhiên từ danh sách).
  - `get_lang()`: Trả về danh sách ngôn ngữ hỗ trợ (ví dụ: `['en', 'vi', 'jp']`).
- **Xử lý lỗi cải tiến**: Trả về `None` cho `language`, `group`, hoặc `name` không hợp lệ. Cảnh báo console cho `type` sai (phải là `"text"` hoặc `"random"`).
- **Thay đổi phá vỡ**: Bỏ các phương thức cũ như `lang()`, `group()`, `get_text()`, `random_text()`. Cập nhật mã của bạn để dùng API `get()` mới.

## Hướng dẫn sử dụng

### 1. Nhập thư viện
```python
import lang_custom
```

### 2. Khởi tạo database
Trước khi dùng thư viện, gọi `language_setup()` trong script chính để thiết lập database SQLite và tải dữ liệu từ tệp JSON trong thư mục `import_language/`:
```python
lang_custom.language_setup()
```

Hàm này:
- Tạo thư mục `import_language/` và tệp `en.json` mặc định nếu không có tệp JSON nào.
- Tạo `lang_custom/database/language.db` với bảng cho mỗi ngôn ngữ (ví dụ: `en`, `vi`).
- Xóa sạch tất cả bảng hiện có và tải lại dữ liệu từ tệp JSON.

**Lưu ý**: Chỉ gọi `language_setup()` một lần trong script chính. Các module con có thể dùng `get()` hoặc `get_lang()` mà không cần khởi tạo lại.

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
- **Lưu trữ SQLite**: Dữ liệu ngôn ngữ được lưu trong `lang_custom/database/language.db`, giảm sử dụng bộ nhớ so với parse JSON liên tục.
- **Truy vấn nhanh**: Truy vấn SQLite nhanh hơn parse JSON, đặc biệt với dữ liệu lớn hoặc truy cập thường xuyên.
- **Khởi tạo một lần**: `language_setup()` tải dữ liệu một lần, các module con truy vấn database trực tiếp.

## Tương thích
**v1.1.0 không tương thích ngược** với v1.0.14 hoặc cũ hơn do:
- Kiến trúc mới dựa trên SQLite.
- Thay `lang()`, `group()`, `get_text()`, `random_text()` bằng `get()`.
- Bỏ cơ chế cache (SQLite đảm nhiệm hiệu suất).

Cập nhật mã của bạn theo [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng).

## Phản hồi & Báo lỗi
Gặp lỗi hoặc có ý kiến? Liên hệ tôi:
[Discord me](https://discord.gg/pGcSyr2bcY)

Cảm ơn bạn đã sử dụng Lang Custom! 🚀

![Cảm ơn](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)
