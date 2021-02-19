import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygonets", # Replace with your own username
    version="0.0.1",
    author="Boris Resnick",
    author_email="boris@resnick.ru",
    description="SS Gonets Terminal Protocol Implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scartill/pygonets",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
