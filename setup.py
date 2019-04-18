import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visearch",
    version="0.0.1",
    author="Hanh.Le Van",
    author_email="lvhanh.270597@gmail.com",
    description="Helpful tool to search vietnamese documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lvhanh270597/visearch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
