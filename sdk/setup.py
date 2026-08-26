from setuptools import setup, find_packages

setup(
    name="instagram-poster-api",
    version="1.0.0",
    description="Official Python SDK for Instagram Automated Carousel & Post Publisher MicroSaaS API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Meanus Arcanus",
    author_email="meanusarcanus@gmail.com",
    url="https://github.com/meanusarcanus/instagram_poster_api",
    packages=find_packages(),
    install_requires=["requests>=2.25.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
