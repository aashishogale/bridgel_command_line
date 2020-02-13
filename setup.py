from setuptools import setup

setup(
    name='bridgel',
    version='0.1',
    py_modules=['bridgel'],
    install_requires=[
        'Click',
        'PyGithub',
        'mysql',
        'GitPython'
    ],
    entry_points='''
        [console_scripts]
        bridgel=bridgel:add_to_git
    ''',
)