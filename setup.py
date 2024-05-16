from setuptools import setup, find_packages

with open("README.md", "r") as fp:
    readme = fp.read()

DESCRIPTION = "An improved wrapper for ollama that allows for one-shot launching of local models with URL specification."

setup(
    name="oyama",
    version="0.0.1",
    author="HawkClaws",
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    url="https://github.com/HawkClaws/oyama",
    project_urls={"Source Code": "https://github.com/HawkClaws/oyama"},
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    install_requires=[
        "tqdm",
    ],
)
