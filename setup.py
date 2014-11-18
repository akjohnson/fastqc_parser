from distutils.core import setup

VERSION = "0.1"

DESCRIPTION = """\
FASTQCParser is a tool for automating the processing of basic FastQC results in Python.
Given the contents of fastqc_data.txt, it will parse the results into an object that can
then be used in code.
"""

setup(
    name="fastqc_parser", 
    version=VERSION, 
    description="Parses FastQC result files into Python",
    long_description=DESCRIPTION,
    author="Audra Johnson",
    author_email="audrakjohnson@gmail.com",
    url="https://github.com/akjohnson/fastqc_parser",
    packages=["fastqc_parser"],
    license="Python",
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        ],
    )
