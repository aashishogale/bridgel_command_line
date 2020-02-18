from setuptools import setup, find_packages

setup(
    name='bridgel',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['bridgel'],
    install_requires=[
        'Click',
        'PyGithub',
        'mysql',
        'GitPython',
        'mysqlclient',
        'pytest'
        
    ],
    entry_points='''
        [console_scripts]
        bridgel=bridgel.bridgel:add_to_git
    ''',
    python_requires='>=3.6'
)