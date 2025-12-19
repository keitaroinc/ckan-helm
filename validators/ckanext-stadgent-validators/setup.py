from setuptools import setup, find_packages

setup(
    name='ckanext-stadgent-validators',
    version='0.1.0',
    description='Custom validators for Stad Gent CKAN',
    author='Stad Gent',
    packages=find_packages(),
    namespace_packages=['ckanext'],
    entry_points={
        'ckan.plugins': [
            'stadgent_validators = ckanext.stadgent_validators.plugin:StadGentValidatorsPlugin',
        ],
    },
)
