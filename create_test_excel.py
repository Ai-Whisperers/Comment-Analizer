#!/usr/bin/env python3
"""
Crear archivo Excel válido para testing del pipeline
"""

import pandas as pd
from pathlib import Path

def create_test_excel():
    """Create a proper Excel file for testing"""
    
    # Sample comments data (realistic Paraguay telecom feedback)
    comentarios_data = [
        "Excelente servicio de internet, muy rápido y estable",
        "El soporte técnico es muy bueno, resuelven rápido los problemas", 
        "Internet lento en horas pico, necesitan mejorar la infraestructura",
        "Buena cobertura en el área metropolitana de Asunción",
        "Precios competitivos comparado con otras empresas",
        "Problemas frecuentes de conectividad los fines de semana",
        "Atención al cliente profesional y cordial",
        "Velocidad de subida muy lenta para videoconferencias",
        "Servicio confiable para trabajo remoto",
        "Falta cobertura en el interior del país",
        "Buena relación precio-calidad del servicio",
        "Instalación rápida y técnicos capacitados",
        "Cortes de servicio sin previo aviso",
        "App móvil fácil de usar para gestionar cuenta",
        "Promociones atractivas para nuevos clientes",
        "Servicio 24/7 muy útil para emergencias",
        "Velocidad prometida no siempre se cumple",
        "Personal técnico bien preparado y amable",
        "Internet estable durante tormentas",
        "Facturación clara y transparente"
    ]
    
    # Create DataFrame with proper structure
    df = pd.DataFrame({
        'ID': range(1, len(comentarios_data) + 1),
        'Comentario Final': comentarios_data,
        'NPS': [9, 8, 4, 7, 8, 3, 9, 5, 8, 4, 7, 8, 2, 7, 8, 9, 5, 8, 7, 8],
        'Nota': [4.5, 4.0, 2.0, 3.5, 4.0, 1.5, 4.5, 2.5, 4.0, 2.0, 3.5, 4.0, 1.0, 3.5, 4.0, 4.5, 2.5, 4.0, 3.5, 4.0],
        'Fecha': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'] * 4
    })
    
    # Save to local-reports directory
    local_reports_dir = Path(__file__).parent / "local-reports"
    local_reports_dir.mkdir(exist_ok=True)
    
    output_file = local_reports_dir / "test_comments_valid.xlsx"
    
    # Create Excel with multiple sheets to test robustness
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Main sheet with comments
        df.to_excel(writer, sheet_name='Comentarios', index=False)
        
        # Summary sheet
        summary_df = pd.DataFrame({
            'Métrica': ['Total Comentarios', 'NPS Promedio', 'Nota Promedio'],
            'Valor': [len(comentarios_data), df['NPS'].mean(), df['Nota'].mean()]
        })
        summary_df.to_excel(writer, sheet_name='Resumen', index=False)
    
    print(f"✅ Excel creado: {output_file}")
    print(f"📊 Contenido:")
    print(f"  • {len(comentarios_data)} comentarios")
    print(f"  • NPS promedio: {df['NPS'].mean():.1f}")
    print(f"  • Nota promedio: {df['Nota'].mean():.1f}")
    print(f"  • Columnas: {list(df.columns)}")
    
    return output_file

def create_minimal_test_excel():
    """Create minimal Excel for quick testing"""
    
    minimal_data = [
        "Buen servicio de internet",
        "Atención al cliente excelente", 
        "Velocidad podría mejorar",
        "Precio justo para el servicio",
        "Instalación fue rápida"
    ]
    
    df = pd.DataFrame({
        'Comentario Final': minimal_data,
        'NPS': [8, 9, 5, 7, 8]
    })
    
    local_reports_dir = Path(__file__).parent / "local-reports"
    output_file = local_reports_dir / "test_minimal.xlsx"
    
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"✅ Excel mínimo creado: {output_file}")
    print(f"📊 {len(minimal_data)} comentarios para test rápido")
    
    return output_file

if __name__ == "__main__":
    print("🚀 Creando archivos Excel para testing...")
    
    # Create both versions
    full_file = create_test_excel()
    minimal_file = create_minimal_test_excel()
    
    print(f"\n📁 Archivos creados:")
    print(f"  • Completo: {full_file}")
    print(f"  • Mínimo: {minimal_file}")
    print(f"\n✅ Listos para testing del pipeline")