# 🎨 Modular CSS Architecture

Esta estructura CSS modular está diseñada para ser escalable, mantenible y fácil de consumir por componentes de Streamlit y la carpeta `src`.

## 📁 Estructura de Archivos

```
static/css/
├── base/
│   ├── variables.css          # Variables CSS y design tokens
│   └── reset.css              # Reset CSS y estilos base
├── components/
│   ├── layout.css             # Componentes de layout (headers, cards, grids)
│   ├── streamlit-core.css     # Estilos para componentes core de Streamlit
│   ├── forms.css              # Formularios e inputs
│   └── charts.css             # Gráficos y visualizaciones
├── animations/
│   └── keyframes.css          # Animaciones y efectos
├── utils/
│   └── utilities.css          # Clases utilitarias atómicas
└── README.md                  # Esta documentación
```

## 🔧 Uso en Streamlit

### Importar CSS Principal

```python
# En tu aplicación Streamlit
import streamlit as st

def load_css():
    with open('static/main.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# En main app
load_css()
```

### Importar Módulos Específicos

```python
def load_specific_css(css_file):
    with open(f'static/css/{css_file}') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Cargar solo componentes específicos
load_specific_css('components/forms.css')
load_specific_css('components/charts.css')
```

## 🎯 Uso en Componentes src/

### En componentes de presentación

```python
# src/presentation/streamlit/componentes.py
import streamlit as st

def render_metric_card(title, value, change=None):
    """Renderiza una tarjeta de métrica usando clases CSS modulares"""
    
    change_class = "text-success" if change and change > 0 else "text-error" if change and change < 0 else "text-tertiary"
    
    st.markdown(f"""
    <div class="glass-card stat-card animate-fade-in">
        <div class="stat-value text-gradient">{value}</div>
        <div class="stat-label">{title}</div>
        {f'<div class="{change_class} text-sm">{"+" if change > 0 else ""}{change}%</div>' if change else ''}
    </div>
    """, unsafe_allow_html=True)

def render_section_header(title, subtitle=None):
    """Renderiza un header de sección"""
    subtitle_html = f'<p>{subtitle}</p>' if subtitle else ''
    
    st.markdown(f"""
    <div class="section-header animate-fade-in-up">
        <h2>{title}</h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)
```

## 🎨 Sistema de Variables CSS

### Colores

```css
/* Colores primarios */
var(--primary-purple)
var(--primary-purple-light)
var(--secondary-cyan)

/* Colores semánticos */
var(--success)
var(--warning) 
var(--error)
var(--info)

/* Glass morphism */
var(--glass-bg)
var(--glass-border)
var(--glass-blur)
```

### Espaciado

```css
/* Sistema de espaciado (8px base) */
var(--space-1)    /* 4px */
var(--space-2)    /* 8px */
var(--space-4)    /* 16px */
var(--space-6)    /* 24px */
var(--space-8)    /* 32px */
```

### Tipografía

```css
/* Tamaños de fuente */
var(--size-xs)    /* 12px */
var(--size-sm)    /* 14px */
var(--size-base)  /* 16px */
var(--size-lg)    /* 18px */
var(--size-xl)    /* 20px */

/* Pesos de fuente */
var(--font-weight-normal)    /* 400 */
var(--font-weight-medium)    /* 500 */
var(--font-weight-semibold)  /* 600 */
var(--font-weight-bold)      /* 700 */
```

## 🧩 Clases Utilitarias Principales

### Layout

```css
.flex-center        /* Centrado con flexbox */
.flex-between       /* Espacio entre elementos */
.grid-auto          /* Grid responsivo automático */
.container-xl       /* Contenedor con max-width */
```

### Espaciado

```css
.p-4               /* padding: 1rem */
.m-4               /* margin: 1rem */
.mb-6              /* margin-bottom: 1.5rem */
.gap-4             /* gap: 1rem en flex/grid */
```

### Texto

```css
.text-primary      /* Color de texto principal */
.text-gradient     /* Gradiente de texto */
.font-semibold     /* Peso de fuente 600 */
.text-center       /* Texto centrado */
```

### Efectos

```css
.glass-card        /* Tarjeta con glass morphism */
.shadow-lg         /* Sombra grande */
.rounded-xl        /* Bordes redondeados */
.animate-fade-in   /* Animación de entrada */
```

## 🚀 Componentes Listos para Usar

### Tarjetas de Métricas

```python
st.markdown(f"""
<div class="glass-card stat-card">
    <div class="stat-value">{value}</div>
    <div class="stat-label">{label}</div>
</div>
""", unsafe_allow_html=True)
```

### Headers de Sección

```python
st.markdown(f"""
<div class="section-header">
    <h2>{title}</h2>
    <p>{description}</p>
</div>
""", unsafe_allow_html=True)
```

### Grid de Estadísticas

```python
st.markdown("""
<div class="stats-grid">
    <div class="stat-card">...</div>
    <div class="stat-card">...</div>
    <div class="stat-card">...</div>
</div>
""", unsafe_allow_html=True)
```

## 🎭 Animaciones

### Clases de Animación

```css
.animate-fade-in           /* Aparición suave */
.animate-fade-in-up        /* Aparición desde abajo */
.animate-scale-in          /* Aparición con escala */
.animate-glow              /* Efecto de brillo */
.animate-float             /* Flotación suave */
```

### Delays Escalonados

```css
.animate-delay-100         /* Delay de 100ms */
.animate-delay-200         /* Delay de 200ms */
.animate-delay-300         /* Delay de 300ms */
```

## 📱 Responsive Design

El sistema incluye breakpoints y clases responsive:

```css
/* Breakpoints */
--breakpoint-sm: 640px
--breakpoint-md: 768px  
--breakpoint-lg: 1024px
--breakpoint-xl: 1280px

/* Clases responsive */
.sm\:hidden            /* Oculto en móvil */
.md\:flex              /* Flex en tablet+ */
.lg\:text-2xl          /* Texto grande en desktop+ */
```

## 🎨 Temas y Personalización

### Cambiar Variables Globales

```css
:root {
    --primary-purple: #YOUR_COLOR;
    --glass-bg: rgba(YOUR_COLOR, 0.08);
}
```

### Modo de Alto Contraste

El sistema incluye soporte automático para `prefers-contrast: high`.

### Movimiento Reducido

Soporte automático para `prefers-reduced-motion: reduce`.

## 🔧 Extensión del Sistema

### Agregar Nuevo Componente

1. Crear archivo en `components/`
2. Importar en `main.css`
3. Usar variables existentes
4. Seguir convenciones de nomenclatura

### Agregar Nuevas Variables

```css
/* En base/variables.css */
:root {
    --new-color: #value;
    --new-space: 1rem;
}
```

## 🚀 Performance

- **CSS crítico** cargado primero
- **Lazy loading** de componentes específicos
- **Purging** automático de CSS no usado
- **Optimización** de animaciones para 60fps

## 📋 Checklist de Implementación

- [ ] Cargar `main.css` en aplicación principal
- [ ] Implementar componentes usando clases modulares
- [ ] Probar responsive design en diferentes tamaños
- [ ] Validar accesibilidad y contraste
- [ ] Optimizar performance de animaciones
- [ ] Documentar componentes personalizados

---

## 💡 Tips de Uso

1. **Usa variables CSS** siempre que sea posible
2. **Combina clases utilitarias** para personalización rápida  
3. **Prefiere glass-card** sobre estilos custom para consistencia
4. **Usa animaciones** con moderación para mejor UX
5. **Testa en móvil** siempre por responsive design

¡Esta arquitectura CSS modular está diseñada para escalar con tu aplicación mientras mantiene consistencia y performance! 🎉