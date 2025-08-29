"""
Comment Reader Module
Handles reading and processing customer comments from various file formats
with memory optimization for large datasets
"""

import pandas as pd
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Union
from src.config import Config
from src.utils.memory_manager import MemoryManager, ChunkedDataProcessor, OptimizedDataFrame

# Set up logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class CommentReader:
    """Class to handle reading customer comments from various sources with memory optimization"""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.csv', '.json', '.txt']
        self.data = None
        self.memory_manager = MemoryManager(max_memory_mb=512)
        self.chunked_processor = ChunkedDataProcessor(chunk_size=1000, memory_manager=self.memory_manager)
        
    def read_file(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Read comments from file based on file extension
        
        Args:
            file_path: Path to the file containing comments
            
        Returns:
            pandas.DataFrame: Processed comments data
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_extension = file_path.suffix.lower()
        
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
            
        logger.info(f"Reading file: {file_path}")
        
        try:
            if file_extension == '.xlsx':
                self.data = self._read_excel(file_path)
            elif file_extension == '.csv':
                self.data = self._read_csv(file_path)
            elif file_extension == '.json':
                self.data = self._read_json(file_path)
            elif file_extension == '.txt':
                self.data = self._read_text(file_path)
                
            logger.info(f"Successfully loaded {len(self.data)} comments")
            return self.data
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise
    
    def read_excel_sheet(self, file_path: Path, sheet_name: str) -> pd.DataFrame:
        """
        Read Excel file with specific sheet selection
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Name of the sheet to read
            
        Returns:
            pandas.DataFrame: Processed comments data from the selected sheet
        """
        try:
            logger.info(f"Reading Excel file: {file_path}, sheet: {sheet_name}")
            
            # Read the specified sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Find comment column using the same logic as _read_excel
            comment_columns = [
                'comentario', 'comment', 'comentarios', 'comments',
                'opinion', 'feedback', 'texto', 'text', 'observacion',
                'observaciones', 'nota', 'notas'
            ]
            
            # Find the actual comment column
            actual_columns = df.columns.str.lower()
            comment_col = None
            
            for col_name in comment_columns:
                matching_cols = [col for col in actual_columns if col_name in col]
                if matching_cols:
                    comment_col = df.columns[actual_columns.get_loc(matching_cols[0])]
                    break
            
            if comment_col is None:
                # If no specific comment column found, use the first text column
                text_columns = df.select_dtypes(include=['object']).columns
                if len(text_columns) > 0:
                    comment_col = text_columns[0]
                else:
                    raise ValueError(f"No text columns found in Excel sheet '{sheet_name}'")
            
            # Create standardized DataFrame with pipeline-compatible column names
            result_df = pd.DataFrame()
            result_df['Comentario Final'] = df[comment_col].astype(str)
            result_df['source'] = f'excel-{sheet_name}'
            result_df['file_name'] = file_path.name
            
            # Check for score column for NPS
            score_columns = ['nota', 'score', 'puntuacion', 'calificacion', 'rating', 'nps']
            for col_name in score_columns:
                matching_cols = [col for col in actual_columns if col_name in col]
                if matching_cols:
                    score_col = df.columns[actual_columns.get_loc(matching_cols[0])]
                    result_df['Nota'] = pd.to_numeric(df[score_col], errors='coerce')
                    break
            
            # Add other available columns
            for col in df.columns:
                if col != comment_col:
                    result_df[f'metadata_{col.lower()}'] = df[col]
            
            # Remove empty comments
            result_df = result_df[result_df['Comentario Final'].str.strip() != '']
            result_df = result_df[result_df['Comentario Final'] != 'nan']
            
            logger.info(f"Successfully read {len(result_df)} comments from sheet '{sheet_name}'")
            self.data = result_df.reset_index(drop=True)
            return self.data
            
        except Exception as e:
            logger.error(f"Error reading Excel sheet '{sheet_name}': {str(e)}")
            raise
    
    def _read_excel(self, file_path: Path) -> pd.DataFrame:
        """Read Excel file and extract comments with memory optimization"""
        with self.memory_manager.memory_monitor(f"reading_excel_{file_path.name}"):
            try:
                # Check file size and decide on chunked vs normal reading
                file_size_mb = file_path.stat().st_size / (1024 * 1024)
                
                if file_size_mb > 50:  # Use chunked reading for large files
                    logger.info(f"Large file detected ({file_size_mb:.1f}MB), using chunked reading")
                    return self._read_excel_chunked(file_path)
                
                # Normal reading for smaller files
                df = pd.read_excel(file_path, sheet_name=0)
                
                # Look for comment columns (common names)
                comment_columns = [
                    'comentario', 'comment', 'comentarios', 'comments',
                    'opinion', 'feedback', 'texto', 'text', 'observacion',
                    'observaciones', 'nota', 'notas'
                ]
                
                # Find the actual comment column
                actual_columns = df.columns.str.lower()
                comment_col = None
                
                for col_name in comment_columns:
                    matching_cols = [col for col in actual_columns if col_name in col]
                    if matching_cols:
                        comment_col = df.columns[actual_columns.get_loc(matching_cols[0])]
                        break
                
                if comment_col is None:
                    # If no specific comment column found, use the first text column
                    text_columns = df.select_dtypes(include=['object']).columns
                    if len(text_columns) > 0:
                        comment_col = text_columns[0]
                    else:
                        raise ValueError("No text columns found in Excel file")
                
                # Create standardized DataFrame with pipeline-compatible column names
                result_df = pd.DataFrame()
                result_df['Comentario Final'] = df[comment_col].astype(str)
                result_df['source'] = 'excel'
                result_df['file_name'] = file_path.name
                
                # Check for score column for NPS
                score_columns = ['nota', 'score', 'puntuacion', 'calificacion', 'rating', 'nps']
                for col_name in score_columns:
                    matching_cols = [col for col in actual_columns if col_name in col]
                    if matching_cols:
                        score_col = df.columns[actual_columns.get_loc(matching_cols[0])]
                        result_df['Nota'] = pd.to_numeric(df[score_col], errors='coerce')
                        break
                
                # Add other available columns
                for col in df.columns:
                    if col != comment_col:
                        result_df[f'metadata_{col.lower()}'] = df[col]
                
                # Remove empty comments
                result_df = result_df[result_df['Comentario Final'].str.strip() != '']
                result_df = result_df[result_df['Comentario Final'] != 'nan']
                
                # Optimize DataFrame memory usage
                result_df = OptimizedDataFrame.optimize_dtypes(result_df)
                
                # Clean up original DataFrame
                del df
                self.memory_manager.force_garbage_collection()
                
                return result_df.reset_index(drop=True)
                
            except Exception as e:
                logger.error(f"Error reading Excel file: {str(e)}")
                raise
    
    def _read_excel_chunked(self, file_path: Path) -> pd.DataFrame:
        """Read large Excel file using chunked processing"""
        try:
            chunks = []
            
            for chunk_df in self.chunked_processor.read_excel_chunks(file_path):
                processed_chunk = self._process_excel_chunk(chunk_df, file_path)
                if processed_chunk is not None and not processed_chunk.empty:
                    chunks.append(processed_chunk)
            
            if not chunks:
                raise ValueError("No valid data found in Excel file")
            
            # Combine chunks efficiently
            result_df = pd.concat(chunks, ignore_index=True)
            
            # Clean up chunks
            del chunks
            self.memory_manager.force_garbage_collection()
            
            # Optimize final DataFrame
            result_df = OptimizedDataFrame.optimize_dtypes(result_df)
            
            logger.info(f"Successfully read {len(result_df)} comments using chunked processing")
            return result_df
            
        except Exception as e:
            logger.error(f"Error reading Excel file with chunked processing: {str(e)}")
            raise
    
    def _process_excel_chunk(self, chunk_df: pd.DataFrame, file_path: Path) -> pd.DataFrame:
        """Process a single Excel chunk"""
        try:
            # Look for comment columns
            comment_columns = [
                'comentario', 'comment', 'comentarios', 'comments',
                'opinion', 'feedback', 'texto', 'text', 'observacion',
                'observaciones', 'nota', 'notas'
            ]
            
            actual_columns = chunk_df.columns.str.lower()
            comment_col = None
            
            for col_name in comment_columns:
                matching_cols = [col for col in actual_columns if col_name in col]
                if matching_cols:
                    comment_col = chunk_df.columns[actual_columns.get_loc(matching_cols[0])]
                    break
            
            if comment_col is None:
                text_columns = chunk_df.select_dtypes(include=['object']).columns
                if len(text_columns) > 0:
                    comment_col = text_columns[0]
                else:
                    return None
            
            # Create result DataFrame for chunk with pipeline-compatible column names
            result_chunk = pd.DataFrame()
            result_chunk['Comentario Final'] = chunk_df[comment_col].astype(str)
            result_chunk['source'] = 'excel'
            result_chunk['file_name'] = file_path.name
            
            # Check for score column
            actual_cols = chunk_df.columns.str.lower()
            score_columns = ['nota', 'score', 'puntuacion', 'calificacion', 'rating', 'nps']
            for col_name in score_columns:
                matching_cols = [col for col in actual_cols if col_name in col]
                if matching_cols:
                    score_col = chunk_df.columns[actual_cols.get_loc(matching_cols[0])]
                    result_chunk['Nota'] = pd.to_numeric(chunk_df[score_col], errors='coerce')
                    break
            
            # Add metadata columns
            for col in chunk_df.columns:
                if col != comment_col:
                    result_chunk[f'metadata_{col.lower()}'] = chunk_df[col]
            
            # Remove empty comments
            result_chunk = result_chunk[result_chunk['Comentario Final'].str.strip() != '']
            result_chunk = result_chunk[result_chunk['Comentario Final'] != 'nan']
            
            return result_chunk
            
        except Exception as e:
            logger.error(f"Error processing Excel chunk: {str(e)}")
            return None
    
    def _read_csv(self, file_path: Path) -> pd.DataFrame:
        """Read CSV file and extract comments"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("Could not decode CSV file with any supported encoding")
            
            # Apply similar logic as Excel processing
            return self._standardize_dataframe(df, file_path, 'csv')
            
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            raise
    
    def _read_json(self, file_path: Path) -> pd.DataFrame:
        """Read JSON file and extract comments"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                if 'comments' in data:
                    df = pd.DataFrame(data['comments'])
                elif 'data' in data:
                    df = pd.DataFrame(data['data'])
                else:
                    # Treat dict as single row
                    df = pd.DataFrame([data])
            else:
                raise ValueError("Unsupported JSON structure")
            
            return self._standardize_dataframe(df, file_path, 'json')
            
        except Exception as e:
            logger.error(f"Error reading JSON file: {str(e)}")
            raise
    
    def _read_text(self, file_path: Path) -> pd.DataFrame:
        """Read plain text file with one comment per line"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Clean and filter lines
            comments = [line.strip() for line in lines if line.strip()]
            
            df = pd.DataFrame({
                'Comentario Final': comments,  # Pipeline-compatible column name
                'source': 'text',
                'file_name': file_path.name,
                'line_number': range(1, len(comments) + 1)
            })
            
            return df
            
        except Exception as e:
            logger.error(f"Error reading text file: {str(e)}")
            raise
    
    def _standardize_dataframe(self, df: pd.DataFrame, file_path: Path, source: str) -> pd.DataFrame:
        """Standardize DataFrame format for comments"""
        
        # Find comment column
        comment_columns = [
            'comentario', 'comment', 'comentarios', 'comments',
            'opinion', 'feedback', 'texto', 'text', 'observacion'
        ]
        
        actual_columns = df.columns.str.lower()
        comment_col = None
        
        for col_name in comment_columns:
            matching_cols = [col for col in actual_columns if col_name in col]
            if matching_cols:
                comment_col = df.columns[actual_columns.get_loc(matching_cols[0])]
                break
        
        if comment_col is None:
            text_columns = df.select_dtypes(include=['object']).columns
            if len(text_columns) > 0:
                comment_col = text_columns[0]
            else:
                raise ValueError(f"No text columns found in {source} file")
        
        # Create result DataFrame with standardized column names for pipeline
        result_df = pd.DataFrame()
        result_df['Comentario Final'] = df[comment_col].astype(str)  # Changed from 'comment' to 'Comentario Final'
        result_df['source'] = source
        result_df['file_name'] = file_path.name
        
        # Check for Nota/score columns for NPS analysis
        score_columns = ['nota', 'score', 'puntuacion', 'calificacion', 'rating', 'nps']
        score_col = None
        
        for col_name in score_columns:
            matching_cols = [col for col in actual_columns if col_name in col]
            if matching_cols:
                score_col = df.columns[actual_columns.get_loc(matching_cols[0])]
                result_df['Nota'] = pd.to_numeric(df[score_col], errors='coerce')
                logger.info(f"Found score column '{score_col}' mapped to 'Nota'")
                break
        
        # Add metadata columns
        for col in df.columns:
            if col != comment_col and col != score_col:
                result_df[f'metadata_{col.lower()}'] = df[col]
        
        # Clean data
        result_df = result_df[result_df['Comentario Final'].str.strip() != '']
        result_df = result_df[result_df['Comentario Final'] != 'nan']
        
        return result_df.reset_index(drop=True)
    
    def get_data_info(self) -> Dict:
        """Get information about loaded data"""
        if self.data is None:
            return {"status": "No data loaded"}
        
        # Handle both old and new column names for backward compatibility
        comment_col = 'Comentario Final' if 'Comentario Final' in self.data.columns else 'comment'
        
        return {
            "total_comments": len(self.data),
            "columns": list(self.data.columns),
            "sample_comment": self.data[comment_col].iloc[0] if len(self.data) > 0 and comment_col in self.data.columns else None,
            "sources": self.data['source'].value_counts().to_dict() if 'source' in self.data.columns else {},
            "data_types": self.data.dtypes.to_dict()
        }
    
    def deduplicate_comments(self, df: pd.DataFrame, comment_column: str = 'Comentario Final', 
                           method: str = 'exact') -> tuple[pd.DataFrame, Dict]:
        """
        Deduplicate comments in the DataFrame
        
        Args:
            df: DataFrame containing comments
            comment_column: Name of the comment column
            method: Deduplication method ('exact', 'similar', or 'fuzzy')
            
        Returns:
            Tuple of (deduplicated_df, deduplication_stats)
        """
        logger.info(f"Starting deduplication with method: {method}")
        
        original_count = len(df)
        stats = {
            'original_count': original_count,
            'method': method,
            'duplicates_removed': 0,
            'final_count': 0
        }
        
        if original_count == 0:
            logger.warning("Empty DataFrame provided for deduplication")
            return df, stats
        
        # Ensure comment column exists
        if comment_column not in df.columns:
            raise ValueError(f"Comment column '{comment_column}' not found in DataFrame")
        
        # Remove rows with null or empty comments
        df_clean = df.dropna(subset=[comment_column]).copy()
        df_clean = df_clean[df_clean[comment_column].astype(str).str.strip() != '']
        df_clean = df_clean[df_clean[comment_column].astype(str) != 'nan']
        
        empty_removed = original_count - len(df_clean)
        if empty_removed > 0:
            logger.info(f"Removed {empty_removed} empty/null comments")
        
        # Convert to string for processing
        df_clean[comment_column] = df_clean[comment_column].astype(str)
        
        if method == 'exact':
            # Remove exact duplicates
            df_dedup = df_clean.drop_duplicates(subset=[comment_column], keep='first')
            
        elif method == 'similar':
            # Remove similar comments (case-insensitive, whitespace normalized)
            df_clean['comment_normalized'] = (
                df_clean[comment_column]
                .str.lower()
                .str.strip()
                .str.replace(r'\s+', ' ', regex=True)
            )
            df_dedup = df_clean.drop_duplicates(subset=['comment_normalized'], keep='first')
            df_dedup = df_dedup.drop(columns=['comment_normalized'])
            
        elif method == 'fuzzy':
            # More aggressive deduplication (requires additional processing)
            # For now, implement as similar method
            logger.info("Fuzzy deduplication not yet implemented, using 'similar' method")
            df_clean['comment_normalized'] = (
                df_clean[comment_column]
                .str.lower()
                .str.strip()
                .str.replace(r'[^\w\s]', '', regex=True)  # Remove punctuation
                .str.replace(r'\s+', ' ', regex=True)
            )
            df_dedup = df_clean.drop_duplicates(subset=['comment_normalized'], keep='first')
            df_dedup = df_dedup.drop(columns=['comment_normalized'])
            
        else:
            raise ValueError(f"Unknown deduplication method: {method}")
        
        # Reset index
        df_dedup = df_dedup.reset_index(drop=True)
        
        # Calculate final stats
        final_count = len(df_dedup)
        duplicates_removed = len(df_clean) - final_count
        
        stats.update({
            'duplicates_removed': duplicates_removed,
            'final_count': final_count,
            'deduplication_rate': (duplicates_removed / len(df_clean)) * 100 if len(df_clean) > 0 else 0,
            'empty_comments_removed': empty_removed
        })
        
        logger.info(f"Deduplication complete: {original_count} → {final_count} "
                   f"({duplicates_removed} duplicates + {empty_removed} empty removed)")
        
        return df_dedup, stats

# Example usage and testing
if __name__ == "__main__":
    reader = CommentReader()
    
    # Test with the Personal Paraguay dataset
    try:
        # Cloud-compatible relative path
        data_path = Path(__file__).parent.parent.parent / "data" / "raw" / "Personal_Paraguay_Fiber_To_The_Home_Customer_Comments_Dataset.xlsx"
        if data_path.exists():
            comments_df = reader.read_file(data_path)
            print("Data loaded successfully!")
            print(reader.get_data_info())
        else:
            print("Dataset file not found. Please place the Excel file in data/raw/ directory.")
            print(f"Expected path: {data_path}")
            print("Note: In Streamlit Cloud, use file upload interface instead.")
    except Exception as e:
        print(f"Error: {e}")