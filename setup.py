
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')


setup(
    long_description=readme,
    name='datar',
    version='0.2.0',
    description='Port of dplyr and other related R packages in python, using pipda.',
    python_requires='==3.*,>=3.7.1',
    project_urls={"homepage": "https://github.com/pwwang/datar",
                  "repository": "https://github.com/pwwang/datar"},
    author='pwwang',
    author_email='pwwang@pwwang.com',
    license='MIT',
    packages=['datar', 'datar.base', 'datar.core', 'datar.datar', 'datar.datasets',
              'datar.dplyr', 'datar.stats', 'datar.tibble', 'datar.tidyr', 'datar.utils'],
    package_dir={"": "."},
    package_data={"datar.datasets": ["*.gz"]},
    install_requires=['diot', 'executing', 'pandas==1.*,>=1.2.0',
                      'pipda', 'scipy==1.*,>=1.6.0', 'wcwidth==0.*,>=0.2.0'],
    extras_require={"dev": ["pytest", "pytest-cov"]},
)
