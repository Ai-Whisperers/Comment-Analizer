"""
File Upload Service for Personal Paraguay Comments Analysis Platform
Handles file upload, validation, and processing logic
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Optional
import streamlit as st

from src.data_processing.comment_reader import CommentReader
from src.utils.validators import InputValidator
from src.utils.exceptions import FileProcessingError, DataValidationError


class FileUploadService:
    """Service for handling file upload operations"""

    def __init__(self):
        self.supported_extensions = [".xlsx", ".xls", ".csv", ".json", ".txt"]
        self.max_file_size_mb = 50
        self.max_rows = 20000

    def validate_file_basic(self, uploaded_file) -> Tuple[bool, str, Dict]:
        """
        Perform basic file validation and return metadata

        Returns:
            Tuple of (is_valid, error_message, file_metadata)
        """
        if not uploaded_file:
            return False, "No file uploaded", {}

        file_size_mb = uploaded_file.size / (1024 * 1024)
        file_extension = Path(uploaded_file.name).suffix.lower()

        metadata = {
            "size_mb": file_size_mb,
            "extension": file_extension,
            "name": uploaded_file.name,
            "size_bytes": uploaded_file.size,
        }

        # Size validation
        if file_size_mb > self.max_file_size_mb:
            return (
                False,
                f"File too large: {file_size_mb:.1f}MB (Max: {self.max_file_size_mb}MB)",
                metadata,
            )

        # Format validation
        if file_extension not in self.supported_extensions:
            return False, f"Unsupported format: {file_extension}", metadata

        return True, "", metadata

    def get_validation_display_data(self, metadata: Dict) -> Dict:
        """Get data for displaying validation status"""
        file_size_mb = metadata["size_mb"]
        file_extension = metadata["extension"]

        return {
            "size_status": (
                "success" if file_size_mb <= self.max_file_size_mb else "error"
            ),
            "size_message": f"Size: {file_size_mb:.1f}MB"
            + (
                ""
                if file_size_mb <= self.max_file_size_mb
                else f" (Max: {self.max_file_size_mb}MB)"
            ),
            "format_status": (
                "success" if file_extension in self.supported_extensions else "error"
            ),
            "format_message": f"Format: {file_extension}"
            + ("" if file_extension in self.supported_extensions else " (Unsupported)"),
            "rows_estimate": self._estimate_rows(metadata),
            "rows_status": "info",
        }

    def _estimate_rows(self, metadata: Dict) -> str:
        """Estimate number of rows based on file metadata"""
        file_extension = metadata["extension"]
        file_size_mb = metadata["size_mb"]

        if file_extension == ".csv":
            estimated_rows = min(file_size_mb * 1000, self.max_rows)
            if estimated_rows <= self.max_rows:
                return f"Est. ~{estimated_rows:.0f} rows"
            else:
                return f"Est. ~{estimated_rows:.0f} rows (May exceed limit)"
        elif file_extension in [".xlsx", ".xls"]:
            return "Excel detected - will check rows after processing"
        else:
            return "File ready for processing"

    def process_uploaded_file(
        self, uploaded_file, temp_dir: str = "data/raw"
    ) -> Tuple[bool, str, Optional[pd.DataFrame], Dict]:
        """
        Process uploaded file and return DataFrame with metadata

        Returns:
            Tuple of (success, message, dataframe, processing_info)
        """
        try:
            # Validate file first
            is_valid, validation_message = InputValidator.validate_file_upload(
                uploaded_file
            )
            if not is_valid:
                return False, f"File validation failed: {validation_message}", None, {}

            # Sanitize filename and save temporarily
            safe_filename = InputValidator.sanitize_export_filename(uploaded_file.name)
            temp_path = Path(temp_dir) / safe_filename
            temp_path.parent.mkdir(parents=True, exist_ok=True)

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Process based on file type
            file_extension = Path(uploaded_file.name).suffix.lower()
            processing_info = {
                "temp_path": str(temp_path),
                "file_extension": file_extension,
                "is_excel": file_extension in [".xlsx", ".xls"],
                "sheets": [],
            }

            if processing_info["is_excel"]:
                return self._process_excel_file(temp_path, processing_info)
            else:
                return self._process_regular_file(temp_path, processing_info)

        except Exception as e:
            return False, f"Error processing file: {str(e)}", None, {}

    def _process_excel_file(
        self, temp_path: Path, processing_info: Dict
    ) -> Tuple[bool, str, Optional[pd.DataFrame], Dict]:
        """Process Excel file with sheet detection"""
        try:
            excel_file = pd.ExcelFile(temp_path)
            sheet_names = excel_file.sheet_names
            processing_info["sheets"] = sheet_names
            processing_info["is_multi_sheet"] = len(sheet_names) > 1

            reader = CommentReader()

            if len(sheet_names) > 1:
                # Multi-sheet Excel - let user choose in UI
                processing_info["requires_sheet_selection"] = True
                # Return first sheet as default, UI will handle selection
                comments_df = reader.read_excel_sheet(temp_path, sheet_names[0])
                processing_info["current_sheet"] = sheet_names[0]
            else:
                # Single sheet Excel
                processing_info["requires_sheet_selection"] = False
                comments_df = reader.read_file(temp_path)
                processing_info["current_sheet"] = sheet_names[0]

            # Validate DataFrame content
            is_valid_df, df_validation_message = (
                InputValidator.validate_dataframe_content(comments_df)
            )
            if not is_valid_df:
                return (
                    False,
                    f"Data validation failed: {df_validation_message}",
                    None,
                    processing_info,
                )

            return (
                True,
                "Excel file processed successfully",
                comments_df,
                processing_info,
            )

        except Exception as e:
            return (
                False,
                f"Error processing Excel file: {str(e)}",
                None,
                processing_info,
            )

    def _process_regular_file(
        self, temp_path: Path, processing_info: Dict
    ) -> Tuple[bool, str, Optional[pd.DataFrame], Dict]:
        """Process non-Excel files"""
        try:
            reader = CommentReader()
            comments_df = reader.read_file(temp_path)

            # Validate DataFrame content
            is_valid_df, df_validation_message = (
                InputValidator.validate_dataframe_content(comments_df)
            )
            if not is_valid_df:
                return (
                    False,
                    f"Data validation failed: {df_validation_message}",
                    None,
                    processing_info,
                )

            processing_info["is_multi_sheet"] = False
            processing_info["requires_sheet_selection"] = False

            return True, "File processed successfully", comments_df, processing_info

        except Exception as e:
            return False, f"Error processing file: {str(e)}", None, processing_info

    def process_excel_sheet(
        self, temp_path: str, sheet_name: str
    ) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """Process specific Excel sheet"""
        try:
            reader = CommentReader()
            comments_df = reader.read_excel_sheet(Path(temp_path), sheet_name)

            # Validate DataFrame content
            is_valid_df, df_validation_message = (
                InputValidator.validate_dataframe_content(comments_df)
            )
            if not is_valid_df:
                return False, f"Data validation failed: {df_validation_message}", None

            return True, f"Sheet '{sheet_name}' processed successfully", comments_df

        except Exception as e:
            return False, f"Error processing sheet: {str(e)}", None

    def get_data_quality_metrics(self, comments_df: pd.DataFrame) -> Dict:
        """Calculate data quality metrics"""
        total_rows = len(comments_df)
        empty_comments = (
            comments_df["comment"].isna().sum()
            if "comment" in comments_df.columns
            else 0
        )
        duplicate_comments = comments_df.duplicated().sum()

        quality_score = max(
            0,
            100
            - (empty_comments / total_rows * 50)
            - (duplicate_comments / total_rows * 30),
        )

        if quality_score >= 90:
            quality_status = "Excellent"
            quality_color = "#16a34a"
        elif quality_score >= 70:
            quality_status = "Good"
            quality_color = "#d97706"
        else:
            quality_status = "Needs Review"
            quality_color = "#dc2626"

        return {
            "total_rows": total_rows,
            "empty_comments": empty_comments,
            "duplicate_comments": duplicate_comments,
            "valid_entries": total_rows - empty_comments,
            "quality_score": quality_score,
            "quality_status": quality_status,
            "quality_color": quality_color,
        }
