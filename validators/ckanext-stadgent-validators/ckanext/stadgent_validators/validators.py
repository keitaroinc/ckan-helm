"""
Custom validators for Stad Gent CKAN instance
"""
import re
from ckan.plugins.toolkit import Invalid


def project_code_validator(value):
    """
    Validate project code format: STAD-YYYY-NNN

    Examples:
        STAD-2024-001
        STAD-2025-999

    Raises:
        Invalid: If the format doesn't match
    """
    if not value:
        return value

    # Pattern: STAD-YYYY-NNN (year must be 4 digits, number must be 3 digits)
    pattern = r'^STAD-\d{4}-\d{3}$'

    if not re.match(pattern, value):
        raise Invalid(
            'Projectcode moet het formaat STAD-YYYY-NNN hebben (bijv. STAD-2024-001)'
        )

    return value
