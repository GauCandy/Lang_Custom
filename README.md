# Lang Custom v1.1.4

**Lang Custom** is a Python library for managing translations from JSON files, powered by **SQLite** for fast queries and low memory usage. Perfect for bots or multilingual apps needing high performance and easy maintenance.

---

## 🆕 What's New in v1.1.4?

* ✅ **Default Parameters**: Set default `language`, `group`, and `type` to simplify calls to `get` and `batch`:
  ```python
  await lang_custom.default(language="en", group="reply", type="text")
  text = await lang_custom.get(name="greeting")  # Uses defaults
  ```
* ✅ **Batch Retrieval**: Fetch multiple values at once with a single query:
  ```python
  result = await lang_custom.batch(language="en", group="error", type="text", names=["not_found", "invalid", "missing"])
  print(result)  # {'not_found': 'Resource not found', 'invalid': 'Invalid input', 'missing': ''}
  ```
* ✅ **Auto-initialization**: Database and JSON files are loaded on `import lang_custom`. No need for `language_setup()`.
* ✅ Support for **full reload** or **single-language reload** from JSON.
* ✅ Smart warnings: Suggests corrections for invalid `group`, `name`, or `type` (e.g., "Did you mean 'replies'?").
* ✅ Unified API: Replaced old `lang()`, `group()`, `get_text()`, `random_text()` with a single function:
  ```python
  await lang_custom.get(language="en", group="error", type="text", name="not_found")
  ```

---

## 📦 Installation

```bash
pip install lang_custom==1.1.4
```

---

## 🚀 Usage Guide

### 1. Import the library

```python
import lang_custom
```

Database is automatically initialized, ready to use 🎉

---

### 2. Set default parameters (optional)

Simplify queries by setting defaults for `language`, `group`, and `type`:

```python
await lang_custom.default(language="en", group="reply", type="text")
```

---

### 3. Query language data

```python
# Using defaults
text = await lang_custom.get(name="greeting")  # Uses language="en", group="reply", type="text"
print(text)  # hello :D

# Override defaults
random_text = await lang_custom.get(type="random", name="greetings")
print(random_text)  # hello :D, hi :3, or hey there!

# Full parameters
error_text = await lang_custom.get(language="en", group="error", type="text", name="not_found")
print(error_text)  # Resource not found
```

* `type="text"`: Returns a fixed string.
* `type="random"`: Returns a random item from a list.

---

### 4. Batch query multiple values

Fetch multiple values in one call:

```python
result = await lang_custom.batch(names=["greeting", "welcome", "missing"])  # Uses defaults
print(result)  # {'greeting': 'hello :D', 'welcome': 'hi :3', 'missing': ''}

# With full parameters
result = await lang_custom.batch(language="en", group="error", type="text", names=["not_found", "invalid"])
print(result)  # {'not_found': 'Resource not found', 'invalid': 'Invalid input'}
```

---

### 5. List available languages

```python
langs = await lang_custom.get_lang()
print(langs)  # ['en', 'vi', 'jp']
```

---

### 6. Reload language data

```python
await lang_custom.reload()  # Reload all from JSON
await lang_custom.reload_language("en")  # Reload only "en"
```

---

## 📁 Example `_data_language/en.json`

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

---

## ⚠️ Notes

* **Do not delete** the `_data_language/` folder or `DO_NOT_DELETE.db` file while the app is running.
* To update translations, edit JSON files and call `reload()` or `reload_language()`.

---

## 💬 Feedback & Issues

Join our Discord:
👉 [https://discord.gg/pGcSyr2bcY](https://discord.gg/pGcSyr2bcY)

---

Thank you for using **Lang Custom**! 🚀  
![Thank you](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)

---

# Lang Custom v1.1.4

**Lang Custom** là thư viện Python quản lý bản dịch từ tệp JSON, dùng **SQLite** để truy vấn nhanh và tiết kiệm bộ nhớ. Lý tưởng cho bot hoặc ứng dụng đa ngôn ngữ cần hiệu suất cao và dễ bảo trì.

---

## 🆕 Có gì mới trong v1.1.4?

* ✅ **Thiết lập mặc định**: Đặt `language`, `group`, và `type` mặc định để đơn giản hóa `get` và `batch`:
  ```python
  await lang_custom.default(language="en", group="reply", type="text")
  text = await lang_custom.get(name="greeting")  # Dùng giá trị mặc định
  ```
* ✅ **Lấy hàng loạt**: Lấy nhiều giá trị cùng lúc trong một truy vấn:
  ```python
  result = await lang_custom.batch(language="en", group="error", type="text", names=["not_found", "invalid", "missing"])
  print(result)  # {'not_found': 'Resource not found', 'invalid': 'Invalid input', 'missing': ''}
  ```
* ✅ **Tự động khởi tạo**: Database và JSON được load ngay khi `import lang_custom`. Không cần gọi `language_setup()`.
* ✅ Hỗ trợ **reload toàn bộ** hoặc **reload một ngôn ngữ** từ JSON.
* ✅ Cảnh báo thông minh: Gợi ý khi `group`, `name`, hoặc `type` sai (ví dụ: "Did you mean 'replies'?").
* ✅ Gộp hàm cũ (`lang()`, `group()`, `get_text()`, `random_text()`) thành một hàm duy nhất:
  ```python
  await lang_custom.get(language="en", group="error", type="text", name="not_found")
  ```

---

## 📦 Cài đặt

```bash
pip install lang_custom==1.1.4
```

---

## 🚀 Hướng dẫn sử dụng

### 1. Nhập thư viện

```python
import lang_custom
```

Database tự động khởi tạo, sẵn sàng sử dụng 🎉

---

### 2. Thiết lập tham số mặc định (tùy chọn)

Đơn giản hóa truy vấn bằng cách đặt mặc định cho `language`, `group`, và `type`:

```python
await lang_custom.default(language="en", group="reply", type="text")
```

---

### 3. Truy vấn dữ liệu ngôn ngữ

```python
# Sử dụng mặc định
text = await lang_custom.get(name="greeting")  # Dùng language="en", group="reply", type="text"
print(text)  # hello :D

# Ghi đè mặc định
random_text = await lang_custom.get(type="random", name="greetings")
print(random_text)  # hello :D, hi :3, hoặc hey there!

# Đầy đủ tham số
error_text = await lang_custom.get(language="en", group="error", type="text", name="not_found")
print(error_text)  # Resource not found
```

* `type="text"`: Lấy chuỗi cố định.
* `type="random"`: Lấy ngẫu nhiên từ danh sách.

---

### 4. Truy vấn hàng loạt

Lấy nhiều giá trị trong một lần gọi:

```python
result = await lang_custom.batch(names=["greeting", "welcome", "missing"])  # Dùng mặc định
print(result)  # {'greeting': 'hello :D', 'welcome': 'hi :3', 'missing': ''}

# Với đầy đủ tham số
result = await lang_custom.batch(language="en", group="error", type="text", names=["not_found", "invalid"])
print(result)  # {'not_found': 'Resource not found', 'invalid': 'Invalid input'}
```

---

### 5. Lấy danh sách ngôn ngữ

```python
langs = await lang_custom.get_lang()
print(langs)  # ['en', 'vi', 'jp']
```

---

### 6. Tải lại dữ liệu ngôn ngữ

```python
await lang_custom.reload()  # Tải lại toàn bộ từ JSON
await lang_custom.reload_language("en")  # Tải lại ngôn ngữ "en"
```

---

## 📁 Ví dụ file `_data_language/en.json`

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

---

## ⚠️ Lưu ý

* **Không xóa** thư mục `_data_language/` hoặc file `DO_NOT_DELETE.db` khi ứng dụng đang chạy.
* Cập nhật bản dịch? Chỉnh file JSON và gọi `reload()` hoặc `reload_language()`.

---

## 💬 Góp ý & Báo lỗi

Tham gia Discord:
👉 [https://discord.gg/pGcSyr2bcY](https://discord.gg/pGcSyr2bcY)

---

Cảm ơn bạn đã sử dụng **Lang Custom**! 🚀  
![Cảm ơn](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)