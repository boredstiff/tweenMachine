from setuptools import find_packages, setup

setup(
    name='tweenMachine',
    author='Alex Widener',
    author_email='github@firstnamelastname.com',
    url='https://github.com/alexwidener/tweenMachine',
    package_dir={'': '.'},
    packages=find_packages('.'),
    description='Tween Animation',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'])
