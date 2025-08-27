"""
Pytest configuration and shared fixtures for Comment Analyzer tests
"""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path

# No need for sys.path modifications when package is properly installed
# Install the package in development mode with: pip install -e .


@pytest.fixture
def sample_comments_spanish():
    """Fixture providing sample Spanish comments for testing"""
    return [
        "El servicio es pésimo, se corta todo el tiempo",
        "Excelente atención del técnico, muy profesional",
        "Internet muy lento, no funciona bien",
        "Todo perfecto, sin problemas",
        "Necesito cancelar el servicio, muy caro",
        "La velocidad mejoró mucho después del cambio",
        "No hay señal en mi zona",
        "Servicio regular, podría ser mejor",
        "",  # Empty comment
        "No funciona",  # Short comment
    ]


@pytest.fixture
def sample_dataframe():
    """Fixture providing a sample DataFrame for testing"""
    return pd.DataFrame({
        'Comentario Final': [
            "Servicio malo, muy lento",
            "Excelente servicio",
            "Se corta constantemente",
            "Precio muy caro para la velocidad",
            "Atención al cliente pésima"
        ],
        'NPS': ['Detractor', 'Promotor', 'Detractor', 'Pasivo', 'Detractor'],
        'Nota': [3, 9, 2, 6, 1]
    })


@pytest.fixture
def sample_csv_file(sample_dataframe, tmp_path):
    """Fixture providing a temporary CSV file for testing"""
    file_path = tmp_path / "test_comments.csv"
    sample_dataframe.to_csv(file_path, index=False)
    return str(file_path)


@pytest.fixture
def sample_excel_file(sample_dataframe, tmp_path):
    """Fixture providing a temporary Excel file for testing"""
    file_path = tmp_path / "test_comments.xlsx"
    sample_dataframe.to_excel(file_path, index=False)
    return str(file_path)


@pytest.fixture
def mock_openai_response():
    """Fixture providing mock OpenAI API response"""
    return {
        "choices": [{
            "message": {
                "content": "Negative sentiment detected. The customer is frustrated with service interruptions."
            }
        }]
    }


@pytest.fixture
def pattern_detection_comments():
    """Fixture providing comments for pattern detection testing"""
    return [
        "Se corta la conexión todos los días a la misma hora",
        "El técnico nunca vino a la cita programada",
        "Cobran más de lo acordado en el contrato",
        "Router necesita reiniciarse constantemente",
        "Estoy pensando cambiar a Tigo",
        "Urgente necesito internet para trabajar desde casa",
        "Excelente servicio, lo recomiendo",
        "TERRIBLE SERVICIO!!!",
        "spam spam spam spam spam",
        "Internet lento en las mañanas",
    ]


@pytest.fixture
def mock_streamlit_session():
    """Fixture providing mock Streamlit session state"""
    class MockSession:
        def __init__(self):
            self.session_manager = None
            self.file_service = None
            self.analyzer = None
            self.analysis_results = None
            self.raw_data = None
            self.themes_data = None
    
    return MockSession()


@pytest.fixture
def temp_output_dir(tmp_path):
    """Fixture providing temporary output directory"""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    (output_dir / "exports").mkdir()
    (output_dir / "reports").mkdir()
    (output_dir / "visualizations").mkdir()
    return output_dir