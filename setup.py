import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='aussiebb',
    version='0.3',
    author='Michael Still',
    author_email='mikal@stillhq.com',
    description='A python library to interact with the Aussie Broadband customer portal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.madebymikal.com/aussiebb',
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
