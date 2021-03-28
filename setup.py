from codecs import open

from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


setup(
    name="em-keyboard",
    description="The CLI Emoji Keyboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kenneth Reitz",
    author_email="me@kennethreitz.org",
    maintainer="Hugo van Kemenade",
    url="https://github.com/hugovk/em-keyboard",
    license="ISC",
    keywords=[
        "CLI",
        "emoji",
        "keyboard",
        "search",
    ],
    packages=["em"],
    package_data={"": ["LICENSE", "NOTICE"], "em": ["emoji-en-US.json"]},
    include_package_data=True,
    entry_points={"console_scripts": ["em=em:cli"]},
    zip_safe=False,
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=["setuptools_scm"],
    install_requires=["xerox; platform_system == 'Darwin'"],
    extras_require={"tests": ["pytest", "pytest-cov"]},
    python_requires=">=3.6",
    project_urls={
        "Source": "https://github.com/hugovk/em-keyboard",
    },
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
