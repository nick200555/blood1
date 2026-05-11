from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name='bloodbank',
    version='1.0.0',
    description='Comprehensive Blood Bank Management System for ERPNext',
    author='BloodBank Team',
    author_email='admin@bloodbank.org',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
