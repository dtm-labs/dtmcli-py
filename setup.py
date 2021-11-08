import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dtmcli",
    version="1.5.1.0",
    author="yedf2",
    author_email="120050102@qq.com",
    description="python client for dtm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yedf/dtmcli-py",
    packages=setuptools.find_packages(),
    install_requires=['requests>=2.1.0','pymysql>=1.0.1'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
