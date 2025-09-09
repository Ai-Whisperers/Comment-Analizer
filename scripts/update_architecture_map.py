#!/usr/bin/env python3
"""
Architecture Map Auto-Updater (Git Hook Integration)
Purpose: Zero-token maintenance of useful_architecture_map.md
Triggers: post-commit, pre-push hooks
"""

import os
import re
import ast
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def get_project_root():
    """Get project root directory"""
    script_dir = Path(__file__).parent
    return script_dir.parent

def run_git_command(command: str, cwd: Path = None) -> str:
    """Run git command and return output"""
    try:
        result = subprocess.run(
            command.split(), 
            cwd=cwd or get_project_root(),
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def get_file_stats(filepath: Path) -> Dict:
    """Get file statistics using native git/filesystem tools"""
    if not filepath.exists():
        return {"lines": 0, "size": 0, "last_modified": "", "complexity": "unknown"}
    
    # Line count
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = len(f.readlines())
    except:
        lines = 0
    
    # File size
    size = filepath.stat().st_size
    
    # Last modified (git)
    last_modified = run_git_command(f"git log -1 --format=%ci -- {filepath}")
    
    # Complexity assessment (heuristic)
    if lines < 100:
        complexity = "Low"
    elif lines < 300:
        complexity = "Medium" 
    elif lines < 600:
        complexity = "High"
    else:
        complexity = "Very High"
    
    return {
        "lines": lines,
        "size": size, 
        "last_modified": last_modified,
        "complexity": complexity
    }

def extract_dependencies_from_python_file(filepath: Path) -> List[str]:
    """Extract import dependencies using AST parsing"""
    if not filepath.exists() or not filepath.suffix == '.py':
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        dependencies = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dep_name = alias.name.split('.')[0]
                    if dep_name.startswith('src.'):
                        # Internal dependency
                        component = dep_name.split('.')[-1]
                        dependencies.append(component)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith('src.'):
                    # Internal dependency
                    component = node.module.split('.')[-1] 
                    dependencies.append(component)
        
        return list(set(dependencies))  # Remove duplicates
    except:
        return []

def scan_architecture_components() -> Dict:
    """Scan codebase for architectural components (zero tokens)"""
    project_root = get_project_root()
    components = {}
    
    # Define component patterns
    component_definitions = [
        # PRESENTATION LAYER
        ("StreamlitApp", "streamlit_app.py", "Bootstrap application & configuration validation"),
        ("MainPage", "pages/1_Página_Principal.py", "Landing page with system status"),
        ("UploadPage", "pages/2_Subir.py", "Main workflow - upload → analysis → export"),
        ("EnhancedCSSLoader", "src/presentation/streamlit/enhanced_css_loader.py", "Glassmorphism styling system"),
        ("ChartRenderer", "pages/2_Subir.py", "Plotly-based data visualization"),
        ("SessionManager", "src/presentation/streamlit/session_state_manager.py", "Cross-page state & memory cleanup"),
        
        # APPLICATION LAYER
        ("ExcelAnalysisUseCase", "src/application/use_cases/analizar_excel_maestro_caso_uso.py", "Main orchestrator for Excel → AI analysis workflow"),
        ("AnalysisCompleteDTO", "src/application/dtos/analisis_completo_ia.py", "AI analysis result structure"),
        ("FileProcessingService", "src/infrastructure/file_handlers/lector_archivos_excel.py", "Excel/CSV reading & validation"),
        ("CommentAnalysisUseCase", "src/application/use_cases/analizar_comentarios_caso_uso.py", "Legacy single-comment analysis"),
        
        # DOMAIN LAYER
        ("AnalysisComment", "src/domain/entities/analisis_comentario.py", "Rich AI analysis aggregate with business rules"),
        ("Sentiment", "src/domain/value_objects/sentimiento.py", "Categorical sentiment analysis"),
        ("Emotion", "src/domain/value_objects/emocion.py", "Granular emotion detection"),
        ("MainTheme", "src/domain/value_objects/tema_principal.py", "Theme categorization with relevance"),
        ("PainPoint", "src/domain/value_objects/punto_dolor.py", "Pain point detection with severity"),
        ("CommentQuality", "src/domain/value_objects/calidad_comentario.py", "Comment quality assessment"),
        ("UrgencyLevel", "src/domain/value_objects/nivel_urgencia.py", "Urgency prioritization"),
        ("Comment", "src/domain/entities/comentario.py", "Simple comment entity (legacy)"),
        
        # INFRASTRUCTURE LAYER
        ("AIAnalyzer", "src/infrastructure/external_services/analizador_maestro_ia.py", "OpenAI GPT integration with intelligent caching"),
        ("MemoryRepository", "src/infrastructure/repositories/repositorio_comentarios_memoria.py", "In-memory storage with memory leak prevention"),
        ("DIContainer", "src/infrastructure/dependency_injection/contenedor_dependencias.py", "Thread-safe service management"),
        ("RetryStrategy", "src/infrastructure/external_services/retry_strategy.py", "Intelligent error recovery"),
        ("AIEngineConstants", "src/infrastructure/external_services/ai_engine_constants.py", "Centralized configuration constants"),
        ("ErrorHandler", "src/shared/exceptions/", "Custom exceptions"),
        ("ConfigManager", "streamlit_app.py", "Multi-source configuration"),
    ]
    
    # Scan each component
    for name, rel_path, purpose in component_definitions:
        filepath = project_root / rel_path
        stats = get_file_stats(filepath)
        
        # Extract dependencies for Python files
        dependencies = []
        if filepath.suffix == '.py':
            dependencies = extract_dependencies_from_python_file(filepath)
        
        # Determine layer
        if 'pages/' in rel_path or 'streamlit_app.py' in rel_path or 'presentation/' in rel_path:
            layer = "PRESENTATION"
        elif 'application/' in rel_path:
            layer = "APPLICATION" 
        elif 'domain/' in rel_path:
            layer = "DOMAIN"
        elif 'infrastructure/' in rel_path or 'shared/' in rel_path:
            layer = "INFRASTRUCTURE"
        else:
            layer = "OTHER"
        
        components[name] = {
            "path": rel_path,
            "purpose": purpose,
            "layer": layer,
            "stats": stats,
            "dependencies": dependencies,
            "exists": filepath.exists()
        }
    
    return components

def generate_component_section(name: str, component: Dict) -> str:
    """Generate component section for architecture map"""
    if not component["exists"]:
        return f"### **❌ {name}** *(MISSING)*\n- **📍 Location:** `{component['path']}` *(FILE NOT FOUND)*\n"
    
    stats = component["stats"]
    icon = {
        "PRESENTATION": "📱",
        "APPLICATION": "🧪", 
        "DOMAIN": "🏢",
        "INFRASTRUCTURE": "⚙️"
    }.get(component["layer"], "🔧")
    
    # Format dependencies
    deps = ", ".join(component["dependencies"][:5])  # Limit to 5
    if len(component["dependencies"]) > 5:
        deps += f" (+{len(component['dependencies'])-5} more)"
    
    section = f"""### **{icon} {name}**
- **📍 Location:** [`{component['path']}:1`]({component['path']})
- **🎯 Purpose:** {component['purpose']}
- **📏 Size:** {stats['lines']} lines | **Complexity:** {stats['complexity']}
- **🔗 Uses:** {deps if deps else "No internal dependencies"}
- **👥 Used by:** *(auto-detected on next update)*
"""
    
    return section

def update_architecture_map(dry_run: bool = True) -> bool:
    """Update the useful_architecture_map.md with current codebase state"""
    project_root = get_project_root()
    map_file = project_root / "local-reports/useful_architecture_map.md"
    
    if not map_file.exists():
        print(f"❌ Architecture map not found: {map_file}")
        return False
    
    print(f"🔄 Updating architecture map (dry_run={dry_run})")
    
    # Scan components
    components = scan_architecture_components()
    
    # Read current map
    with open(map_file, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Update statistics in the overview section
    layer_counts = {}
    total_existing = 0
    for comp in components.values():
        if comp["exists"]:
            layer = comp["layer"]
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
            total_existing += 1
    
    # Replace component count section
    count_section = f"""### **📊 Real Component Count**
```
📱 PRESENTATION     →  {layer_counts.get('PRESENTATION', 0)} components  (UI & visualization)
🧪 APPLICATION     →  {layer_counts.get('APPLICATION', 0)} components  (use cases & DTOs)
🏢 DOMAIN          →  {layer_counts.get('DOMAIN', 0)} components  (business logic)
⚙️ INFRASTRUCTURE  →  {layer_counts.get('INFRASTRUCTURE', 0)} components  (external services)
─────────────────────────────────────────────────────
🎯 TOTAL REAL       → {total_existing} components  (auto-updated)
```"""
    
    # Update the content
    updated_content = re.sub(
        r'### \*\*📊 Real Component Count\*\*.*?```',
        count_section,
        current_content,
        flags=re.DOTALL
    )
    
    # Add update timestamp  
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_note = f"\n<!-- AUTO-UPDATED: {timestamp} by update_architecture_map.py -->\n"
    
    if update_note not in updated_content:
        updated_content += update_note
    
    # Write updated content
    if not dry_run:
        with open(map_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"✅ Architecture map updated: {map_file}")
        
        # Commit the update
        run_git_command(f"git add {map_file}")
        run_git_command(f"git commit -m '🤖 AUTO-UPDATE: Architecture map synchronized with codebase [{timestamp}]'")
        print(f"✅ Changes committed automatically")
    else:
        print(f"🔍 DRY RUN - Would update {total_existing} components")
        print(f"📊 Layer distribution: {layer_counts}")
    
    return True

def main():
    """Main entry point for git hooks"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Update architecture map')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Show what would be updated')
    parser.add_argument('--execute', action='store_true', default=False,
                       help='Actually update the map')
    parser.add_argument('--source', default='local-reports/useful_architecture_map.md',
                       help='Architecture map file to update')
    
    args = parser.parse_args()
    
    # Override dry_run if --execute specified
    dry_run = not args.execute
    
    print("🤖 ARCHITECTURE MAP AUTO-UPDATER")
    print("=" * 40)
    
    success = update_architecture_map(dry_run=dry_run)
    
    if success:
        if dry_run:
            print("✅ Analysis complete - use --execute to apply changes")
        else:
            print("✅ Architecture map successfully updated")
    else:
        print("❌ Update failed")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())