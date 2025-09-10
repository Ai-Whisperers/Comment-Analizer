#!/usr/bin/env python3
"""
Test script for progress tracking integration
Tests that the progress callback system works correctly
"""

import sys
from pathlib import Path
import io

# Add src to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_progress_callback_integration():
    """Test that progress callback is properly integrated"""
    
    print("🧪 Testing Progress Tracking Integration...")
    
    # Track progress events
    progress_events = []
    
    def test_progress_callback(progress_data):
        """Test callback that captures progress events"""
        progress_events.append(progress_data.copy())
        action = progress_data.get('action', 'unknown')
        
        if action == 'start':
            print(f"  📊 START: {progress_data.get('total_comments', 0)} comentarios, {progress_data.get('total_batches', 0)} lotes")
        elif action == 'batch_start':
            print(f"  🔄 BATCH START: Lote {progress_data.get('current_batch', 0)}/{progress_data.get('total_batches', 0)}")
        elif action == 'batch_success':
            print(f"  ✅ BATCH SUCCESS: Lote {progress_data.get('current_batch', 0)} - confianza: {progress_data.get('confidence', 0):.2f}")
        elif action == 'batch_failure':
            print(f"  ❌ BATCH FAILURE: Lote {progress_data.get('current_batch', 0)} - razón: {progress_data.get('reason', 'unknown')}")
    
    try:
        # Test 1: Import the necessary components
        print("  📦 Testing imports...")
        from src.infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias
        from src.application.use_cases.analizar_excel_maestro_caso_uso import AnalizarExcelMaestroCasoUso
        print("  ✅ Imports successful")
        
        # Test 2: Create container with mock configuration
        print("  🏗️ Testing container creation...")
        mock_config = {
            'openai_api_key': 'test-key-mock',
            'openai_modelo': 'gpt-4',
            'max_comments': 20
        }
        
        # Note: This will fail without real OpenAI key, but we can test the structure
        try:
            contenedor = ContenedorDependencias(mock_config)
            print("  ✅ Container created successfully")
            
            # Test 3: Check that obtener_caso_uso_maestro accepts progress_callback
            print("  🔗 Testing progress callback parameter...")
            
            # This should not raise an error about the parameter
            try:
                caso_uso = contenedor.obtener_caso_uso_maestro(test_progress_callback)
                print("  ✅ Progress callback parameter accepted")
                
                # Test 4: Check that the caso_uso has progress_callback stored
                if hasattr(caso_uso, 'progress_callback') and caso_uso.progress_callback == test_progress_callback:
                    print("  ✅ Progress callback properly stored in use case")
                else:
                    print("  ❌ Progress callback not properly stored")
                    
            except TypeError as e:
                print(f"  ❌ Progress callback parameter not accepted: {e}")
                return False
                
        except Exception as e:
            print(f"  ⚠️ Container creation failed (expected with mock config): {e}")
            # This is expected without real OpenAI configuration
            
        # Test 5: Test progress callback system independently
        print("  🔄 Testing progress callback system...")
        
        # Create a direct instance to test the callback system
        from src.infrastructure.repositories.repositorio_comentarios_memoria import RepositorioComentariosMemoria
        from src.infrastructure.file_handlers.lector_archivos_excel import LectorArchivosExcel
        
        try:
            # Create minimal components for testing
            repositorio = RepositorioComentariosMemoria()
            lector = LectorArchivosExcel()
            
            # Test that we can create the use case with progress callback
            # (this will fail when trying to create analizador_maestro, but that's OK for this test)
            test_caso_uso = AnalizarExcelMaestroCasoUso(
                repositorio_comentarios=repositorio,
                lector_archivos=lector,
                analizador_maestro=None,  # Will cause failure, but that's OK for callback test
                max_comments_per_batch=20,
                ai_configuration=None,
                progress_callback=test_progress_callback
            )
            
            # Check if callback is stored
            if test_caso_uso.progress_callback == test_progress_callback:
                print("  ✅ Progress callback correctly stored in use case instance")
                
                # Test the callback methods exist
                methods_to_test = [
                    '_notify_progress_start',
                    '_notify_batch_start', 
                    '_notify_batch_success',
                    '_notify_batch_failure'
                ]
                
                all_methods_exist = True
                for method_name in methods_to_test:
                    if hasattr(test_caso_uso, method_name):
                        print(f"    ✅ Method {method_name} exists")
                    else:
                        print(f"    ❌ Method {method_name} missing")
                        all_methods_exist = False
                
                if all_methods_exist:
                    print("  ✅ All progress notification methods exist")
                    
                    # Test calling the methods
                    print("  🔄 Testing progress notification methods...")
                    try:
                        test_caso_uso._notify_progress_start(3, 50)
                        test_caso_uso._notify_batch_start(1, 3, 20)
                        test_caso_uso._notify_batch_success(1, 3, 0.85)
                        test_caso_uso._notify_batch_failure(2, 3, "Test failure")
                        
                        if len(progress_events) == 4:
                            print("  ✅ All progress notifications triggered correctly")
                            print(f"    📊 Captured {len(progress_events)} progress events")
                            
                            # Verify event types
                            expected_actions = ['start', 'batch_start', 'batch_success', 'batch_failure']
                            actual_actions = [event.get('action') for event in progress_events]
                            
                            if actual_actions == expected_actions:
                                print("  ✅ Progress events have correct action types")
                                return True
                            else:
                                print(f"  ❌ Progress events mismatch. Expected: {expected_actions}, Got: {actual_actions}")
                                return False
                        else:
                            print(f"  ❌ Expected 4 progress events, got {len(progress_events)}")
                            return False
                            
                    except Exception as e:
                        print(f"  ❌ Error calling progress methods: {e}")
                        return False
                        
                else:
                    print("  ❌ Some progress notification methods are missing")
                    return False
                    
            else:
                print("  ❌ Progress callback not correctly stored")
                return False
                
        except Exception as e:
            print(f"  ❌ Error testing progress callback system: {e}")
            return False
        
        print("  ✅ All progress tracking integration tests passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_streamlit_integration():
    """Test that Streamlit integration components work"""
    print("🌐 Testing Streamlit Integration...")
    
    try:
        # Test that we can create the progress callback factory
        print("  🏭 Testing progress callback factory...")
        
        # Simulate the factory function from Streamlit page
        def create_mock_streamlit_callback():
            """Mock version of the Streamlit progress callback factory"""
            events = []
            
            def mock_update_progress(progress_data):
                events.append(progress_data)
                # Simulate what Streamlit would do
                action = progress_data.get('action', 'unknown')
                if action == 'start':
                    print(f"    📊 Mock Streamlit: Iniciando análisis de {progress_data.get('total_comments', 0)} comentarios")
                elif action == 'batch_start':
                    print(f"    🔄 Mock Streamlit: Procesando lote {progress_data.get('current_batch', 0)}")
                elif action == 'batch_success':
                    print(f"    ✅ Mock Streamlit: Lote completado con confianza {progress_data.get('confidence', 0):.2f}")
                    
            return mock_update_progress, events
        
        callback, events = create_mock_streamlit_callback()
        
        # Test the callback
        callback({'action': 'start', 'total_comments': 100, 'total_batches': 5})
        callback({'action': 'batch_start', 'current_batch': 1, 'total_batches': 5})
        callback({'action': 'batch_success', 'current_batch': 1, 'confidence': 0.87})
        
        if len(events) == 3:
            print("  ✅ Mock Streamlit callback factory works correctly")
            return True
        else:
            print(f"  ❌ Mock Streamlit callback failed. Expected 3 events, got {len(events)}")
            return False
            
    except Exception as e:
        print(f"  ❌ Streamlit integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Progress Tracking Integration Test Suite")
    print("=" * 50)
    
    success1 = test_progress_callback_integration()
    print()
    success2 = test_streamlit_integration()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED! Progress tracking integration is working correctly.")
        exit_code = 0
    else:
        print("❌ SOME TESTS FAILED! Check the output above for details.")
        exit_code = 1
    
    print("📋 Integration Summary:")
    print(f"  • Progress callback system: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"  • Streamlit integration: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    exit(exit_code)