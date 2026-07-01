import re
from setuptools import setup, find_packages

with open("src/pati/__init__.py") as f:
    version = re.search(r'__version__ = "([^"]+)"', f.read()).group(1)

setup(
    name="patisserie",
    version=version,
    author="Peter Verhas",
    author_email="peter.verhas@gmail.com",
    description="Language-agnostic boilerplate generator from YAML data models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT OR Apache-2.0",
    url="https://github.com/yourusername/pati",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "pati": ["examples/**/*"],
    },
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "jinja2>=3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "twine>=4.0",
            "build>=0.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "pati=pati.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
