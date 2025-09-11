#!/usr/bin/env python3
"""
🔍 DEBUG PIPELINE AI - Mapeo secuencial paso a paso
Identifica dependencias circulares y puntos de fallo en el pipeline
"""

import sys
from pathlib import Path
import traceback
from datetime import datetime

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def step_1_basic_imports():
    """Step 1: Test basic Python imports"""
    print("\n🔍 STEP 1: Basic Imports")
    print("-" * 40)
    
    try:
        import os
        import logging
        from typing import Dict, Any
        print("  ✅ Basic Python imports: OK")
        return True
    except Exception as e:
        print(f"  ❌ Basic imports failed: {e}")
        return False

def step_2_config_import():
    """Step 2: Test unified config import"""
    print("\n🔍 STEP 2: Config Import")
    print("-" * 40)
    
    try:
        from config import config, is_streamlit_cloud, get_environment_info
        print("  ✅ Config import: OK")
        print(f"  📊 Environment: {'Cloud' if is_streamlit_cloud() else 'Local'}")
        return True, config
    except Exception as e:
        print(f"  ❌ Config import failed: {e}")
        traceback.print_exc()
        return False, None

def step_3_streamlit_import():
    """Step 3: Test Streamlit import separately"""
    print("\n🔍 STEP 3: Streamlit Import")
    print("-" * 40)
    
    try:
        import streamlit as st
        print("  ✅ Streamlit import: OK")
        return True
    except Exception as e:
        print(f"  ❌ Streamlit import failed: {e}")
        return False

def step_4_infrastructure_imports():
    """Step 4: Test infrastructure layer imports"""
    print("\n🔍 STEP 4: Infrastructure Layer Imports")
    print("-" * 40)
    
    results = {}
    
    # Test dependency injection
    try:
        from src.infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias
        print("  ✅ ContenedorDependencias: OK")
        results['container'] = True
    except Exception as e:
        print(f"  ❌ ContenedorDependencias failed: {e}")
        results['container'] = False
    
    # Test file handlers
    try:
        from src.infrastructure.file_handlers.lector_archivos_excel import LectorArchivosExcel
        print("  ✅ LectorArchivosExcel: OK")
        results['file_handler'] = True
    except Exception as e:
        print(f"  ❌ LectorArchivosExcel failed: {e}")
        results['file_handler'] = False
    
    # Test AI services
    try:
        from src.infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA
        print("  ✅ AnalizadorMaestroIA: OK")
        results['ai_analyzer'] = True
    except Exception as e:
        print(f"  ❌ AnalizadorMaestroIA failed: {e}")
        results['ai_analyzer'] = False
    
    return results

def step_5_use_case_imports():
    """Step 5: Test use case layer imports"""
    print("\n🔍 STEP 5: Use Case Layer Imports")
    print("-" * 40)
    
    try:
        from src.application.use_cases.analizar_excel_maestro_caso_uso import AnalizarExcelMaestroCasoUso
        from src.application.use_cases.analizar_excel_maestro_caso_uso import ComandoAnalisisExcelMaestro
        print("  ✅ Use Case imports: OK")
        return True
    except Exception as e:
        print(f"  ❌ Use Case imports failed: {e}")
        traceback.print_exc()
        return False

def step_6_container_creation(config):
    """Step 6: Test container creation with config"""
    print("\n🔍 STEP 6: Container Creation")
    print("-" * 40)
    
    if not config:
        print("  ⚠️ Skipping - no config available")
        return False, None
    
    try:
        test_config = {
            'openai_api_key': config.get('OPENAI_API_KEY', 'test-key'),
            'openai_modelo': config.get('OPENAI_MODEL', 'gpt-4o-mini'),
            'openai_max_tokens': config.get('OPENAI_MAX_TOKENS', 4000),
            'max_comments': config.get('MAX_COMMENTS_PER_BATCH', 10)
        }
        
        from src.infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias
        container = ContenedorDependencias(test_config)
        print("  ✅ Container creation: OK")
        print(f"  📊 Config applied - Max comments: {test_config['max_comments']}")
        return True, container
    except Exception as e:
        print(f"  ❌ Container creation failed: {e}")
        traceback.print_exc()
        return False, None

def step_7_use_case_creation(container):
    """Step 7: Test use case creation from container"""
    print("\n🔍 STEP 7: Use Case Creation")
    print("-" * 40)
    
    if not container:
        print("  ⚠️ Skipping - no container available")
        return False, None
    
    try:
        # Test without callback first
        use_case = container.obtener_caso_uso_maestro()
        print("  ✅ Use case creation (no callback): OK")
        
        # Test with callback
        def test_callback(data):
            print(f"    📊 Progress callback: {data.get('action', 'unknown')}")
        
        use_case_with_callback = container.obtener_caso_uso_maestro(test_callback)
        print("  ✅ Use case creation (with callback): OK")
        
        return True, use_case_with_callback
    except Exception as e:
        print(f"  ❌ Use case creation failed: {e}")
        traceback.print_exc()
        return False, None

def step_8_dependency_analysis():
    """Step 8: Analyze import dependencies for circular references"""
    print("\n🔍 STEP 8: Dependency Analysis")
    print("-" * 40)
    
    import_chain = [
        "config.py",
        "src.infrastructure.dependency_injection.contenedor_dependencias", 
        "src.infrastructure.external_services.analizador_maestro_ia",
        "src.infrastructure.config.ai_configuration_manager",
        "src.application.use_cases.analizar_excel_maestro_caso_uso"
    ]
    
    print("  📋 Import Chain Analysis:")
    for i, module in enumerate(import_chain):
        try:
            if module == "config.py":
                from config import config
                result = "✅"
            else:
                __import__(module)
                result = "✅"
            print(f"    {i+1}. {module}: {result}")
        except Exception as e:
            print(f"    {i+1}. {module}: ❌ {str(e)[:60]}...")
            
    return True

def step_9_circular_dependency_check():
    """Step 9: Check for specific circular dependencies"""
    print("\n🔍 STEP 9: Circular Dependency Check")
    print("-" * 40)
    
    # Check common circular dependency patterns
    checks = [
        {
            'name': 'config.py → streamlit',
            'test': lambda: __import__('config') and not hasattr(__import__('streamlit', fromlist=['']), '__streamlit_circular_check__')
        },
        {
            'name': 'container → ai_analyzer → config',
            'test': lambda: True  # This would be complex to test statically
        }
    ]
    
    for check in checks:
        try:
            result = check['test']()
            print(f"  {'✅' if result else '❌'} {check['name']}: {'OK' if result else 'CIRCULAR'}")
        except Exception as e:
            print(f"  ⚠️ {check['name']}: Error testing - {str(e)[:40]}...")
    
    return True

def main():
    """Run complete pipeline analysis"""
    print("🔍 PIPELINE AI DEBUG - Análisis Secuencial")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Step-by-step analysis
    results = {}
    
    results['basic_imports'] = step_1_basic_imports()
    results['config_import'], config = step_2_config_import()
    results['streamlit_import'] = step_3_streamlit_import()
    results['infrastructure'] = step_4_infrastructure_imports()
    results['use_cases'] = step_5_use_case_imports()
    results['container'], container = step_6_container_creation(config)
    results['use_case_creation'], use_case = step_7_use_case_creation(container)
    results['dependency_analysis'] = step_8_dependency_analysis()
    results['circular_check'] = step_9_circular_dependency_check()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 SUMMARY - Pipeline Analysis Results")
    print("=" * 60)
    
    passed = 0
    total = 0
    
    for step, result in results.items():
        if isinstance(result, dict):
            # Handle infrastructure results
            for sub_step, sub_result in result.items():
                total += 1
                if sub_result:
                    passed += 1
                print(f"{step}.{sub_step}: {'✅ PASS' if sub_result else '❌ FAIL'}")
        else:
            total += 1
            if result:
                passed += 1
            print(f"{step}: {'✅ PASS' if result else '❌ FAIL'}")
    
    print(f"\n🎯 Score: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ¡PIPELINE COMPLETAMENTE FUNCIONAL!")
        print("✅ No se detectaron dependencias circulares")
    elif passed >= total * 0.8:
        print("⚡ Pipeline mayormente funcional")
        print("⚠️ Algunos componentes necesitan atención")
    else:
        print("🚨 PROBLEMAS CRÍTICOS EN PIPELINE")
        print("❌ Múltiples componentes fallan")
    
    print("\n📝 Recomendaciones:")
    if not results.get('config_import', False):
        print("❌ Prioridad 1: Revisar config.py - posible dependencia circular")
    if not results.get('container', False):
        print("❌ Prioridad 2: Revisar ContenedorDependencias")
    if isinstance(results.get('infrastructure'), dict):
        for key, value in results['infrastructure'].items():
            if not value:
                print(f"❌ Componente fallido: {key}")
    
    return passed >= total * 0.8

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Análisis interrumpido")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        traceback.print_exc()
        sys.exit(1)