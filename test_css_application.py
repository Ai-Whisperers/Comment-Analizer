"""
CSS Application Test Page
Tests if modular CSS is being properly applied with glassmorphism effects
"""

import sys
import streamlit as st
from pathlib import Path

# Add to path
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

st.set_page_config(page_title="CSS Test", layout="wide")

# Apply modular styles
from shared.styling.modular_css import initialize_modular_styles, show_css_diagnostics
success = initialize_modular_styles(dark_mode=True)

st.title("🎨 CSS Application Test")
st.markdown(f"**Modular CSS Loading Success:** {'✅ Yes' if success else '❌ No'}")

# Test glassmorphism elements
st.markdown("## Glass Effect Test")
st.markdown("""
<div class="glass-card">
    <h3>🔮 Glassmorphism Test Card</h3>
    <p>This card should have glassmorphism effects with backdrop blur and subtle transparency.</p>
    <button class="glass-button">Glass Button</button>
</div>
""", unsafe_allow_html=True)

# Test Web3 elements
st.markdown("## Web3 Elements Test")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Test Metric", "1,234", "↗️ +12%")

with col2:
    if st.button("🚀 Web3 Button"):
        st.success("Button clicked!")

with col3:
    st.selectbox("Theme Test", ["Dark", "Light"])

# CSS Diagnostics
show_css_diagnostics()

# Raw CSS content verification
st.markdown("## CSS Content Verification")
if st.checkbox("Show Raw CSS Content"):
    from shared.styling.modular_css import ModularStyleManager
    manager = ModularStyleManager()
    
    for css_file in ["core.css", "glassmorphism.css"]:
        with st.expander(f"📄 {css_file}"):
            content = manager._get_cached_css_content(f"static/css/{css_file}")
            if content:
                st.code(content[:1000] + "..." if len(content) > 1000 else content, language="css")
                st.caption(f"File size: {len(content)} characters (minified)")
            else:
                st.error(f"Failed to load {css_file}")