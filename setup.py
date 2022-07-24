from distutils.core import setup

# This will pull the first # header in the README
# and use it as the PyPI official description
with open("README.md") as fh:
    long_description = ""
    header_count = 0
    for line in fh:
        if line.startswith("#"):
            header_count += 1
        if header_count < 2:
            long_description += line
        else:
            break


setup(
  name = 'midbench',
  packages = ['midbench'],
  version = '0.1',
  license='MIT',
  description = "The Maryland Inverse Design (MID) Benchmark Suite",
  long_description = long_description,
  long_description_content_type="text/markdown",
  author = 'The Information for Design, Engineering, And Learning Laboratory',
  author_email = 'fuge@umd.edu',
  url = 'https://github.com/IDEALLab/midbench',
  download_url = 'https://github.com/IDEALLab/midbench/archive/v0.1.tar.gz',
  install_requires=[
          'numpy',
          'torch',
          'dataclasses',
          'typing_extensions',
          'importlib-metadata',
          'pandas'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research'
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
  ],
)
