#!/usr/bin/env python3
"""
Cálculo de configuración óptima para archivos de 1000 comentarios
Target: Procesar 1000 comentarios en <60s manteniendo calidad y respetando rate limits
"""

import math

def calculate_optimal_config_for_1000_comments():
    """Calcular configuración óptima para 1000 comentarios"""
    
    print("🎯 OPTIMIZACIÓN PARA ARCHIVOS DE 1000 COMENTARIOS")
    print("=" * 55)
    
    # Parámetros base
    total_comments = 1000
    target_time_seconds = 60  # Target: 1 minuto máximo
    
    # OpenAI gpt-4o-mini limits (el modelo que usamos)
    rate_limit_requests_per_min = 200
    rate_limit_tokens_per_min = 2_000_000
    context_window = 16_384
    
    # Parámetros del sistema actual
    base_tokens = 1200  # JSON structure
    tokens_per_comment = 80  # Estimated
    buffer_percentage = 1.10  # 10% safety
    avg_request_time = 3.0  # seconds (incluye latency)
    
    print(f"📊 Target: {total_comments} comentarios en <{target_time_seconds}s")
    print(f"🤖 Modelo: gpt-4o-mini")
    print(f"🔄 Rate limits: {rate_limit_requests_per_min} req/min, {rate_limit_tokens_per_min:,} tokens/min")
    print()
    
    # CÁLCULO 1: Máximo comentarios por request (basado en context window)
    available_tokens = context_window - base_tokens
    max_comments_per_request = int(available_tokens / tokens_per_comment / buffer_percentage)
    
    print(f"📏 Context window: {context_window:,} tokens")
    print(f"💬 Máximo comentarios/request: {max_comments_per_request}")
    
    # CÁLCULO 2: Número de requests necesarios para diferentes batch sizes
    batch_sizes = [40, 50, 60, 70, 80, 90, 100]
    scenarios = []
    
    print(f"\n📈 ANÁLISIS DE BATCH SIZES:")
    print("-" * 40)
    
    for batch_size in batch_sizes:
        if batch_size > max_comments_per_request:
            continue
            
        # Calcular requests necesarios
        num_requests = math.ceil(total_comments / batch_size)
        
        # Tokens por request
        tokens_per_request = base_tokens + (batch_size * tokens_per_comment * buffer_percentage)
        total_tokens = num_requests * tokens_per_request
        
        # Tiempo estimado
        estimated_time = num_requests * avg_request_time
        
        # Rate limit validation
        requests_per_minute = num_requests / (estimated_time / 60) if estimated_time > 0 else 999
        tokens_per_minute = total_tokens / (estimated_time / 60) if estimated_time > 0 else 999
        
        within_rate_limits = (
            requests_per_minute <= rate_limit_requests_per_min and
            tokens_per_minute <= rate_limit_tokens_per_min
        )
        
        meets_target = estimated_time <= target_time_seconds
        
        scenario = {
            'batch_size': batch_size,
            'num_requests': num_requests,
            'tokens_per_request': int(tokens_per_request),
            'total_tokens': int(total_tokens),
            'estimated_time': estimated_time,
            'meets_target': meets_target,
            'within_rate_limits': within_rate_limits,
            'comments_per_second': total_comments / estimated_time,
            'requests_per_minute': requests_per_minute,
            'tokens_per_minute': tokens_per_minute
        }
        
        scenarios.append(scenario)
        
        # Display scenario
        status = "✅" if meets_target and within_rate_limits else "❌"
        print(f"{status} Batch {batch_size:2d}: {num_requests:2d} requests, {estimated_time:4.1f}s, {scenario['comments_per_second']:4.1f} c/s")
    
    # Find optimal scenarios
    valid_scenarios = [s for s in scenarios if s['meets_target'] and s['within_rate_limits']]
    
    if valid_scenarios:
        # Sort by efficiency (comments per second)
        valid_scenarios.sort(key=lambda x: x['comments_per_second'], reverse=True)
        
        print(f"\n🏆 TOP CONFIGURACIONES VÁLIDAS:")
        print("-" * 35)
        
        for i, scenario in enumerate(valid_scenarios[:3], 1):
            print(f"{i}. 📦 Batch size: {scenario['batch_size']}")
            print(f"   🔄 Requests: {scenario['num_requests']}")
            print(f"   🕐 Tiempo: {scenario['estimated_time']:.1f}s")
            print(f"   ⚡ Eficiencia: {scenario['comments_per_second']:.1f} comentarios/s")
            print(f"   🎯 Tokens/req: {scenario['tokens_per_request']:,}")
            print()
        
        # Recomendación
        best = valid_scenarios[0]
        print(f"🎯 RECOMENDACIÓN ÓPTIMA PARA 1000 COMENTARIOS:")
        print(f"  📦 MAX_COMMENTS_PER_BATCH = {best['batch_size']}")
        print(f"  🎯 OPENAI_MAX_TOKENS = {best['tokens_per_request'] + 1000}")  # Buffer extra
        print(f"  ⚡ Performance esperado: {best['estimated_time']:.1f}s para 1000 comentarios")
        print(f"  💰 Requests necesarios: {best['num_requests']} (costo ~${best['num_requests'] * 0.004:.3f})")
        
        return best
    
    else:
        print("❌ NO SE ENCONTRARON CONFIGURACIONES VÁLIDAS")
        print("🔧 Considerar:")
        print("  - Reducir batch size")
        print("  - Aumentar target time")
        print("  - Usar modelo con mayor context window")
        return None

def analyze_current_vs_optimal():
    """Comparar configuración actual vs óptima"""
    
    print(f"\n🔍 COMPARACIÓN: ACTUAL vs ÓPTIMA")
    print("=" * 40)
    
    # Configuración actual
    current_batch = 60
    current_max_tokens = 12000
    
    # Configuración óptima calculada
    optimal = calculate_optimal_config_for_1000_comments()
    
    if optimal:
        print(f"\n📊 CONFIGURACIÓN ACTUAL:")
        print(f"  📦 Batch size: {current_batch}")
        print(f"  🎯 Max tokens: {current_max_tokens:,}")
        
        # Calcular performance actual
        num_requests_current = math.ceil(1000 / current_batch)
        estimated_time_current = num_requests_current * 3.0  # 3s por request
        
        print(f"  🔄 Requests para 1000: {num_requests_current}")
        print(f"  ⏱️ Tiempo estimado: {estimated_time_current:.1f}s")
        
        print(f"\n📊 CONFIGURACIÓN ÓPTIMA:")
        print(f"  📦 Batch size: {optimal['batch_size']}")
        print(f"  🎯 Max tokens: {optimal['tokens_per_request'] + 1000:,}")
        print(f"  🔄 Requests para 1000: {optimal['num_requests']}")
        print(f"  ⏱️ Tiempo estimado: {optimal['estimated_time']:.1f}s")
        
        # Comparación
        improvement_ratio = estimated_time_current / optimal['estimated_time']
        print(f"\n💡 MEJORA POTENCIAL:")
        print(f"  ⚡ Speedup: {improvement_ratio:.1f}x más rápido")
        print(f"  📉 Requests: {num_requests_current} → {optimal['num_requests']} ({num_requests_current - optimal['num_requests']:+d})")
        
        if improvement_ratio > 1.2:
            print("🚀 RECOMENDACIÓN: Aplicar configuración óptima")
        else:
            print("✅ RECOMENDACIÓN: Configuración actual está bien optimizada")

if __name__ == "__main__":
    optimal_config = calculate_optimal_config_for_1000_comments()
    analyze_current_vs_optimal()
    
    if optimal_config:
        print(f"\n🔧 PARA APLICAR EN SECRETS.TOML:")
        print(f'MAX_COMMENTS_PER_BATCH = "{optimal_config["batch_size"]}"')
        print(f'OPENAI_MAX_TOKENS = "{optimal_config["tokens_per_request"] + 1000}"')
    
    print("\n✅ Análisis completado")