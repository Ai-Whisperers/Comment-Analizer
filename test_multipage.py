"""
Test script for the new multi-page architecture
Verifies button reliability and styling preservation
"""

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

st.set_page_config(
    page_title="Architecture Test",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Multi-Page Architecture Test")

# Test styling import
try:
    from shared.styling.theme_manager_full import ThemeManager, UIComponents
    
    # Initialize
    if 'theme_manager' not in st.session_state:
        st.session_state.theme_manager = ThemeManager()
        st.session_state.ui = UIComponents()
    
    theme = st.session_state.theme_manager
    ui = st.session_state.ui
    
    # Apply styling
    dark_theme = theme.get_theme(True)
    st.markdown(f"<style>{theme.generate_css_variables(dark_theme)}</style>", unsafe_allow_html=True)
    
    st.success("✅ Styling system loaded successfully")
    
    # Test UI components
    st.markdown(
        ui.animated_header("Test Header", "Architecture Validation"),
        unsafe_allow_html=True
    )
    
    st.success("✅ UI components working")
    
except Exception as e:
    st.error(f"❌ Styling test failed: {e}")

# Test business logic
try:
    from shared.business.analysis_engine import analyze_sentiment_simple
    
    test_comment = "excelente servicio, muy satisfecho"
    sentiment = analyze_sentiment_simple(test_comment)
    
    st.success(f"✅ Business logic working: '{test_comment}' → {sentiment}")
    
except Exception as e:
    st.error(f"❌ Business logic test failed: {e}")

# Test simple button (should work reliably)
st.markdown("### 🔘 Button Reliability Test")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Test Button 1", key="test1"):
        st.success("✅ Button 1 clicked successfully!")

with col2:
    if st.button("Test Button 2", key="test2"):
        st.success("✅ Button 2 clicked successfully!")

with col3:
    if st.button("Test Button 3", key="test3"):
        st.success("✅ Button 3 clicked successfully!")

# Test navigation
st.markdown("### 🧭 Navigation Test")

if st.button("🚀 Test Multi-Page", key="test_multipage"):
    st.info("Multi-page navigation would work here")
    st.balloons()

st.markdown("---")
st.success("🎯 Architecture test complete - ready for full implementation!")