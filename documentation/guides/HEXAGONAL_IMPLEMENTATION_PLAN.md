# Hexagonal Architecture Implementation Plan
## Comment Analyzer Pipeline Refactoring

**Created:** 2025-08-26  
**Objective:** Fix critical pipeline issues using hexagonal architecture principles without massive refactoring

## 1. Architecture Overview

### Current State (Problematic)
```
Excel File → FileUploadService → CommentReader → EnhancedAnalyzer → API → Export
            (Tightly Coupled, Column Mismatches, Silent Failures)
```

### Target State (Hexagonal)
```
                    DOMAIN (Core Business Logic)
                 ┌─────────────────────────────────┐
                 │  • Comment Entity               │
                 │  • Analysis Result Entity        │
                 │  • NPS Calculation Logic         │
                 │  • Sentiment Analysis Rules      │
                 └─────────────────────────────────┘
                           ↑         ↑
                      [PORTS - Interfaces]
                           ↑         ↑
    ┌──────────────────────┼─────────┼──────────────────────┐
    │                      │         │                      │
[ADAPTER]             [ADAPTER]  [ADAPTER]            [ADAPTER]
Excel Reader          API Client  Validator           Excel Writer
(Infrastructure)      (External)  (Application)       (Infrastructure)
```

## 2. Implementation Phases

### Phase 1: Critical Fixes (Day 1) 🔴 BLOCKING
Fix the pipeline breaks that prevent Excel processing

#### Task 1.1: Fix Column Name Mismatch
**File:** `src/data_processing/comment_reader.py`
```python
# Add standardization method
def standardize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names for pipeline compatibility"""
    column_mapping = {
        'comment': 'Comentario Final',
        'score': 'Nota',
        'nps_category': 'NPS'
    }
    
    # Rename columns if they exist
    for old_name, new_name in column_mapping.items():
        if old_name in df.columns and new_name not in df.columns:
            df.rename(columns={old_name: new_name}, inplace=True)
    
    return df
```

#### Task 1.2: Add Data Validation Layer
**New File:** `src/core/validators/schema_validator.py`
```python
from typing import Dict, List, Optional
import pandas as pd

class SchemaValidator:
    """Port for data validation"""
    
    REQUIRED_COLUMNS = ['Comentario Final']
    OPTIONAL_COLUMNS = ['Nota', 'NPS', 'metadata_fecha']
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> Dict[str, any]:
        """Validate DataFrame schema for pipeline"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'column_mapping': {}
        }
        
        # Check required columns
        for col in SchemaValidator.REQUIRED_COLUMNS:
            if col not in df.columns:
                # Try to find similar column
                similar = SchemaValidator._find_similar_column(df.columns, col)
                if similar:
                    validation_result['column_mapping'][similar] = col
                    validation_result['warnings'].append(
                        f"Column '{similar}' will be mapped to '{col}'"
                    )
                else:
                    validation_result['is_valid'] = False
                    validation_result['errors'].append(
                        f"Required column '{col}' not found"
                    )
        
        # Check optional columns
        for col in SchemaValidator.OPTIONAL_COLUMNS:
            if col not in df.columns:
                validation_result['warnings'].append(
                    f"Optional column '{col}' not found - feature will be disabled"
                )
        
        return validation_result
    
    @staticmethod
    def _find_similar_column(columns: List[str], target: str) -> Optional[str]:
        """Find column with similar name"""
        target_lower = target.lower()
        for col in columns:
            if target_lower in col.lower() or col.lower() in target_lower:
                return col
        return None
```

#### Task 1.3: Fix Silent Exception Handling
**File:** `src/sentiment_analysis/enhanced_analyzer.py`
```python
# Replace all except:pass with proper error handling
import logging

logger = logging.getLogger(__name__)

# Line 206 - Replace:
# except:
#     pass

# With:
except Exception as e:
    logger.error(f"API call failed: {str(e)}")
    return {
        'sentiment': 'unknown',
        'confidence': 0,
        'error': str(e)
    }

# Similar replacements for lines 260 and 300
```

### Phase 2: Domain Model Creation (Day 2)
Create clean domain entities independent of infrastructure

#### Task 2.1: Create Domain Entities
**New File:** `src/core/domain/entities.py`
```python
from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class Sentiment(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"

class NPSCategory(Enum):
    PROMOTER = "promoter"
    PASSIVE = "passive"
    DETRACTOR = "detractor"

@dataclass
class Comment:
    """Core domain entity for a comment"""
    id: str
    text: str
    source: str = "excel"
    timestamp: Optional[datetime] = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        self.validate()
    
    def validate(self):
        """Business rule validation"""
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Comment text cannot be empty")
        if len(self.text) > 5000:
            raise ValueError("Comment exceeds maximum length")

@dataclass
class NPSScore:
    """Domain entity for NPS scoring"""
    value: Optional[int]
    category: Optional[NPSCategory] = None
    
    def __post_init__(self):
        if self.value is not None:
            if not 0 <= self.value <= 10:
                raise ValueError("NPS score must be between 0 and 10")
            self.category = self._calculate_category()
    
    def _calculate_category(self) -> NPSCategory:
        """Business logic for NPS categorization"""
        if self.value >= 9:
            return NPSCategory.PROMOTER
        elif self.value >= 7:
            return NPSCategory.PASSIVE
        else:
            return NPSCategory.DETRACTOR

@dataclass
class AnalysisResult:
    """Domain entity for analysis results"""
    comment_id: str
    sentiment: Sentiment
    confidence: float
    emotions: List[str]
    topics: List[str]
    nps: Optional[NPSScore] = None
    api_response: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for export"""
        return {
            'comment_id': self.comment_id,
            'sentiment': self.sentiment.value,
            'confidence': self.confidence,
            'emotions': self.emotions,
            'topics': self.topics,
            'nps_score': self.nps.value if self.nps else None,
            'nps_category': self.nps.category.value if self.nps else None
        }
```

### Phase 3: Port Definition (Day 2)
Define interfaces for external interactions

#### Task 3.1: Create Port Interfaces
**New File:** `src/core/ports/data_ingestion.py`
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd
from ..domain.entities import Comment

class DataIngestionPort(ABC):
    """Port for ingesting data from various sources"""
    
    @abstractmethod
    def read_file(self, file_path: str, **kwargs) -> pd.DataFrame:
        """Read file and return DataFrame"""
        pass
    
    @abstractmethod
    def validate_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate ingested data"""
        pass
    
    @abstractmethod
    def transform_to_comments(self, data: pd.DataFrame) -> List[Comment]:
        """Transform raw data to domain entities"""
        pass
```

**New File:** `src/core/ports/analysis.py`
```python
from abc import ABC, abstractmethod
from typing import List, Dict
from ..domain.entities import Comment, AnalysisResult

class AnalysisPort(ABC):
    """Port for analysis operations"""
    
    @abstractmethod
    def analyze_sentiment(self, comment: Comment) -> AnalysisResult:
        """Analyze sentiment of a single comment"""
        pass
    
    @abstractmethod
    def analyze_batch(self, comments: List[Comment]) -> List[AnalysisResult]:
        """Analyze batch of comments"""
        pass
    
    @abstractmethod
    def calculate_metrics(self, results: List[AnalysisResult]) -> Dict:
        """Calculate aggregate metrics"""
        pass
```

### Phase 4: Adapter Implementation (Day 3)
Implement adapters for specific technologies

#### Task 4.1: Excel Adapter
**New File:** `src/adapters/excel_adapter.py`
```python
import pandas as pd
from typing import List, Dict, Any
import logging
from ..core.ports.data_ingestion import DataIngestionPort
from ..core.domain.entities import Comment
from ..core.validators.schema_validator import SchemaValidator

logger = logging.getLogger(__name__)

class ExcelAdapter(DataIngestionPort):
    """Adapter for Excel file ingestion"""
    
    def __init__(self, validator: SchemaValidator = None):
        self.validator = validator or SchemaValidator()
    
    def read_file(self, file_path: str, sheet_name: str = None) -> pd.DataFrame:
        """Read Excel file with proper error handling"""
        try:
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            logger.info(f"Successfully read Excel file: {file_path}")
            return df
            
        except Exception as e:
            logger.error(f"Failed to read Excel file: {str(e)}")
            raise ValueError(f"Cannot read Excel file: {str(e)}")
    
    def validate_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate Excel data structure"""
        validation_result = self.validator.validate_dataframe(data)
        
        if not validation_result['is_valid']:
            logger.error(f"Validation failed: {validation_result['errors']}")
            raise ValueError(f"Data validation failed: {validation_result['errors']}")
        
        # Apply column mappings if needed
        if validation_result['column_mapping']:
            for old_col, new_col in validation_result['column_mapping'].items():
                data.rename(columns={old_col: new_col}, inplace=True)
                logger.info(f"Mapped column '{old_col}' to '{new_col}'")
        
        return validation_result
    
    def transform_to_comments(self, data: pd.DataFrame) -> List[Comment]:
        """Transform DataFrame rows to Comment entities"""
        comments = []
        
        for idx, row in data.iterrows():
            try:
                # Extract comment text
                text = str(row.get('Comentario Final', ''))
                if not text or text == 'nan':
                    continue
                
                # Create comment entity
                comment = Comment(
                    id=f"excel_{idx}",
                    text=text,
                    source="excel",
                    metadata={
                        'row_index': idx,
                        'nps_score': row.get('Nota'),
                        'nps_category': row.get('NPS'),
                        **{k: v for k, v in row.items() 
                           if k not in ['Comentario Final', 'Nota', 'NPS']}
                    }
                )
                comments.append(comment)
                
            except ValueError as e:
                logger.warning(f"Skipping invalid comment at row {idx}: {str(e)}")
                continue
        
        logger.info(f"Transformed {len(comments)} valid comments from {len(data)} rows")
        return comments
```

#### Task 4.2: API Adapter
**New File:** `src/adapters/api_adapter.py`
```python
from typing import List, Dict
import logging
from ..core.ports.analysis import AnalysisPort
from ..core.domain.entities import Comment, AnalysisResult, Sentiment, NPSScore
from ..api.api_client import APIClient

logger = logging.getLogger(__name__)

class APIAdapter(AnalysisPort):
    """Adapter for external API analysis"""
    
    def __init__(self, api_client: APIClient = None):
        self.api_client = api_client or APIClient()
    
    def analyze_sentiment(self, comment: Comment) -> AnalysisResult:
        """Analyze single comment via API"""
        try:
            # Call API
            api_response = self.api_client.analyze_text(comment.text)
            
            # Transform API response to domain entity
            result = AnalysisResult(
                comment_id=comment.id,
                sentiment=self._parse_sentiment(api_response),
                confidence=api_response.get('confidence', 0.5),
                emotions=api_response.get('emotions', []),
                topics=api_response.get('topics', []),
                nps=NPSScore(comment.metadata.get('nps_score')) 
                    if comment.metadata.get('nps_score') else None,
                api_response=api_response
            )
            
            return result
            
        except Exception as e:
            logger.error(f"API analysis failed for comment {comment.id}: {str(e)}")
            # Return degraded result
            return AnalysisResult(
                comment_id=comment.id,
                sentiment=Sentiment.UNKNOWN,
                confidence=0,
                emotions=[],
                topics=[],
                nps=NPSScore(comment.metadata.get('nps_score')) 
                    if comment.metadata.get('nps_score') else None
            )
    
    def analyze_batch(self, comments: List[Comment]) -> List[AnalysisResult]:
        """Analyze batch with proper error handling"""
        results = []
        
        # Validate batch size
        if len(comments) > 100:
            logger.warning(f"Batch size {len(comments)} exceeds limit, processing in chunks")
            
        for comment in comments:
            result = self.analyze_sentiment(comment)
            results.append(result)
        
        return results
    
    def calculate_metrics(self, results: List[AnalysisResult]) -> Dict:
        """Calculate aggregate metrics"""
        metrics = {
            'total_comments': len(results),
            'sentiment_distribution': {},
            'nps_score': None,
            'average_confidence': 0
        }
        
        # Calculate sentiment distribution
        for sentiment in Sentiment:
            count = sum(1 for r in results if r.sentiment == sentiment)
            metrics['sentiment_distribution'][sentiment.value] = count
        
        # Calculate NPS if available
        nps_scores = [r.nps.value for r in results if r.nps and r.nps.value is not None]
        if nps_scores:
            promoters = sum(1 for s in nps_scores if s >= 9)
            detractors = sum(1 for s in nps_scores if s <= 6)
            metrics['nps_score'] = ((promoters - detractors) / len(nps_scores)) * 100
        
        # Calculate average confidence
        confidences = [r.confidence for r in results if r.confidence > 0]
        if confidences:
            metrics['average_confidence'] = sum(confidences) / len(confidences)
        
        return metrics
    
    def _parse_sentiment(self, api_response: Dict) -> Sentiment:
        """Parse sentiment from API response"""
        sentiment_str = api_response.get('sentiment', 'unknown').lower()
        
        if sentiment_str in ['positive', 'positivo']:
            return Sentiment.POSITIVE
        elif sentiment_str in ['negative', 'negativo']:
            return Sentiment.NEGATIVE
        elif sentiment_str in ['neutral', 'neutro']:
            return Sentiment.NEUTRAL
        else:
            return Sentiment.UNKNOWN
```

### Phase 5: Pipeline Orchestrator (Day 4)
Create the main pipeline orchestrator using hexagonal principles

#### Task 5.1: Pipeline Orchestrator
**New File:** `src/core/pipeline_orchestrator.py`
```python
import logging
from typing import Dict, Any, List
import pandas as pd
from pathlib import Path

from .ports.data_ingestion import DataIngestionPort
from .ports.analysis import AnalysisPort
from .domain.entities import Comment, AnalysisResult
from ..adapters.excel_adapter import ExcelAdapter
from ..adapters.api_adapter import APIAdapter

logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """
    Orchestrates the complete analysis pipeline using hexagonal architecture.
    Core business logic independent of infrastructure.
    """
    
    def __init__(
        self, 
        ingestion_adapter: DataIngestionPort = None,
        analysis_adapter: AnalysisPort = None
    ):
        """Initialize with dependency injection"""
        self.ingestion_adapter = ingestion_adapter or ExcelAdapter()
        self.analysis_adapter = analysis_adapter or APIAdapter()
        self.results_cache = {}
    
    def process_excel_file(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Main pipeline execution method.
        Processes Excel file through complete analysis pipeline.
        """
        pipeline_result = {
            'status': 'started',
            'file_path': file_path,
            'stages': {},
            'errors': [],
            'results': None
        }
        
        try:
            # Stage 1: Data Ingestion
            logger.info("Stage 1: Data Ingestion")
            pipeline_result['stages']['ingestion'] = 'started'
            
            df = self.ingestion_adapter.read_file(file_path, **kwargs)
            pipeline_result['stages']['ingestion'] = 'completed'
            pipeline_result['total_rows'] = len(df)
            
            # Stage 2: Data Validation
            logger.info("Stage 2: Data Validation")
            pipeline_result['stages']['validation'] = 'started'
            
            validation_result = self.ingestion_adapter.validate_data(df)
            pipeline_result['validation'] = validation_result
            pipeline_result['stages']['validation'] = 'completed'
            
            # Stage 3: Transform to Domain Entities
            logger.info("Stage 3: Transform to Domain Entities")
            pipeline_result['stages']['transformation'] = 'started'
            
            comments = self.ingestion_adapter.transform_to_comments(df)
            pipeline_result['valid_comments'] = len(comments)
            pipeline_result['stages']['transformation'] = 'completed'
            
            if not comments:
                raise ValueError("No valid comments found in file")
            
            # Stage 4: Analysis
            logger.info("Stage 4: Analysis")
            pipeline_result['stages']['analysis'] = 'started'
            
            analysis_results = self.analysis_adapter.analyze_batch(comments)
            pipeline_result['analyzed_comments'] = len(analysis_results)
            pipeline_result['stages']['analysis'] = 'completed'
            
            # Stage 5: Metrics Calculation
            logger.info("Stage 5: Metrics Calculation")
            pipeline_result['stages']['metrics'] = 'started'
            
            metrics = self.analysis_adapter.calculate_metrics(analysis_results)
            pipeline_result['metrics'] = metrics
            pipeline_result['stages']['metrics'] = 'completed'
            
            # Stage 6: Result Compilation
            logger.info("Stage 6: Result Compilation")
            pipeline_result['stages']['compilation'] = 'started'
            
            compiled_results = self._compile_results(
                comments, 
                analysis_results, 
                metrics, 
                df
            )
            pipeline_result['results'] = compiled_results
            pipeline_result['stages']['compilation'] = 'completed'
            
            # Mark pipeline as successful
            pipeline_result['status'] = 'completed'
            logger.info("Pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            pipeline_result['status'] = 'failed'
            pipeline_result['errors'].append(str(e))
            
            # Mark current stage as failed
            for stage, status in pipeline_result['stages'].items():
                if status == 'started':
                    pipeline_result['stages'][stage] = 'failed'
        
        return pipeline_result
    
    def _compile_results(
        self, 
        comments: List[Comment], 
        analysis_results: List[AnalysisResult],
        metrics: Dict,
        original_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Compile results back into DataFrame for export"""
        
        # Create results dictionary
        results_dict = {
            comment.id: result 
            for comment, result in zip(comments, analysis_results)
        }
        
        # Add analysis results to original DataFrame
        result_df = original_df.copy()
        
        # Add new columns for analysis results
        result_df['sentiment'] = None
        result_df['confidence'] = None
        result_df['emotions'] = None
        result_df['topics'] = None
        
        for idx, row in result_df.iterrows():
            comment_id = f"excel_{idx}"
            if comment_id in results_dict:
                result = results_dict[comment_id]
                result_df.at[idx, 'sentiment'] = result.sentiment.value
                result_df.at[idx, 'confidence'] = result.confidence
                result_df.at[idx, 'emotions'] = ', '.join(result.emotions)
                result_df.at[idx, 'topics'] = ', '.join(result.topics)
        
        # Add metrics as metadata
        result_df.attrs['metrics'] = metrics
        result_df.attrs['pipeline_version'] = '2.0'
        result_df.attrs['architecture'] = 'hexagonal'
        
        return result_df
```

### Phase 6: Integration & Testing (Day 5)
Integrate new components and add tests

#### Task 6.1: Update Main Application
**File:** `src/main.py`
```python
# Add at top after imports
from src.core.pipeline_orchestrator import PipelineOrchestrator

# Replace initialization section with:
def initialize_pipeline():
    """Initialize pipeline with proper error handling"""
    if 'pipeline' not in st.session_state:
        try:
            st.session_state.pipeline = PipelineOrchestrator()
            logger.info("Pipeline initialized successfully")
        except Exception as e:
            st.error(f"Failed to initialize pipeline: {str(e)}")
            logger.error(f"Pipeline initialization failed: {str(e)}")
            st.session_state.pipeline = None
    
    return st.session_state.pipeline

# Update file processing section
def process_uploaded_file(file):
    """Process uploaded file through pipeline"""
    pipeline = initialize_pipeline()
    
    if not pipeline:
        st.error("Pipeline not initialized")
        return None
    
    try:
        # Save uploaded file temporarily
        temp_path = save_temp_file(file)
        
        # Process through pipeline
        with st.spinner("Processing file through analysis pipeline..."):
            result = pipeline.process_excel_file(temp_path)
        
        if result['status'] == 'completed':
            st.success(f"Successfully processed {result['valid_comments']} comments")
            return result['results']
        else:
            st.error(f"Pipeline failed: {', '.join(result['errors'])}")
            return None
            
    except Exception as e:
        st.error(f"Processing failed: {str(e)}")
        logger.error(f"File processing error: {str(e)}")
        return None
```

## 3. Implementation Schedule

### Week 1: Critical Fixes & Core Domain
- **Day 1:** Fix column mismatches, add validation, fix silent exceptions
- **Day 2:** Create domain entities and ports
- **Day 3:** Implement Excel and API adapters
- **Day 4:** Build pipeline orchestrator
- **Day 5:** Integration and initial testing

### Week 2: Cleanup & Optimization
- **Day 6-7:** Fix remaining error handling issues
- **Day 8:** Remove unused imports and global state
- **Day 9:** Add comprehensive logging
- **Day 10:** Full integration testing

## 4. Benefits of This Approach

### 1. **Separation of Concerns**
- Domain logic independent of infrastructure
- Easy to test business rules in isolation
- Clear boundaries between layers

### 2. **Flexibility**
- Can swap Excel adapter for CSV without changing core
- Can replace OpenAI with another API easily
- Can add new data sources without touching domain

### 3. **Testability**
- Domain entities can be unit tested
- Adapters can be mocked for testing
- Pipeline can be tested with fake adapters

### 4. **Maintainability**
- Clear structure makes code easier to understand
- Changes are localized to specific layers
- Reduced coupling between components

### 5. **Error Handling**
- Each layer handles its own errors appropriately
- Pipeline orchestrator provides unified error reporting
- No more silent failures

## 5. Migration Strategy

### Step 1: Run in Parallel
- Keep existing code running
- Implement new pipeline alongside
- Add feature flag to switch between old/new

### Step 2: Gradual Migration
- Start with Excel upload flow
- Migrate one analysis type at a time
- Compare results between old and new

### Step 3: Full Cutover
- Once validated, switch to new pipeline
- Archive old code
- Update documentation

## 6. Success Metrics

### Technical Metrics
- ✅ No silent failures (0 except:pass)
- ✅ 100% input validation coverage
- ✅ All columns properly mapped
- ✅ Error messages logged appropriately

### Business Metrics
- ✅ Excel files process successfully
- ✅ NPS calculations are accurate
- ✅ API failures don't crash pipeline
- ✅ Results exported correctly

## 7. Risk Mitigation

### Risk 1: Breaking Existing Functionality
**Mitigation:** Run both pipelines in parallel initially

### Risk 2: Performance Impact
**Mitigation:** Profile and optimize critical paths

### Risk 3: Learning Curve
**Mitigation:** Comprehensive documentation and examples

## 8. Next Steps

1. Review and approve this plan
2. Set up development branch
3. Begin Phase 1 implementation
4. Daily progress reviews
5. Testing at each phase completion

This hexagonal architecture approach will make the codebase more maintainable, testable, and flexible while fixing all critical issues identified in the analysis.