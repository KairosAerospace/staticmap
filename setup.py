from __future__ import print_function

# largely borrowed from
# https://github.com/pypa/sampleproject/blob/master/setup.py

import importlib
from pip.commands.install import InstallCommand as pip_install
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import sys
import os

MAJOR_VERSION = 0
MINOR_VERSION = 9
BUILD_NUMBER = os.environ.get('CIRCLE_BUILD_NUM', 'DEVSNAPSHOT')

# top-level of project directory
__HERE__ = path.abspath(path.dirname(__file__))

config = {
    "name": "kairos_staticmap",
    "version": "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, BUILD_NUMBER),
    "packages": find_packages(),
    "description": "Kairos fork of komoot/staticmap",
    "url": "Github Project URL (changeme)",

    # this should stay in sync with requirements.txt - we always want to
    # install via pip if we can
    "install_requires": [
        "requests",
        "Pillow"

    ],

    "setup_requires": [
        "nose>=1.3.7",
    ],
    "package_data": {
        # other data to bundle with the package
        # see https://setuptools.readthedocs.io/en/latest/pkg_resources.html#resourcemanager-api
        # "package": ["list", "of", "relative paths", "to package"]
    },
    "scripts": [
        # "binaries to link into path"i
    ],
    # metadata for upload to PyPI
    "author": "Matt Gordon",
    "author_email": "matt@kairosaerospace.com",  # (changeme)
    "license": "All rights reserved.",
}
####################################################################################################
# Git release tagging
####################################################################################################
# comment this out to disable git tagging of buildlib
# (needs buildlib loaded into the virtualenv)
print("Making sure buildlib is present and current.")
pip_install().main(["--upgrade", "kairos-buildlib"])

import buildlib.git as git

try:
    repo = git.ensure_git_repo(__HERE__)
    if len(repo.branches) > 0:
        pkg_name = config["name"]
        pkg_root = os.path.join(__HERE__, pkg_name)
        # publish packages for branches that start with 'x-'
        git.branchify_package(pkg_root, pkg_name, config, rename_prefix="x-")
    else:
        print("Skipping git release tagging since this project is not currently tracked by git.")
except git.NotAGitRepoError:
    print("Skipping git release tagging since this project is not currently tracked by git.")

####################################################################################################

# read the long description into the package
readme = path.join(__HERE__, "README.rst")
if path.exists(readme):
    with open(readme, encoding="utf-8") as f:
        config["long_description"] = f.read()

# make sure we don't accidentally publish to PyPI
# See:
# https://www.tomaz.me/2013/09/03/prevent-accidental-publishing-of-a-private-python-package.html
if "register" in sys.argv:
    print("register has been disabled to avoid accidental PyPI publishing of Kairos packages", file=sys.stderr)
    sys.exit(2)

# actually run setup down here
setup(**config)
