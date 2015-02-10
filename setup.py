# coding: utf-8

import os

from setuptools.command.install import install as Install
from setuptools import setup, Extension


with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()


class MakeCommand(Install):
    def run(self):
        os.system('make.bat')
        source_dir = os.path.join('tgrocery', 'learner')
        target_dir = os.path.join(self.build_lib, 'tgrocery', 'learner')
        os.system('mkdir %s\liblinear' % target_dir)
        os.system('copy %s\util.dll %s' % (source_dir, target_dir))
        os.system('copy %s\liblinear\liblinear.dll %s\liblinear' % (source_dir, target_dir))
        Install.run(self)


util = Extension(
    'tgrocery.learner.util',
    [os.path.join('tgrocery', 'learner', 'util.c')],
    include_dirs=[os.path.join('tgrocery', 'learner', 'liblinear')]
)

setup(
    name='tgrocery',
    version='0.1.3',
    packages=['tgrocery', 'tgrocery.learner', 'tgrocery.learner.liblinear.python'],
    url='https://github.com/2shou/TextGrocery',
    license='BSD',
    author='2shou',
    author_email='gavin.zgz@gmail.com',
    description='A simple short-text classification tool based on LibLinear',
    long_description=LONG_DESCRIPTION,
    install_requires=['jieba'],
    keywords='text classification svm liblinear libshorttext',
    cmdclass={'install': MakeCommand},
    # ext_modules=[util]
)
