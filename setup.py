from setuptools import setup
from setuptools import find_packages

long_description= """
# millefeuille-api
A package to make generating content for Millefeuille easier.
"""

required = [
    "iiif-prezi3",
    "Pillow",
    "opencv-python",
    "pydub"
]

setup(
    name="mfapi",
    version="0.0.1",
    description="Generate content for Millefeuille",
    long_description=long_description,
    author="Jacob Hart",
    author_email="jacob.dchart@gmail.com",
    url="https://github.com/jdchart/millefeuille-api",
    install_requires=required,
    # classifiers=[
    #     "Development Status :: 5 - Production/Stable",
    #     "Intended Audience :: Developers",
    #     "Intended Audience :: Education",
    #     "Intended Audience :: Science/Research",
    #     "License :: OSI Approved :: MIT License",
    #     "Programming Language :: Python :: 3.10",
    #     "Topic :: Multimedia :: Video",
    #     "Topic :: Software Development :: Libraries :: Python Modules",
    # ],
    packages=find_packages()
)