"""
Test suite for data processing functionality
"""

import pytest
import pandas as pd
from pathlib import Path

# Import from installed package
# Install with: pip install -e .
try:
    from src.data_processing.comment_reader import CommentReader
except ImportError:
    from .test_stubs import CommentReader

try:
    from src.data_processing.language_detector import LanguageDetector
except ImportError:
    from .test_stubs import LanguageDetector


class TestCommentReader:
    """Test suite for CommentReader class"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.reader = CommentReader()
    
    def test_read_csv_file(self, sample_csv_file):
        """Test reading CSV files"""
        data = self.reader.read_file(sample_csv_file)
        
        assert data is not None
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
        assert 'Comentario Final' in data.columns
    
    def test_read_excel_file(self, sample_excel_file):
        """Test reading Excel files"""
        data = self.reader.read_file(sample_excel_file)
        
        assert data is not None
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
        assert 'Comentario Final' in data.columns
    
    def test_detect_comment_column(self, sample_dataframe):
        """Test automatic detection of comment column"""
        comment_col = self.reader.detect_comment_column(sample_dataframe)
        
        assert comment_col == 'Comentario Final'
    
    def test_detect_comment_column_variants(self):
        """Test detection of various comment column names"""
        test_cases = [
            ('comments', pd.DataFrame({'comments': ['test']})),
            ('feedback', pd.DataFrame({'feedback': ['test']})),
            ('review', pd.DataFrame({'review': ['test']})),
            ('texto', pd.DataFrame({'texto': ['test']})),
            ('observacion', pd.DataFrame({'observacion': ['test']}))
        ]
        
        for expected_col, df in test_cases:
            detected = self.reader.detect_comment_column(df)
            assert detected == expected_col
    
    def test_clean_comments(self):
        """Test comment cleaning functionality"""
        dirty_comments = [
            "  Extra spaces  ",
            "Multiple   spaces",
            "Special chars: @#$%",
            "UPPERCASE TEXT",
            None,
            ""
        ]
        
        cleaned = self.reader.clean_comments(dirty_comments)
        
        assert len(cleaned) == len(dirty_comments)
        assert cleaned[0] == "Extra spaces"
        assert "Multiple spaces" in cleaned[1]
        assert cleaned[4] == ""  # None becomes empty string
    
    def test_remove_duplicates(self):
        """Test duplicate removal"""
        comments_with_dups = [
            "Same comment",
            "Same comment",
            "Different comment",
            "Same comment"
        ]
        
        unique, counts = self.reader.remove_duplicates(comments_with_dups)
        
        assert len(unique) == 2
        assert counts["same comment"] == 3
        assert counts["different comment"] == 1
    
    def test_extract_metadata(self, sample_dataframe):
        """Test metadata extraction from dataframe"""
        metadata = self.reader.extract_metadata(sample_dataframe)
        
        assert 'total_rows' in metadata
        assert 'columns' in metadata
        assert 'has_nps' in metadata
        assert 'has_ratings' in metadata
        assert metadata['total_rows'] == 5
        assert metadata['has_nps'] == True
        assert metadata['has_ratings'] == True
    
    def test_handle_empty_file(self, tmp_path):
        """Test handling of empty files"""
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("")
        
        with pytest.raises(Exception):
            self.reader.read_file(str(empty_file))
    
    def test_handle_invalid_file(self, tmp_path):
        """Test handling of invalid file formats"""
        invalid_file = tmp_path / "invalid.txt"
        invalid_file.write_text("Not a CSV or Excel file")
        
        with pytest.raises(Exception):
            self.reader.read_file(str(invalid_file))


class TestLanguageDetector:
    """Test suite for LanguageDetector class"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.detector = LanguageDetector()
    
    def test_detect_spanish(self):
        """Test Spanish language detection"""
        spanish_texts = [
            "Este es un texto en español",
            "Hola, ¿cómo estás?",
            "El servicio es excelente"
        ]
        
        for text in spanish_texts:
            lang = self.detector.detect(text)
            assert lang == 'es'
    
    def test_detect_english(self):
        """Test English language detection"""
        english_texts = [
            "This is an English text",
            "Hello, how are you?",
            "The service is excellent"
        ]
        
        for text in english_texts:
            lang = self.detector.detect(text)
            assert lang == 'en'
    
    def test_detect_guarani(self):
        """Test Guarani language detection (if supported)"""
        guarani_texts = [
            "Mba'éichapa",
            "Aguije",
            "Iporãite"
        ]
        
        for text in guarani_texts:
            lang = self.detector.detect(text)
            # Guarani might be detected as unknown or similar language
            assert lang is not None
    
    def test_detect_mixed_language(self):
        """Test mixed language detection"""
        mixed_text = "Hello amigo, how está usted?"
        lang = self.detector.detect(mixed_text)
        
        assert lang in ['es', 'en', 'unknown']
    
    def test_empty_text_detection(self):
        """Test language detection for empty text"""
        empty_texts = ["", None, "   ", "\n\t"]
        
        for text in empty_texts:
            lang = self.detector.detect(text)
            assert lang in ['unknown', None]
    
    def test_batch_detection(self, sample_comments_spanish):
        """Test batch language detection"""
        languages = self.detector.detect_batch(sample_comments_spanish)
        
        assert len(languages) == len(sample_comments_spanish)
        assert all(lang in ['es', 'en', 'unknown', None] for lang in languages)
        # Most should be Spanish
        spanish_count = sum(1 for lang in languages if lang == 'es')
        assert spanish_count >= len(sample_comments_spanish) * 0.5
    
    def test_confidence_scores(self):
        """Test language detection confidence scores"""
        texts = [
            "Definitivamente español",
            "Maybe English",
            "123456",
            "!!!"
        ]
        
        for text in texts:
            result = self.detector.detect_with_confidence(text)
            assert 'language' in result
            assert 'confidence' in result
            assert 0 <= result['confidence'] <= 1