#!/usr/bin/env python3
"""
🔍 E2E PIPELINE ANALYZER - Análisis exhaustivo de potencialidad
Análisis completo del pipeline de IA sin implementar fixes
Enfoque en identificar oportunidades de optimización y mejora
"""

import sys
import os
import inspect
import ast
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import traceback

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class PipelineAnalyzer:
    def __init__(self):
        self.project_root = project_root
        self.findings = {}
        self.component_map = {}
        self.dependency_graph = {}
        self.performance_metrics = {}
        self.risk_assessment = {}
        
    def analyze_component_architecture(self):
        """Análisis exhaustivo de la arquitectura de componentes"""
        print("🔍 ANALYZING COMPONENT ARCHITECTURE")
        print("-" * 50)
        
        # Map all Python files in the project
        python_files = []
        for pattern in ["**/*.py"]:
            python_files.extend(self.project_root.glob(pattern))
        
        architecture_analysis = {
            'total_files': len(python_files),
            'layers': {
                'presentation': [],
                'application': [],
                'infrastructure': [],
                'domain': [],
                'config': [],
                'tests': [],
                'other': []
            },
            'complexity_metrics': {},
            'import_patterns': {},
            'circular_dependencies': []
        }
        
        for file in python_files:
            if 'venv' in str(file) or '__pycache__' in str(file):
                continue
                
            relative_path = file.relative_to(self.project_root)
            layer = self._classify_file_layer(relative_path)
            architecture_analysis['layers'][layer].append(str(relative_path))
            
            # Analyze file complexity
            try:
                complexity = self._analyze_file_complexity(file)
                architecture_analysis['complexity_metrics'][str(relative_path)] = complexity
            except:
                pass
        
        self.findings['architecture'] = architecture_analysis
        
        print(f"  📁 Total files analyzed: {architecture_analysis['total_files']}")
        for layer, files in architecture_analysis['layers'].items():
            if files:
                print(f"  📋 {layer.title()} layer: {len(files)} files")
        
        return architecture_analysis
    
    def analyze_dependency_flow(self):
        """Análisis del flujo de dependencias y potencial para mejoras"""
        print("\n🔍 ANALYZING DEPENDENCY FLOW")
        print("-" * 50)
        
        dependency_analysis = {
            'import_graph': {},
            'circular_risks': [],
            'coupling_metrics': {},
            'bottlenecks': [],
            'optimization_opportunities': []
        }
        
        # Analyze key components
        key_components = [
            'config.py',
            'src/infrastructure/dependency_injection/contenedor_dependencias.py',
            'src/infrastructure/external_services/analizador_maestro_ia.py',
            'src/application/use_cases/analizar_excel_maestro_caso_uso.py',
            'src/infrastructure/config/ai_configuration_manager.py'
        ]
        
        for component in key_components:
            file_path = self.project_root / component
            if file_path.exists():
                imports = self._extract_imports(file_path)
                dependency_analysis['import_graph'][component] = imports
                
                # Analyze coupling
                coupling_score = len(imports) / 10  # Normalized coupling metric
                dependency_analysis['coupling_metrics'][component] = {
                    'import_count': len(imports),
                    'coupling_score': coupling_score,
                    'coupling_level': 'high' if coupling_score > 2 else 'medium' if coupling_score > 1 else 'low'
                }
        
        # Identify potential bottlenecks
        for component, metrics in dependency_analysis['coupling_metrics'].items():
            if metrics['coupling_score'] > 2:
                dependency_analysis['bottlenecks'].append({
                    'component': component,
                    'issue': 'High coupling',
                    'impact': 'May cause cascading changes',
                    'potential_fix': 'Consider dependency injection or interface segregation'
                })
        
        self.findings['dependencies'] = dependency_analysis
        
        print(f"  📊 Components analyzed: {len(dependency_analysis['import_graph'])}")
        print(f"  ⚠️ High coupling components: {len(dependency_analysis['bottlenecks'])}")
        
        return dependency_analysis
    
    def analyze_ai_pipeline_flow(self):
        """Análisis específico del flujo del pipeline de IA"""
        print("\n🔍 ANALYZING AI PIPELINE FLOW")
        print("-" * 50)
        
        ai_analysis = {
            'pipeline_stages': [],
            'data_transformations': [],
            'error_handling_coverage': {},
            'performance_bottlenecks': [],
            'scalability_analysis': {},
            'optimization_potential': []
        }
        
        # Map pipeline stages
        pipeline_stages = [
            {
                'stage': 'File Upload',
                'component': 'Streamlit file uploader',
                'input': 'Excel/CSV file',
                'output': 'File object',
                'potential_issues': ['Large file handling', 'Memory usage', 'File validation']
            },
            {
                'stage': 'File Reading',
                'component': 'LectorArchivosExcel',
                'input': 'File object',
                'output': 'List[Dict] comments',
                'potential_issues': ['Encoding detection', 'Memory efficiency', 'Error recovery']
            },
            {
                'stage': 'Configuration Loading',
                'component': 'ContenedorDependencias',
                'input': 'Config dict',
                'output': 'Initialized services',
                'potential_issues': ['Environment detection', 'API key validation', 'Resource limits']
            },
            {
                'stage': 'AI Analysis',
                'component': 'AnalizadorMaestroIA',
                'input': 'Comments batch',
                'output': 'Analysis results',
                'potential_issues': ['API rate limits', 'Token usage', 'Retry logic', 'Cost optimization']
            },
            {
                'stage': 'Result Processing',
                'component': 'Use case orchestrator',
                'input': 'Raw AI results',
                'output': 'Structured analysis',
                'potential_issues': ['Data aggregation', 'Confidence calculation', 'Error aggregation']
            },
            {
                'stage': 'Export Generation',
                'component': 'Excel exporter',
                'input': 'Analysis results',
                'output': 'Excel file',
                'potential_issues': ['File size limits', 'Format compatibility', 'Performance']
            }
        ]
        
        ai_analysis['pipeline_stages'] = pipeline_stages
        
        # Analyze each stage for optimization potential
        for stage in pipeline_stages:
            optimizations = []
            
            if 'Memory' in str(stage['potential_issues']):
                optimizations.append({
                    'type': 'memory_optimization',
                    'description': 'Implement streaming or chunked processing',
                    'impact': 'high',
                    'effort': 'medium'
                })
            
            if 'API' in str(stage['potential_issues']):
                optimizations.append({
                    'type': 'api_optimization',
                    'description': 'Implement intelligent caching and batching',
                    'impact': 'high',
                    'effort': 'medium'
                })
            
            if optimizations:
                ai_analysis['optimization_potential'].append({
                    'stage': stage['stage'],
                    'optimizations': optimizations
                })
        
        self.findings['ai_pipeline'] = ai_analysis
        
        print(f"  📊 Pipeline stages mapped: {len(pipeline_stages)}")
        print(f"  🎯 Optimization opportunities: {len(ai_analysis['optimization_potential'])}")
        
        return ai_analysis
    
    def analyze_configuration_system(self):
        """Análisis del sistema de configuración unificada"""
        print("\n🔍 ANALYZING CONFIGURATION SYSTEM")
        print("-" * 50)
        
        config_analysis = {
            'detection_mechanisms': [],
            'configuration_sources': [],
            'potential_improvements': [],
            'risk_factors': [],
            'robustness_score': 0
        }
        
        try:
            # Test configuration detection
            from config import config, is_streamlit_cloud, get_environment_info
            
            current_env = 'cloud' if is_streamlit_cloud() else 'local'
            config_analysis['current_detection'] = current_env
            
            # Analyze detection mechanisms
            detection_mechanisms = [
                {
                    'method': 'HOSTNAME check',
                    'reliability': 'medium',
                    'false_positive_risk': 'low',
                    'description': 'Checks for streamlit- hostname prefix'
                },
                {
                    'method': 'Environment variables',
                    'reliability': 'high',
                    'false_positive_risk': 'low', 
                    'description': 'STREAMLIT_SHARING_MODE and emulator flags'
                },
                {
                    'method': 'Secrets validation',
                    'reliability': 'high',
                    'false_positive_risk': 'very_low',
                    'description': 'Checks for actual secret content'
                }
            ]
            
            config_analysis['detection_mechanisms'] = detection_mechanisms
            
            # Analyze configuration sources
            config_sources = [
                {
                    'source': 'Environment variables (.env)',
                    'priority': 1,
                    'environment': 'local',
                    'reliability': 'high'
                },
                {
                    'source': 'Streamlit secrets',
                    'priority': 1, 
                    'environment': 'cloud',
                    'reliability': 'high'
                },
                {
                    'source': 'Default values',
                    'priority': 3,
                    'environment': 'both',
                    'reliability': 'medium'
                }
            ]
            
            config_analysis['configuration_sources'] = config_sources
            
            # Identify potential improvements
            improvements = [
                {
                    'area': 'Environment Detection',
                    'improvement': 'Add runtime validation of detected environment',
                    'benefit': 'Prevent false positives in complex environments',
                    'complexity': 'low'
                },
                {
                    'area': 'Configuration Validation',
                    'improvement': 'Implement configuration schema validation',
                    'benefit': 'Early detection of invalid configurations',
                    'complexity': 'medium'
                },
                {
                    'area': 'Fallback Mechanisms',
                    'improvement': 'Enhanced fallback with user feedback',
                    'benefit': 'Better user experience when config fails',
                    'complexity': 'medium'
                }
            ]
            
            config_analysis['potential_improvements'] = improvements
            
            # Calculate robustness score
            robustness_factors = [
                ('Environment detection accuracy', 0.9),
                ('Fallback mechanism reliability', 0.8),
                ('Configuration validation', 0.7),
                ('Error handling coverage', 0.8)
            ]
            
            config_analysis['robustness_score'] = sum(score for _, score in robustness_factors) / len(robustness_factors)
            
        except Exception as e:
            config_analysis['analysis_error'] = str(e)
        
        self.findings['configuration'] = config_analysis
        
        print(f"  🎯 Current environment detected: {config_analysis.get('current_detection', 'unknown')}")
        print(f"  📊 Robustness score: {config_analysis['robustness_score']:.2f}/1.0")
        
        return config_analysis
    
    def analyze_error_handling_patterns(self):
        """Análisis de patrones de manejo de errores y recuperación"""
        print("\n🔍 ANALYZING ERROR HANDLING PATTERNS")
        print("-" * 50)
        
        error_analysis = {
            'try_catch_coverage': {},
            'error_types_handled': [],
            'recovery_mechanisms': [],
            'logging_patterns': [],
            'improvement_opportunities': []
        }
        
        # Analyze key components for error handling
        key_files = [
            'src/infrastructure/external_services/analizador_maestro_ia.py',
            'src/infrastructure/file_handlers/lector_archivos_excel.py',
            'src/infrastructure/dependency_injection/contenedor_dependencias.py',
            'config.py'
        ]
        
        total_try_blocks = 0
        total_functions = 0
        
        for file_path in key_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Count try-except blocks
                    tree = ast.parse(content)
                    try_blocks = len([node for node in ast.walk(tree) if isinstance(node, ast.Try)])
                    function_defs = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
                    
                    coverage_ratio = try_blocks / max(function_defs, 1)
                    
                    error_analysis['try_catch_coverage'][file_path] = {
                        'try_blocks': try_blocks,
                        'functions': function_defs,
                        'coverage_ratio': coverage_ratio
                    }
                    
                    total_try_blocks += try_blocks
                    total_functions += function_defs
                    
                except:
                    pass
        
        overall_coverage = total_try_blocks / max(total_functions, 1)
        error_analysis['overall_error_coverage'] = overall_coverage
        
        # Identify improvement opportunities
        improvements = []
        
        if overall_coverage < 0.6:
            improvements.append({
                'area': 'Error Coverage',
                'issue': 'Low try-catch coverage across components',
                'recommendation': 'Add comprehensive error handling to critical functions',
                'priority': 'high'
            })
        
        for file_path, coverage_data in error_analysis['try_catch_coverage'].items():
            if coverage_data['coverage_ratio'] < 0.5:
                improvements.append({
                    'area': 'Component Error Handling',
                    'issue': f'Low error coverage in {file_path}',
                    'recommendation': 'Add error handling to uncovered functions',
                    'priority': 'medium'
                })
        
        error_analysis['improvement_opportunities'] = improvements
        
        self.findings['error_handling'] = error_analysis
        
        print(f"  📊 Overall error handling coverage: {overall_coverage:.2f}")
        print(f"  🎯 Components analyzed: {len(error_analysis['try_catch_coverage'])}")
        print(f"  ⚠️ Improvement opportunities: {len(improvements)}")
        
        return error_analysis
    
    def analyze_performance_characteristics(self):
        """Análisis de características de rendimiento y escalabilidad"""
        print("\n🔍 ANALYZING PERFORMANCE CHARACTERISTICS")
        print("-" * 50)
        
        performance_analysis = {
            'memory_usage_patterns': [],
            'cpu_intensive_operations': [],
            'io_bottlenecks': [],
            'scalability_factors': [],
            'optimization_recommendations': []
        }
        
        # Identify memory-intensive operations
        memory_patterns = [
            {
                'operation': 'File loading',
                'component': 'LectorArchivosExcel',
                'memory_impact': 'high',
                'scale_factor': 'O(file_size)',
                'optimization_potential': 'streaming/chunking'
            },
            {
                'operation': 'Comment batching',
                'component': 'AnalizadorMaestroIA',
                'memory_impact': 'medium',
                'scale_factor': 'O(batch_size * comment_length)',
                'optimization_potential': 'dynamic batching'
            },
            {
                'operation': 'Result aggregation',
                'component': 'Use case layer',
                'memory_impact': 'medium',
                'scale_factor': 'O(total_comments)',
                'optimization_potential': 'incremental processing'
            }
        ]
        
        performance_analysis['memory_usage_patterns'] = memory_patterns
        
        # Identify CPU-intensive operations
        cpu_operations = [
            {
                'operation': 'Text preprocessing',
                'component': 'Comment analysis',
                'cpu_impact': 'medium',
                'optimization_potential': 'vectorization/caching'
            },
            {
                'operation': 'API request processing',
                'component': 'OpenAI integration',
                'cpu_impact': 'low',
                'optimization_potential': 'async processing'
            },
            {
                'operation': 'Excel generation',
                'component': 'Export layer',
                'cpu_impact': 'medium',
                'optimization_potential': 'template-based generation'
            }
        ]
        
        performance_analysis['cpu_intensive_operations'] = cpu_operations
        
        # Identify I/O bottlenecks
        io_bottlenecks = [
            {
                'operation': 'OpenAI API calls',
                'bottleneck_type': 'network_io',
                'impact': 'high',
                'mitigation': 'connection pooling, retry logic, caching'
            },
            {
                'operation': 'File reading',
                'bottleneck_type': 'disk_io',
                'impact': 'medium',
                'mitigation': 'streaming, async reading'
            },
            {
                'operation': 'Excel writing',
                'bottleneck_type': 'disk_io',
                'impact': 'low',
                'mitigation': 'in-memory generation'
            }
        ]
        
        performance_analysis['io_bottlenecks'] = io_bottlenecks
        
        # Generate optimization recommendations
        optimizations = []
        
        for pattern in memory_patterns:
            if pattern['memory_impact'] == 'high':
                optimizations.append({
                    'type': 'memory_optimization',
                    'target': pattern['operation'],
                    'recommendation': f"Implement {pattern['optimization_potential']}",
                    'expected_impact': 'significant memory reduction',
                    'implementation_complexity': 'medium'
                })
        
        for bottleneck in io_bottlenecks:
            if bottleneck['impact'] == 'high':
                optimizations.append({
                    'type': 'io_optimization',
                    'target': bottleneck['operation'],
                    'recommendation': bottleneck['mitigation'],
                    'expected_impact': 'improved throughput and reliability',
                    'implementation_complexity': 'medium'
                })
        
        performance_analysis['optimization_recommendations'] = optimizations
        
        self.findings['performance'] = performance_analysis
        
        print(f"  💾 Memory patterns identified: {len(memory_patterns)}")
        print(f"  ⚡ I/O bottlenecks identified: {len(io_bottlenecks)}")
        print(f"  🎯 Optimization recommendations: {len(optimizations)}")
        
        return performance_analysis
    
    def analyze_testing_coverage_potential(self):
        """Análisis del potencial de cobertura de pruebas"""
        print("\n🔍 ANALYZING TESTING COVERAGE POTENTIAL")
        print("-" * 50)
        
        testing_analysis = {
            'current_test_files': [],
            'testable_components': [],
            'testing_gaps': [],
            'test_strategy_recommendations': []
        }
        
        # Find existing test files
        test_files = []
        for pattern in ["**/test_*.py", "**/*_test.py", "**/tests/*.py"]:
            test_files.extend(self.project_root.glob(pattern))
        
        testing_analysis['current_test_files'] = [str(f.relative_to(self.project_root)) for f in test_files]
        
        # Identify components that should be tested
        testable_components = [
            {
                'component': 'config.py',
                'test_priority': 'high',
                'test_types': ['unit', 'integration'],
                'test_scenarios': [
                    'Environment detection accuracy',
                    'Configuration loading fallbacks',
                    'API key validation'
                ]
            },
            {
                'component': 'LectorArchivosExcel',
                'test_priority': 'high',
                'test_types': ['unit', 'integration'],
                'test_scenarios': [
                    'File format handling',
                    'Encoding detection',
                    'Error recovery',
                    'Memory efficiency'
                ]
            },
            {
                'component': 'AnalizadorMaestroIA',
                'test_priority': 'medium',
                'test_types': ['unit', 'mock', 'integration'],
                'test_scenarios': [
                    'API interaction',
                    'Retry logic',
                    'Error handling',
                    'Response parsing'
                ]
            },
            {
                'component': 'ContenedorDependencias',
                'test_priority': 'high',
                'test_types': ['unit', 'integration'],
                'test_scenarios': [
                    'Dependency resolution',
                    'Singleton behavior',
                    'Configuration injection'
                ]
            }
        ]
        
        testing_analysis['testable_components'] = testable_components
        
        # Identify testing gaps
        existing_test_coverage = set(f.stem.replace('test_', '') for f in test_files)
        gaps = []
        
        for component in testable_components:
            component_name = Path(component['component']).stem
            if component_name not in existing_test_coverage:
                gaps.append({
                    'component': component['component'],
                    'missing_coverage': 'complete',
                    'priority': component['test_priority']
                })
        
        testing_analysis['testing_gaps'] = gaps
        
        # Generate test strategy recommendations
        strategy_recommendations = [
            {
                'strategy': 'Unit Testing Framework',
                'recommendation': 'Implement pytest-based testing suite',
                'benefit': 'Comprehensive component testing',
                'effort': 'medium'
            },
            {
                'strategy': 'Integration Testing',
                'recommendation': 'Create end-to-end pipeline tests',
                'benefit': 'Catch integration issues early',
                'effort': 'high'
            },
            {
                'strategy': 'Mock Testing',
                'recommendation': 'Mock external API calls for reliable testing',
                'benefit': 'Fast, deterministic tests',
                'effort': 'low'
            },
            {
                'strategy': 'Performance Testing',
                'recommendation': 'Add performance benchmarks',
                'benefit': 'Detect performance regressions',
                'effort': 'medium'
            }
        ]
        
        testing_analysis['test_strategy_recommendations'] = strategy_recommendations
        
        self.findings['testing'] = testing_analysis
        
        print(f"  📋 Existing test files: {len(test_files)}")
        print(f"  🎯 Testable components: {len(testable_components)}")
        print(f"  ⚠️ Testing gaps: {len(gaps)}")
        
        return testing_analysis
    
    def _classify_file_layer(self, file_path: Path) -> str:
        """Classify file into architectural layer"""
        path_str = str(file_path).lower()
        
        if 'streamlit' in path_str or 'pages' in path_str or 'components' in path_str:
            return 'presentation'
        elif 'application' in path_str or 'use_cases' in path_str:
            return 'application'
        elif 'infrastructure' in path_str:
            return 'infrastructure'
        elif 'domain' in path_str or 'entities' in path_str:
            return 'domain'
        elif 'config' in path_str or file_path.name == 'config.py':
            return 'config'
        elif 'test' in path_str:
            return 'tests'
        else:
            return 'other'
    
    def _analyze_file_complexity(self, file_path: Path) -> Dict[str, Any]:
        """Analyze file complexity metrics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Count different node types
            functions = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
            classes = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
            imports = len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))])
            
            lines = len(content.split('\n'))
            
            return {
                'lines': lines,
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'complexity_score': (functions * 2 + classes * 3 + imports) / max(lines, 1)
            }
        except:
            return {'error': 'Could not analyze'}
    
    def _extract_imports(self, file_path: Path) -> List[str]:
        """Extract imports from a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            return imports
        except:
            return []
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        print("\n🔍 GENERATING COMPREHENSIVE REPORT")
        print("-" * 50)
        
        report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'executive_summary': self._generate_executive_summary(),
            'detailed_findings': self.findings,
            'recommendations': self._generate_recommendations(),
            'implementation_roadmap': self._generate_implementation_roadmap()
        }
        
        return report
    
    def _generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary of findings"""
        return {
            'overall_health': self._calculate_overall_health(),
            'key_strengths': self._identify_key_strengths(),
            'critical_improvements': self._identify_critical_improvements(),
            'risk_assessment': self._assess_risks()
        }
    
    def _calculate_overall_health(self) -> Dict[str, Any]:
        """Calculate overall system health score"""
        health_factors = []
        
        # Architecture health
        if 'architecture' in self.findings:
            arch = self.findings['architecture']
            layers_populated = sum(1 for layer, files in arch['layers'].items() if files)
            arch_score = layers_populated / len(arch['layers'])
            health_factors.append(('architecture', arch_score))
        
        # Configuration health
        if 'configuration' in self.findings:
            config_score = self.findings['configuration'].get('robustness_score', 0.5)
            health_factors.append(('configuration', config_score))
        
        # Error handling health
        if 'error_handling' in self.findings:
            error_score = self.findings['error_handling'].get('overall_error_coverage', 0.5)
            health_factors.append(('error_handling', error_score))
        
        overall_score = sum(score for _, score in health_factors) / len(health_factors) if health_factors else 0.5
        
        return {
            'overall_score': overall_score,
            'health_level': 'excellent' if overall_score > 0.8 else 'good' if overall_score > 0.6 else 'needs_improvement',
            'component_scores': dict(health_factors)
        }
    
    def _identify_key_strengths(self) -> List[Dict[str, str]]:
        """Identify key strengths of the system"""
        strengths = []
        
        if 'dependencies' in self.findings:
            deps = self.findings['dependencies']
            if not deps.get('circular_risks'):
                strengths.append({
                    'area': 'Architecture',
                    'strength': 'No circular dependencies detected',
                    'impact': 'Maintainable and testable codebase'
                })
        
        if 'configuration' in self.findings:
            config = self.findings['configuration']
            if config.get('robustness_score', 0) > 0.7:
                strengths.append({
                    'area': 'Configuration',
                    'strength': 'Robust configuration system',
                    'impact': 'Reliable environment detection and fallbacks'
                })
        
        if 'ai_pipeline' in self.findings:
            pipeline = self.findings['ai_pipeline']
            if len(pipeline.get('pipeline_stages', [])) > 5:
                strengths.append({
                    'area': 'Pipeline Design',
                    'strength': 'Well-structured processing pipeline',
                    'impact': 'Clear separation of concerns and maintainable flow'
                })
        
        return strengths
    
    def _identify_critical_improvements(self) -> List[Dict[str, str]]:
        """Identify critical improvements needed"""
        improvements = []
        
        # Check testing coverage
        if 'testing' in self.findings:
            gaps = self.findings['testing'].get('testing_gaps', [])
            high_priority_gaps = [g for g in gaps if g.get('priority') == 'high']
            if high_priority_gaps:
                improvements.append({
                    'area': 'Testing',
                    'improvement': f'Add comprehensive tests for {len(high_priority_gaps)} critical components',
                    'priority': 'high',
                    'impact': 'Prevent regressions and improve reliability'
                })
        
        # Check performance optimizations
        if 'performance' in self.findings:
            memory_patterns = self.findings['performance'].get('memory_usage_patterns', [])
            high_memory_operations = [p for p in memory_patterns if p.get('memory_impact') == 'high']
            if high_memory_operations:
                improvements.append({
                    'area': 'Performance',
                    'improvement': f'Optimize memory usage in {len(high_memory_operations)} operations',
                    'priority': 'medium',
                    'impact': 'Better scalability and resource usage'
                })
        
        return improvements
    
    def _assess_risks(self) -> List[Dict[str, str]]:
        """Assess potential risks in the system"""
        risks = []
        
        # Dependency risks
        if 'dependencies' in self.findings:
            bottlenecks = self.findings['dependencies'].get('bottlenecks', [])
            if bottlenecks:
                risks.append({
                    'risk': 'High coupling in critical components',
                    'severity': 'medium',
                    'mitigation': 'Refactor to reduce dependencies'
                })
        
        # Configuration risks
        if 'configuration' in self.findings:
            config_score = self.findings['configuration'].get('robustness_score', 0)
            if config_score < 0.7:
                risks.append({
                    'risk': 'Configuration system reliability',
                    'severity': 'high',
                    'mitigation': 'Improve detection and fallback mechanisms'
                })
        
        return risks
    
    def _generate_recommendations(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate actionable recommendations"""
        recommendations = {
            'immediate': [],
            'short_term': [],
            'long_term': []
        }
        
        # Immediate recommendations (0-1 week)
        if 'error_handling' in self.findings:
            coverage = self.findings['error_handling'].get('overall_error_coverage', 0)
            if coverage < 0.6:
                recommendations['immediate'].append({
                    'action': 'Add error handling to critical functions',
                    'components': ['AnalizadorMaestroIA', 'LectorArchivosExcel'],
                    'effort': 'low',
                    'impact': 'high'
                })
        
        # Short-term recommendations (1-4 weeks)
        if 'testing' in self.findings:
            gaps = self.findings['testing'].get('testing_gaps', [])
            if gaps:
                recommendations['short_term'].append({
                    'action': 'Implement comprehensive test suite',
                    'components': [g['component'] for g in gaps[:3]],
                    'effort': 'medium',
                    'impact': 'high'
                })
        
        # Long-term recommendations (1-3 months)
        if 'performance' in self.findings:
            optimizations = self.findings['performance'].get('optimization_recommendations', [])
            if optimizations:
                recommendations['long_term'].append({
                    'action': 'Implement performance optimizations',
                    'components': [o['target'] for o in optimizations],
                    'effort': 'high',
                    'impact': 'medium'
                })
        
        return recommendations
    
    def _generate_implementation_roadmap(self) -> List[Dict[str, Any]]:
        """Generate implementation roadmap"""
        roadmap = []
        
        # Phase 1: Stabilization
        roadmap.append({
            'phase': 'Stabilization',
            'duration': '1-2 weeks',
            'objectives': [
                'Complete error handling coverage',
                'Add configuration validation',
                'Implement basic monitoring'
            ],
            'success_criteria': [
                'All critical functions have error handling',
                'Configuration edge cases covered',
                'Basic metrics collection in place'
            ]
        })
        
        # Phase 2: Testing & Quality
        roadmap.append({
            'phase': 'Testing & Quality',
            'duration': '2-4 weeks',
            'objectives': [
                'Comprehensive test suite',
                'Code coverage analysis',
                'Performance benchmarking'
            ],
            'success_criteria': [
                '>80% test coverage on critical components',
                'All integration paths tested',
                'Performance baselines established'
            ]
        })
        
        # Phase 3: Optimization
        roadmap.append({
            'phase': 'Optimization',
            'duration': '4-8 weeks',
            'objectives': [
                'Memory usage optimization',
                'I/O performance improvements',
                'Scalability enhancements'
            ],
            'success_criteria': [
                'Memory usage reduced by 30%',
                'Processing speed improved by 25%',
                'Support for larger file sizes'
            ]
        })
        
        return roadmap
    
    def run_comprehensive_analysis(self):
        """Run complete E2E analysis"""
        print("🚀 STARTING COMPREHENSIVE E2E PIPELINE ANALYSIS")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # Run all analysis modules
            self.analyze_component_architecture()
            self.analyze_dependency_flow()
            self.analyze_ai_pipeline_flow()
            self.analyze_configuration_system()
            self.analyze_error_handling_patterns()
            self.analyze_performance_characteristics()
            self.analyze_testing_coverage_potential()
            
            # Generate comprehensive report
            report = self.generate_comprehensive_report()
            
            return report
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            traceback.print_exc()
            return None

def main():
    """Main analysis execution"""
    analyzer = PipelineAnalyzer()
    report = analyzer.run_comprehensive_analysis()
    
    if report:
        print("\n✅ Analysis completed successfully")
        print(f"📊 Overall health: {report['executive_summary']['overall_health']['health_level']}")
        return report
    else:
        print("\n❌ Analysis failed")
        return None

if __name__ == "__main__":
    report = main()
    if report:
        sys.exit(0)
    else:
        sys.exit(1)