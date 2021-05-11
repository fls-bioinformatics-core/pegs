"""
Setup script to install PEGS (Peak-set Enrichment of Gene-Sets)
"""

from setuptools import setup
import codecs
import os.path

# Installation requirements
install_requires = ['numpy==1.16',
                    'scipy==1.1.0',
                    'matplotlib==2.2.3',
                    'pillow==8.1.1',
                    'seaborn==0.9.0',
                    'xlsxwriter >= 0.8.4',
                    'pathlib2',
                    'future',]

# Acquire package version for installation
# (see https://packaging.python.org/guides/single-sourcing-package-version/)
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

PEGS_VERSION = get_version("pegs/__init__.py")

setup(
    name = "pegs",
    version = PEGS_VERSION,
    description = "Peak-set Enrichment of Gene-Sets (PEGS)",
    long_description = "PEGS is a Python bioinformatics utility for " \
    "calculating enrichments of gene cluster enrichments from peak data " \
    "at different genomic distances",
    url = 'https://github.com/fls-bioinformatics-core/pegs',
    author = 'Mudassar Iqbal, Peter Briggs',
    maintainer = 'Peter Briggs',
    maintainer_email = 'peter.briggs@manchester.ac.uk',
    packages = ['pegs'],
    entry_points = { 'console_scripts': [
        'pegs = pegs.cli:pegs',
        'mk_pegs_intervals = pegs.cli:mk_pegs_intervals',]
    },
    license = 'BSD-3-Clause',
    keywords = ['PEGS',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires = install_requires,
    data_files = [ ('pegs-%s' % PEGS_VERSION,
                    ['data/refGene_hg38_120719_intervals.bed',
                     'data/refGene_mm10_120719_intervals.bed',]),],
    include_package_data=True,
    zip_safe = False
)
