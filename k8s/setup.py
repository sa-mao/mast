from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from subprocess import check_output, CalledProcessError

from setuptools import setup, find_packages
from warnings import warn


def version():
    date_string = datetime.now().strftime("1.%Y%m%d.%H%M%S")
    try:
        git_sha = check_output(["git", "describe", "--always", "--dirty=dirty", "--match=NOTHING"]).strip().decode()
        return "{}+{}".format(date_string, git_sha)
    except CalledProcessError as e:
        warn("Error calling git: {}".format(e))
    return date_string


setup(
    name="k8s-client",
    url="https://github.schibsted.io/spt-infrastructure/schip-spinnaker-webhook",
    maintainer="Platform Delivery",
    maintainer_email="platform-delivery@schibsted.com",
    version=version(),
    packages=find_packages(),
    install_requires=["requests == 2.13.0"],
    extras_require={
        "dev": [
            'flake8==3.3.0', "flake8-comprehensions==1.3.0", "flake8-print==2.0.2", "pep8-naming==0.4.1", 'mock==2.0.0',
            'pytest-sugar==0.8.0', 'pytest==3.0.7', "pytest-cov==2.4.0", "pytest-html==1.14.2", 'yapf==0.16.1',
            "tox==2.7.0", "tox-travis==0.8"
        ]
    },
    setup_requires=['setuptools>=17.1', 'pytest-runner', 'wheel'],
    entry_points={},
)
