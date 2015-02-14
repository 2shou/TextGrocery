from os.path import join

import numpy


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('svm', parent_package, top_path)

    liblinear_sources = ['liblinear.c',
                         join('src', 'liblinear', '*.cpp')]

    liblinear_depends = [join('src', 'liblinear', '*.h'),
                         join('src', 'liblinear', 'liblinear_helper.c')]

    config.add_extension('liblinear',
                         sources=liblinear_sources,
                         libraries=['cblas'],
                         include_dirs=[join('src', 'cblas'),
                                       numpy.get_include()],
                         extra_compile_args=[],
                         depends=liblinear_depends)

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup

    setup(**configuration(top_path='').todict())
