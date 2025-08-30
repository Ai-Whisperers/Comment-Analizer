"""
AI Overseer Module - Final Quality Control and Enhancement Layer
Acts as the final AI-powered validation and enhancement layer for analysis results
"""

import logging
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np
from openai import OpenAI

from src.config import Config
from src.api.api_client import get_global_client
from src.api.cache_manager import CacheManager
from src.utils.exceptions import APIConnectionError, AnalysisProcessingError

logger = logging.getLogger(__name__)


@dataclass
class OverseerValidation:
    """Results from AI Overseer validation"""
    is_valid: bool = True
    confidence_score: float = 0.0
    issues_found: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    enhanced_insights: List[Dict[str, Any]] = field(default_factory=list)
    quality_metrics: Dict[str, float] = field(default_factory=dict)
    corrected_data: Optional[Dict] = None
    validation_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class AIAnalysisOverseer:
    """
    AI Overseer that reviews and enhances analysis results
    
    Key Responsibilities:
    1. Validate sentiment analysis accuracy
    2. Check for logical inconsistencies
    3. Detect missed patterns or insights
    4. Enhance recommendations with AI insights
    5. Quality assurance of final output
    """
    
    def __init__(self, use_cache: bool = True, strict_mode: bool = False, language: str = 'es'):
        """
        Initialize AI Overseer
        
        Args:
            use_cache: Whether to cache validation results
            strict_mode: If True, blocks low-confidence results
            language: Output language ('es' for Spanish, 'en' for English)
        """
        self.ai_available = bool(Config.OPENAI_API_KEY)
        self.strict_mode = strict_mode
        self.use_cache = use_cache
        self.language = language
        self.cache_manager = CacheManager() if use_cache else None
        
        if self.ai_available:
            try:
                self.client = get_global_client()
                self.model = "gpt-4o-mini"
                logger.info("AI Overseer initialized with OpenAI")
            except Exception as e:
                logger.warning(f"AI Overseer fallback mode: {e}")
                self.ai_available = False
        else:
            logger.warning("AI Overseer running without AI - rule-based validation only")
    
    def oversee_analysis(self, analysis_results: Dict) -> Tuple[Dict, OverseerValidation]:
        """
        Main oversight function - validates and enhances analysis results
        
        Args:
            analysis_results: Complete analysis results from the pipeline
            
        Returns:
            Tuple of (enhanced_results, validation_report)
        """
        validation = OverseerValidation()
        enhanced_results = analysis_results.copy()
        
        try:
            # Step 1: Validate data consistency
            validation = self._validate_data_consistency(analysis_results, validation)
            
            # Step 2: Check sentiment analysis quality
            validation = self._validate_sentiment_analysis(analysis_results, validation)
            
            # Step 3: Verify statistical accuracy
            validation = self._validate_statistics(analysis_results, validation)
            
            # Step 4: AI-powered deep validation (if available)
            if self.ai_available:
                validation, enhanced_results = self._ai_deep_validation(
                    analysis_results, validation, enhanced_results
                )
            
            # Step 5: Generate quality score
            validation.quality_metrics = self._calculate_quality_metrics(
                analysis_results, validation
            )
            
            # Step 6: Apply corrections if needed
            if validation.corrected_data:
                enhanced_results.update(validation.corrected_data)
            
            # Step 7: Add overseer metadata
            enhanced_results['overseer_validation'] = {
                'validated': True,
                'confidence': validation.confidence_score,
                'quality_score': validation.quality_metrics.get('overall', 0),
                'timestamp': validation.validation_timestamp,
                'ai_enhanced': self.ai_available
            }
            
            # Block if strict mode and confidence too low
            if self.strict_mode and validation.confidence_score < 0.7:
                logger.warning(f"Overseer blocked results: confidence {validation.confidence_score:.2f} < 0.7")
                validation.is_valid = False
                validation.issues_found.append("Results blocked due to low confidence score")
            
        except Exception as e:
            logger.error(f"Overseer validation error: {e}")
            validation.issues_found.append(f"Validation error: {str(e)}")
            validation.confidence_score = 0.5
        
        return enhanced_results, validation
    
    def _validate_data_consistency(self, results: Dict, validation: OverseerValidation) -> OverseerValidation:
        """Check for data consistency issues"""
        issues = []
        
        # Check totals match
        total = results.get('total', 0)
        positive = results.get('positive_count', 0)
        neutral = results.get('neutral_count', 0)
        negative = results.get('negative_count', 0)
        
        if positive + neutral + negative != total:
            if self.language == 'es':
                issues.append(f"Los conteos de sentimiento no suman al total: {positive}+{neutral}+{negative} != {total}")
            else:
                issues.append(f"Sentiment counts don't sum to total: {positive}+{neutral}+{negative} != {total}")
        
        # Check percentages
        pos_pct = results.get('positive_pct', 0)
        expected_pos_pct = (positive / total * 100) if total > 0 else 0
        
        if abs(pos_pct - expected_pos_pct) > 1:
            if self.language == 'es':
                issues.append(f"Discrepancia en porcentajes: reportado {pos_pct}% vs calculado {expected_pos_pct:.1f}%")
            else:
                issues.append(f"Percentage mismatch: reported {pos_pct}% vs calculated {expected_pos_pct:.1f}%")
        
        # Check for missing required fields
        required_fields = ['total', 'comments', 'sentiments', 'analysis_date']
        for field in required_fields:
            if field not in results or results[field] is None:
                if self.language == 'es':
                    issues.append(f"Campo requerido faltante: {field}")
                else:
                    issues.append(f"Missing required field: {field}")
        
        validation.issues_found.extend(issues)
        
        # Calculate consistency score
        consistency_score = max(0, 1 - (len(issues) * 0.2))
        validation.confidence_score = consistency_score
        
        return validation
    
    def _validate_sentiment_analysis(self, results: Dict, validation: OverseerValidation) -> OverseerValidation:
        """Validate sentiment analysis quality"""
        
        comments = results.get('comments', [])
        sentiments = results.get('sentiments', [])
        
        if len(comments) != len(sentiments):
            validation.issues_found.append(f"Comments/sentiments mismatch: {len(comments)} != {len(sentiments)}")
            return validation
        
        # Sample validation of sentiment logic
        suspicious_patterns = []
        
        for i, (comment, sentiment) in enumerate(zip(comments[:20], sentiments[:20])):  # Check first 20
            comment_lower = str(comment).lower()
            
            # Check obvious mismatches
            if 'excelente' in comment_lower and sentiment == 'negativo':
                if self.language == 'es':
                    suspicious_patterns.append(f"Comentario {i}: Contiene 'excelente' pero marcado negativo")
                else:
                    suspicious_patterns.append(f"Comment {i}: Contains 'excelente' but marked negative")
            elif 'pésimo' in comment_lower and sentiment == 'positivo':
                if self.language == 'es':
                    suspicious_patterns.append(f"Comentario {i}: Contiene 'pésimo' pero marcado positivo")
                else:
                    suspicious_patterns.append(f"Comment {i}: Contains 'pésimo' but marked positive")
            elif 'no funciona' in comment_lower and sentiment == 'positivo':
                if self.language == 'es':
                    suspicious_patterns.append(f"Comentario {i}: Contiene 'no funciona' pero marcado positivo")
                else:
                    suspicious_patterns.append(f"Comment {i}: Contains 'no funciona' but marked positive")
        
        if suspicious_patterns:
            validation.issues_found.extend(suspicious_patterns[:3])  # Report top 3
            if self.language == 'es':
                validation.suggestions.append("Revisar reglas de análisis de sentimiento para mayor precisión")
            else:
                validation.suggestions.append("Review sentiment analysis rules for accuracy")
        
        # Update confidence based on suspicious patterns
        suspicion_rate = len(suspicious_patterns) / min(20, len(comments)) if comments else 0
        validation.confidence_score *= (1 - suspicion_rate * 0.5)
        
        return validation
    
    def _validate_statistics(self, results: Dict, validation: OverseerValidation) -> OverseerValidation:
        """Validate statistical calculations"""
        
        # Check NPS calculation if present
        if 'nps' in results:
            nps_data = results['nps']
            promoters = nps_data.get('promoters', 0)
            detractors = nps_data.get('detractors', 0)
            total = results.get('total', 1)
            
            expected_nps = ((promoters - detractors) / total * 100) if total > 0 else 0
            reported_nps = nps_data.get('score', 0)
            
            if abs(expected_nps - reported_nps) > 1:
                validation.issues_found.append(
                    f"NPS calculation error: expected {expected_nps:.1f}, got {reported_nps}"
                )
        
        # Check theme counts
        if 'theme_counts' in results:
            theme_counts = results['theme_counts']
            if all(count == 0 for count in theme_counts.values()) and results.get('total', 0) > 10:
                validation.suggestions.append("No themes detected - consider reviewing theme detection logic")
        
        return validation
    
    def _ai_deep_validation(self, results: Dict, validation: OverseerValidation, 
                           enhanced_results: Dict) -> Tuple[OverseerValidation, Dict]:
        """Use AI for deep validation and enhancement"""
        
        if not self.ai_available:
            return validation, enhanced_results
        
        try:
            # Prepare summary for AI review
            summary = self._prepare_analysis_summary(results)
            
            # Create AI validation prompt in appropriate language
            if self.language == 'es':
                prompt = f"""
                Eres un Supervisor de Calidad de IA revisando resultados de análisis de sentimientos.
                
                Resumen del Análisis:
                {json.dumps(summary, indent=2, ensure_ascii=False)}
                
                Por favor valida:
                1. ¿Son razonables las distribuciones de sentimiento?
                2. ¿Los temas coinciden con el patrón de sentimiento?
                3. ¿Hay inconsistencias lógicas?
                4. ¿Qué insights clave podrían faltar?
                
                Responde en JSON en ESPAÑOL:
                {{
                    "confidence_score": 0.0-1.0,
                    "issues": ["lista de problemas encontrados en español"],
                    "insights": ["insights adicionales en español"],
                    "recommendations": ["recomendaciones accionables en español"],
                    "quality_assessment": "evaluación breve de calidad en español"
                }}
                """
            else:
                prompt = f"""
                You are an AI Quality Overseer reviewing sentiment analysis results.
                
                Analysis Summary:
                {json.dumps(summary, indent=2, ensure_ascii=False)}
                
                Please validate:
                1. Are the sentiment distributions reasonable?
                2. Do the themes match the sentiment pattern?
                3. Are there any logical inconsistencies?
                4. What key insights might be missing?
                
                Respond in JSON format:
                {{
                    "confidence_score": 0.0-1.0,
                    "issues": ["list of issues found"],
                    "insights": ["additional insights"],
                    "recommendations": ["actionable recommendations"],
                    "quality_assessment": "brief quality assessment"
                }}
                """
            
            # Use robust client with timeout handling
            try:
                # Try to use the OpenAI client directly
                from openai import OpenAI
                client = OpenAI(api_key=Config.OPENAI_API_KEY)
                completion = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=500
                )
                response = completion.choices[0].message.content
            except Exception as api_err:
                logger.warning(f"Direct OpenAI call failed: {api_err}")
                response = None
            
            if response:
                try:
                    # Try to parse JSON response
                    ai_validation = json.loads(response)
                except json.JSONDecodeError:
                    # If JSON parsing fails, extract key information manually
                    logger.warning("AI response not in expected JSON format, extracting manually")
                    ai_validation = {
                        'confidence_score': 0.85,
                        'issues': [],
                        'insights': [response[:200]] if response else [],
                        'recommendations': [],
                        'quality_assessment': 'AI analysis completed'
                    }
                
                # Update validation with AI insights
                validation.confidence_score = (validation.confidence_score + ai_validation['confidence_score']) / 2
                validation.issues_found.extend(ai_validation.get('issues', []))
                validation.suggestions.extend(ai_validation.get('recommendations', []))
                
                # Add enhanced insights
                for insight in ai_validation.get('insights', []):
                    validation.enhanced_insights.append({
                        'type': 'ai_insight',
                        'content': insight,
                        'confidence': ai_validation['confidence_score']
                    })
                
                # Add to enhanced results
                enhanced_results['ai_insights'] = ai_validation.get('insights', [])
                enhanced_results['ai_quality_assessment'] = ai_validation.get('quality_assessment', '')
                
                logger.info(f"AI validation complete: confidence {ai_validation['confidence_score']:.2f}")
        
        except Exception as e:
            logger.error(f"AI deep validation failed: {e}")
            validation.suggestions.append("Consider manual review - AI validation unavailable")
        
        return validation, enhanced_results
    
    def _calculate_quality_metrics(self, results: Dict, validation: OverseerValidation) -> Dict[str, float]:
        """Calculate comprehensive quality metrics"""
        
        metrics = {}
        
        # Data completeness score
        required_fields = ['total', 'comments', 'sentiments', 'theme_counts', 'analysis_date']
        present_fields = sum(1 for f in required_fields if f in results and results[f])
        metrics['completeness'] = present_fields / len(required_fields)
        
        # Data quality score
        total = results.get('total', 0)
        duplicates = results.get('duplicates_removed', 0)
        metrics['data_quality'] = 1 - (duplicates / (total + duplicates)) if (total + duplicates) > 0 else 1
        
        # Analysis depth score
        has_themes = bool(results.get('theme_counts') and any(results['theme_counts'].values()))
        has_nps = 'nps' in results
        has_frequencies = 'comment_frequencies' in results
        
        depth_score = sum([has_themes, has_nps, has_frequencies]) / 3
        metrics['analysis_depth'] = depth_score
        
        # Confidence score from validation
        metrics['validation_confidence'] = validation.confidence_score
        
        # Overall quality score (weighted average)
        metrics['overall'] = (
            metrics['completeness'] * 0.25 +
            metrics['data_quality'] * 0.25 +
            metrics['analysis_depth'] * 0.25 +
            metrics['validation_confidence'] * 0.25
        )
        
        return metrics
    
    def _prepare_analysis_summary(self, results: Dict) -> Dict:
        """Prepare a summary for AI review"""
        
        # Sample comments for context
        sample_comments = results.get('comments', [])[:5]
        sample_sentiments = results.get('sentiments', [])[:5]
        
        summary = {
            'total_comments': results.get('total', 0),
            'sentiment_distribution': {
                'positive': f"{results.get('positive_pct', 0)}%",
                'neutral': f"{results.get('neutral_pct', 0)}%",
                'negative': f"{results.get('negative_pct', 0)}%"
            },
            'top_themes': dict(list(results.get('theme_counts', {}).items())[:3]),
            'sample_analysis': [
                {'comment': c[:100], 'sentiment': s} 
                for c, s in zip(sample_comments, sample_sentiments)
            ],
            'duplicates_removed': results.get('duplicates_removed', 0),
            'analysis_method': results.get('analysis_method', 'UNKNOWN')
        }
        
        return summary
    
    def _process_insight_content(self, content: str) -> str:
        """Extract clean content from potentially JSON-formatted insight"""
        if not isinstance(content, str):
            return str(content)
        
        # Remove JSON formatting if present
        if content.startswith('```json'):
            content = content.replace('```json', '').replace('```', '').strip()
        
        # Try to parse JSON and extract meaningful text
        if content.startswith('{'):
            try:
                parsed = json.loads(content)
                return self._extract_meaningful_json_content(parsed)
            except (json.JSONDecodeError, TypeError):
                pass
        
        # If not JSON or parsing fails, clean up the string
        content = content.replace('\\n', ' ').replace('\\t', ' ')
        if len(content) > 200:
            content = content[:200] + "..."
        
        return content
    
    def _extract_meaningful_json_content(self, parsed: dict) -> str:
        """Extract the most relevant information from parsed JSON"""
        # Try specific keys first
        for key in ['issues', 'insights', 'quality_assessment']:
            if key in parsed and parsed[key]:
                value = parsed[key]
                if isinstance(value, list) and value:
                    return str(value[0])
                else:
                    return str(value)
        
        # Fallback to first meaningful value
        for key, value in parsed.items():
            if key != 'confidence_score' and value and str(value).strip():
                if isinstance(value, (list, dict)):
                    if isinstance(value, list) and value:
                        return str(value[0])
                    else:
                        return str(value)
                else:
                    return str(value)
        
        return str(parsed)

    def generate_oversight_report(self, validation: OverseerValidation) -> str:
        """Generate human-readable oversight report"""
        
        report = []
        report.append("=" * 50)
        
        if self.language == 'es':
            report.append("REPORTE DE VALIDACIÓN DEL SUPERVISOR IA")
            report.append("=" * 50)
            report.append(f"Fecha/Hora: {validation.validation_timestamp}")
            report.append(f"Confianza General: {validation.confidence_score:.1%}")
            report.append(f"Estado de Validación: {'APROBADO' if validation.is_valid else 'RECHAZADO'}")
            
            if validation.quality_metrics:
                report.append("\nMétricas de Calidad:")
                metric_names = {
                    'completeness': 'Completitud',
                    'data_quality': 'Calidad de Datos',
                    'analysis_depth': 'Profundidad de Análisis',
                    'validation_confidence': 'Confianza de Validación',
                    'overall': 'Calidad General'
                }
                for metric, score in validation.quality_metrics.items():
                    metric_name = metric_names.get(metric, metric)
                    report.append(f"  - {metric_name}: {score:.1%}")
            
            if validation.issues_found:
                report.append(f"\nProblemas Encontrados ({len(validation.issues_found)}):")
                for issue in validation.issues_found[:5]:
                    report.append(f"  ⚠️ {issue}")
            
            if validation.suggestions:
                report.append(f"\nSugerencias ({len(validation.suggestions)}):")
                for suggestion in validation.suggestions[:5]:
                    report.append(f"  💡 {suggestion}")
            
            if validation.enhanced_insights:
                report.append(f"\nInsights de IA ({len(validation.enhanced_insights)}):")
                for insight in validation.enhanced_insights[:3]:
                    content = self._process_insight_content(insight['content'])
                    report.append(f"  🤖 {content}")
        else:
            report.append("AI OVERSEER VALIDATION REPORT")
            report.append("=" * 50)
            report.append(f"Timestamp: {validation.validation_timestamp}")
            report.append(f"Overall Confidence: {validation.confidence_score:.1%}")
            report.append(f"Validation Status: {'PASSED' if validation.is_valid else 'FAILED'}")
            
            if validation.quality_metrics:
                report.append("\nQuality Metrics:")
                for metric, score in validation.quality_metrics.items():
                    report.append(f"  - {metric}: {score:.1%}")
            
            if validation.issues_found:
                report.append(f"\nIssues Found ({len(validation.issues_found)}):")
                for issue in validation.issues_found[:5]:
                    report.append(f"  ⚠️ {issue}")
            
            if validation.suggestions:
                report.append(f"\nSuggestions ({len(validation.suggestions)}):")
                for suggestion in validation.suggestions[:5]:
                    report.append(f"  💡 {suggestion}")
            
            if validation.enhanced_insights:
                report.append(f"\nAI Insights ({len(validation.enhanced_insights)}):")
                for insight in validation.enhanced_insights[:3]:
                    content = self._process_insight_content(insight['content'])
                    report.append(f"  🤖 {content}")
        
        report.append("=" * 50)
        
        return "\n".join(report)


# Integration helper for easy pipeline integration
def apply_ai_oversight(analysis_results: Dict, strict: bool = False, language: str = 'es') -> Dict:
    """
    Easy integration function to add AI oversight to existing pipeline
    
    Args:
        analysis_results: Results from current analysis pipeline
        strict: Whether to block low-confidence results
        language: Output language ('es' for Spanish, 'en' for English)
        
    Returns:
        Enhanced analysis results with oversight validation
    """
    try:
        overseer = AIAnalysisOverseer(use_cache=True, strict_mode=strict, language=language)
        enhanced_results, validation = overseer.oversee_analysis(analysis_results)
        
        # Log the report
        report = overseer.generate_oversight_report(validation)
        logger.info(f"Oversight Report:\n{report}")
        
        # Add report to results
        enhanced_results['oversight_report'] = report
        
        return enhanced_results
        
    except Exception as e:
        logger.error(f"AI Oversight failed: {e}")
        # Return original results on failure
        analysis_results['oversight_report'] = f"Oversight unavailable: {str(e)}"
        return analysis_results


if __name__ == "__main__":
    # Test the overseer with sample data
    sample_results = {
        'total': 100,
        'positive_count': 45,
        'neutral_count': 30,
        'negative_count': 25,
        'positive_pct': 45.0,
        'neutral_pct': 30.0,
        'negative_pct': 25.0,
        'comments': ["Excelente servicio", "Muy malo", "Regular"],
        'sentiments': ["positivo", "negativo", "neutral"],
        'theme_counts': {'velocidad': 10, 'precio': 5},
        'analysis_date': datetime.now().isoformat(),
        'duplicates_removed': 5
    }
    
    # Run oversight
    enhanced = apply_ai_oversight(sample_results, strict=False)
    
    # Print report
    if 'oversight_report' in enhanced:
        print(enhanced['oversight_report'])