"""
CKAN plugin to register Stad Gent custom validators
"""
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.stadgent_validators.validators import project_code_validator


class StadGentValidatorsPlugin(plugins.SingletonPlugin):
    """
    Plugin to register custom validators for Stad Gent
    """
    plugins.implements(plugins.IValidators)

    def get_validators(self):
        """
        Register custom validators
        """
        return {
            'project_code_validator': project_code_validator,
        }
