# coding: utf-8

import os

from setuptools.command.install import install

from setuptools import setup


with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()


class MakeCommand(install):
    def run(self):
        os.system('make')
        common_dir = 'tgrocery/learner'
        target_dir = '%s/%s' % (self.build_lib, common_dir)
        self.mkpath(target_dir)
        os.system('cp %s/util.so.1 %s' % (common_dir, target_dir))
        common_dir = 'tgrocery/learner/liblinear'
        target_dir = '%s/%s' % (self.build_lib, common_dir)
        self.mkpath(target_dir)
        os.system('cp %s/liblinear.so.1 %s' % (common_dir, target_dir))
        install.run(self)


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
    cmdclass={'install': MakeCommand}
)
