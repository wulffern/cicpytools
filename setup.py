######################################################################
##        Copyright (c) 2020 Carsten Wulff Software, Norway 
## ###################################################################
## Created       : wulff at 2020-1-25
## ###################################################################
##  The MIT License (MIT)
## 
##  Permission is hereby granted, free of charge, to any person obtaining a copy
##  of this software and associated documentation files (the "Software"), to deal
##  in the Software without restriction, including without limitation the rights
##  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##  copies of the Software, and to permit persons to whom the Software is
##  furnished to do so, subject to the following conditions:
## 
##  The above copyright notice and this permission notice shall be included in all
##  copies or substantial portions of the Software.
## 
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##  SOFTWARE.
##  
######################################################################
#Shout out to https://github.com/bast/somepackage/. Thanks!


from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.rst')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'cicpytools', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='cicpytools',
    version=version['__version__'],
    description=('Scripts to easy use of ciccreator'),
    long_description=long_description,
    author='Carsten Wulff',
    author_email='carsten@wulff.no',
    url='https://github.com/wulffern/cicpytools',
    license='MPL-2.0',
    packages=['cicpytools'],
#   no dependencies in this example
   install_requires=[
       'click>7.0',
       're>2.2.1',
   ],
#   no scripts in this example
   scripts=['bin/cicpytool.py'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 0 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6'],
    )
