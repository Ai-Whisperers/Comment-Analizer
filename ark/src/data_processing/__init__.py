"""
Data Processing Module for Personal Paraguay Fiber Comments Analysis
"""

from .comment_reader import CommentReader
from .language_detector import LanguageDetector, get_comment_language

__all__ = ['CommentReader', 'LanguageDetector', 'get_comment_language']