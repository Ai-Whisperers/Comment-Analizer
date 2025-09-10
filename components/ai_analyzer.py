"""
AI Analysis Component - Streamlit Native Caching
Optimized AI processing using Streamlit's native performance features
"""

import streamlit as st
import openai
import json
import time
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


@st.cache_resource
def get_openai_client(_config_hash: str) -> openai.OpenAI:
    """
    Get cached OpenAI client instance using Streamlit native resource caching
    
    Cache Strategy:
    - Global resource cached across all sessions
    - Thread-safe by Streamlit design
    - Automatic lifecycle management
    """
    config = st.session_state.config
    client = openai.OpenAI(api_key=config['openai_api_key'])
    logger.info(f"🤖 OpenAI client cached for model: {config.get('openai_modelo', 'default')}")
    return client


@st.cache_data(ttl=1800, show_spinner="Analizando con IA...")
def analyze_comments_optimized(
    comments_tuple: Tuple[str, ...],  # Tuple is hashable for Streamlit caching
    model_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Optimized AI analysis with Streamlit native caching
    
    Key Optimizations vs Current System:
    1. Streamlit native caching (vs 150-line custom implementation)
    2. Larger batch sizes (50-80 vs 20 comments)
    3. Minimal rate limiting (0.2s vs 3-5s between calls)
    4. Direct OpenAI integration (vs complex abstraction layers)
    
    Cache Strategy:
    - TTL: 30 minutes (reasonable for AI analysis results)
    - Key: Automatic based on comments content + model config
    - Benefit: Same content analysis is instant
    """
    comments = list(comments_tuple)
    client = get_openai_client(hash(str(model_config)))
    
    # Determine optimal batch size based on model capabilities
    batch_size = get_optimal_batch_size(model_config.get('openai_modelo', 'gpt-4o-mini'))
    
    logger.info(f"🚀 Starting optimized analysis: {len(comments)} comments in batches of {batch_size}")
    
    # Create optimized batches
    batches = [comments[i:i + batch_size] 
              for i in range(0, len(comments), batch_size)]
    
    logger.info(f"📦 Created {len(batches)} optimized batches (vs {len(comments)//20} with old system)")
    
    # Process batches with minimal delay
    all_results = []
    start_time = time.time()
    
    for i, batch in enumerate(batches):
        logger.info(f"🔄 Processing optimized batch {i+1}/{len(batches)} ({len(batch)} comments)")
        
        # Update progress in session state for fragment display
        if 'analysis_progress' in st.session_state:
            st.session_state.analysis_progress.update({
                'current_batch': i + 1,
                'total_batches': len(batches),
                'elapsed_time': time.time() - start_time
            })
        
        # Optimized rate limiting (0.2s vs 3-5s)
        if i > 0:
            time.sleep(0.2)  # Minimal delay for OpenAI API respect
        
        # Direct AI processing with optimized settings
        try:
            batch_result = process_single_batch(batch, client, model_config)
            all_results.append(batch_result)
            logger.info(f"✅ Batch {i+1} completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Batch {i+1} failed: {str(e)}")
            # Simple retry with minimal delay
            time.sleep(0.5)
            try:
                batch_result = process_single_batch(batch, client, model_config)
                all_results.append(batch_result)
                logger.info(f"✅ Batch {i+1} retry successful")
            except Exception as retry_error:
                logger.error(f"❌ Batch {i+1} retry failed: {str(retry_error)}")
                # Create fallback result for failed batch
                fallback_result = create_fallback_batch_result(batch)
                all_results.append(fallback_result)
    
    # Aggregate results efficiently
    final_result = aggregate_analysis_results(all_results, comments)
    
    total_time = time.time() - start_time
    logger.info(f"🎉 Optimized analysis completed in {total_time:.2f}s for {len(comments)} comments")
    
    return final_result


def get_optimal_batch_size(model: str) -> int:
    """
    Determine optimal batch size based on model token limits and cost
    
    Optimization Strategy:
    - Cheaper models: Larger batches (more cost efficient)
    - Expensive models: Moderate batches (balance cost vs speed)
    - Based on token limits and processing efficiency
    """
    batch_sizes = {
        'gpt-4o-mini': 80,  # 16K context, cheap, maximize batch size
        'gpt-4o': 60,       # 128K context, balanced cost
        'gpt-4': 40,        # 128K context, expensive, moderate batches
        'gpt-4-turbo': 60   # 128K context, balanced
    }
    
    size = batch_sizes.get(model, 50)
    logger.debug(f"📊 Optimal batch size for {model}: {size} comments")
    return size


def process_single_batch(batch: List[str], client: openai.OpenAI, 
                        config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process single batch with optimized prompt and settings
    Streamlined for Streamlit caching wrapper
    """
    # Create optimized prompt (shorter and more efficient)
    prompt = create_optimized_prompt(batch)
    
    # Calculate optimal tokens for this batch size
    max_tokens = calculate_dynamic_tokens(len(batch), config.get('openai_modelo', 'gpt-4o-mini'))
    
    # Direct API call with optimized settings
    response = client.chat.completions.create(
        model=config.get('openai_modelo', 'gpt-4o-mini'),
        messages=[
            {
                "role": "system", 
                "content": "Expert comment analyst for telecommunications. Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.0,  # Deterministic results
        max_tokens=max_tokens,
        response_format={"type": "json_object"}
    )
    
    return parse_ai_response(response, batch)


def create_optimized_prompt(batch: List[str]) -> str:
    """Create optimized prompt for better AI performance"""
    comments_text = '\n'.join([
        f"{i+1}. {comment[:400]}" + ("..." if len(comment) > 400 else "")
        for i, comment in enumerate(batch)
    ])
    
    # Streamlined prompt for faster processing
    return f"""Analyze {len(batch)} telecom customer comments. Return JSON only.

COMMENTS:
{comments_text}

FORMAT:
{{
  "summary": {{"trend": "positive|neutral|negative", "confidence": 0.85}},
  "comments": [
    {{"id": 1, "sentiment": "positive", "confidence": 0.9, "theme": "service", "emotion": "satisfaction", "urgency": "low"}}
  ],
  "stats": {{"positive": 0, "neutral": 0, "negative": 0, "total": {len(batch)}}}
}}

Analyze exactly {len(batch)} comments (numbered 1-{len(batch)}). Return exactly {len(batch)} items in "comments" array."""


def calculate_dynamic_tokens(num_comments: int, model: str) -> int:
    """Calculate optimal token allocation for batch size and model"""
    base_tokens = 800  # Reduced from 1200 (more efficient prompt)
    tokens_per_comment = 60  # Reduced from 80 (optimized format)
    
    calculated = base_tokens + (num_comments * tokens_per_comment)
    
    # Model-specific limits
    model_limits = {
        'gpt-4o-mini': 4096,  # Conservative for speed
        'gpt-4o': 8192,       # Balanced
        'gpt-4': 8192,        # Balanced 
        'gpt-4-turbo': 8192   # Balanced
    }
    
    limit = model_limits.get(model, 4096)
    final_tokens = min(calculated, limit)
    
    logger.debug(f"🔢 Tokens for {num_comments} comments: {final_tokens}")
    return final_tokens


def parse_ai_response(response, batch: List[str]) -> Dict[str, Any]:
    """Parse OpenAI response with error handling"""
    try:
        content = response.choices[0].message.content
        result = json.loads(content)
        
        # Validate response structure
        if 'comments' not in result or len(result['comments']) != len(batch):
            logger.warning(f"⚠️ AI returned {len(result.get('comments', []))} results for {len(batch)} comments")
        
        # Add metadata
        result['batch_size'] = len(batch)
        result['model_used'] = response.model if hasattr(response, 'model') else 'unknown'
        result['processing_time'] = getattr(response, 'processing_time', 0)
        
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON parse error: {str(e)}")
        return create_fallback_batch_result(batch)
    except Exception as e:
        logger.error(f"❌ Response parsing error: {str(e)}")
        return create_fallback_batch_result(batch)


def create_fallback_batch_result(batch: List[str]) -> Dict[str, Any]:
    """Create fallback result for failed AI processing"""
    return {
        'summary': {'trend': 'neutral', 'confidence': 0.3},
        'comments': [
            {
                'id': i + 1,
                'sentiment': 'neutral',
                'confidence': 0.3,
                'theme': 'unknown',
                'emotion': 'neutral',
                'urgency': 'low'
            }
            for i in range(len(batch))
        ],
        'stats': {'positive': 0, 'neutral': len(batch), 'negative': 0, 'total': len(batch)},
        'batch_size': len(batch),
        'fallback': True,
        'error': True
    }


def aggregate_analysis_results(batch_results: List[Dict[str, Any]], 
                              original_comments: List[str]) -> Dict[str, Any]:
    """
    Aggregate multiple batch results into final analysis
    Optimized for Streamlit display components
    """
    if not batch_results:
        return create_fallback_batch_result(original_comments)
    
    # Aggregate sentiment statistics
    total_positive = sum(r.get('stats', {}).get('positive', 0) for r in batch_results)
    total_neutral = sum(r.get('stats', {}).get('neutral', 0) for r in batch_results)
    total_negative = sum(r.get('stats', {}).get('negative', 0) for r in batch_results)
    
    # Aggregate all comments
    all_comment_analyses = []
    for result in batch_results:
        all_comment_analyses.extend(result.get('comments', []))
    
    # Calculate overall confidence
    confidences = [c.get('confidence', 0.5) for c in all_comment_analyses]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5
    
    # Determine overall trend
    if total_positive > total_negative and total_positive > total_neutral:
        overall_trend = 'positive'
    elif total_negative > total_positive and total_negative > total_neutral:
        overall_trend = 'negative'  
    else:
        overall_trend = 'neutral'
    
    # Create aggregated result optimized for Streamlit charts
    aggregated_result = {
        'summary': {
            'trend': overall_trend,
            'confidence': avg_confidence,
            'total_comments': len(original_comments)
        },
        'distribution': {
            'sentiments': {
                'positivo': total_positive,
                'neutral': total_neutral, 
                'negativo': total_negative
            }
        },
        'comments': all_comment_analyses,
        'metadata': {
            'total_batches_processed': len(batch_results),
            'processing_method': 'streamlit_optimized',
            'cache_enabled': True
        }
    }
    
    logger.info(f"📊 Aggregated {len(batch_results)} batches into final result")
    return aggregated_result