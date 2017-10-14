from setuptools import setup, find_packages

setup(
    name='Your Application',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click==6.7',
        'Flask==0.12.2',
        'itsdangerous==0.24',
        'Jinja2==2.9.6',
        'MarkupSafe==1.0',
        'tinydb==3.5.0',
        'Werkzeug==0.12.2'
    ]
)