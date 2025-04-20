from setuptools import setup, find_packages

# Đọc nội dung từ README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lang_custom",
    version="1.1.1",
    author="Gấu Kẹo",
    author_email="gaulolipop@gmail.com",
    description="A simple language manager for Python projects.",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    url="https://github.com/GauCandy/lang_custom",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,  
)
