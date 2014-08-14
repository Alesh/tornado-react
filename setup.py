from setuptools import setup

setup(
    name = "Tornado-React",
    license = "MIT License",
    version = '0.1',
    zip_safe = False,
    py_modules = ['reactmixin'],
    include_package_data = True,
    install_requires = ['Tornado', 'PyExecJS'],
    author = 'Alexey Poryadin',
    author_email = 'alexey.poryadin@gmail.com',
    url='https://github.com/Alesh/tornado-react',
    description = 'Mixins for using React.js features within tornado.web.Application.',    
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: JavaScript',        
    ]    
)