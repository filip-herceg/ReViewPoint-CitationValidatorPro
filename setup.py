"""
Setup script for Citation Validator Pro package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    requirements = [
        "beautifulsoup4>=4.12.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0"
    ]

setup(
    name="citation-validator-pro",
    version="2.0.0",
    author="Filip Herceg",
    author_email="filip.herceg@example.com",
    description="A comprehensive tool for validating academic citations using LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filip-herceg/ReViewPoint-CitationValidatorPro",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Markup :: HTML",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="citation, validation, academic, research, llm, ai, html",
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.991",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-mock>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "citation-validator=citation_validator.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/filip-herceg/ReViewPoint-CitationValidatorPro/issues",
        "Source": "https://github.com/filip-herceg/ReViewPoint-CitationValidatorPro",
        "Documentation": "https://github.com/filip-herceg/ReViewPoint-CitationValidatorPro#readme",
    },
)
