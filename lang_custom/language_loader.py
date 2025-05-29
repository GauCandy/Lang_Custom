# Lang Custom v1.1.2

**Lang Custom** là một thư viện Python giúp quản lý và tải bản dịch từ các tệp JSON, sử dụng **SQLite** để đạt hiệu suất cao và giảm tiêu tốn bộ nhớ. Tạm biệt việc parse JSON lằng nhằng và chào đón một hệ thống ngôn ngữ chuẩn hóa, không còn đau đầu!

## Tại sao dùng Lang Custom?

Lang Custom ra đời để đơn giản hóa hỗ trợ đa ngôn ngữ cho bot và ứng dụng. Quản lý bản dịch có thể trở nên hỗn loạn nếu không có hệ thống chuẩn—tệp JSON rải rác, parse không đồng nhất, không có tiêu chuẩn. Thư viện này mang lại trật tự với API rõ ràng, lưu trữ bằng SQLite, và các tệp ngôn ngữ tùy chỉnh. Dù bạn xây dựng bot nhỏ hay ứng dụng lớn, Lang Custom giúp quản lý ngôn ngữ đáng tin cậy và hiệu quả.

## Cài đặt

Cài đặt thư viện bằng pip:
```sh
pip install lang_custom==1.1.2
```

## Hướng dẫn sử dụng

### 1. Nhập thư viện
```python
import lang_custom
```

### 2. Khởi tạo database
Gọi `language_setup()` trong script chính để thiết lập database SQLite và tải dữ liệu từ tệp JSON trong thư mục `_data_language/`:
```python
lang_custom.language_setup()
```

Hàm này:
- Tạo thư mục `_data_language/` và tệp `en.json` mặc định nếu không có tệp JSON nào.
- Tạo `_data_language/DO_NOT_DELETE.db` với bảng cho mỗi ngôn ngữ (ví dụ: `en`, `vi`).
- Xóa sạch tất cả bảng hiện có và tải lại dữ liệu từ tệp JSON.

**Quan trọng**:
- Chỉ gọi `language_setup()` một lần trong script chính. Các module con có thể dùng `get()`, `get_lang()`, hoặc `reload_language()` mà không cần khởi tạo lại.
- **Không xóa** thư mục `_data_language/` hoặc tệp `DO_NOT_DELETE.db`, đặc biệt khi bot hoặc ứng dụng đang chạy, vì sẽ gây mất dữ liệu và lỗi.

### 3. Lấy danh sách ngôn ngữ hỗ trợ
Để xem các ngôn ngữ có sẵn (dựa trên tệp JSON hoặc bảng SQLite):
```python
import asyncio
languages = asyncio.run(lang_custom.get_lang())
print(languages)  # Ví dụ: ['en', 'vi', 'jp']
```

### 4. Tải lại dữ liệu ngôn ngữ
Sử dụng `reload()` để tải lại tất cả dữ liệu từ các tệp JSON hoặc `reload_language(language)` để tải lại dữ liệu cho một ngôn ngữ cụ thể:
```python
# Tải lại tất cả ngôn ngữ
asyncio.run(lang_custom.reload())

# Tải lại một ngôn ngữ cụ thể
asyncio.run(lang_custom.reload_language("vi"))
```

### 5. Lấy dữ liệu ngôn ngữ
Dùng `get(language, group, type, name)` để lấy dữ liệu từ SQLite:
- `language`: Tên ngôn ngữ (ví dụ: `"en"`, `"vi"`).
- `group`: Nhóm dữ liệu trong cấu trúc JSON (ví dụ: `"reply"`, `"error"`).
- `type`: `"text"` cho chuỗi cố định hoặc `"random"` cho chọn ngẫu nhiên từ danh sách.
- `name`: Khóa trong nhóm (ví dụ: `"greeting"`, `"greetings"`).

Ví dụ:
```python
# Lấy chuỗi cố định
text = asyncio.run(lang_custom.get(language="en", group="error", type="text", name="not_found"))
print(text)  # Output: Resource not found

# Lấy chuỗi ngẫu nhiên từ danh sách
random_text = asyncio.run(lang_custom.get(language="en", group="reply", type="random", name="greetings"))
print(random_text)  # Output: hello :D hoặc hi :3 hoặc hey there!
```

Nếu `language`, `group`, hoặc `name` không tồn tại, hoặc `type` không hợp lệ (không phải `"text"` hoặc `"random"`), hàm trả về `None` và hiển thị cảnh báo trên console, ví dụ:
```
lang_custom/language_loader.py:XXX: UserWarning: No data found for group 'reply' in language 'en'. Did you mean 'replies'?
```

### 6. Cấu trúc tệp
Tệp ngôn ngữ được lưu trong `_data_language/` (bản dịch do người dùng thêm). Ví dụ `_data_language/en.json`:
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

Thêm tệp JSON của bạn (ví dụ: `vi.json`, `jp.json`) vào `_data_language/` với cấu trúc tương tự. Chạy `language_setup()` hoặc `reload()` để tải chúng vào SQLite.

## Có gì mới trong v1.1.2?

- **Hỗ trợ bất đồng bộ**: Thêm các hàm bất đồng bộ `reload()`, `reload_language()`, `get_lang()`, và `get()` sử dụng `aiosqlite` để hỗ trợ ứng dụng bất đồng bộ.
- **Kiểm tra lỗi nâng cao**: Cảnh báo chi tiết hơn khi `language`, `group`, hoặc `name` không tồn tại, với gợi ý từ `difflib` (ví dụ: "Did you mean 'replies'?").
- **Tối ưu hiệu suất**: Giao dịch độc quyền (`BEGIN EXCLUSIVE TRANSACTION`) trong `reload()` và `reload_language()` để đảm bảo tính toàn vẹn dữ liệu.
- **Cải thiện bảo trì**: Loại bỏ mã trùng lặp và tối ưu hóa quy trình tải dữ liệu.

## Lợi ích hiệu suất
- **Lưu trữ SQLite**: Dữ liệu ngôn ngữ được lưu trong `_data_language/DO_NOT_DELETE.db`, giảm sử dụng bộ nhớ so với parse JSON liên tục.
- **Truy vấn nhanh**: Truy vấn SQLite nhanh hơn parse JSON, đặc biệt với dữ liệu lớn hoặc truy cập thường xuyên.
- **Khởi tạo một lần**: `language_setup()` tải dữ liệu một lần, các module con truy vấn database trực tiếp.

## Tương thích
**v1.1.2 không tương thích ngược** với v1.0.14 hoặc cũ hơn do:
- Kiến trúc mới dựa trên SQLite.
- Thay `lang()`, `group()`, `get_text()`, `random_text()` bằng `get()`.
- Thêm hỗ trợ bất đồng bộ và các hàm mới như `reload()`, `reload_language()`.

Cập nhật mã của bạn theo [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng).

## Lưu ý quan trọng
- **Không xóa** thư mục `_data_language/` hoặc tệp `DO_NOT_DELETE.db` khi bot hoặc ứng dụng đang chạy. Tệp này chứa toàn bộ dữ liệu ngôn ngữ, và xóa nó sẽ khiến ứng dụng lỗi.
- Nếu cần reset database, gọi lại `language_setup()` hoặc `reload()`, nhưng lưu ý các hàm này sẽ xóa và tải lại toàn bộ dữ liệu từ tệp JSON.
- Các hàm `get()`, `get_lang()`, `reload()`, và `reload_language()` là bất đồng bộ, cần sử dụng `asyncio.run()` hoặc trong một vòng lặp sự kiện.

## Phản hồi & Báo lỗi
Gặp lỗi hoặc có ý kiến? Liên hệ tôi:
[Discord me](https://discord.gg/pGcSyr2bcY)

Cảm ơn bạn đã sử dụng Lang Custom! 🚀

![Cảm ơn](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)
