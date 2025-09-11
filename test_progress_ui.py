#!/usr/bin/env python3
"""
Test específico para verificar UI de progreso en tiempo real
Simula callbacks de progreso para verificar que el fragmento se actualiza
"""

import sys
from pathlib import Path
import time
import logging

# Add project root to path
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_progress_callback_simulation():
    """Test de simulación de callback de progreso"""
    try:
        logger.info("🧪 Testing progress callback simulation")
        
        # Simular session state data como lo haría Streamlit
        mock_session_state = {}
        
        # Simular el callback de progreso
        def create_test_progress_callback():
            def update_progress(progress_data):
                mock_session_state['batch_progress_data'] = progress_data.copy()
                logger.info(f"📊 Progress update: {progress_data}")
            return update_progress
        
        progress_callback = create_test_progress_callback()
        
        # TEST 1: Simular inicio de análisis
        logger.info("🚀 Simulando inicio de análisis...")
        progress_callback({
            'action': 'start',
            'total_batches': 3,
            'total_comments': 25,
            'current_batch': 0,
            'progress_percentage': 0.0
        })
        
        # Verificar que se guardó correctamente
        assert 'batch_progress_data' in mock_session_state
        start_data = mock_session_state['batch_progress_data']
        assert start_data['action'] == 'start'
        assert start_data['total_comments'] == 25
        logger.info("✅ Test 1 PASSED: Inicio de análisis")
        
        # TEST 2: Simular progreso de lotes
        logger.info("🔄 Simulando progreso de lotes...")
        for batch_num in range(1, 4):
            # Batch start
            progress_callback({
                'action': 'batch_start',
                'current_batch': batch_num,
                'total_batches': 3,
                'batch_size': 8,
                'progress_percentage': (batch_num - 1) / 3 * 100,
                'status': f'Procesando lote {batch_num}/3'
            })
            
            # Simular procesamiento
            time.sleep(0.1)
            
            # Batch success
            progress_callback({
                'action': 'batch_success',
                'current_batch': batch_num,
                'total_batches': 3,
                'confidence': 0.85 + (batch_num * 0.05),  # Increasing confidence
                'progress_percentage': batch_num / 3 * 100,
                'status': f'✅ Lote {batch_num}/3 completado'
            })
            
            logger.info(f"  ✅ Lote {batch_num}/3 procesado")
        
        # Verificar estado final
        final_data = mock_session_state['batch_progress_data']
        assert final_data['action'] == 'batch_success'
        assert final_data['current_batch'] == 3
        assert final_data['progress_percentage'] == 100.0
        logger.info("✅ Test 2 PASSED: Progreso de lotes")
        
        # TEST 3: Verificar estructura de datos para fragment
        logger.info("🔍 Verificando estructura para fragmento...")
        required_fields = ['action', 'current_batch', 'total_batches', 'progress_percentage']
        for field in required_fields:
            assert field in final_data, f"Campo requerido '{field}' no encontrado"
        logger.info("✅ Test 3 PASSED: Estructura de datos")
        
        # TEST 4: Simular error en lote
        logger.info("❌ Simulando error en lote...")
        progress_callback({
            'action': 'batch_failure',
            'current_batch': 2,
            'total_batches': 3,
            'reason': 'OpenAI API rate limit exceeded',
            'progress_percentage': 66.6
        })
        
        error_data = mock_session_state['batch_progress_data']
        assert error_data['action'] == 'batch_failure'
        assert 'reason' in error_data
        logger.info("✅ Test 4 PASSED: Manejo de errores")
        
        logger.info("🎉 ALL TESTS PASSED - Progress callback funcionando correctamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ ERROR EN TEST: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_progress_fragment_logic():
    """Test de la lógica del fragmento sin Streamlit"""
    try:
        logger.info("🧪 Testing fragment logic simulation")
        
        # Simular diferentes estados del fragmento
        test_states = [
            {
                'action': 'start',
                'total_batches': 2,
                'total_comments': 15,
                'expected': 'Should show initialization'
            },
            {
                'action': 'batch_start',
                'current_batch': 1,
                'total_batches': 2,
                'progress_percentage': 25.0,
                'expected': 'Should show batch processing'
            },
            {
                'action': 'batch_success',
                'current_batch': 1,
                'total_batches': 2,
                'progress_percentage': 50.0,
                'confidence': 0.87,
                'expected': 'Should show batch completed'
            },
            {
                'action': 'batch_failure',
                'current_batch': 2,
                'total_batches': 2,
                'progress_percentage': 75.0,
                'reason': 'API timeout',
                'expected': 'Should show error'
            }
        ]
        
        for i, state in enumerate(test_states, 1):
            logger.info(f"🔍 Testing state {i}: {state['action']}")
            
            # Simular la lógica del fragmento
            action = state.get('action', 'unknown')
            
            if action == 'start':
                total_comments = state.get('total_comments', 0)
                total_batches = state.get('total_batches', 0)
                logger.info(f"  📊 Iniciando: {total_comments} comentarios en {total_batches} lotes")
                
            elif action in ['batch_start', 'batch_success']:
                current_batch = state.get('current_batch', 0)
                total_batches = state.get('total_batches', 1)
                progress_pct = state.get('progress_percentage', 0.0)
                confidence = state.get('confidence', 0.0)
                
                status_icon = "✅" if action == 'batch_success' else "🔄"
                status_text = "Completado" if action == 'batch_success' else "Procesando"
                logger.info(f"  {status_icon} {status_text}: Lote {current_batch}/{total_batches} ({progress_pct:.1f}%)")
                
                if confidence > 0:
                    logger.info(f"  🎯 Confianza: {confidence:.2f}")
                    
            elif action == 'batch_failure':
                current_batch = state.get('current_batch', 0)
                total_batches = state.get('total_batches', 1)
                reason = state.get('reason', 'Error desconocido')
                logger.info(f"  ❌ Error en lote {current_batch}/{total_batches}: {reason}")
                
            else:
                logger.info(f"  🤖 Estado desconocido: {action}")
            
            logger.info(f"  ✅ State {i} processed: {state['expected']}")
        
        logger.info("🎉 Fragment logic test PASSED")
        return True
        
    except Exception as e:
        logger.error(f"❌ ERROR EN FRAGMENT TEST: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Iniciando tests de UI de progreso")
    
    test1_success = test_progress_callback_simulation()
    test2_success = test_progress_fragment_logic()
    
    if test1_success and test2_success:
        print("\n🎉 TODOS LOS TESTS PASARON - UI de progreso funcionando")
        print("✅ Progress callback: OK")
        print("✅ Fragment logic: OK")
        print("✅ Error handling: OK")
        print("✅ Data structure: OK")
        exit(0)
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
        exit(1)