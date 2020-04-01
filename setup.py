from setuptools import find_packages, setup

from peto import __version__

install_requires = [
    "eventsourcing<=8.2.9999",
]

long_description = """
Event sourced system to support mass periodic testing for infectious disease

`Please raise issues on GitHub <https://github.com/johnbywater/peto/issues>`_.
"""

packages = find_packages(exclude=["docs"])

setup(
    name="peto",
    version=__version__,
    description="System for mass periodic infectious disease testing",
    author="John Bywater",
    author_email="john.bywater@appropriatesoftware.net",
    url="https://github.com/johnbywater/peto",
    license="GNU General Public License v3 (GPLv3)",
    packages=packages,
    install_requires=install_requires,
    zip_safe=False,
    long_description=long_description,
    keywords=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
)
