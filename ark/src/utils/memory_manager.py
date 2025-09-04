"""
Memory Management and Optimization Module
Handles memory efficient processing and prevents memory leaks in large dataset operations
"""

import gc
import psutil
import pandas as pd
import logging
from typing import Iterator, Tuple, Dict, List, Optional
from contextlib import contextmanager
from pathlib import Path
import weakref

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Memory management utility for efficient data processing
    Prevents memory leaks and optimizes memory usage for large datasets
    """
    
    def __init__(self, max_memory_mb: int = 1024):
        """
        Initialize memory manager
        
        Args:
            max_memory_mb: Maximum memory usage in MB before triggering cleanup
        """
        self.max_memory_mb = max_memory_mb
        self.tracked_objects = weakref.WeakSet()
        self.chunk_cache = {}
        
    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage statistics"""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            "rss_mb": memory_info.rss / (1024 * 1024),  # Resident Set Size
            "vms_mb": memory_info.vms / (1024 * 1024),  # Virtual Memory Size
            "percent": process.memory_percent(),
            "available_mb": psutil.virtual_memory().available / (1024 * 1024)
        }
    
    def check_memory_threshold(self) -> bool:
        """Check if memory usage exceeds threshold"""
        usage = self.get_memory_usage()
        return usage["rss_mb"] > self.max_memory_mb
    
    def force_garbage_collection(self):
        """Force garbage collection and clear cache"""
        # Clear chunk cache
        self.chunk_cache.clear()
        
        # Force garbage collection
        gc.collect()
        
        logger.info("Forced garbage collection completed")
    
    @contextmanager
    def memory_monitor(self, operation_name: str = "operation"):
        """Context manager to monitor memory usage during operations"""
        initial_memory = self.get_memory_usage()
        logger.info(f"Starting {operation_name}, initial memory: {initial_memory['rss_mb']:.1f}MB")
        
        try:
            yield self
        finally:
            final_memory = self.get_memory_usage()
            memory_diff = final_memory['rss_mb'] - initial_memory['rss_mb']
            
            logger.info(
                f"Completed {operation_name}, final memory: {final_memory['rss_mb']:.1f}MB "
                f"(change: {memory_diff:+.1f}MB)"
            )
            
            # Auto-cleanup if memory usage is high
            if self.check_memory_threshold():
                logger.warning("Memory threshold exceeded, forcing cleanup")
                self.force_garbage_collection()


class ChunkedDataProcessor:
    """
    Process large datasets in memory-efficient chunks
    Prevents memory exhaustion when working with large files
    """
    
    def __init__(self, chunk_size: int = 1000, memory_manager: Optional[MemoryManager] = None):
        """
        Initialize chunked processor
        
        Args:
            chunk_size: Number of rows to process per chunk
            memory_manager: Memory manager instance (creates one if None)
        """
        self.chunk_size = chunk_size
        self.memory_manager = memory_manager or MemoryManager()
    
    def read_excel_chunks(self, file_path: Path, sheet_name: str = None) -> Iterator[pd.DataFrame]:
        """
        Read Excel file in chunks to minimize memory usage
        
        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name to read (None for first sheet)
            
        Yields:
            DataFrame chunks
        """
        try:
            # First, get total rows to determine chunk processing
            with pd.ExcelFile(file_path) as excel_file:
                if sheet_name is None:
                    sheet_name = excel_file.sheet_names[0]
                
                # Read file in chunks using nrows parameter
                total_rows = 0
                chunk_start = 0
                
                while True:
                    try:
                        # Read chunk with skiprows and nrows
                        chunk_df = pd.read_excel(
                            file_path, 
                            sheet_name=sheet_name,
                            skiprows=chunk_start,
                            nrows=self.chunk_size
                        )
                        
                        if chunk_df.empty:
                            break
                            
                        # If this is the first chunk, it contains headers
                        if chunk_start == 0:
                            headers = chunk_df.columns.tolist()
                        else:
                            # For subsequent chunks, set column names manually
                            chunk_df.columns = headers
                        
                        total_rows += len(chunk_df)
                        yield chunk_df
                        
                        # Cleanup chunk from memory
                        del chunk_df
                        
                        # Check memory and cleanup if needed
                        if self.memory_manager.check_memory_threshold():
                            self.memory_manager.force_garbage_collection()
                        
                        chunk_start += self.chunk_size
                        
                    except Exception as e:
                        logger.error(f"Error reading chunk starting at row {chunk_start}: {e}")
                        break
                        
        except Exception as e:
            logger.error(f"Error reading Excel file {file_path}: {e}")
            raise
    
    def read_csv_chunks(self, file_path: Path, encoding: str = 'utf-8') -> Iterator[pd.DataFrame]:
        """
        Read CSV file in chunks
        
        Args:
            file_path: Path to CSV file
            encoding: File encoding
            
        Yields:
            DataFrame chunks
        """
        try:
            # Use pandas chunksize parameter for memory efficiency
            chunk_reader = pd.read_csv(
                file_path,
                encoding=encoding,
                chunksize=self.chunk_size
            )
            
            for chunk_df in chunk_reader:
                yield chunk_df
                
                # Cleanup and memory check
                if self.memory_manager.check_memory_threshold():
                    self.memory_manager.force_garbage_collection()
                    
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            raise
    
    def process_chunks_safely(self, chunks: Iterator[pd.DataFrame], 
                             processor_func: callable) -> List[Dict]:
        """
        Process chunks with memory management and error handling
        
        Args:
            chunks: Iterator of DataFrame chunks
            processor_func: Function to process each chunk
            
        Returns:
            List of processed results
        """
        results = []
        chunk_count = 0
        
        with self.memory_manager.memory_monitor(f"chunked_processing"):
            for chunk_df in chunks:
                try:
                    chunk_count += 1
                    logger.info(f"Processing chunk {chunk_count} ({len(chunk_df)} rows)")
                    
                    # Process chunk
                    chunk_result = processor_func(chunk_df)
                    if chunk_result:
                        results.extend(chunk_result if isinstance(chunk_result, list) else [chunk_result])
                    
                    # Explicit cleanup
                    del chunk_df
                    
                    # Memory management
                    if chunk_count % 5 == 0:  # Every 5 chunks
                        self.memory_manager.force_garbage_collection()
                        
                except Exception as e:
                    logger.error(f"Error processing chunk {chunk_count}: {e}")
                    # Continue with next chunk instead of failing entirely
                    continue
        
        logger.info(f"Completed processing {chunk_count} chunks, got {len(results)} results")
        return results


class OptimizedDataFrame:
    """
    Memory-optimized DataFrame operations
    Reduces memory footprint of DataFrames through type optimization
    """
    
    @staticmethod
    def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize DataFrame data types to reduce memory usage
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with optimized dtypes
        """
        optimized_df = df.copy()
        
        # Optimize numeric columns
        for col in optimized_df.select_dtypes(include=['int64']).columns:
            if optimized_df[col].min() >= -128 and optimized_df[col].max() <= 127:
                optimized_df[col] = optimized_df[col].astype('int8')
            elif optimized_df[col].min() >= -32768 and optimized_df[col].max() <= 32767:
                optimized_df[col] = optimized_df[col].astype('int16')
            elif optimized_df[col].min() >= -2147483648 and optimized_df[col].max() <= 2147483647:
                optimized_df[col] = optimized_df[col].astype('int32')
        
        # Optimize float columns
        for col in optimized_df.select_dtypes(include=['float64']).columns:
            # Try to convert to float32 if precision allows
            if optimized_df[col].dtype == 'float64':
                optimized_df[col] = pd.to_numeric(optimized_df[col], downcast='float')
        
        # Optimize object columns (strings)
        for col in optimized_df.select_dtypes(include=['object']).columns:
            # Convert to category if the number of unique values is small
            unique_ratio = optimized_df[col].nunique() / len(optimized_df)
            if unique_ratio < 0.5:  # Less than 50% unique values
                optimized_df[col] = optimized_df[col].astype('category')
        
        return optimized_df
    
    @staticmethod
    def get_memory_usage(df: pd.DataFrame) -> Dict[str, float]:
        """Get detailed memory usage of DataFrame"""
        memory_usage = df.memory_usage(deep=True)
        
        return {
            "total_mb": memory_usage.sum() / (1024 * 1024),
            "per_column_mb": {
                col: usage / (1024 * 1024) 
                for col, usage in memory_usage.items()
            },
            "rows": len(df),
            "columns": len(df.columns)
        }
    
    @staticmethod
    def sample_efficiently(df: pd.DataFrame, n: int, 
                          random_state: int = 42) -> pd.DataFrame:
        """
        Sample DataFrame efficiently without loading entire dataset into memory
        
        Args:
            df: Input DataFrame
            n: Number of samples
            random_state: Random seed
            
        Returns:
            Sampled DataFrame
        """
        if len(df) <= n:
            return df.copy()
        
        # Use pandas sample which is memory efficient
        sampled = df.sample(n=n, random_state=random_state)
        
        # Reset index to avoid memory fragmentation
        return sampled.reset_index(drop=True)


class BatchProcessor:
    """
    Process large datasets in batches with memory management
    Designed for AI analysis operations that may consume significant memory
    """
    
    def __init__(self, batch_size: int = 50, memory_limit_mb: int = 512):
        """
        Initialize batch processor
        
        Args:
            batch_size: Number of items per batch
            memory_limit_mb: Memory limit for processing
        """
        self.batch_size = batch_size
        self.memory_manager = MemoryManager(max_memory_mb=memory_limit_mb)
    
    def create_batches(self, items: List, batch_size: Optional[int] = None) -> Iterator[List]:
        """
        Create batches from list of items
        
        Args:
            items: List of items to batch
            batch_size: Override default batch size
            
        Yields:
            Batches of items
        """
        batch_size = batch_size or self.batch_size
        
        for i in range(0, len(items), batch_size):
            yield items[i:i + batch_size]
    
    def process_batches_with_memory_management(self, 
                                               batches: Iterator[List],
                                               processor_func: callable,
                                               cleanup_func: Optional[callable] = None) -> List:
        """
        Process batches with automatic memory management
        
        Args:
            batches: Iterator of batches
            processor_func: Function to process each batch
            cleanup_func: Optional cleanup function to call between batches
            
        Returns:
            Combined results from all batches
        """
        all_results = []
        batch_count = 0
        
        with self.memory_manager.memory_monitor("batch_processing"):
            for batch in batches:
                try:
                    batch_count += 1
                    
                    # Process batch
                    batch_results = processor_func(batch)
                    if batch_results:
                        all_results.extend(batch_results if isinstance(batch_results, list) else [batch_results])
                    
                    # Custom cleanup if provided
                    if cleanup_func:
                        cleanup_func()
                    
                    # Memory management every few batches
                    if batch_count % 3 == 0:
                        self.memory_manager.force_garbage_collection()
                        
                        # Log memory status
                        memory_info = self.memory_manager.get_memory_usage()
                        logger.info(f"Batch {batch_count}: Memory usage {memory_info['rss_mb']:.1f}MB")
                    
                except Exception as e:
                    logger.error(f"Error processing batch {batch_count}: {e}")
                    # Continue processing instead of failing completely
                    continue
        
        return all_results


# Utility functions for memory optimization

def optimize_session_state():
    """Clean up Streamlit session state to free memory"""
    import streamlit as st
    
    # Keys that are safe to remove for memory cleanup
    removable_keys = [
        'temp_data', 'raw_data', 'processed_chunks', 
        'analysis_cache', 'temp_results'
    ]
    
    removed_count = 0
    for key in removable_keys:
        if key in st.session_state:
            del st.session_state[key]
            removed_count += 1
    
    if removed_count > 0:
        logger.info(f"Cleaned up {removed_count} items from session state")


def log_memory_status():
    """Log current memory status for debugging"""
    manager = MemoryManager()
    memory_info = manager.get_memory_usage()
    
    logger.info(
        f"Memory Status - RSS: {memory_info['rss_mb']:.1f}MB, "
        f"VMS: {memory_info['vms_mb']:.1f}MB, "
        f"Percent: {memory_info['percent']:.1f}%, "
        f"Available: {memory_info['available_mb']:.1f}MB"
    )
    
    return memory_info