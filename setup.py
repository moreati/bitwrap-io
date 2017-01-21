from setuptools import setup, find_packages

setup(
    name="bitwrap_pnml",
    version="0.1.6",
    author="Matthew York",
    author_email="myork@stackdump.com",
    description="A blockchain style eventsourcing service using cyclone.io and lmdb",
    license='MIT',
    keywords='PNML petri-net eventsourcing actor-model',
    packages=find_packages() + ['twisted.plugins'],
    include_package_data=True,
    install_requires=['cyclone==1.1', 'lmdb==0.92', 'service-identity==16.0.0', 'txRDQ==0.2.14', 'ujson==1.35', 'xxhash==0.6.1', 'PyYAML==3.12'],
    long_description="A blockchain style eventsourcing service using cyclone.io and lmdb",
    url="http://getbitwrap.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: MIT License"
    ],
)
