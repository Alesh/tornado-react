from setuptools import setup

setup(
    name = "Tornado-React",
    version = '0.1',
    zip_safe = False,
    py_modules = ['reactmixin'],
    include_package_data = True,
    install_requires = ['Tornado', 'PyExecJS'],
)