import os
import io
import tarfile
from pathlib import Path

sdk_dir = Path(__file__).parent
dist_dir = sdk_dir / "dist"
dist_dir.mkdir(exist_ok=True)

pkg_info_content = """Metadata-Version: 2.1
Name: instagram-poster-api
Version: 1.0.0
Summary: Official Python SDK for Instagram Automated Carousel & Post Publisher MicroSaaS API.
Home-page: https://github.com/meanusarcanus/instagram_poster_api
Author: Meanus Arcanus
Author-email: meanusarcanus@gmail.com
License: MIT
Description-Content-Type: text/markdown

# 📸 Instagram Automated Carousel & Post Publisher Python SDK

Official Python SDK for `instagram-poster-api`. Turn product URLs into 5-slide 1080x1350 visual carousel posts, AI copywriting, Amazon affiliate link tagging, and Instagram publishing in 1 line of Python code.
"""

tar_path = dist_dir / "instagram_poster_api-1.0.0.tar.gz"

with tarfile.open(tar_path, "w:gz") as tar:
    info = tarfile.TarInfo(name="instagram_poster_api-1.0.0/PKG-INFO")
    data = pkg_info_content.encode("utf-8")
    info.size = len(data)
    tar.addfile(info, fileobj=io.BytesIO(data))

    setup_file = sdk_dir / "setup.py"
    if setup_file.exists():
        tar.add(setup_file, arcname="instagram_poster_api-1.0.0/setup.py")

    pyproject_file = sdk_dir / "pyproject.toml"
    if pyproject_file.exists():
        tar.add(pyproject_file, arcname="instagram_poster_api-1.0.0/pyproject.toml")

    readme_file = sdk_dir / "README.md"
    if readme_file.exists():
        tar.add(readme_file, arcname="instagram_poster_api-1.0.0/README.md")

    pkg_dir = sdk_dir / "instagram_poster"
    for f in pkg_dir.glob("*.py"):
        tar.add(f, arcname=f"instagram_poster_api-1.0.0/instagram_poster/{f.name}")

print(f"✓ Rebuilt valid PyPI sdist with PKG-INFO: {tar_path}")
