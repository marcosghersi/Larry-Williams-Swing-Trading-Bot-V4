# 🚀 Kraken Trading Bot V4 - Advanced AI System

Bot de trading de última generación con **Machine Learning**, **On-Chain Analysis**, **Sentiment Analysis**, **Multi-Strategy Ensemble** y **Reinforcement Learning**.

## 🆕 Novedades en V4

### 🎯 Nuevas Funcionalidades Avanzadas

#### 1. **📊 Sentiment Analysis** (CryptoCompare API)
- Análisis de noticias en tiempo real
- Métricas de redes sociales (Twitter, Reddit)
- Score de sentiment (-1 a +1)
- Filtrado de señales basado en sentiment del mercado

#### 2. **🔗 On-Chain Metrics**
- Exchange flows (deposits/withdrawals)
- Active addresses trend
- Transaction volume analysis
- Whale activity detection
- Señales blockchain específicas de crypto

#### 3. **🤝 Multi-Strategy Ensemble**
- **4 estrategias** ejecutándose en paralelo:
  - Swing Trading (detección de pivots)
  - Momentum Strategy (RSI + ROC)
  - Mean Reversion (Bollinger Bands)
  - Trend Following (MA crossovers)
- Sistema de **votación ponderada**
- Nivel de **consenso** entre estrategias
- Decisión final más robusta

#### 4. **🤖 Reinforcement Learning Position Sizing**
- Tamaño de posición **dinámico** basado en RL
- Aprende de trades anteriores
- Ajusta allocation y leverage según condiciones
- Q-Learning con estados discretizados
- Persiste conocimiento entre ejecuciones

---

## 📋 Requisitos

### APIs Necesarias

1. **Kraken API**
   - Account con margin trading
   - API key + secret con permisos de trading

2. **CryptoCompare API** (NUEVO)
   - Cuenta gratuita en [CryptoCompare](https://www.cryptocompare.com/)
   - API key para sentiment y on-chain data
   - Free tier: 100,000 calls/month

3. **Telegram Bot** (opcional)
   - Bot token
   - Chat ID

---

## 🚀 Setup Rápido

### 1. Configurar Secrets en GitHub

**Settings → Secrets and variables → Actions**

```
KRAKEN_API_KEY=tu_kraken_key
KRAKEN_API_SECRET=tu_kraken_secret
CRYPTOCOMPARE_API_KEY=tu_cryptocompare_key  # NUEVO
TELEGRAM_BOT_TOKEN=tu_telegram_token
TELEGRAM_CHAT_ID=tu_chat_id
```

### 2. Estructura de Archivos

```
tu-repo/
├── .github/
│   └── workflows/
│       └── trading-bot-v4.yml
├── kraken_bot_v3_multi_asset.py  # Bot base (V3)
├── sentiment_analyzer.py          # NUEVO
├── onchain_metrics.py             # NUEVO
├── ensemble_strategies.py         # NUEVO
├── rl_position_sizing.py          # NUEVO
├── requirements.txt               # Actualizado
└── README_V4.md
```

### 3. Actualizar requirements.txt

```txt
requests>=2.31.0
yfinance>=1.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
scikit-learn>=1.3.0  # Para ML adicional
```

---

## ⚙️ Configuración

### Variables de Entorno

En `trading-bot-v4.yml`:

```yaml
# APIs
KRAKEN_API_KEY: ${{ secrets.KRAKEN_API_KEY }}
KRAKEN_API_SECRET: ${{ secrets.KRAKEN_API_SECRET }}
CRYPTOCOMPARE_API_KEY: ${{ secrets.CRYPTOCOMPARE_API_KEY }}  # NUEVO

# Sentiment Analysis
USE_SENTIMENT_ANALYSIS: 'true'           # NUEVO
MIN_SENTIMENT_CONFIDENCE: '0.5'          # NUEVO

# On-Chain Analysis  
USE_ONCHAIN_ANALYSIS: 'true'             # NUEVO
MIN_ONCHAIN_STRENGTH: '0.5'              # NUEVO

# Ensemble System
USE_ENSEMBLE_SYSTEM: 'true'              # NUEVO
MIN_ENSEMBLE_CONSENSUS: '0.5'            # NUEVO
MIN_ENSEMBLE_CONFIDENCE: '0.5'           # NUEVO

# Reinforcement Learning
USE_RL_POSITION_SIZING: 'true'           # NUEVO
RL_LEARNING_RATE: '0.1'                  # NUEVO
RL_EPSILON: '0.1'                        # NUEVO

# Strategy Weights (Ensemble)
WEIGHT_SWING: '0.30'                     # NUEVO
WEIGHT_MOMENTUM: '0.25'                  # NUEVO
WEIGHT_MEAN_REVERSION: '0.25'            # NUEVO
WEIGHT_TREND_FOLLOWING: '0.20'           # NUEVO

# Trading (existing)
MAX_POSITIONS: '3'
LEVERAGE: '3'
STOP_LOSS_PCT: '4.0'
TAKE_PROFIT_PCT: '8.0'
# ... resto de configuración V3
```

---

## 🎮 Uso del Sistema

### Flujo de Decisión V4

```
1. Obtener datos de mercado (yfinance)
   ↓
2. Análisis Multi-Layer:
   ├─ Swing Detection (V3)
   ├─ Sentiment Analysis (NEWS + SOCIAL) ← NUEVO
   ├─ On-Chain Metrics (BLOCKCHAIN) ← NUEVO
   └─ Ensemble Strategies (4 estrategias) ← NUEVO
   ↓
3. Decisión Agregada:
   - Todas las capas deben estar alineadas
   - Consenso mínimo requerido
   - Confianza mínima requerida
   ↓
4. RL Position Sizing: ← NUEVO
   - Calcula estado del mercado
   - Selecciona mejor acción
   - Determina capital y leverage óptimos
   ↓
5. Ejecutar Trade
   ↓
6. Actualizar RL Agent:
   - Calcular reward
   - Actualizar Q-values
   - Guardar conocimiento
```

### Ejemplo de Salida

```
═══════════════════════════════════════════════════════════
KRAKEN TRADING BOT V4 - ADVANCED AI SYSTEM
═══════════════════════════════════════════════════════════
📅 2024-12-28 15:30:00
Mode: 🧪 SIMULATION

💰 Balance: 1,250.50 EUR
   Margin disponible: 1,100.00 EUR
   Posiciones abiertas: 1/3

🔍 Analizando BTC-USD...

   💭 Sentiment: Overall=0.45 (BULLISH)
      News=0.40, Social=0.50, Confidence=1.0
   
   🔗 OnChain: BULLISH (strength: 0.65)
      Metrics: exchange_flow=0.3, address_trend=0.4

   📊 ENSEMBLE DECISION
   Signal: BUY
   Confidence: 78%
   Consensus: 75% (3/4 strategies agree)
   
   Individual votes:
   ✓ swing: BUY (0.85)
   ✓ momentum: BUY (0.70)
   ✗ mean_reversion: NONE (0.00)
   ✓ trend_following: BUY (0.65)

   🤖 RL Position Sizing:
      State: vol=0.025, trend=0.08, wr=0.60
      Decision: $400.00 @ 4x leverage
      (Alloc: 40%, Lev mult: 1.3x)

🟢 Abriendo BUY en BTC-USD
   Precio: $42,350.00
   Volumen: 0.0094
   Leverage: 4x
   Margen: 400.00 EUR
   
   Confianza Ensemble: 78%
   Sentiment: BULLISH (0.45)
   OnChain: BULLISH (0.65)

✅ Orden ejecutada
```

---

## 📊 Sistema Ensemble Detallado

### Estrategias Incluidas

#### 1. **Swing Trading**
- Detección de intermediate highs/lows
- Validación con volumen
- ML scoring de calidad

#### 2. **Momentum Strategy**
- RSI (Relative Strength Index)
- Rate of Change (ROC)
- Confirmación de volumen
- Detecta breakouts y reversiones

#### 3. **Mean Reversion**
- Bollinger Bands
- Oversold/Overbought zones
- Ideal para mercados laterales

#### 4. **Trend Following**
- Moving Average crossovers
- Golden/Death crosses
- Trend strength measurement

### Pesos por Defecto

| Estrategia | Peso | Cuándo es Mejor |
|------------|------|------------------|
| Swing | 30% | Mercados con rangos definidos |
| Momentum | 25% | Breakouts y tendencias fuertes |
| Mean Reversion | 25% | Mercados laterales |
| Trend Following | 20% | Tendencias sostenidas |

**Personalizable** en configuración.

---

## 🤖 Reinforcement Learning

### ¿Cómo Funciona?

1. **Estado del Mercado** (6 features):
   - Volatilidad actual
   - Fuerza de tendencia
   - Win rate reciente
   - Drawdown actual
   - Posiciones abiertas
   - Confianza de señal

2. **Acciones Disponibles** (15 combinaciones):
   - Allocation: 20%, 33%, 50%, 70%, 100%
   - Leverage multiplier: 0.5x, 1.0x, 1.5x

3. **Recompensas**:
   - Basadas en PnL% del trade
   - Bonificación por trades grandes ganadores
   - Penalización por grandes pérdidas
   - Bonus por uso correcto de stops

4. **Aprendizaje**:
   - Q-Learning con estados discretizados
   - Epsilon-greedy exploration (10%)
   - Learning rate: 0.1
   - Discount factor: 0.95

### Persistencia

- Q-table se guarda en `rl_state.json`
- Se carga automáticamente en cada ejecución
- Mejora con el tiempo según resultados

---

## 🔬 Backtesting

El sistema V4 es compatible con el backtester V3 existente. Para integrar las nuevas funcionalidades:

### Backtesting con Ensemble

```python
# En backtest_v3_walkforward.py, modificar:

from ensemble_strategies import EnsembleSystem

class BacktesterV4(BacktesterV3):
    def __init__(self, config, market_data):
        super().__init__(config, market_data)
        self.ensemble = EnsembleSystem()
    
    def _look_for_signals(self, current_date, current_prices):
        # ... código existente ...
        
        for symbol, data in data_up_to_date.items():
            # Swing signal
            signal, signal_price, confidence = self.detectors[symbol].get_signal_at_date(current_date)
            
            if signal:
                # Verificar con ensemble
                ensemble_decision = self.ensemble.get_ensemble_decision(
                    data, (signal, signal_price, confidence)
                )
                
                if (ensemble_decision.final_signal == signal and 
                    ensemble_decision.consensus_level > 0.5):
                    # Proceder con el trade
                    pass
```

---

## 📈 Métricas y Monitoring

### Nuevas Métricas V4

1. **Sentiment Accuracy**
   - Correlación sentiment vs performance
   - True positive rate de señales bullish/bearish

2. **Ensemble Performance**
   - Win rate por estrategia individual
   - Consenso promedio en trades ganadores vs perdedores
   - Contribución de cada estrategia al PnL total

3. **RL Learning Progress**
   - Evolución de Q-values
   - Exploration vs exploitation ratio
   - Reward promedio por episodio

4. **On-Chain Signal Accuracy**
   - Precisión de exchange flow signals
   - Active addresses correlation con price movement

### Dashboard Sugerido

```python
import matplotlib.pyplot as plt

def plot_v4_metrics(trades_df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # 1. Sentiment vs Performance
    axes[0,0].scatter(trades_df['sentiment_score'], 
                     trades_df['pnl_pct'])
    axes[0,0].set_title('Sentiment vs PnL')
    
    # 2. Ensemble Consensus Distribution
    axes[0,1].hist(trades_df['ensemble_consensus'], bins=20)
    axes[0,1].set_title('Ensemble Consensus')
    
    # 3. RL Allocation Over Time
    axes[1,0].plot(trades_df['date'], 
                  trades_df['rl_allocation'])
    axes[1,0].set_title('RL Position Sizing Evolution')
    
    # 4. Strategy Win Rates
    strategy_wr = trades_df.groupby('winning_strategy')['is_win'].mean()
    axes[1,1].bar(strategy_wr.index, strategy_wr.values)
    axes[1,1].set_title('Win Rate by Strategy')
    
    plt.tight_layout()
    plt.savefig('v4_metrics.png')
```

---

## 🎯 Estrategias Recomendadas

### Perfil Conservador

```yaml
# Configuración conservadora con IA
MAX_POSITIONS: '2'
LEVERAGE: '2'

# Sentiment & OnChain muy estrictos
MIN_SENTIMENT_CONFIDENCE: '0.7'
MIN_ONCHAIN_STRENGTH: '0.7'

# Ensemble requiere alto consenso
MIN_ENSEMBLE_CONSENSUS: '0.75'  # 3/4 estrategias deben coincidir
MIN_ENSEMBLE_CONFIDENCE: '0.7'

# RL explorará menos
RL_EPSILON: '0.05'

# Pesos equilibrados
WEIGHT_SWING: '0.25'
WEIGHT_MOMENTUM: '0.25'
WEIGHT_MEAN_REVERSION: '0.30'  # Mayor en laterales
WEIGHT_TREND_FOLLOWING: '0.20'
```

### Perfil Agresivo (IA Experimental)

```yaml
MAX_POSITIONS: '4'
LEVERAGE: '5'

# Menos restrictivo
MIN_SENTIMENT_CONFIDENCE: '0.3'
MIN_ONCHAIN_STRENGTH: '0.3'

# Menor consenso requerido
MIN_ENSEMBLE_CONSENSUS: '0.5'  # 2/4 basta
MIN_ENSEMBLE_CONFIDENCE: '0.5'

# RL explora más
RL_EPSILON: '0.2'  # 20% exploración

# Pesos a momentum y trend
WEIGHT_SWING: '0.20'
WEIGHT_MOMENTUM: '0.35'  # Más agresivo
WEIGHT_MEAN_REVERSION: '0.15'
WEIGHT_TREND_FOLLOWING: '0.30'
```

### Perfil Balanced (Recomendado)

```yaml
MAX_POSITIONS: '3'
LEVERAGE: '3'

MIN_SENTIMENT_CONFIDENCE: '0.5'
MIN_ONCHAIN_STRENGTH: '0.5'

MIN_ENSEMBLE_CONSENSUS: '0.6'
MIN_ENSEMBLE_CONFIDENCE: '0.6'

RL_EPSILON: '0.1'

# Pesos default
WEIGHT_SWING: '0.30'
WEIGHT_MOMENTUM: '0.25'
WEIGHT_MEAN_REVERSION: '0.25'
WEIGHT_TREND_FOLLOWING: '0.20'
```

---

## 🔧 Troubleshooting

### CryptoCompare API Issues

**Error: API key invalid**
- Verifica que el secret esté configurado correctamente
- Asegúrate de que la key esté activa en CryptoCompare

**Error: Rate limit exceeded**
- Free tier: 100k calls/month
- Añade más cache en los módulos
- Aumenta `cache_duration` en analyzers

### RL No Mejora

**Síntomas**: Q-values no cambian, siempre misma acción
- Verifica que `rl_state.json` se esté guardando
- Aumenta `RL_EPSILON` para más exploración
- Revisa que rewards se estén calculando correctamente

**Solución**: Elimina `rl_state.json` para reset completo

### Ensemble Nunca Opera

**Síntomas**: Siempre sin señal o consenso muy bajo
- Reduce `MIN_ENSEMBLE_CONSENSUS` (ej: 0.5)
- Ajusta pesos de estrategias
- Verifica que datos tengan suficiente historial (180 días)

---

## 📚 Documentación API

### Sentiment Analyzer

```python
from sentiment_analyzer import SentimentAnalyzer, should_trade_based_on_sentiment

analyzer = SentimentAnalyzer(api_key)
sentiment = analyzer.get_sentiment('BTC')

print(f"Overall: {sentiment.overall_score}")
print(f"Bullish: {sentiment.is_bullish()}")
print(f"Bearish: {sentiment.is_bearish()}")

# Usar en decisión
can_trade = should_trade_based_on_sentiment(
    sentiment, 'BUY', min_confidence=0.5
)
```

### On-Chain Analyzer

```python
from onchain_metrics import OnChainAnalyzer, should_trade_based_on_onchain

analyzer = OnChainAnalyzer(api_key)
signal = analyzer.get_onchain_signal('BTC')

print(f"Signal: {signal.signal_type}")
print(f"Strength: {signal.strength}")
print(f"Metrics: {signal.metrics}")

can_trade = should_trade_based_on_onchain(
    signal, 'BUY', min_strength=0.5
)
```

### Ensemble System

```python
from ensemble_strategies import EnsembleSystem

ensemble = EnsembleSystem(weights={...})
decision = ensemble.get_ensemble_decision(data, swing_signal)

print(f"Final: {decision.final_signal}")
print(f"Confidence: {decision.confidence}")
print(f"Consensus: {decision.consensus_level}")

ensemble.print_decision_summary(decision)
```

### RL Position Sizer

```python
from rl_position_sizing import RLPositionSizer, PositionSizeCalculator

rl_sizer = RLPositionSizer()
calculator = PositionSizeCalculator(rl_sizer)

capital, leverage = calculator.get_optimal_size(
    data=market_data,
    signal_confidence=0.75,
    available_capital=1000,
    base_leverage=3,
    open_positions=1,
    recent_trades=trades_history,
    training=True
)

# Después del trade
reward = rl_sizer.calculate_reward(trade_result)
rl_sizer.update_q_value(state, action_idx, reward, next_state)
rl_sizer.save_state()
```

---

## 🚦 Roadmap Futuro

### V4.1 - Short Term
- [ ] Integración con más fuentes de sentiment (Twitter API v2)
- [ ] Métricas on-chain desde Glassnode/CryptoQuant
- [ ] Dashboard web en tiempo real
- [ ] Backtesting completo con todas las features V4

### V4.2 - Medium Term  
- [ ] Deep RL (DQN/PPO) en lugar de Q-Learning
- [ ] Ensemble con meta-learning
- [ ] Optimización bayesiana de hiperparámetros
- [ ] Multi-timeframe analysis

### V5.0 - Long Term
- [ ] LLM integration para análisis de noticias
- [ ] Predicción de volatilidad con LSTM
- [ ] Portfolio optimization con Markowitz
- [ ] Auto-tuning completo del sistema

---

## 📄 Licencia

MIT License - Usa bajo tu propio riesgo

---

## ⚠️ Disclaimer

**Este bot es experimental y educativo.**

- Los mercados son impredecibles
- RL y ML pueden fallar en condiciones no vistas
- SIEMPRE empieza en modo simulación
- No inviertas más de lo que puedes perder
- Monitorea el bot constantemente
- Las APIs externas pueden fallar o cambiar
- El performance pasado no garantiza resultados futuros

**El sistema V4 es más complejo = más puntos de falla potenciales.**

---

## 🆘 Soporte

### Logs y Debug

1. GitHub Actions → Workflow runs → Ver logs
2. Buscar errores en cada módulo:
   - `sentiment_analyzer`
   - `onchain_metrics`
   - `ensemble_strategies`
   - `rl_position_sizing`

### Issues Comunes

- **No genera señales**: Ajusta thresholds, verifica datos
- **RL siempre explora**: Normal al inicio, converge tras ~50 trades
- **Sentiment siempre neutral**: Verifica API key, revisa rate limits
- **Ensemble indeciso**: Reduce `MIN_ENSEMBLE_CONSENSUS`

---

## 🙏 Contribuciones

Pull requests bienvenidos para:
- Nuevas estrategias para ensemble
- Mejoras en RL agent
- Más fuentes de sentiment/on-chain
- Optimizaciones de performance
- Documentación

---

## 📞 Contacto

Para dudas técnicas o reportar bugs, abre un Issue en GitHub.

---

**🚀 Happy AI Trading!**

*V4.0 - Advanced AI System - Diciembre 2024*

# 🔄 Cambios Clave en trading-bot-v4.yml

## ✅ Archivo Actualizado

Reemplaza tu `trading-bot-v4.yml` actual por la nueva versión.

---

## 📝 Cambios Principales

### 1. **Nombre del archivo ejecutable corregido**

```yaml
# ANTES (en tu archivo original):
python kraken_bot_v4_advanced.py

# AHORA (actualizado):
python kraken_bot_v4_advanced.py  # ✓ Nombre correcto
```

### 2. **Cache del RL State mejorado**

```yaml
# ANTES: Cache básico
- uses: actions/cache@v3

# AHORA: Cache con restore-keys mejorado
- name: 📂 Cargar RL State
  uses: actions/cache@v3
  with:
    path: rl_state.json
    key: rl-state-${{ github.run_number }}
    restore-keys: |
      rl-state-    # ✓ Busca estados previos
```

**Beneficio:** El RL agent mantiene su aprendizaje entre ejecuciones.

### 3. **Variables de entorno organizadas**

```yaml
# Ahora con secciones claras:
# ═══ APIS ═══
# ═══ SENTIMENT ANALYSIS (V4) ═══
# ═══ ON-CHAIN ANALYSIS (V4) ═══
# ═══ ENSEMBLE (V4) ═══
# ═══ RL (V4) ═══
# ═══ MULTI-ASSET (V3) ═══
# ═══ RISK MANAGEMENT ═══
# ═══ STRATEGY (V3) ═══
# ═══ MODE ═══
```

**Beneficio:** Más fácil de entender y modificar.

### 4. **Inputs manuales para testing**

```yaml
workflow_dispatch:
  inputs:
    dry_run: 'true'
    use_sentiment: 'true'   # ✓ Activar/desactivar individualmente
    use_onchain: 'true'
    use_ensemble: 'true'
    use_rl: 'true'
```

**Beneficio:** Puedes probar cada feature por separado.

### 5. **Echo mejorado con info del bot**

```yaml
run: |
  echo "🤖 AI Features V4:"
  echo "   Sentiment Analysis: $USE_SENTIMENT_ANALYSIS"
  echo "   On-Chain Metrics: $USE_ONCHAIN_ANALYSIS"
  echo "   Ensemble System: $USE_ENSEMBLE_SYSTEM"
  echo "   RL Position Sizing: $USE_RL_POSITION_SIZING"
```

**Beneficio:** Ves inmediatamente qué features están activas.

---

## 🎯 Configuraciones Recomendadas

### Para Testing Inicial

```yaml
# En las variables de entorno, ajusta:
DRY_RUN: 'true'              # ✓ SIMULACIÓN
MAX_POSITIONS: '1'           # ✓ Solo 1 posición
LEVERAGE: '2'                # ✓ Leverage bajo
MIN_ENSEMBLE_CONSENSUS: '0.75'  # ✓ Muy conservador
```

### Para Producción Conservadora

```yaml
DRY_RUN: 'false'             # ⚠️ REAL
MAX_POSITIONS: '2'
LEVERAGE: '3'
MIN_ENSEMBLE_CONSENSUS: '0.6'
MIN_SENTIMENT_CONFIDENCE: '0.6'
MIN_ONCHAIN_STRENGTH: '0.6'
```

### Para Producción Agresiva

```yaml
DRY_RUN: 'false'             # ⚠️ REAL
MAX_POSITIONS: '3'
LEVERAGE: '4'
MIN_ENSEMBLE_CONSENSUS: '0.5'
MIN_SENTIMENT_CONFIDENCE: '0.4'
MIN_ONCHAIN_STRENGTH: '0.4'
RL_EPSILON: '0.15'           # Más exploración
```

---

## 🔍 Cómo Ejecutar Manualmente

### 1. Ve a tu repositorio en GitHub

### 2. Click en "Actions"

### 3. Selecciona "Kraken Trading Bot V4 - Advanced AI"

### 4. Click "Run workflow"

### 5. Configura opciones:

```
dry_run: true               ← Empieza con simulación
use_sentiment: true         ← Activa sentiment
use_onchain: true          ← Activa on-chain
use_ensemble: true         ← Activa ensemble
use_rl: true               ← Activa RL
```

### 6. Click "Run workflow" (verde)

### 7. Espera 2-3 minutos

### 8. Revisa los logs:
- Click en el workflow que acaba de ejecutarse
- Click en "trade"
- Verás todos los logs del bot

---

## 📊 Qué Esperar en los Logs

### Inicio:
```
════════════════════════════════════════════════════════════════════
🚀 KRAKEN TRADING BOT V4 - ADVANCED AI SYSTEM
════════════════════════════════════════════════════════════════════
📅 2024-12-28 15:30:00
🎯 Mode: SIMULATION

🤖 AI Features V4:
   Sentiment Analysis: true
   On-Chain Metrics: true
   Ensemble System: true
   RL Position Sizing: true
════════════════════════════════════════════════════════════════════
```

### Durante ejecución:
```
🚀 INITIALIZING KRAKEN TRADING BOT V4
   ✓ Sentiment Analyzer activado
   ✓ On-Chain Analyzer activado
   ✓ Ensemble System activado
   ✓ RL Position Sizing activado

💰 Balance: 1,250.50 EUR
   Margen disponible: 1,100.00 EUR

📊 Descargando datos multi-asset...
   ✓ BTC-USD: 4320 velas
   ✓ ETH-USD: 4320 velas
   ...

🔍 Buscando señales con análisis V4...

   🎯 BTC-USD: Señal BUY detectada

   📊 Layer 1: Sentiment Analysis
   ✓ Sentiment confirma

   🔗 Layer 2: On-Chain Metrics
   ✓ On-Chain confirma

   🎯 Layer 3: Ensemble Strategies
   ✓ Ensemble confirma con 75% consenso

   🤖 Layer 4: RL Position Sizing
   RL: $400.00 @ 3x

✅ DECISIÓN: BUY
   Confianza final: 78%

🟢 Abriendo BUY en BTC-USD
   ...
```

---

## ⚠️ Errores Comunes

### Error: "CRYPTOCOMPARE_API_KEY not set"

**Solución:**
1. Ve a Settings → Secrets → Actions
2. Agrega `CRYPTOCOMPARE_API_KEY`
3. Valor: tu key de CryptoCompare

### Error: "Module 'sentiment_analyzer' not found"

**Solución:**
```bash
# Verifica que todos los archivos V4 estén en el repo:
git add sentiment_analyzer.py
git add onchain_metrics.py
git add ensemble_strategies.py
git add rl_position_sizing.py
git commit -m "Add V4 modules"
git push
```

### Error: "kraken_bot_v4_advanced.py: No such file"

**Solución:**
```bash
# Asegúrate que el archivo principal está:
git add kraken_bot_v4_advanced.py
git commit -m "Add V4 main bot"
git push
```

---

## 🔄 Ejecución Automática

El workflow se ejecuta **automáticamente cada 15 minutos**.

Para cambiar la frecuencia:

```yaml
schedule:
  - cron: '*/30 * * * *'  # Cada 30 minutos
  # O
  - cron: '0 * * * *'     # Cada hora
  # O
  - cron: '0 */2 * * *'   # Cada 2 horas
```

---

## ✅ Checklist Final

Antes de hacer push:

- [ ] `trading-bot-v4.yml` actualizado en `.github/workflows/`
- [ ] `kraken_bot_v4_advanced.py` en la raíz del repo
- [ ] Todos los módulos V4 presentes:
  - [ ] `sentiment_analyzer.py`
  - [ ] `onchain_metrics.py`
  - [ ] `ensemble_strategies.py`
  - [ ] `rl_position_sizing.py`
- [ ] `requirements.txt` actualizado
- [ ] Secrets configurados en GitHub:
  - [ ] `KRAKEN_API_KEY`
  - [ ] `KRAKEN_API_SECRET`
  - [ ] `CRYPTOCOMPARE_API_KEY`
  - [ ] `TELEGRAM_BOT_TOKEN` (opcional)
  - [ ] `TELEGRAM_CHAT_ID` (opcional)

---

## 🚀 Comando para subir todo

```bash
# 1. Agregar todos los archivos nuevos
git add .github/workflows/trading-bot-v4.yml
git add kraken_bot_v4_advanced.py
git add sentiment_analyzer.py
git add onchain_metrics.py
git add ensemble_strategies.py
git add rl_position_sizing.py
git add requirements.txt

# 2. Commit
git commit -m "Add complete V4 system with AI features"

# 3. Push
git push

# 4. Ve a GitHub Actions y ejecuta manualmente
```

---

**🎉 ¡Workflow actualizado y listo para V4!**
