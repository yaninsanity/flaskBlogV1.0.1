from setuptools import find_packages, setup

#该setup.py文件描述了您的项目以及属于它的文件。
setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)