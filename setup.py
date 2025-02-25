from setuptools import setup, find_packages

# Đọc nội dung từ README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lang_custom",
    version="1.0.9",
    author="Gấu Kẹo",
    author_email="you@example.com",
    description="Mô tả ngắn gọn về thư viện",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    url="https://github.com/GauCandy/lang_custom",
    packages=find_packages(),  # Tự động tìm tất cả thư mục có __init__.py
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,  
)
