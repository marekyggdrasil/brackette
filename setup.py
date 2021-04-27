import setuptools

setuptools.setup(
    name='truthsayer',
    version='0.0.1',
    packages=['truthsayer',],
    license='MIT',
    description = 'Package that manages state of Dune the Boardgame',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author = 'Marek Narozniak',
    author_email = '',
    install_requires=['diff-match-patch'],
    url = 'https://github.com/marekyggdrasil/truthsayer',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
