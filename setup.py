from setuptools import setup, find_packages

setup(
    name = "komunist",
    version = "0.1",
    packages = find_packages(exclude=["tests", "docs", "scripts", "db"]),

    description = "Search"
)
