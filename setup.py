from setuptools import setup, find_packages

version = '0.2.0'

setup(
    name='fabricant',
    version=version,
    description="A set of helpers, based on Fabric and Cuisine.",
    long_description="""\
    """,
    classifiers=[],
    keywords='fabric deployment',
    author='Alexander Artemenko',
    author_email='svetlyak.40wt@gmail.com',
    url='http://github.com/svetlyak40wt/fabricant',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Fabric',
        'cuisine',
    ],
)
