#####################################################################################
#
#  Copyright (C) MCode GmbH
#
#  Unless a separate license agreement exists between you and MCode GmbH (e.g. you
#  have purchased a commercial license), the license terms below apply.
#
#  Should you enter into a separate license agreement after having received a copy of
#  this software, then the terms of such license agreement replace the terms below at
#  the time at which such license agreement becomes effective.
#
#  In case a separate license agreement ends, and such agreement ends without being
#  replaced by another separate license agreement, the license terms below apply
#  from the time at which said agreement ends.
#
#  LICENSE TERMS
#
#  This program is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License, version 3, as published by the
#  Free Software Foundation. This program is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU Affero General Public License Version 3 for more details.
#
#  You should have received a copy of the GNU Affero General Public license along
#  with this program. If not, see <http://www.gnu.org/licenses/agpl-3.0.en.html>.
#
#####################################################################################

import os
from setuptools import setup, find_namespace_packages

about = {}
base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "pyclm", "monitoring", "__about__.py")) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.md"), "r") as f:
    long_description = f.read()


def parse_requirements_file(filename):
    with open(filename) as fid:
        return [ln.strip() for ln in fid if ln.strip() and not ln.strip().startswith("#")]


install_requires = parse_requirements_file("requirements.txt")

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=about["__license__"],
    url=about["__uri__"],
    project_urls={
        "Bug Tracker": "https://github.com/mcode-cc/python-yandex-cloud-monitoring/issues",
    },
    author=about["__author__"],
    author_email=about["__email__"],
    platforms=['Any'],
    install_requires=install_requires,
    packages=find_namespace_packages(include=["pyclm.*"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6,<=3.8",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Development Status :: 3 - Alpha",
        "Environment :: No Input/Output (Daemon)",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Networking"
    ],
    keywords='yandex cloud monitoring trace'
)
