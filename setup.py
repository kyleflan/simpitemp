from setuptools import setup

REQUIREMENTS = [i.strip() for i in open('requirements.txt').readlines()]

setup(
    name='simpitemp',
    version='0.1.0',
#    packages=['TimeLimitedRedisDict'],
    url='https://github.com/kyleflan/simpitemp',
    license='Apache License, Version 2.0',
    author='kyleflan',
    author_email='kyleflanagan@gmail.com',
    description='A Raspberry Pi-based temperature and humidity sensor and web app',
    install_requires=REQUIREMENTS,
    include_package_data=True
)
