from setuptools import setup, find_packages

setup(
    name='tartiflette-django',
    version='0.1.0',
    url='https://github.com/mixkorshun/tartiflette-django',
    description='',
    keywords="api graphql protocol api rest relay tartiflette",

    author='Vladislav Bakin',
    license='MIT',

    install_requires=[
        'tartiflette'
    ],

    packages=find_packages(),

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Framework :: Django',
        'Framework :: Django :: 3',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
