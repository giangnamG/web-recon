"""
    This module initializes the Exposor package.

    Exposor is a Python-based tool for unified exploration across
    multiple search engines, enabling security researchers
    to identify potential risks efficiently.
"""

__title__ = "Exposor"
__url__ = "https://github.com/abuyv/exposor"
__version__ = "1.0.0"
__author__ = "Abdulla Abdullayev (Abu)"
__license__ = "MIT"
__status__ = "Production"


from .exposor import main

__all__ = ["main"]
