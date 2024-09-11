import setuptools

setuptools.setup(
    name="CPyS",
    version="0.0.4",
    author="Stella Bourdin",
    author_email="stella.bourdin@lsce.ipsl.fr",
    description="A python package from compute the Hart Cyclone Phase Space parameters",
    long_description="A python package from compute the Hart Cyclone Phase Space parameters",
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["numpy", "pandas", "xarray","pyproj","matplotlib"],
    #include_package_data=True,
    #package_data={"":['_data/*.csv', "_data/iho.*"]}
)


# Black formatting:
# `python -m black <directory or file(s)>`

# To generate the distribution:
# 1 / Check that wheel is up to date with `pip install --user --upgrade setuptools wheel`
# 2 / Run `python setup.py sdist bdist_wheel`

# To upload to PyPI:
# 1 / Check that twine is up-to-date `pip install --user --upgrade twine`
# 2 / Upload with `python -m twine upload --repository pypi dist/*`
