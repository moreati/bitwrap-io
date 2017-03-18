from setuptools import setup, find_packages

setup(
    name="bitwrap_io",
    version="0.1.8",
    author="Matthew York",
    author_email="myork@stackdump.com",
    description="A blockchain-style python eventstore w/ mysql or LMDB backend",
    license='MIT',
    keywords='PNML petri-net eventstore state-machine actor-model',
    packages=find_packages() + ['twisted.plugins'],
    include_package_data=True,
    install_requires=['cyclone==1.1', 'lmdb==0.92', 'service-identity==16.0.0', 'ujson==1.35', 'xxhash==0.6.1', 'PyMySQL==0.7.9'],
    long_description="""
# Bitwrap-pnml

A blockchain-style python eventstore using choice of mysql or LMDB backend

### Reference

Read Martin Fowler's description of [Event Sourcing](http://martinfowler.com/eaaDev/EventSourcing.html)

Watch an event sourcing video from [Greg Young](https://www.youtube.com/watch?v=8JKjvY4etTY)

Read an article about how event sourcing compliments blockchain [ 6 Components of any Blockchain design solution ] (http://blockchain.glorat.net/2015/11/16/6-components-of-any-blockchain-design-solution/)

""",
    url="http://getbitwrap.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: MIT License"
    ],
)
