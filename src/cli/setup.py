import setuptools

INSTALL_REQUIRES = [
    'certifi',
    'charset-normalizer',
    'docker',
    'fire',
    'idna',
    'requests',
    'six',
    'tabulate',
    'termcolor',
    'toml',
    'urllib3',
    'websocket-client'
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bm-cli",
    version="0.1.2",
    author="coyote963",
    author_email="coyoteandbird@gmail.com",
    description="Command line interface for boring man servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coyote963/bm-server-tools/",
    project_urls={
        "Bug Tracker": "https://github.com/coyote963/bm-server-tools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [
            'bmcli = bm_cli.cli:main',
        ]
    }
)