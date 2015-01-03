from distutils.core import setup
from distutils.command.install import install as DistutilsInstall
from distutils.command.clean import clean as Clean
import shutil
import os
from os.path import join


class MakeCommand(DistutilsInstall):
    def run(self):
        os.system('make')
        common_dir = 'tgrocery/libshorttext/converter/stemmer'
        target_dir = '%s/%s' % (self.build_lib, common_dir)
        self.mkpath(target_dir)
        os.system('cp %s/porter.so.1 %s' % (common_dir, target_dir))
        common_dir = 'tgrocery/libshorttext/classifier/learner'
        target_dir = '%s/%s' % (self.build_lib, common_dir)
        self.mkpath(target_dir)
        os.system('cp %s/util.so.1 %s' % (common_dir, target_dir))
        common_dir = 'tgrocery/libshorttext/classifier/learner/liblinear'
        target_dir = '%s/%s' % (self.build_lib, common_dir)
        self.mkpath(target_dir)
        os.system('cp %s/liblinear.so.1 %s' % (common_dir, target_dir))
        DistutilsInstall.run(self)


class CleanCommand(Clean):
    description = "Remove build artifacts from the source tree"

    def run(self):
        Clean.run(self)
        if os.path.exists('build'):
            shutil.rmtree('build')
        for dirpath, dirnames, filenames in os.walk('tgrocery'):
            for filename in filenames:
                if (filename.endswith('.o') or filename.endswith('.a') or filename.endswith(
                        '.so.1') or filename.endswith(
                        '.pyd') or filename.endswith(
                        '.dll') or filename.endswith('.pyc')):
                    os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))


setup(
    name='tgrocery',
    version='1.0',
    packages=['', 'tgrocery', 'tgrocery.libshorttext.analyzer', 'tgrocery.libshorttext.converter',
              'tgrocery.libshorttext.converter.stemmer',
              'tgrocery.libshorttext.classifier', 'tgrocery.libshorttext.classifier.learner',
              'tgrocery.libshorttext.classifier.learner.liblinear',
              'tgrocery.libshorttext.classifier.learner.liblinear.python'],
    package_data={'tgrocery': [join('libshorttext', 'converter', 'stop-words', '*')]},
    url='https://github.com/2shou/TextGrocery',
    license='',
    author='2shou',
    author_email='gavin.zgz@gmail.com',
    description='A simple short-text classification tool based on LibShortText',
    cmdclass={
        'install': MakeCommand,
        'clean': CleanCommand,
    },
)
