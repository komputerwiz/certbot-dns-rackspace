from setuptools import setup, find_packages

version = '0.0.1.dev2'

# read contents of README.md
from os import path
current_dir = path.abspath(path.dirname(__file__))
with open(path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Remember to update local-oldest-requirements.txt when changing the minimum acme/certbot version.
install_requires = [
    'acme>=0.37.1',
    'certbot>=0.37.1',
    'mock',
    'requests>=2.22.0',
    'setuptools',
    'zope.interface',
]

setup(
    name='certbot-dns-rackspace',
    version=version,
    description="Rackspace Cloud DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/komputerwiz/certbot-dns-rackspace',
    author='Matthew Barry',
    author_email='matthew@komputerwiz.net',
    license='Apache License 2.0',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-rackspace = certbot_dns_rackspace:Authenticator',
        ],
    },
)
