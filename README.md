# Lang Custom v1.0.11

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

Sửa lại logic:
cũ
```python
lang_custom.set_group("name")
lang_custom.get_text("en", "text")
```
thành giúp dễ dàng kiểm soát hơn
```python
lang_custom.lang("en").group("name").get_text("text")
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

console example
```
en,vi,jp
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
- `cache=True` là tùy chọn để sử dụng cache giúp bot truy xuất dữ liệu nhanh hơn (nhược điểm không cập nhập nóng được mặc định nếu bạn không đề cập là `True`).

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


