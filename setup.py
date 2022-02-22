import sys

from setuptools import setup

if sys.version_info[0] < 3:
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
else:
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="cron-validator",
    packages=["cron_validator"],
    version="1.0.4",
    license="MIT",
    description="Unix cron implementation by Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="vcoder",
    author_email="doanngocbao@gmail.com",
    url="https://github.com/vcoder4c/cron-validator",
    keywords=["cron", "python", "cron expression validator", "cron expression iterator", "cron scheduler"],
    download_url="https://github.com/vcoder4c/cron-validator/archive/v1.0.4.tar.gz",
    install_requires=["python_dateutil", "pytz"],
)
