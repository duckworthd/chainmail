from setuptools import setup, find_packages

setup(
    name = 'chainmail',
    version = '0.1.1',
    author = 'Daniel Duckworth',
    author_email = 'duckworthd@gmail.com',
    description = 'Sending email is hard. Let\'s go shopping!',
    license = 'BSD',
    keywords = 'smtp email',
    url = 'http://github.com/duckworthd/chainmail',
    packages = find_packages(),
    classifiers = [
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
    ],
    install_requires = [      # dependencies
    ],
    tests_require = [         # test dependencies
    ]
)

