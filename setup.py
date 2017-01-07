from distutils.core import setup

setup(
    name="bitwrap_pnml",
    packages=['bitwrap_pnml'],
    install_requires=['cyclone==1.1', 'lmdb==0.92', 'service-identity==16.0.0', 'txRDQ==0.2.14', 'ujson==1.35', 'xxhash==0.6.1', 'PyYAML==3.12'],
    version="0.1.0",
    url="http://getbitwrap.com",
    author="Matthew York",
    author_email="myork@stackdump.com"
)
