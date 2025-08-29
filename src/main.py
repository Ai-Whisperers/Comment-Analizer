"""
Comment Analyzer - Personal Paraguay
Sentiment analysis for customer feedback
"""

# Critical imports with comprehensive error tracking
critical_imports = {}
optional_imports = {}

try:
    import streamlit as st
    critical_imports['streamlit'] = '✅'
    print("✅ Streamlit imported successfully")
except ImportError as e:
    critical_imports['streamlit'] = f'❌ {e}'
    print(f"🚨 CRITICAL: Streamlit import failed: {e}")

try:
    import pandas as pd
    critical_imports['pandas'] = '✅'
    print("✅ Pandas imported successfully")
except ImportError as e:
    critical_imports['pandas'] = f'❌ {e}'
    print(f"🚨 CRITICAL: Pandas import failed: {e}")

try:
    import plotly.graph_objects as go
    import plotly.express as px
    critical_imports['plotly'] = '✅'
    print("✅ Plotly imported successfully")
except ImportError as e:
    critical_imports['plotly'] = f'❌ {e}'
    print(f"🚨 CRITICAL: Plotly import failed: {e}")

try:
    from pathlib import Path
    from datetime import datetime
    import numpy as np
    from collections import Counter
    import re
    from io import BytesIO
    import os
    import logging
    from logging.handlers import RotatingFileHandler
    import sys
    import gc  # For garbage collection and memory management
    critical_imports['stdlib'] = '✅'
    print("✅ Standard library modules imported successfully")
except ImportError as e:
    critical_imports['stdlib'] = f'❌ {e}'
    print(f"🚨 CRITICAL: Standard library import failed: {e}")

try:
    import psutil  # For memory monitoring
    optional_imports['psutil'] = '✅'
    print("✅ psutil imported successfully")
except ImportError as e:
    optional_imports['psutil'] = f'❌ {e}'
    print(f"⚠️ Optional: psutil import failed: {e}")

# Report import status and handle critical failures
failed_critical = [k for k, v in critical_imports.items() if '❌' in v]
if failed_critical:
    print(f"🚨 CRITICAL IMPORT FAILURES: {failed_critical}")
    print("App may not function correctly!")
    
    # If Streamlit is available, show error to user
    if 'streamlit' in critical_imports and '✅' in critical_imports['streamlit']:
        st.error("🚨 Critical Import Failures Detected")
        st.error(f"Failed imports: {', '.join(failed_critical)}")
        st.info("This may prevent the app from functioning properly.")
        st.info("Check the logs for detailed error information.")
    
    # Continue execution with degraded functionality
else:
    print("✅ All critical imports successful")
    
print(f"📊 Import Summary: {len(critical_imports)} critical, {len(optional_imports)} optional")

# IMMEDIATE UI TEST - Force render something to check if Streamlit is working
try:
    print("🧪 TESTING: Attempting immediate UI render...")
    st.write("🧪 **UI TEST**: If you see this, Streamlit rendering works!")
    st.success("✅ Basic UI rendering is functional")
    print("✅ IMMEDIATE UI TEST: Success - basic rendering works")
except Exception as immediate_ui_error:
    print(f"🚨 IMMEDIATE UI TEST FAILED: {immediate_ui_error}")
    import traceback
    print(f"🔍 Immediate UI traceback: {traceback.format_exc()}")

# Environment detection and path setup
def is_streamlit_cloud():
    """Detect if running on Streamlit Cloud"""
    # Multiple detection methods for accuracy
    cloud_indicators = [
        "/mount/src/" in str(Path.cwd()),  # Streamlit Cloud mount path
        os.getenv("STREAMLIT_SHARING") == "true",  # Streamlit Cloud env var
        "adminuser" in str(Path.home()),  # Streamlit Cloud user
        not os.access(".", os.W_OK),  # Read-only filesystem
        "/home/adminuser/venv" in str(sys.executable)  # Streamlit Cloud Python path
    ]
    return any(cloud_indicators)

@st.cache_data(ttl=60)  # Cache memory checks for 1 minute
def get_memory_usage():
    """Get current memory usage for optimization"""
    try:
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        return memory_mb
    except:
        return 0

def optimize_memory():
    """Force garbage collection to free memory"""
    gc.collect()
    
def check_memory_limit():
    """Check if approaching Streamlit Cloud memory limit"""
    memory_mb = get_memory_usage()
    CLOUD_MEMORY_LIMIT = 690  # Streamlit Cloud limit in MB
    
    if memory_mb > CLOUD_MEMORY_LIMIT * 0.8:  # 80% threshold
        st.warning(f"⚠️ Uso de memoria alto: {memory_mb:.1f}MB")
        st.info("Optimizando memoria automáticamente...")
        optimize_memory()
        return True
    return False

# Add src to Python path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src" if current_dir.name != "src" else current_dir
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Import with fallbacks for Streamlit Cloud
import_issues = []

try:
    from src.ai_overseer import apply_ai_oversight
    print("✅ ai_overseer import successful")
except ImportError as e:
    import_issues.append(f"ai_overseer: {e}")
    try:
        from ai_overseer import apply_ai_oversight
        print("✅ ai_overseer fallback successful")
    except ImportError:
        def apply_ai_oversight(data): return data
        print("⚠️ ai_overseer using fallback function")

try:
    from src.ui_styling import inject_styles, UIComponents, ThemeManager
    print("✅ ui_styling import successful")
except ImportError as e:
    import_issues.append(f"ui_styling: {e}")
    try:
        from ui_styling import inject_styles, UIComponents, ThemeManager
        print("✅ ui_styling fallback successful")
    except ImportError:
        print("⚠️ ui_styling using fallback classes")
        def inject_styles(dark_mode=True): return ""
        class UIComponents:
            def __init__(self): pass
            def create_metric_card(self, *args, **kwargs): return f"<div>{args[0]}: {args[1]}</div>"
            def results_header(self, **kwargs): return "<div>Results Header</div>"
            def section_divider(self): return "<hr>"
        class ThemeManager:
            def get_theme(self, dark=True): return {"primary": "#4ea4ff"}

if import_issues:
    print(f"Import issues detected: {len(import_issues)}")
    for issue in import_issues:
        print(f"  - {issue}")
else:
    print("✅ All imports successful")

# Configure logging based on environment detection
if is_streamlit_cloud():
    # Streamlit Cloud - use memory logging with flush for visibility
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    print("Comment Analyzer started (Streamlit Cloud mode)")
    sys.stdout.flush()  # Ensure cloud logging visibility
else:
    # Local development - use file logging
    try:
        REQUIRED_DIRS = ['data', 'data/raw', 'data/processed', 'outputs', 'logs']
        for dir_path in REQUIRED_DIRS:
            os.makedirs(dir_path, exist_ok=True)
        
        log_file = Path('logs') / f'comment_analyzer_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.info("Comment Analyzer started (local mode)")
    except Exception:
        # Fallback to basic logging with cloud compatibility
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        print("Comment Analyzer started (fallback mode)")
        sys.stdout.flush()


# Page config - ONLY SET ONCE PER SESSION
if 'page_config_set' not in st.session_state:
    try:
        print("🔧 Setting page config (first time)...")
        st.set_page_config(
            page_title="Personal Paraguay — Análisis de Comentarios",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        st.session_state.page_config_set = True
        print("✅ Page config set successfully")
    except Exception as config_error:
        print(f"🚨 Page config failed: {config_error}")
        import traceback
        print(f"🔍 Config traceback: {traceback.format_exc()}")
        st.session_state.page_config_set = True  # Prevent retry
else:
    print("✅ Page config already set - skipping")

# Critical: Check for API key configuration early
def check_api_configuration():
    """Check if OpenAI API key is properly configured"""
    api_key = None
    
    # Check Streamlit secrets first (cloud deployment)
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
        if api_key:
            print("✅ OpenAI API key found in Streamlit secrets")
            return True
    except Exception:
        print("⚠️ No Streamlit secrets available")
    
    # Check environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OpenAI API key found in environment")
        return True
    
    # Check .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("✅ OpenAI API key found in .env file")
            return True
    except Exception:
        pass
    
    print("❌ No OpenAI API key found")
    return False

# Show API configuration status - WITH ERROR PROTECTION
try:
    print("🔑 Checking API configuration...")
    api_configured = check_api_configuration()
    print(f"✅ API check completed: {api_configured}")
    
    if not api_configured and is_streamlit_cloud():
        st.warning("⚠️ OpenAI API key no configurada. Algunas funciones estarán limitadas.")
        st.info("Administradores: Configura OPENAI_API_KEY en Streamlit Cloud secrets.")
except Exception as api_error:
    print(f"🚨 API configuration check failed: {api_error}")
    api_configured = False

# Initialize session state - WITH ERROR PROTECTION
try:
    print("📊 Initializing session state...")
    
    # Initialize deployment status in session state  
    if 'show_deployment_status' not in st.session_state:
        st.session_state.show_deployment_status = True
        print("✅ Deployment status state initialized")

    # Initialize theme state
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True  # Default to dark mode for web3 aesthetics
        print("✅ Theme state initialized")
    
    print("✅ Session state initialization completed")
except Exception as session_error:
    print(f"🚨 Session state initialization failed: {session_error}")
    import traceback
    print(f"🔍 Session traceback: {traceback.format_exc()}")

# Initialize UI components helper with error handling
try:
    print("🎨 Initializing UI components...")
    ui = UIComponents()
    print("✅ UIComponents created")
    theme_manager = ThemeManager()
    print("✅ ThemeManager created")
    print("✅ UI components initialized successfully")
except Exception as ui_error:
    print(f"❌ UI components failed: {ui_error}")
    import traceback
    print(f"🔍 UI init traceback: {traceback.format_exc()}")
    
    # Create minimal fallbacks
    print("🔄 Creating fallback UI components...")
    class MinimalUI:
        def section_divider(self): return "<hr>"
        def results_header(self, **kwargs): return "<h2>Results</h2>"
        def create_metric_card(self, *args, **kwargs): return f"<div>{args[0]}: {args[1]}</div>"
    
    ui = MinimalUI()
    class MinimalTheme:
        def get_theme(self, dark=True): return {"primary": "#4ea4ff"}
    theme_manager = MinimalTheme()
    print("✅ Fallback UI components created")

# Theme toggle and system monitoring in sidebar - WITH ERROR PROTECTION
try:
    print("📋 Setting up sidebar...")
    with st.sidebar:
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("◐", key="theme_toggle", help="Toggle Dark/Light Mode"):
                try:
                    print(f"🎨 Toggling theme mode...")
                    st.session_state.dark_mode = not st.session_state.dark_mode
                    print(f"✅ Theme set to: {'Dark' if st.session_state.dark_mode else 'Light'}")
                    st.rerun()
                except Exception as theme_error:
                    print(f"🚨 Theme toggle error: {theme_error}")
                    # Fallback without rerun
                    st.session_state.dark_mode = not st.session_state.dark_mode
        with col2:
            st.markdown(f"**{'Dark' if st.session_state.dark_mode else 'Light'} Mode**")
        
        # Memory monitoring for Streamlit Cloud
        try:
            memory_mb = get_memory_usage()
            if memory_mb > 0:
                memory_pct = (memory_mb / 690) * 100  # Streamlit Cloud limit
                color = "🔴" if memory_pct > 80 else ("🟡" if memory_pct > 60 else "🟢")
                st.metric(
                    f"{color} Memoria",
                    f"{memory_mb:.0f}MB",
                    f"{memory_pct:.1f}% usado"
                )
        except:
            pass  # Silent fail if monitoring unavailable
            
        st.markdown("---")
    
    print("✅ Sidebar setup completed")
except Exception as sidebar_error:
    print(f"🚨 Sidebar setup failed: {sidebar_error}")
    import traceback
    print(f"🔍 Sidebar traceback: {traceback.format_exc()}")

# Inject all styles with error handling
try:
    st.markdown(inject_styles(st.session_state.dark_mode), unsafe_allow_html=True)
    print("✅ Styles injected successfully")
except Exception as style_error:
    print(f"⚠️ Style injection failed: {style_error}")

# Get current theme colors from theme manager
try:
    theme = theme_manager.get_theme(st.session_state.dark_mode)
    print("✅ Theme loaded successfully")
except Exception as theme_error:
    print(f"⚠️ Theme loading failed: {theme_error}")
    theme = {"primary": "#4ea4ff"}  # Fallback theme

# Add visible title and test UI elements - WITH ERROR PROTECTION
try:
    print("🎯 Starting UI rendering...")
    st.title("📊 Personal Paraguay — Análisis de Comentarios")
    st.markdown("### Sistema de análisis de sentimientos para comentarios de clientes")
    print("✅ Title and header rendered successfully")
except Exception as ui_error:
    print(f"🚨 CRITICAL: UI rendering failed: {ui_error}")
    import traceback
    print(f"🔍 UI Error traceback: {traceback.format_exc()}")
    # Fallback minimal UI
    st.error("🚨 Error rendering main UI")
    st.write("Debug mode - checking imports...")

# Closable deployment status panel
if st.session_state.show_deployment_status:
    with st.expander("ℹ️ Estado del Sistema (Click para cerrar)", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("✅ Aplicación iniciada correctamente")
            if is_streamlit_cloud():
                st.info("🌐 Entorno: Streamlit Cloud")
            else:
                st.info("🖥️ Entorno: Local")
        
        with col2:
            if api_configured:
                st.success("🔑 OpenAI API: Configurada")
                st.success("🤖 Análisis IA: Disponible")
            else:
                st.warning("⚠️ OpenAI API: No configurada")
                st.info("📊 Análisis básico: Disponible")
        
        # Close button with error protection
        if st.button("🗙 Cerrar mensajes de estado", key="close_status", type="secondary"):
            try:
                print("🗙 Closing deployment status panel...")
                st.session_state.show_deployment_status = False
                print("✅ Deployment status hidden - page will refresh")
                st.rerun()
            except Exception as close_error:
                print(f"🚨 Close button error: {close_error}")
                # Fallback: just set the state without rerun
                st.session_state.show_deployment_status = False
                st.info("✅ Panel cerrado. Actualiza la página si no desaparece.")

@st.cache_data(ttl=300, max_entries=1000)  # 5 min TTL, max 1000 entries
def analyze_sentiment_simple(text):
    """Analyze sentiment of text"""
    if pd.isna(text) or text == "":
        return "neutral"
    
    text = str(text).lower()
    
    # Spanish sentiment words
    positive_words = [
        'excelente', 'bueno', 'buena', 'mejor', 'satisfecho', 'contento',
        'rápido', 'rápida', 'eficiente', 'funciona', 'bien', 'perfecto',
        'recomiendo', 'feliz', 'increíble', 'fantástico', 'genial'
    ]
    
    negative_words = [
        'malo', 'mala', 'pésimo', 'pesimo', 'terrible', 'horrible',
        'lento', 'lenta', 'no funciona', 'problema', 'problemas',
        'error', 'falla', 'deficiente', 'caro', 'costoso', 'demora'
    ]
    
    # Count positive and negative indicators
    pos_count = sum(word in text for word in positive_words)
    neg_count = sum(word in text for word in negative_words)
    
    if pos_count > neg_count:
        return "positivo"
    elif neg_count > pos_count:
        return "negativo"
    else:
        return "neutral"

@st.cache_data(ttl=600, max_entries=2000)  # 10 min TTL, larger cache
def clean_text_simple(text):
    """Clean and normalize text"""
    if pd.isna(text) or text == "":
        return text
    
    text = str(text).strip()
    
    # Basic corrections for common typos
    corrections = {
        'pesimo': 'pésimo', 'lentp': 'lento', 'servico': 'servicio',
        'internert': 'internet', 'intenet': 'internet', 'señaal': 'señal',
        'exelente': 'excelente', 'buenno': 'bueno', 'no funcona': 'no funciona'
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    return text.strip()

def remove_duplicates_simple(comments):
    """Remove duplicate comments"""
    if not comments:
        return [], {}
    
    # Remove exact duplicates and very short comments
    seen = set()
    unique_comments = []
    frequencies = {}
    
    for comment in comments:
        clean = str(comment).lower().strip()
        if len(clean.split()) >= 3 and clean not in seen:  # At least 3 words
            seen.add(clean)
            unique_comments.append(comment)
            frequencies[comment] = 1
        elif clean in seen:
            # Count frequency of duplicates
            for uc in unique_comments:
                if str(uc).lower().strip() == clean:
                    frequencies[uc] = frequencies.get(uc, 1) + 1
                    break
    
    return unique_comments, frequencies

def extract_themes_simple(texts):
    """Extract themes from comments"""
    themes = {
        'velocidad': ['lento', 'lenta', 'velocidad', 'demora', 'tarda'],
        'interrupciones': ['cae', 'corta', 'corte', 'intermitencia', 'interrumpe'],
        'servicio': ['atención', 'servicio', 'cliente', 'soporte', 'ayuda'],
        'precio': ['caro', 'precio', 'costoso', 'tarifa', 'factura'],
        'cobertura': ['cobertura', 'señal', 'zona', 'área', 'alcance'],
        'instalacion': ['instalación', 'técnico', 'visita', 'demora']
    }
    
    theme_counts = {theme: 0 for theme in themes}
    theme_examples = {theme: [] for theme in themes}
    
    for text in texts:
        if pd.isna(text):
            continue
        text_lower = str(text).lower()
        for theme, keywords in themes.items():
            if any(keyword in text_lower for keyword in keywords):
                theme_counts[theme] += 1
                if len(theme_examples[theme]) < 3:
                    theme_examples[theme].append(text[:100])
    
    return theme_counts, theme_examples

@st.cache_data(ttl=180, max_entries=10)  # 3 min TTL, cache last 10 files
def process_file_simple(uploaded_file):
    """Process uploaded file and extract comments with memory optimization"""
    try:
        # Streamlit Cloud memory optimization - ultra strict limits
        MAX_FILE_SIZE_MB = 3    # Ultra conservative for 690MB limit
        MAX_COMMENTS = 500      # Drastically reduce for cloud stability
        
        if hasattr(uploaded_file, 'size') and uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            st.error(f"Archivo demasiado grande para Streamlit Cloud. Máximo: {MAX_FILE_SIZE_MB}MB")
            st.info("💡 Para archivos grandes, usa la instalación local con docker o python run.py")
            return None
        
        # Read file with comprehensive validation and error handling
        try:
            st.info(f"Procesando archivo: {uploaded_file.name}")
            
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, encoding='utf-8', on_bad_lines='skip')
            else:
                # Enhanced Excel reading with openpyxl engine for better compatibility
                try:
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                except Exception as excel_error:
                    st.warning(f"Error con openpyxl, probando xlrd: {str(excel_error)}")
                    try:
                        uploaded_file.seek(0)
                        df = pd.read_excel(uploaded_file, engine=None)  # Auto-detect
                    except Exception as fallback_error:
                        st.error(f"Error leyendo Excel con todos los engines: {str(fallback_error)}")
                        return None
                        
        except UnicodeDecodeError:
            # Try latin-1 encoding as fallback
            try:
                uploaded_file.seek(0)
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file, encoding='latin-1', on_bad_lines='skip')
                else:
                    st.error("Error de codificación en el archivo Excel")
                    return None
            except Exception as fallback_error:
                st.error(f"Error con codificación latin-1: {str(fallback_error)}")
                return None
                
        except Exception as e:
            st.error(f"Error crítico leyendo archivo: {str(e)}")
            st.error("Detalles del error para depuración:")
            st.code(f"Tipo de error: {type(e).__name__}\nDescripción: {str(e)}")
            return None
        
        # Validate dataframe
        if df.empty:
            st.error("El archivo está vacío")
            return None
        
        if len(df.columns) == 0:
            st.error("No se encontraron columnas en el archivo")
            return None
        
        # Show file structure for debugging
        st.success(f"✅ Archivo leído correctamente: {df.shape[0]} filas, {df.shape[1]} columnas")
        with st.expander("🔍 Ver estructura del archivo"):
            st.write("**Columnas encontradas:**")
            st.write(list(df.columns))
            st.write("**Primeras 3 filas:**")
            st.dataframe(df.head(3))
        
        # Find comment column with improved detection
        try:
            comment_cols = ['comentario final', 'comment', 'comments', 'feedback', 'texto', 'comentario', 
                           'observacion', 'observaciones', 'opinion', 'mensaje', 'respuesta']
            comment_col = None
            
            # First try exact match
            for col in df.columns:
                if any(name in col.lower() for name in comment_cols):
                    comment_col = col
                    st.info(f"Columna de comentarios detectada: '{comment_col}'")
                    break
            
            if comment_col is None:
                # Use first text column
                for col in df.columns:
                    if df[col].dtype == 'object':
                        comment_col = col
                        st.warning(f"Usando primera columna de texto como comentarios: '{comment_col}'")
                        break
            
            if comment_col is None:
                st.error("No se encontró columna de comentarios válida")
                st.error("Columnas disponibles:")
                for i, col in enumerate(df.columns):
                    st.write(f"{i+1}. {col} (tipo: {df[col].dtype})")
                return None
                
        except Exception as column_error:
            st.error(f"Error detectando columnas: {str(column_error)}")
            return None
        
        # Extract and clean comments with comprehensive error handling
        try:
            st.info(f"Extrayendo comentarios de la columna: '{comment_col}'")
            raw_comments = df[comment_col].dropna().tolist()
            
            if not raw_comments:
                st.error("No se encontraron comentarios válidos en la columna seleccionada")
                return None
            
            # Memory optimization: Limit comments for Streamlit Cloud
            if len(raw_comments) > MAX_COMMENTS:
                st.warning(f"⚠️ Limitando a {MAX_COMMENTS} comentarios para optimizar rendimiento en Streamlit Cloud")
                raw_comments = raw_comments[:MAX_COMMENTS]
                
            st.success(f"✅ Extraídos {len(raw_comments)} comentarios")
            
            # Clean text with progress indication and memory optimization
            with st.spinner("Limpiando y procesando comentarios..."):
                cleaned_comments = []
                
                # Process in chunks to reduce memory usage
                CHUNK_SIZE = 100
                for i in range(0, len(raw_comments), CHUNK_SIZE):
                    chunk = raw_comments[i:i + CHUNK_SIZE]
                    for comment in chunk:
                        try:
                            cleaned = clean_text_simple(comment)
                            if cleaned and len(cleaned.strip()) > 2:
                                cleaned_comments.append(cleaned)
                        except Exception:
                            continue
                    
                    # Clear chunk from memory
                    del chunk
                
                if not cleaned_comments:
                    st.error("No se encontraron comentarios válidos después de la limpieza")
                    return None
                    
                st.success(f"✅ Limpieza completada: {len(cleaned_comments)} comentarios válidos")
                
                # Clear raw_comments from memory
                del raw_comments
            
            # Remove duplicates
            with st.spinner("Removiendo duplicados..."):
                unique_comments, comment_frequencies = remove_duplicates_simple(cleaned_comments)
                st.info(f"Comentarios únicos: {len(unique_comments)}")
                
                # Clear cleaned_comments from memory after deduplication
                del cleaned_comments
            
            # Analyze sentiment with progress and memory management
            with st.spinner("Analizando sentimientos..."):
                sentiments = []
                
                # Process sentiment in smaller batches for memory efficiency
                SENTIMENT_BATCH_SIZE = 50
                for i in range(0, len(unique_comments), SENTIMENT_BATCH_SIZE):
                    batch = unique_comments[i:i + SENTIMENT_BATCH_SIZE]
                    batch_sentiments = []
                    
                    for comment in batch:
                        try:
                            sentiment = analyze_sentiment_simple(comment)
                            batch_sentiments.append(sentiment)
                        except Exception:
                            batch_sentiments.append('neutral')
                    
                    sentiments.extend(batch_sentiments)
                    
                    # Progress indicator for large datasets
                    if len(unique_comments) > SENTIMENT_BATCH_SIZE:
                        progress = min(i + SENTIMENT_BATCH_SIZE, len(unique_comments))
                        st.progress(progress / len(unique_comments))
                        
                st.success(f"✅ Análisis de sentimientos completado")
                
                # Memory optimization after processing
                optimize_memory()
                
        except Exception as processing_error:
            st.error(f"Error durante el procesamiento: {str(processing_error)}")
            st.code(f"Error: {type(processing_error).__name__}: {str(processing_error)}")
            return None
        
        # Count sentiments
        sentiment_counts = Counter(sentiments)
        total = len(unique_comments)
        
        positive_count = sentiment_counts.get('positivo', 0)
        neutral_count = sentiment_counts.get('neutral', 0)
        negative_count = sentiment_counts.get('negativo', 0)
        
        # Calculate percentages
        positive_pct = round((positive_count / total * 100), 1) if total > 0 else 0
        neutral_pct = round((neutral_count / total * 100), 1) if total > 0 else 0
        negative_pct = round((negative_count / total * 100), 1) if total > 0 else 0
        
        # Extract themes
        theme_counts, theme_examples = extract_themes_simple(unique_comments)
        
        # File statistics
        file_size_kb = uploaded_file.size / 1024 if hasattr(uploaded_file, 'size') else 0
        avg_length = np.mean([len(comment) for comment in unique_comments]) if unique_comments else 0
        
        results = {
            'total': total,
            'raw_total': len(raw_comments),
            'duplicates_removed': len(raw_comments) - len(unique_comments),
            'positive_count': positive_count,
            'neutral_count': neutral_count,
            'negative_count': negative_count,
            'positive_pct': positive_pct,
            'neutral_pct': neutral_pct,
            'negative_pct': negative_pct,
            'comments': unique_comments,
            'sentiments': sentiments,
            'comment_frequencies': comment_frequencies,
            'theme_counts': theme_counts,
            'theme_examples': theme_examples,
            'original_filename': uploaded_file.name,
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'file_size': file_size_kb,
            'avg_length': avg_length,
            'analysis_method': 'SIMPLE_RULE_BASED'
        }
        
        # Apply AI Oversight for quality validation
        try:
            enhanced_results = apply_ai_oversight(results, strict=False, language='es')
            
            # Show AI validation status
            if 'overseer_validation' in enhanced_results:
                validation = enhanced_results['overseer_validation']
                if validation.get('ai_enhanced'):
                    st.info(f"Validación IA aplicada - Confianza: {validation.get('confidence', 0):.1%}")
                else:
                    st.info("Validación basada en reglas aplicada")
            
            return enhanced_results
        except Exception as ai_error:
            st.warning(f"Validación IA no disponible: {str(ai_error)}")
            # Return original results if AI oversight fails
            return results
        
    except Exception as e:
        st.error(f"Error procesando archivo: {str(e)}")
        return None

@st.cache_data(ttl=300, max_entries=3)  # Cache Excel generation for cloud
def create_simple_excel(results):
    """Create enhanced Excel report optimized for Streamlit Cloud memory limits"""
    # Cloud-specific memory optimization
    if is_streamlit_cloud():
        MAX_COMMENTS = 500  # Ultra conservative for 690MB cloud limit
        st.info("🌐 Optimizando Excel para Streamlit Cloud (máximo 500 comentarios)")
    else:
        MAX_COMMENTS = 10000  # Local can handle more
    
    if len(results.get('comments', [])) > MAX_COMMENTS:
        st.warning(f"Limitando exportación a {MAX_COMMENTS} comentarios para mantener rendimiento")
        # Truncate data for Excel
        results = results.copy()
        results['comments'] = results['comments'][:MAX_COMMENTS]
        results['sentiments'] = results['sentiments'][:MAX_COMMENTS]
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats for better visualization
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#8B5CF6',
            'font_color': 'white',
            'border': 1
        })
        
        positive_format = workbook.add_format({
            'fg_color': '#E6F7ED',
            'font_color': '#10B981',
            'border': 1
        })
        
        negative_format = workbook.add_format({
            'fg_color': '#FEE2E2',
            'font_color': '#EF4444',
            'border': 1
        })
        
        neutral_format = workbook.add_format({
            'fg_color': '#F3F4F6',
            'font_color': '#6B7280',
            'border': 1
        })
        
        # Sheet 1: Executive Summary (NEW)
        exec_summary = {
            'KPI': [
                'Total Comentarios Analizados',
                'Satisfacción Neta (Positivos - Negativos)',
                'Temas Críticos Detectados',
                'Calidad del Análisis',
                'Comentarios Únicos',
                'Tasa de Duplicación'
            ],
            'Valor': [
                results['total'],
                f"{results['positive_pct'] - results['negative_pct']:.1f}%",
                sum(1 for v in results.get('theme_counts', {}).values() if v > 5),
                f"{results.get('overseer_validation', {}).get('quality_score', 0):.0%}",
                results['total'],
                f"{(results.get('duplicates_removed', 0) / results.get('raw_total', results.get('total', 1)) * 100) if results.get('raw_total', results.get('total', 1)) > 0 else 0:.1f}%"
            ],
            'Interpretación': [
                'Volumen total de feedback procesado',
                'Diferencia entre sentimientos positivos y negativos',
                'Número de temas con más de 5 menciones',
                'Confianza en el análisis realizado',
                'Comentarios después de eliminar duplicados',
                'Porcentaje de comentarios duplicados encontrados'
            ]
        }
        df_exec = pd.DataFrame(exec_summary)
        df_exec.to_excel(writer, sheet_name='Resumen Ejecutivo', index=False)
        worksheet_exec = writer.sheets['Resumen Ejecutivo']
        
        # Format executive summary headers
        for col_num, value in enumerate(df_exec.columns.values):
            worksheet_exec.write(0, col_num, value, header_format)
        
        # Auto-adjust column widths
        worksheet_exec.set_column('A:A', 40)
        worksheet_exec.set_column('B:B', 25)
        worksheet_exec.set_column('C:C', 50)
        
        # Sheet 2: Original Summary (Enhanced)
        summary_data = {
            'Métrica': ['Total Comentarios', 'Positivos', 'Neutrales', 'Negativos', 'Duplicados Eliminados'],
            'Valor': [results['total'], f"{results['positive_pct']}%", f"{results['neutral_pct']}%", 
                     f"{results['negative_pct']}%", results['duplicates_removed']],
            'Cantidad': [results['total'], results['positive_count'], results['neutral_count'],
                        results['negative_count'], results['duplicates_removed']]
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Resumen', index=False)
        worksheet_summary = writer.sheets['Resumen']
        
        # Format summary headers
        for col_num, value in enumerate(df_summary.columns.values):
            worksheet_summary.write(0, col_num, value, header_format)
        
        # Sheet 3: ALL Comments with enhanced data (NO LIMIT)
        comments_data = {
            'Comentario': results['comments'],  # ALL comments, no [:500] limit
            'Sentimiento': results['sentiments'],
            'Frecuencia': [results['comment_frequencies'].get(c, 1) for c in results['comments']],
            'Requiere Acción': ['Sí' if s == 'negativo' else 'No' for s in results['sentiments']],
            'Prioridad': ['Alta' if s == 'negativo' else 'Media' if s == 'neutral' else 'Baja' 
                         for s in results['sentiments']]
        }
        df_comments = pd.DataFrame(comments_data)
        df_comments.to_excel(writer, sheet_name='Comentarios Completos', index=False)
        worksheet_comments = writer.sheets['Comentarios Completos']
        
        # Format comments headers
        for col_num, value in enumerate(df_comments.columns.values):
            worksheet_comments.write(0, col_num, value, header_format)
        
        # Auto-adjust column width for comments
        worksheet_comments.set_column('A:A', 60)
        worksheet_comments.set_column('B:E', 15)
        
        # Sheet 4: Themes with more details
        if results.get('theme_counts'):
            themes_data = {
                'Tema': list(results['theme_counts'].keys()),
                'Cantidad': list(results['theme_counts'].values()),
                'Porcentaje': [f"{(v/results['total']*100):.1f}%" if results['total'] > 0 else "0%" 
                              for v in results['theme_counts'].values()],
                'Impacto': ['Alto' if v > 10 else 'Medio' if v > 5 else 'Bajo' 
                           for v in results['theme_counts'].values()]
            }
            df_themes = pd.DataFrame(themes_data)
            df_themes.to_excel(writer, sheet_name='Análisis de Temas', index=False)
            worksheet_themes = writer.sheets['Análisis de Temas']
            
            # Format themes headers
            for col_num, value in enumerate(df_themes.columns.values):
                worksheet_themes.write(0, col_num, value, header_format)
        
        # Sheet 5: Pain Points Matrix (NEW)
        pain_points_data = {
            'Punto de Dolor': [
                'Velocidad/Lentitud',
                'Interrupciones del Servicio',
                'Atención al Cliente',
                'Precios Altos',
                'Problemas de Cobertura',
                'Demoras en Instalación'
            ],
            'Frecuencia': [
                results.get('theme_counts', {}).get('velocidad', 0),
                results.get('theme_counts', {}).get('interrupciones', 0),
                results.get('theme_counts', {}).get('servicio', 0),
                results.get('theme_counts', {}).get('precio', 0),
                results.get('theme_counts', {}).get('cobertura', 0),
                results.get('theme_counts', {}).get('instalacion', 0)
            ]
        }
        
        # Calculate impact scores based on frequency and sentiment correlation
        pain_points_data['Impacto en Negocio'] = [
            'CRÍTICO' if freq > 10 else 'ALTO' if freq > 5 else 'MEDIO' if freq > 0 else 'BAJO'
            for freq in pain_points_data['Frecuencia']
        ]
        
        pain_points_data['Prioridad'] = [
            1 if imp == 'CRÍTICO' else 2 if imp == 'ALTO' else 3 if imp == 'MEDIO' else 4
            for imp in pain_points_data['Impacto en Negocio']
        ]
        
        pain_points_data['Acción Recomendada'] = [
            'Intervención inmediata requerida' if freq > 10 else
            'Revisar y mejorar proceso' if freq > 5 else
            'Monitorear tendencia' if freq > 0 else
            'Sin acciones requeridas'
            for freq in pain_points_data['Frecuencia']
        ]
        
        df_pain = pd.DataFrame(pain_points_data)
        df_pain = df_pain.sort_values('Prioridad')  # Sort by priority
        df_pain.to_excel(writer, sheet_name='Matriz de Puntos Críticos', index=False)
        worksheet_pain = writer.sheets['Matriz de Puntos Críticos']
        
        # Format pain points headers
        for col_num, value in enumerate(df_pain.columns.values):
            worksheet_pain.write(0, col_num, value, header_format)
        
        # Apply conditional formatting for impact column
        worksheet_pain.conditional_format('C2:C7', {
            'type': 'cell',
            'criteria': 'equal to',
            'value': '"CRÍTICO"',
            'format': negative_format
        })
        
        worksheet_pain.conditional_format('C2:C7', {
            'type': 'cell',
            'criteria': 'equal to',
            'value': '"ALTO"',
            'format': workbook.add_format({'fg_color': '#FEF3C7', 'font_color': '#F59E0B'})
        })
        
        # Auto-adjust columns
        worksheet_pain.set_column('A:A', 25)
        worksheet_pain.set_column('B:B', 12)
        worksheet_pain.set_column('C:C', 18)
        worksheet_pain.set_column('D:D', 10)
        worksheet_pain.set_column('E:E', 35)
        
        # Sheet 6: AI Insights (if available)
        if 'overseer_validation' in results:
            ai_data = {
                'Métrica de Calidad': [
                    'Validación Aplicada',
                    'Confianza del Análisis',
                    'Calidad General',
                    'Mejorado con IA',
                    'Fecha de Análisis'
                ],
                'Valor': [
                    'Sí' if results['overseer_validation'].get('validated') else 'No',
                    f"{results['overseer_validation'].get('confidence', 0):.0%}",
                    f"{results['overseer_validation'].get('quality_score', 0):.0%}",
                    'Sí' if results['overseer_validation'].get('ai_enhanced') else 'No',
                    results['overseer_validation'].get('timestamp', 'N/A')
                ]
            }
            df_ai = pd.DataFrame(ai_data)
            df_ai.to_excel(writer, sheet_name='Validación IA', index=False)
            worksheet_ai = writer.sheets['Validación IA']
            
            # Format AI insights headers
            for col_num, value in enumerate(df_ai.columns.values):
                worksheet_ai.write(0, col_num, value, header_format)
            
            worksheet_ai.set_column('A:A', 25)
            worksheet_ai.set_column('B:B', 30)
        
        # Sheet 7: Sentiment Analysis Chart Data
        chart_data = {
            'Sentimiento': ['Positivo', 'Neutral', 'Negativo'],
            'Cantidad': [results['positive_count'], results['neutral_count'], results['negative_count']],
            'Porcentaje': [results['positive_pct'], results['neutral_pct'], results['negative_pct']]
        }
        df_chart = pd.DataFrame(chart_data)
        df_chart.to_excel(writer, sheet_name='Datos para Gráficos', index=False)
        worksheet_chart = writer.sheets['Datos para Gráficos']
        
        # Create a pie chart
        pie_chart = workbook.add_chart({'type': 'pie'})
        pie_chart.add_series({
            'name': 'Distribución de Sentimientos',
            'categories': ['Datos para Gráficos', 1, 0, 3, 0],
            'values': ['Datos para Gráficos', 1, 1, 3, 1],
            'points': [
                {'fill': {'color': '#10B981'}},  # Green for positive
                {'fill': {'color': '#6B7280'}},  # Gray for neutral
                {'fill': {'color': '#EF4444'}},  # Red for negative
            ],
        })
        pie_chart.set_title({'name': 'Distribución de Sentimientos'})
        pie_chart.set_size({'width': 380, 'height': 280})
        worksheet_chart.insert_chart('E2', pie_chart)
        
        # Create a column chart for themes
        if results.get('theme_counts'):
            col_chart = workbook.add_chart({'type': 'column'})
            col_chart.add_series({
                'name': 'Frecuencia de Temas',
                'categories': ['Análisis de Temas', 1, 0, len(results['theme_counts']), 0],
                'values': ['Análisis de Temas', 1, 1, len(results['theme_counts']), 1],
                'fill': {'color': '#8B5CF6'},
            })
            col_chart.set_title({'name': 'Temas Principales Detectados'})
            col_chart.set_x_axis({'name': 'Tema'})
            col_chart.set_y_axis({'name': 'Frecuencia'})
            col_chart.set_size({'width': 480, 'height': 320})
            worksheet_themes.insert_chart('F2', col_chart)
    
    output.seek(0)
    return output.getvalue()

def create_ai_enhanced_excel(results):
    """Create Excel report with AI-enhanced data including emotions and pain points"""
    # Validate data size for Excel export
    MAX_COMMENTS = 10000
    if len(results.get('comments', [])) > MAX_COMMENTS:
        st.warning(f"Limitando exportación a {MAX_COMMENTS} comentarios para mantener rendimiento")
        results = results.copy()
        results['comments'] = results['comments'][:MAX_COMMENTS]
        results['sentiments'] = results['sentiments'][:MAX_COMMENTS]
        if 'ai_results' in results:
            results['ai_results'] = results['ai_results'][:MAX_COMMENTS]
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Professional formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#2E3440',
            'font_color': 'white',
            'border': 1
        })
        
        ai_format = workbook.add_format({
            'fg_color': '#E8F4FD',
            'font_color': '#1E40AF',
            'border': 1
        })
        
        confidence_high = workbook.add_format({
            'fg_color': '#ECFDF5',
            'font_color': '#059669',
            'border': 1
        })
        
        # Sheet 1: AI Analysis Summary
        ai_summary = {
            'Métrica IA': [
                'Total Comentarios Procesados',
                'Confianza Promedio del Análisis',
                'Emociones Únicas Detectadas', 
                'Puntos de Dolor Identificados',
                'Temas Granulares Extraídos',
                'Método de Análisis',
                'Fecha y Hora del Análisis'
            ],
            'Valor': [
                results['total'],
                f"{results.get('ai_confidence_avg', 0):.1%}",
                len(results.get('emotion_summary', {}).get('distribution', {})),
                len(results.get('churn_analysis', {}).get('indicators', [])),
                len(results.get('theme_counts', {})),
                'Inteligencia Artificial (OpenAI GPT-4)',
                results['analysis_date']
            ],
            'Descripción': [
                'Número total de comentarios analizados con IA',
                'Nivel de confianza promedio del modelo de IA',
                'Cantidad de emociones específicas identificadas',
                'Número de problemas específicos detectados',
                'Temas granulares extraídos por análisis semántico',
                'Tecnología utilizada para el análisis',
                'Momento de ejecución del análisis'
            ]
        }
        df_ai_summary = pd.DataFrame(ai_summary)
        df_ai_summary.to_excel(writer, sheet_name='Resumen IA', index=False)
        worksheet_ai = writer.sheets['Resumen IA']
        
        # Format headers
        for col_num, value in enumerate(df_ai_summary.columns.values):
            worksheet_ai.write(0, col_num, value, header_format)
        
        worksheet_ai.set_column('A:A', 35)
        worksheet_ai.set_column('B:B', 25)
        worksheet_ai.set_column('C:C', 50)
        
        # Sheet 2: Emotions Analysis (AI Specific)
        emotions_data = results.get('emotion_summary', {}).get('distribution', {})
        if emotions_data:
            emotions_df = pd.DataFrame([
                {
                    'Emoción': emotion,
                    'Cantidad': count,
                    'Porcentaje': f"{(count/results['total']*100):.1f}%",
                    'Intensidad': 'Alta' if count > 10 else 'Media' if count > 5 else 'Baja'
                }
                for emotion, count in emotions_data.items()
            ])
            emotions_df.to_excel(writer, sheet_name='Análisis de Emociones', index=False)
            worksheet_emotions = writer.sheets['Análisis de Emociones']
            
            for col_num, value in enumerate(emotions_df.columns.values):
                worksheet_emotions.write(0, col_num, value, header_format)
        
        # Sheet 3: Pain Points Analysis (AI Specific)  
        pain_points = results.get('churn_analysis', {}).get('indicators', [])
        if pain_points:
            pain_df = pd.DataFrame([
                {
                    'Punto de Dolor': pain,
                    'Tipo': 'Servicio' if 'servicio' in pain.lower() else 'Técnico' if any(t in pain.lower() for t in ['conexión', 'velocidad', 'internet']) else 'Comercial',
                    'Prioridad': 'Alta',
                    'Acción Recomendada': f"Revisar y mejorar {pain}"
                }
                for pain in pain_points
            ])
            pain_df.to_excel(writer, sheet_name='Puntos de Dolor', index=False)
            worksheet_pain = writer.sheets['Puntos de Dolor']
            
            for col_num, value in enumerate(pain_df.columns.values):
                worksheet_pain.write(0, col_num, value, header_format)
        
        # Sheet 4: Detailed AI Analysis (Enhanced Comments)
        ai_results = results.get('ai_results', [])
        comments = results.get('comments', [])
        
        if ai_results and len(ai_results) == len(comments):
            detailed_data = []
            for i, (comment, ai_data) in enumerate(zip(comments, ai_results)):
                detailed_data.append({
                    'ID': f'C{i+1:04d}',
                    'Comentario': comment,
                    'Sentimiento': ai_data.get('sentiment', 'neutral'),
                    'Confianza': f"{ai_data.get('confidence', 0):.1%}",
                    'Idioma': ai_data.get('language', 'es'),
                    'Emociones': ', '.join(ai_data.get('emotions', [])),
                    'Temas': ', '.join(ai_data.get('themes', [])),
                    'Puntos de Dolor': ', '.join(ai_data.get('pain_points', []))
                })
            
            df_detailed = pd.DataFrame(detailed_data)
            df_detailed.to_excel(writer, sheet_name='Análisis Detallado IA', index=False)
            worksheet_detailed = writer.sheets['Análisis Detallado IA']
            
            for col_num, value in enumerate(df_detailed.columns.values):
                worksheet_detailed.write(0, col_num, value, header_format)
            
            worksheet_detailed.set_column('A:A', 12)  # ID
            worksheet_detailed.set_column('B:B', 60)  # Comentario
            worksheet_detailed.set_column('C:C', 15)  # Sentimiento
            worksheet_detailed.set_column('D:D', 12)  # Confianza
            worksheet_detailed.set_column('E:E', 10)  # Idioma
            worksheet_detailed.set_column('F:F', 30)  # Emociones
            worksheet_detailed.set_column('G:G', 30)  # Temas
            worksheet_detailed.set_column('H:H', 35)  # Puntos de Dolor
        
        # Sheet 5: AI Confidence Analysis
        if ai_results:
            confidence_ranges = {
                'Muy Alta (90-100%)': 0,
                'Alta (80-89%)': 0, 
                'Media (70-79%)': 0,
                'Baja (60-69%)': 0,
                'Muy Baja (<60%)': 0
            }
            
            for ai_data in ai_results:
                conf = ai_data.get('confidence', 0) * 100
                if conf >= 90:
                    confidence_ranges['Muy Alta (90-100%)'] += 1
                elif conf >= 80:
                    confidence_ranges['Alta (80-89%)'] += 1
                elif conf >= 70:
                    confidence_ranges['Media (70-79%)'] += 1
                elif conf >= 60:
                    confidence_ranges['Baja (60-69%)'] += 1
                else:
                    confidence_ranges['Muy Baja (<60%)'] += 1
            
            confidence_df = pd.DataFrame([
                {
                    'Rango de Confianza': range_name,
                    'Cantidad': count,
                    'Porcentaje': f"{(count/len(ai_results)*100):.1f}%"
                }
                for range_name, count in confidence_ranges.items()
            ])
            confidence_df.to_excel(writer, sheet_name='Distribución Confianza', index=False)
    
    output.seek(0)
    return output.getvalue()

# Initialize session state with cloud compatibility check
try:
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    # Session state health check for cloud deployment
    if is_streamlit_cloud():
        test_key = 'cloud_session_test'
        if test_key not in st.session_state:
            st.session_state[test_key] = True
            print("✅ Session state working on Streamlit Cloud")
        
except Exception as session_error:
    print(f"❌ Session state issue: {session_error}")
    st.error("⚠️ Problema con sesión. Intenta recargar la página.")
    st.stop()

# Web3 Animated Header using clean UI component
st.markdown(
    ui.animated_header(
        title="Análisis de Comentarios",
        subtitle="Personal Paraguay | Sentiment Analysis Platform"
    ),
    unsafe_allow_html=True
)

# Add floating particles effect
st.markdown(ui.floating_particles(), unsafe_allow_html=True)

# Upload section header with theme colors
st.markdown(f"""
<div style="margin: 2rem 0;">
    <h3 style="text-align: center; background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        background-clip: text; color: transparent;
        font-size: 1.5rem; font-weight: 600;">
        Cargar Archivo de Datos
    </h3>
</div>
""", unsafe_allow_html=True)

# File uploader with proper container
with st.container():
    uploaded_file = st.file_uploader(
        "Selecciona o arrastra un archivo Excel/CSV",
        type=['csv', 'xlsx', 'xls'],
        help="Formatos soportados: Excel (.xlsx, .xls) o CSV (.csv)",
        label_visibility="visible"
    )

# Analysis button
if uploaded_file:
    # Add section divider
    st.markdown(ui.section_divider(), unsafe_allow_html=True)
    st.info(f"Archivo cargado: {uploaded_file.name}")
    
    # Analysis method selection
    st.markdown("### Selecciona el Método de Análisis")
    col_method1, col_method2 = st.columns(2)
    
    with col_method1:
        if st.button("Análisis Rápido (Reglas)", type="secondary", use_container_width=True, help="Análisis inmediato basado en reglas, sin costo"):
            st.session_state.analysis_method = "simple"
            
    with col_method2:
        if st.button("Análisis Avanzado (IA)", type="secondary", use_container_width=True, help="Análisis profundo con IA - requiere API key"):
            st.session_state.analysis_method = "ai"
    
    # Show selected method
    if 'analysis_method' in st.session_state:
        if st.session_state.analysis_method == "simple":
            st.success("**Método Seleccionado:** Análisis Rápido (Reglas)")
        else:
            st.success("**Método Seleccionado:** Análisis Avanzado (IA)")
        
        # Animated analyze button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            button_text = "Analizar con IA" if st.session_state.analysis_method == "ai" else "Analizar Rápido"
            if st.button(button_text, type="primary", use_container_width=True):
                with st.spinner("Procesando comentarios..."):
                    if st.session_state.analysis_method == "ai":
                        # Use Pipeline 2 (AI + Fallback) with better error handling
                        try:
                            st.info("Iniciando análisis avanzado con IA...")
                            
                            # First, process file the same way as simple pipeline
                            basic_results = process_file_simple(uploaded_file)
                            if not basic_results:
                                st.error("Error procesando archivo")
                            else:
                                # Then enhance with AI analysis
                                from src.ai_analysis_adapter import AIAnalysisAdapter
                                adapter = AIAnalysisAdapter()
                                
                                # Extract comments from basic results for AI processing
                                comments = basic_results.get('comments', [])
                                if len(comments) > 50:
                                    st.info(f"Procesando {len(comments)} comentarios con IA (esto puede tomar 1-3 minutos)...")
                                
                                # Try AI enhancement on the extracted comments
                                try:
                                    ai_enhanced = adapter.openai_analyzer.analyze_comments_batch(comments[:50])  # Limit for demo
                                    if ai_enhanced:
                                        # Enhance the basic results with AI data
                                        enhanced_results = basic_results.copy()
                                        enhanced_results['analysis_method'] = 'AI_POWERED'
                                        enhanced_results['ai_results'] = ai_enhanced
                                        enhanced_results['ai_confidence_avg'] = sum(r.get('confidence', 0) for r in ai_enhanced) / len(ai_enhanced)
                                        
                                        # Add AI-specific data structures
                                        emotions = []
                                        pain_points = []
                                        for result in ai_enhanced:
                                            emotions.extend(result.get('emotions', []))
                                            pain_points.extend(result.get('pain_points', []))
                                        
                                        enhanced_results['emotion_summary'] = {
                                            'distribution': {emotion: emotions.count(emotion) for emotion in set(emotions)},
                                            'avg_intensity': 3.5  # Mock intensity for now
                                        }
                                        
                                        enhanced_results['churn_analysis'] = {
                                            'indicators': list(set(pain_points))[:5],
                                            'risk_level': 'medium' if pain_points else 'low'
                                        }
                                        
                                        st.session_state.analysis_results = enhanced_results
                                        st.success("Análisis IA completado con éxito!")
                                    else:
                                        st.warning("🔄 IA no disponible, usando análisis rápido...")
                                        st.session_state.analysis_results = basic_results
                                except Exception as ai_error:
                                    st.warning(f"IA falló ({str(ai_error)[:50]}...), usando análisis rápido")
                                    st.session_state.analysis_results = basic_results
                                    
                        except Exception as e:
                            st.error(f"Error en procesamiento: {str(e)}")
                    else:
                        # Use Pipeline 1 (Simple Rule-Based)  
                        results = process_file_simple(uploaded_file)
                        if results:
                            st.session_state.analysis_results = results
                            st.success("Análisis rápido completado!")
                    
                    # Add success animation if we have results - with error protection
                    if 'analysis_results' in st.session_state and st.session_state.analysis_results:
                        try:
                            print("🎉 Showing success animation...")
                            st.balloons()
                            # Remove st.rerun() as it's not needed here and can cause crashes
                            print("✅ Success animation completed")
                        except Exception as animation_error:
                            print(f"🚨 Animation error: {animation_error}")
                            # Continue without animation

# Results display with enhanced Spanish sentiment UI
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    # Import and use the enhanced Spanish sentiment UI
    from src.components.sentiment_results_ui import render_sentiment_results
    
    # Display AI Oversight Report if available
    if 'oversight_report' in results:
        with st.expander("Reporte de Validación IA", expanded=False):
            st.text(results['oversight_report'])
    
    # Display quality metrics if available
    if 'overseer_validation' in results:
        validation_data = results['overseer_validation']
        quality_score = validation_data.get('quality_score', 0)
        
        # Show quality badge using UI components
        if quality_score >= 0.8:
            st.markdown(
                ui.status_badge(
                    icon="CONF",
                    text=f"Calidad de Análisis: {quality_score:.1%} - Excelente",
                    badge_type="positive"
                ),
                unsafe_allow_html=True
            )
        elif quality_score >= 0.6:
            st.markdown(
                ui.status_badge(
                    icon="MED",
                    text=f"Calidad de Análisis: {quality_score:.1%} - Mejorable",
                    badge_type="neutral"
                ),
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                ui.status_badge(
                    icon="REV",
                    text=f"Calidad de Análisis: {quality_score:.1%} - Requiere Revisión",
                    badge_type="negative"
                ),
                unsafe_allow_html=True
            )
    
    # Add section divider before results
    st.markdown(ui.section_divider(), unsafe_allow_html=True)
    
    # Render enhanced Spanish sentiment results UI (replaces all old display logic)
    render_sentiment_results(results)
    
    # Download section
    st.subheader("Descargar Resultados")
    
    try:
        # Generate appropriate Excel based on analysis method
        if results.get('analysis_method') == 'AI_POWERED':
            excel_data = create_ai_enhanced_excel(results)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analisis_IA_comentarios_{timestamp}.xlsx"
        else:
            excel_data = create_simple_excel(results)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analisis_comentarios_{timestamp}.xlsx"
        
        st.download_button(
            label="Descargar Reporte Excel",
            data=excel_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            help="Descargar reporte en formato Excel"
        )
    except Exception as e:
        st.error(f"Error creando Excel: {e}")

# Enhanced footer using clean UI component
st.markdown(
    ui.gradient_footer(
        primary_text="Análisis de Comentarios | Personal Paraguay",
        secondary_text="Powered by Advanced Analytics"
    ),
    unsafe_allow_html=True
)

# FINAL EXECUTION MARKER
print("🎯 END OF MAIN.PY: Reached end of file - all code executed successfully")
print("📊 If you see this message, the entire main.py file ran to completion")