# coding: utf-8


with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration(None, parent_package, top_path)
    config.add_subpackage('tgrocery')
    return config


from numpy.distutils.core import setup

metadata = dict(
    name='tgrocery',
    version='0.2.0',
    url='https://github.com/2shou/TextGrocery',
    license='BSD',
    author='2shou',
    author_email='gavin.zgz@gmail.com',
    description='A simple short-text classification tool based on LibLinear',
    long_description=LONG_DESCRIPTION,
    install_requires=['numpy', 'jieba'],
    keywords='text classification svm liblinear libshorttext',
)

metadata['configuration'] = configuration

setup(**metadata)
