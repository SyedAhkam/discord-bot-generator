from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

exec(open("discord_bot_generator/__version__.py").read())


setup(
    name="discord-bot-generator",
    version=__version__,
    author="SyedAhkam",
    author_email="smahkam57@gmail.com",
    description="Fastest and easiest way to create a new discord bot project ✨🚀",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SyedAhkam/discord-bot-generator",
    packages=find_packages(exclude=["tests"]),
    py_modules=["discord-bot-generator"],
    install_requires=["click", "colorama"],
    setup_requires=[],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        discord-bot-generator=discord_bot_generator:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
)
