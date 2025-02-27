# Lang Custom

Lang Custom is a simple Python library for managing and loading translations from JSON files.

## Why did I create Lang Custom?

One day, I decided to make my bot support multiple languages. However, when searching for translation libraries, I realized that most of them were quite bad. So, I decided to create my own language files with customizable tone.

At first, managing language files seemed simple, but then I realized that without a proper library, things became messy. Even though they were all JSON files, different code sections loaded language data in different ways—especially if you used AI tools like ChatGPT for assistance. There was no universal standard.

Looking back at my code, I could only exclaim: **"Oh my god, this looks horrible!"** I wasn’t sure if my code was working as intended, and every time I made changes, I feared that while some parts would still work fine, others might crash due to inconsistent handling.

That's why I created **Lang Custom**—a library to help manage language systems more easily, consistently, and without the headaches.

## Installation

You can install this library using pip:
```sh
pip install lang_custom
```

## Usage Guide

### 1. Import the library
```python
import lang_custom
```

### 2. Get available language files
The library will automatically detect all JSON language files stored in the `Lang_data` directory inside your source code. To list all available language files, use:
```python
languages = lang_custom.get()
print(languages)  #example: en,vi,.. depending on the number of json files in the Lang_Data folder
```
Where each item represents a JSON file found in the language directories.

### 3. Select a data group
Before retrieving text, you need to select a data group from the JSON file:
```python
lang_custom.set_group("name")
```
Where `name` is the group you want to access in the JSON structure.

### 4. Retrieve text data
After selecting a group, retrieve text using:
```python
text = lang_custom.get_text("en", "text")
print(text)  # Displays the corresponding value for key "text" in group "name" from en.json
```
Where:
- `"en.json"` is the file name of the language you want to use.
- `"text"` is the key to retrieve within the selected group.

## Language File Structure
Each language file is stored in either the `Lang_Custom` directory (default translations) or `Lang_data` (user-added translations). Example of `Lang_Custom/en.json`:
```json
{
    "name": {
        "text": "hello friend :D",
        "example": "text2"
    },
    "name2": {
        "example": "text",
        "example2": "text2"
    }
}
```
Users can add their own JSON language files in the `Lang_data` directory, as long as they follow the correct structure.

## Feedback & Issues
For any feedback or issues, please contact me:
[Discord me](https://discord.gg/pGcSyr2bcY)

Thank you for using Lang_custom

![Thank You](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)

# Lang Custom

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

## Hướng dẫn sử dụng

### 1. Nhập thư viện
```python
import lang_custom
```

### 2. Lấy danh sách các tệp ngôn ngữ có sẵn
Thư viện sẽ tự động phát hiện tất cả các tệp JSON trong thư mục `Lang_data` trong mã nguồn của bạn. Để liệt kê các tệp ngôn ngữ có sẵn, sử dụng:
```python
languages = lang_custom.get()
print(languages)  # Ví dụ: en,vi,.. tùy vào số lượng file json trong thư mục Lang_Data
```
Mỗi phần tử trong danh sách đại diện cho một tệp JSON có trong thư mục ngôn ngữ.

### 3. Chọn nhóm dữ liệu
Trước khi lấy dữ liệu văn bản, bạn cần chọn một nhóm dữ liệu từ tệp JSON:
```python
lang_custom.set_group("name")
```
Trong đó `name` là nhóm bạn muốn truy cập trong cấu trúc JSON.

### 4. Lấy dữ liệu văn bản
Sau khi chọn nhóm, bạn có thể lấy văn bản bằng cách sử dụng:
```python
text = lang_custom.get_text("en", "text")
print(text)  # Hiển thị giá trị tương ứng với khóa "text" trong nhóm "name" từ en.json
```
Trong đó:
- `"en.json"` là tệp ngôn ngữ bạn muốn sử dụng.
- `"text"` là khóa bạn muốn lấy trong nhóm đã chọn.

## Cấu trúc tệp ngôn ngữ
Mỗi tệp ngôn ngữ được lưu trong thư mục `Lang_Custom` (bản dịch mặc định) hoặc `Lang_data` (bản dịch do người dùng thêm vào). Ví dụ về `Lang_Custom/en.json`:
```json
{
    "name": {
        "text": "hello friend :D",
        "example": "text2"
    },
    "name2": {
        "example": "text",
        "example2": "text2"
    }
}
```
Người dùng có thể thêm các tệp JSON ngôn ngữ của riêng mình trong thư mục `Lang_data`, miễn là tuân theo cấu trúc hợp lệ.

## Phản hồi & Báo lỗi
Nếu bạn có phản hồi hoặc gặp vấn đề, vui lòng liên hệ tôi:
[Discord me](https://discord.gg/pGcSyr2bcY)

Cảm ơn bạn đã sử dụng Lang_Custom!

![Cảm ơn](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)


