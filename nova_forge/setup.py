from setuptools import find_packages, setup

setup(
    name="nova_forge",
    version="0.1.0-alpha",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests>=2.28.0",
        "pandas>=2.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings",
        "graphviz",
    ],
    entry_points={
        "console_scripts": [
            "nova-forge=nova_forge.cli.commands:main",
        ],
    },
)
