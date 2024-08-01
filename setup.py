from setuptools import setup, find_packages

setup(
    name='soundcld',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/faridrasidov/soundcld',
    license='BSL-1.0 license',
    author='Farid',
    author_email='ftm5pv70@duck.com',
    description='Soundcloud Api Lib For Python',
    install_requires=[
        'requests',
        'dacite',
        'python-dateutil'
    ],
    extras_require={
        'dev': [
            'pytest'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
