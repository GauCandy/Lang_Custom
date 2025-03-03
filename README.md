# Lang Custom v1.0.14

Lang Custom is a simple Python library that helps manage and load translations from JSON files.

## Why did I create Lang Custom?

One day, I decided to make my bot support multiple languages. However, when searching for translation libraries, I realized that most of them were quite bad. So, I decided to create my own language files with customizable tones.

Initially, managing language files seemed simple, but then I realized that without a standard library, everything became very messy. Even though they were all JSON files, different code segments loaded language data in their own way—especially if you use AI tools like ChatGPT for assistance. There was no common standard.

Looking back at my source code, I could only exclaim: **"It's amazing it doesn't crash :v"** I wasn't sure if my code was working as expected, and every time I made changes, I was always worried that some parts would still work fine, but others might encounter errors due to inconsistent handling.

So, I created **Lang Custom**—a library that helps manage the language system more easily, consistently, and without headaches.

## Installation

You can install this library using pip:
```sh
pip install lang_custom
```
## What's new

Updated output structure:
```python
lang_custom.get() 
```
Version 1.0.14:
```python
languages = lang_custom.get()
print(languages)
```
Console output will be in the format:
```['en', 'vi', 'jp',..]```
instead of version 1.0.11:
```en,vi,jp,..```

## Usage Guide

### 1. Import the library
```python
import lang_custom
```

### 2. Get the list of available language files
The library will automatically detect all JSON files in the `Lang_data` directory in your source code. To list the available language files, use:
```python
languages = lang_custom.get()
print(languages)  # Example: ['en', 'vi', 'jp',..] depending on the number of JSON files in the Lang_Data directory
```

console example
```
['en', 'vi', 'jp']
```

Each element in the list represents a JSON file in the language directory.

### 3. Select language and data group
Before retrieving text data, you need to select a language and data group from the JSON file:
```python
lang_custom.lang("en").group("bot_random", cache=True)
```
Where:
- `"en"` is the language you want to use.
- `"bot_random"` is the group you want to access in the JSON structure.
- `cache=True` is an option to use cache to help the bot retrieve data faster (the downside is that it does not update in real-time, the default if not specified is `True`). You must use the `reload` method to update if needed.

### 4. Retrieve text data
After selecting the language and group, you can retrieve the text using:
```python
text = lang_custom.lang("en").group("bot_reply", cache=True).get_text("text1")
print(text)  # Displays the value corresponding to the key "text1" in the group "bot_random" from en.json
```

console example
```
hello :D
```

Or retrieve random text from a list:
```python
random_text = lang_custom.lang("en").group("bot_random").random_text("text_random")
print(random_text)  # Displays a random value from the list "text_random" in the group "bot_random" from en.json
```

console example
```
text1 or text2 or 3
```

### 5. Clear and update cache
If you want to clear and update all cache, you can use the `reload` method:
```python
lang_custom.reload()
```
This method will clear all cache and update data from the JSON files.

## Language file structure
Each language file is stored in the `Lang_Custom` directory (default translations) or `Lang_data` directory (user-added translations). Example of `Lang_Custom/en.json`:
```json
{
    "bot_reply": {
        "text1": "hello :D",
        "text2": "hi :3"
    },
    "bot_random": {
        "instruct": "use square brackets to random",
        "text_random": ["text1", "text2", "text.."]
    }
}
```
Users can add their own language JSON files in the `Lang_data` directory, as long as they follow the valid structure.

## Feedback & Issues
If you have feedback or encounter issues, please contact me:
[Discord me](https://discord.gg/pGcSyr2bcY)

Thank you for using Lang_Custom!

![Thank you](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)



# Lang Custom v1.0.14

Lang Custom là một thư viện Python đơn giản giúp quản lý và tải bản dịch từ các tệp JSON.

## Tại sao tôi tạo ra Lang Custom?

Một ngày nọ, tôi quyết định làm cho bot của mình hỗ trợ nhiều ngôn ngữ. Tuy nhiên, khi tìm kiếm các thư viện dịch thuật, tôi nhận ra rằng hầu hết chúng đều khá tệ. Vì vậy, tôi quyết định tự tạo các tệp ngôn ngữ với ngữ điệu có thể tùy chỉnh.

Ban đầu, việc quản lý các tệp ngôn ngữ có vẻ đơn giản, nhưng sau đó tôi nhận ra rằng nếu không có một thư viện chuẩn, mọi thứ trở nên rất lộn xộn. Dù tất cả đều là tệp JSON, nhưng các đoạn mã khác nhau lại tải dữ liệu ngôn ngữ theo cách riêng—đặc biệt nếu bạn dùng các công cụ AI như ChatGPT để hỗ trợ. Không có một tiêu chuẩn chung nào cả.

Nhìn lại mã nguồn của mình, tôi chỉ có thể thốt lên: **"Tởm vl nó ko crash được cũng hay đấy :v"** không chắc liệu đoạn mã của mình có hoạt động đúng như mong muốn không, và mỗi khi chỉnh sửa, lúc nào cũng lo sợ rằng một số phần vẫn hoạt động tốt, nhưng những phần khác có thể gặp lỗi do xử lý không đồng nhất.

Vì vậy, tôi đã tạo ra **Lang Custom**—một thư viện giúp quản lý hệ thống ngôn ngữ dễ dàng hơn, nhất quán hơn và không còn gây đau đầu nữa.

## Cài đặt

Bạn có thể cài đặt thư viện này bằng pip:
```sh
pip install lang_custom
```
## Có gì mới

Sửa lại cấu trúc xuất ra:
```python
lang_custom.get() 
```
Phiên bản 1.0.14:
```python
languages = lang_custom.get()
print(languages)
```
Console sẽ có dạng:
```['en', 'vi', 'jp',..]```
thay vì như 1.0.11:
```en,vi,jp,..```

## Hướng dẫn sử dụng

### 1. Nhập thư viện
```python
import lang_custom
```

### 2. Lấy danh sách các tệp ngôn ngữ có sẵn
Thư viện sẽ tự động phát hiện tất cả các tệp JSON trong thư mục `Lang_data` trong mã nguồn của bạn. Để liệt kê các tệp ngôn ngữ có sẵn, sử dụng:
```python
languages = lang_custom.get()
print(languages)  # Ví dụ: ['en', 'vi', 'jp',..] tùy vào số lượng file json trong thư mục Lang_Data
```

console example
```
['en', 'vi', 'jp']
```

Mỗi phần tử trong danh sách đại diện cho một tệp JSON có trong thư mục ngôn ngữ.

### 3. Chọn ngôn ngữ và nhóm dữ liệu
Trước khi lấy dữ liệu văn bản, bạn cần chọn ngôn ngữ và nhóm dữ liệu từ tệp JSON:
```python
lang_custom.lang("en").group("bot_random", cache=True)
```
Trong đó:
- `"en"` là ngôn ngữ bạn muốn sử dụng.
- `"bot_random"` là nhóm bạn muốn truy cập trong cấu trúc JSON.
- `cache=True` là tùy chọn để sử dụng cache giúp bot truy xuất dữ liệu nhanh hơn (nhược điểm không cập nhật nóng được, mặc định nếu bạn không đề cập là `True`). Bạn phải sử dụng phương thức `reload` để cập nhật lại nếu muốn.

### 4. Lấy dữ liệu văn bản
Sau khi chọn ngôn ngữ và nhóm, bạn có thể lấy văn bản bằng cách sử dụng:
```python
text = lang_custom.lang("en").group("bot_reply", cache=True).get_text("text1")
print(text)  # Hiển thị giá trị tương ứng với khóa "text1" trong nhóm "bot_random" từ en.json
```

console example
```
hello :D
```

Hoặc lấy văn bản ngẫu nhiên từ danh sách:
```python
random_text = lang_custom.lang("en").group("bot_random").random_text("text_random")
print(random_text)  # Hiển thị một giá trị ngẫu nhiên từ danh sách "text_random" trong nhóm "bot_random" từ en.json
```

console example
```
text1 or text2 or 3
```

### 5. Xóa và cập nhật lại cache
Nếu bạn muốn xóa và cập nhật lại tất cả cache, bạn có thể sử dụng phương thức `reload`:
```python
lang_custom.reload()
```
Phương thức này sẽ xóa toàn bộ cache và cập nhật lại dữ liệu từ các tệp JSON.

## Cấu trúc tệp ngôn ngữ
Mỗi tệp ngôn ngữ được lưu trong thư mục `Lang_Custom` (bản dịch mặc định) hoặc `Lang_data` (bản dịch do người dùng thêm vào). Ví dụ về `Lang_Custom/en.json`:
```json
{
    "bot_reply": {
        "text1": "hello :D",
        "text2": "hi :3"
    },
    "bot_random": {
        "instruct": "use square brackets to random",
        "text_random": ["text1", "text2", "text.."]
    }
}
```
Người dùng có thể thêm các tệp JSON ngôn ngữ của riêng mình trong thư mục `Lang_data`, miễn là tuân theo cấu trúc hợp lệ.

## Phản hồi & Báo lỗi
Nếu bạn có phản hồi hoặc gặp vấn đề, vui lòng liên hệ tôi:
[Discord me](https://discord.gg/pGcSyr2bcY)

Cảm ơn bạn đã sử dụng Lang_Custom!

![Cảm ơn](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)


