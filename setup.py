import os

from setuptools import setup, Extension
from distutils.command.build_py import build_py as du_build_py

# wow, this is a mixed bag ... I am pretty upset about all of this ...
from setuptools.command.build_py import build_py
from setuptools.command.build_ext import build_ext


class build_ext_nofail(build_ext):

    """Doesn't fail when build our optional extensions"""

    def run(self):
        try:
            build_ext.run(self)
        except Exception:
            print("Ignored failure when building extensions, pure python modules will be used instead")
        # END ignore errors


def get_data_files(self):
    """Can you feel the pain ? So, in python2.5 and python2.4 coming with maya, 
    the line dealing with the ``plen`` has a bug which causes it to truncate too much.
    It is fixed in the system interpreters as they receive patches, and shows how
    bad it is if something doesn't have proper unittests.
    The code here is a plain copy of the python2.6 version which works for all.

    Generate list of '(package,src_dir,build_dir,filenames)' tuples"""
    data = []
    if not self.packages:
        return data

    # this one is just for the setup tools ! They don't iniitlialize this variable
    # when they should, but do it on demand using this method.Its crazy
    if hasattr(self, 'analyze_manifest'):
        self.analyze_manifest()
    # END handle setuptools ...

    for package in self.packages:
        # Locate package source directory
        src_dir = self.get_package_dir(package)

        # Compute package build directory
        build_dir = os.path.join(*([self.build_lib] + package.split('.')))

        # Length of path to strip from found files
        plen = 0
        if src_dir:
            plen = len(src_dir) + 1

        # Strip directory from globbed filenames
        filenames = [
            file[plen:] for file in self.find_data_files(package, src_dir)
        ]
        data.append((package, src_dir, build_dir, filenames))
    return data

du_build_py.get_data_files = get_data_files
build_py._get_data_files = get_data_files
# END apply setuptools patch too

__author__ = "Sebastian Thiel"
__contact__ = "byronimo@gmail.com"
__homepage__ = "https://github.com/gitpython-developers/gitdb-speedups"
__version__ = '0.1.0'

pkg = 'gitdb_speedups'

setup(
    cmdclass={'build_ext': build_ext_nofail},
    name="gitdb-speedups",
    version=__version__,
    description="Git Object Database: C speedups",
    author=__author__,
    author_email=__contact__,
    url=__homepage__,
    packages=[pkg],
    package_dir = {pkg: pkg},
    ext_modules=[Extension(
      pkg + '._perf',
      [pkg + '/_fun.c', pkg + '/_delta_apply.c'],
      include_dirs=[pkg],
    )],
    license = "BSD License",
    zip_safe=False,
    install_requires=['smmap >= 0.8.5'],
    long_description = """gitdb-speedups are a pure-c git object database speedups""",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
