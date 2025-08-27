"""
Test suite for input validation functionality
"""

import pytest
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.validators import Validators


class TestValidators:
    """Test suite for Validators class"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.validator = Validators()
    
    def test_validate_file_extension(self):
        """Test file extension validation"""
        valid_files = [
            "data.csv",
            "comments.xlsx",
            "feedback.xls",
            "DATA.CSV",
            "test.XlSx"
        ]
        
        invalid_files = [
            "data.txt",
            "comments.pdf",
            "feedback.doc",
            "data",
            "test.json"
        ]
        
        for file in valid_files:
            assert self.validator.validate_file_extension(file) == True
        
        for file in invalid_files:
            assert self.validator.validate_file_extension(file) == False
    
    def test_validate_dataframe(self):
        """Test DataFrame validation"""
        # Valid DataFrame
        valid_df = pd.DataFrame({
            'comments': ['test1', 'test2'],
            'rating': [5, 4]
        })
        assert self.validator.validate_dataframe(valid_df) == True
        
        # Empty DataFrame
        empty_df = pd.DataFrame()
        assert self.validator.validate_dataframe(empty_df) == False
        
        # None
        assert self.validator.validate_dataframe(None) == False
        
        # Not a DataFrame
        assert self.validator.validate_dataframe("not a dataframe") == False
    
    def test_validate_comment_text(self):
        """Test comment text validation"""
        valid_comments = [
            "This is a valid comment",
            "¡Excelente servicio!",
            "123 test comment",
            "Comment with special chars: @#$"
        ]
        
        invalid_comments = [
            "",
            None,
            "   ",
            "\n\t",
            123,  # Not a string
            []   # Not a string
        ]
        
        for comment in valid_comments:
            assert self.validator.validate_comment(comment) == True
        
        for comment in invalid_comments:
            assert self.validator.validate_comment(comment) == False
    
    def test_validate_language_code(self):
        """Test language code validation"""
        valid_codes = ['es', 'en', 'pt', 'fr', 'de']
        invalid_codes = ['esp', 'english', '123', '', None, 'xx']
        
        for code in valid_codes:
            assert self.validator.validate_language_code(code) == True
        
        for code in invalid_codes:
            assert self.validator.validate_language_code(code) == False
    
    def test_validate_sentiment_label(self):
        """Test sentiment label validation"""
        valid_labels = [
            'positive', 'negative', 'neutral',
            'positivo', 'negativo', 'neutral',
            'POSITIVE', 'Negative', 'NEUTRAL'
        ]
        
        invalid_labels = [
            'good', 'bad', 'unknown',
            '', None, 123,
            'pos', 'neg'
        ]
        
        for label in valid_labels:
            assert self.validator.validate_sentiment_label(label) == True
        
        for label in invalid_labels:
            assert self.validator.validate_sentiment_label(label) == False
    
    def test_validate_nps_score(self):
        """Test NPS score validation"""
        valid_scores = [0, 1, 5, 9, 10]
        invalid_scores = [-1, 11, 100, 1.5, '5', None]
        
        for score in valid_scores:
            assert self.validator.validate_nps_score(score) == True
        
        for score in invalid_scores:
            assert self.validator.validate_nps_score(score) == False
    
    def test_validate_email(self):
        """Test email validation"""
        valid_emails = [
            "user@example.com",
            "test.user@company.co",
            "name+tag@domain.org"
        ]
        
        invalid_emails = [
            "not-an-email",
            "@example.com",
            "user@",
            "user @example.com",
            "",
            None
        ]
        
        for email in valid_emails:
            assert self.validator.validate_email(email) == True
        
        for email in invalid_emails:
            assert self.validator.validate_email(email) == False
    
    def test_validate_date_format(self):
        """Test date format validation"""
        valid_dates = [
            "2024-01-15",
            "2024-12-31",
            "2023-06-01"
        ]
        
        invalid_dates = [
            "15-01-2024",
            "2024/01/15",
            "2024-13-01",
            "2024-01-32",
            "not-a-date",
            "",
            None
        ]
        
        for date in valid_dates:
            assert self.validator.validate_date_format(date) == True
        
        for date in invalid_dates:
            assert self.validator.validate_date_format(date) == False
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        test_cases = [
            ("<script>alert('xss')</script>", "alert('xss')"),
            ("Normal text", "Normal text"),
            ("Text with <b>HTML</b>", "Text with HTML"),
            ("Multiple  spaces", "Multiple spaces"),
            ("  Trim spaces  ", "Trim spaces")
        ]
        
        for input_text, expected in test_cases:
            sanitized = self.validator.sanitize_input(input_text)
            assert expected in sanitized or sanitized == expected
    
    def test_validate_file_size(self):
        """Test file size validation"""
        # Valid sizes (in bytes)
        valid_sizes = [
            1024,  # 1 KB
            1048576,  # 1 MB
            10485760,  # 10 MB
        ]
        
        # Invalid sizes
        invalid_sizes = [
            0,
            -1,
            104857600,  # 100 MB (too large)
            None
        ]
        
        for size in valid_sizes:
            assert self.validator.validate_file_size(size, max_size_mb=50) == True
        
        for size in invalid_sizes:
            assert self.validator.validate_file_size(size, max_size_mb=50) == False
    
    def test_validate_column_names(self):
        """Test column name validation"""
        valid_columns = ['comment', 'rating', 'date', 'user_id']
        invalid_columns = ['', None, 'column with spaces', 'column-with-dashes']
        
        df_valid = pd.DataFrame(columns=valid_columns)
        df_invalid = pd.DataFrame(columns=['valid', ''])
        
        assert self.validator.validate_column_names(df_valid) == True
        assert self.validator.validate_column_names(df_invalid) == False
    
    def test_validate_percentage(self):
        """Test percentage validation"""
        valid_percentages = [0, 50, 100, 0.5, 99.99]
        invalid_percentages = [-1, 101, 1000, None, "50%"]
        
        for pct in valid_percentages:
            assert self.validator.validate_percentage(pct) == True
        
        for pct in invalid_percentages:
            assert self.validator.validate_percentage(pct) == False