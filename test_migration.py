"""
Test script para verificar la migración a Clean Architecture
"""

import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_clean_architecture_imports():
    """Test que todas las importaciones de la nueva arquitectura funcionen"""
    print("🧪 Testing Clean Architecture imports...")
    
    try:
        # Test basic application
        from src.aplicacion_principal import crear_aplicacion
        print("✅ aplicacion_principal import: OK")
        
        # Test domain layer
        from src.domain.entities.comentario import Comentario
        from src.domain.value_objects.sentimiento import Sentimiento
        from src.domain.value_objects.calidad_comentario import CalidadComentario
        from src.domain.value_objects.nivel_urgencia import NivelUrgencia
        print("✅ Domain layer imports: OK")
        
        # Test application layer
        from src.application.use_cases.analizar_comentarios_caso_uso import AnalizarComentariosCasoUso
        from src.application.dtos.resultado_analisis import ResultadoAnalisis
        print("✅ Application layer imports: OK")
        
        # Test infrastructure layer
        from src.infrastructure.external_services.analizador_openai import AnalizadorOpenAI
        from src.infrastructure.external_services.analizador_reglas import AnalizadorReglas
        from src.infrastructure.file_handlers.lector_archivos_excel import LectorArchivosExcel
        print("✅ Infrastructure layer imports: OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")
        return False

def test_application_creation():
    """Test que se pueda crear la aplicación"""
    print("\n🏗️ Testing application creation...")
    
    try:
        from src.aplicacion_principal import crear_aplicacion
        
        # Create app without API key (should work with rules fallback)
        app = crear_aplicacion(openai_api_key=None)
        print("✅ App creation without API key: OK")
        
        # Test app info
        if hasattr(app, 'obtener_info_sistema'):
            info = app.obtener_info_sistema()
            print(f"✅ App info: {info.get('version', 'unknown')} - {info.get('arquitectura', 'unknown')}")
        
        # Test stats
        if hasattr(app, 'obtener_estadisticas_repositorio'):
            stats = app.obtener_estadisticas_repositorio()
            print(f"✅ App stats: {stats.get('total', 0)} comments in repository")
        
        return True
        
    except Exception as e:
        print(f"❌ Application creation error: {str(e)}")
        return False

def test_value_objects():
    """Test que los value objects funcionen correctamente"""
    print("\n🎯 Testing Value Objects...")
    
    try:
        from src.domain.value_objects.sentimiento import Sentimiento, TipoSentimiento
        from src.domain.value_objects.calidad_comentario import CalidadComentario, NivelCalidad
        from src.domain.value_objects.nivel_urgencia import NivelUrgencia, PrioridadUrgencia
        
        # Test Sentimiento
        sentimiento = Sentimiento.crear_positivo(0.8, "test")
        assert sentimiento.es_positivo()
        assert sentimiento.confianza == 0.8
        print("✅ Sentimiento value object: OK")
        
        # Test CalidadComentario
        calidad = CalidadComentario.evaluar_desde_texto("Este es un comentario largo y detallado sobre el servicio", 3)
        assert calidad.es_alta_calidad()
        print("✅ CalidadComentario value object: OK")
        
        # Test NivelUrgencia
        urgencia = NivelUrgencia.evaluar_urgencia(["sin servicio", "no funciona"], True, 0.9)
        assert urgencia.es_critico()
        print("✅ NivelUrgencia value object: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Value objects error: {str(e)}")
        return False

def test_entity_creation():
    """Test que se puedan crear entidades"""
    print("\n🏷️ Testing Entity creation...")
    
    try:
        from src.domain.entities.comentario import Comentario
        from src.domain.value_objects.sentimiento import Sentimiento
        from datetime import datetime
        
        # Create a comment entity
        comentario = Comentario(
            id="test_001",
            texto="Servicio excelente, muy satisfecho",
            texto_limpio="servicio excelente muy satisfecho",
            frecuencia=1,
            fecha_analisis=datetime.now()
        )
        
        assert comentario.es_valido()
        print("✅ Comment entity creation: OK")
        
        # Add sentiment
        sentimiento = Sentimiento.crear_positivo(0.9, "test")
        comentario.sentimiento = sentimiento
        
        # Add themes
        comentario.agregar_tema("servicio")
        comentario.agregar_tema("satisfaccion")
        
        assert len(comentario.temas) == 2
        print("✅ Comment entity manipulation: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Entity creation error: {str(e)}")
        return False

def test_dependency_container():
    """Test que el contenedor de dependencias funcione"""
    print("\n🔌 Testing Dependency Container...")
    
    try:
        from src.infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias
        
        config = {
            'openai_api_key': None,  # Test without API key
            'max_comments': 100
        }
        
        contenedor = ContenedorDependencias(config)
        
        # Test repository
        repo = contenedor.obtener_repositorio_comentarios()
        assert repo is not None
        print("✅ Repository injection: OK")
        
        # Test file reader
        lector = contenedor.obtener_lector_archivos()
        assert lector is not None
        print("✅ File reader injection: OK")
        
        # Test sentiment service
        servicio = contenedor.obtener_servicio_sentimientos()
        assert servicio is not None
        print("✅ Sentiment service injection: OK")
        
        # Test use case
        caso_uso = contenedor.obtener_caso_uso_analisis()
        assert caso_uso is not None
        print("✅ Use case injection: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Dependency container error: {str(e)}")
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🚀 Starting Clean Architecture Migration Tests")
    print("=" * 50)
    
    tests = [
        test_clean_architecture_imports,
        test_application_creation,
        test_value_objects,
        test_entity_creation,
        test_dependency_container
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print("❌ Test failed")
        except Exception as e:
            print(f"💥 Test crashed: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"🏆 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - Migration successful!")
    else:
        print(f"❌ {total - passed} tests failed - Check issues above")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)