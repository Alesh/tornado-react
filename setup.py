from setuptools import setup, find_packages

setup(
    name = "Tornado-React",
    version = '0.1',
    zip_safe = False,
    packages = find_packages(),
    include_package_data = True,
    install_requires = ['Tornado', 'PyExecJS'],
)