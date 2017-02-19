from setuptools import setup, find_packages

setup(
    name="bitwrap_pnml",
    version="0.3.0",
    author="Matthew York",
    author_email="myork@stackdump.com",
    description="A blockchain style embedded eventstore using twisted, cyclone.io and lmdb",
    license='MIT',
    keywords='PNML petri-net eventsourcing actor-model',
    packages=find_packages() + ['twisted.plugins'],
    include_package_data=True,
    install_requires=['cyclone==1.1', 'lmdb==0.92', 'service-identity==16.0.0', 'txRDQ==0.2.14', 'ujson==1.35', 'xxhash==0.6.1', 'PyYAML==3.12'],
    long_description="""
# Bitwrap-pnml

A blockchain style eventsourcing service using cyclone.io and lmdb - Symas Lightning Memory-mapped Database

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
