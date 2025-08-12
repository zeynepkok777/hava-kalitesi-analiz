from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hava-kalitesi-analiz",
    version="1.0.0",
    author="Hava Kalitesi Uzmanı",
    author_email="info@hava-kalitesi.com",
    description="AI destekli hava kalitesi analiz ve öneri sistemi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/hava-kalitesi-projesi",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "hava-kalitesi=app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
