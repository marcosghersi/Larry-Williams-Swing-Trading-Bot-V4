"""
REINFORCEMENT LEARNING POSITION SIZING
Sistema RL para determinar tamaño óptimo de posiciones dinámicamente

Implementa un agente RL simplificado que aprende:
- Cuánto capital asignar por trade basado en condiciones de mercado
- Ajuste dinámico según performance reciente
- Gestión de riesgo adaptativa
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class MarketState:
    """Estado del mercado para RL."""
    volatility: float  # Volatilidad actual
    trend_strength: float  # Fuerza de tendencia
    win_rate_recent: float  # Win rate últimos trades
    drawdown_current: float  # Drawdown actual
    positions_open: int  # Número de posiciones abiertas
    confidence_signal: float  # Confianza de la señal actual
    
    def to_array(self) -> np.ndarray:
        """Convierte estado a array numpy."""
        return np.array([
            self.volatility,
            self.trend_strength,
            self.win_rate_recent,
            self.drawdown_current,
            self.positions_open / 5,  # Normalizar (max 5 posiciones)
            self.confidence_signal
        ])


@dataclass
class PositionSizingAction:
    """Acción de position sizing."""
    allocation_pct: float  # % del capital disponible (0.0 - 1.0)
    leverage_multiplier: float  # Multiplicador del leverage base
    
    def __repr__(self):
        return f"Alloc: {self.allocation_pct:.1%}, Lev: {self.leverage_multiplier:.1f}x"


class RLPositionSizer:
    """
    Agente RL para position sizing dinámico.
    
    Usa Q-Learning simplificado con estados discretizados.
    """
    
    def __init__(self, 
                 learning_rate: float = 0.1,
                 discount_factor: float = 0.95,
                 epsilon: float = 0.1,
                 state_file: str = "rl_state.json"):
        """
        Args:
            learning_rate: Tasa de aprendizaje (alpha)
            discount_factor: Factor de descuento (gamma)
            epsilon: Probabilidad de exploración
            state_file: Archivo para persistir Q-table
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.state_file = state_file
        
        # Q-table: state -> action -> Q-value
        self.q_table: Dict[str, Dict[int, float]] = {}
        
        # Acciones disponibles (discretizadas)
        self.actions = self._define_actions()
        
        # Historial
        self.history = []
        
        # Cargar estado previo si existe
        self.load_state()
    
    def _define_actions(self) -> List[PositionSizingAction]:
        """
        Define espacio de acciones discreto.
        
        Returns:
            Lista de acciones posibles
        """
        actions = []
        
        # Combinaciones de allocation y leverage
        allocations = [0.2, 0.33, 0.5, 0.7, 1.0]  # % del capital
        leverage_mults = [0.5, 1.0, 1.5]  # Multiplicador del leverage base
        
        for alloc in allocations:
            for lev_mult in leverage_mults:
                actions.append(PositionSizingAction(alloc, lev_mult))
        
        return actions
    
    def _discretize_state(self, state: MarketState) -> str:
        """
        Discretiza estado continuo a string para Q-table.
        """
        # Discretizar cada componente
        vol_bucket = int(min(4, state.volatility * 100))  # 0-4
        trend_bucket = int(min(2, abs(state.trend_strength) * 10))  # 0-2
        winrate_bucket = int(state.win_rate_recent * 2)  # 0-2 (0-50%, 50-100%)
        dd_bucket = int(min(3, abs(state.drawdown_current) * 10))  # 0-3
        pos_bucket = min(3, state.positions_open)  # 0-3
        conf_bucket = int(state.confidence_signal * 3)  # 0-3
        
        return f"{vol_bucket}_{trend_bucket}_{winrate_bucket}_{dd_bucket}_{pos_bucket}_{conf_bucket}"
    
    def select_action(self, state: MarketState, training: bool = True) -> Tuple[int, PositionSizingAction]:
        """
        Selecciona acción usando epsilon-greedy.
        
        Args:
            state: Estado del mercado
            training: Si True, usa exploración
        
        Returns:
            (action_index, action)
        """
        state_key = self._discretize_state(state)
        
        # Exploración vs explotación
        if training and np.random.random() < self.epsilon:
            # Exploración: acción aleatoria
            action_idx = np.random.randint(len(self.actions))
        else:
            # Explotación: mejor acción conocida
            if state_key not in self.q_table:
                self.q_table[state_key] = {i: 0.0 for i in range(len(self.actions))}
            
            q_values = self.q_table[state_key]
            action_idx = max(q_values.items(), key=lambda x: x[1])[0]
        
        return action_idx, self.actions[action_idx]
    
    def update_q_value(self, state: MarketState, action_idx: int, 
                      reward: float, next_state: Optional[MarketState] = None):
        """
        Actualiza Q-value usando Q-learning.
        
        Q(s,a) = Q(s,a) + α * [reward + γ * max(Q(s',a')) - Q(s,a)]
        """
        state_key = self._discretize_state(state)
        
        # Inicializar si es nuevo estado
        if state_key not in self.q_table:
            self.q_table[state_key] = {i: 0.0 for i in range(len(self.actions))}
        
        current_q = self.q_table[state_key][action_idx]
        
        # Calcular max Q del siguiente estado
        if next_state:
            next_state_key = self._discretize_state(next_state)
            if next_state_key not in self.q_table:
                self.q_table[next_state_key] = {i: 0.0 for i in range(len(self.actions))}
            max_next_q = max(self.q_table[next_state_key].values())
        else:
            max_next_q = 0.0
        
        # Actualizar Q-value
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        
        self.q_table[state_key][action_idx] = new_q
    
    def calculate_reward(self, trade_result: Dict) -> float:
        """
        Calcula recompensa basada en resultado del trade.
        
        Args:
            trade_result: Dict con 'pnl_pct', 'closed', etc.
        
        Returns:
            Reward value
        """
        if not trade_result.get('closed', False):
            return 0.0  # Sin reward si trade aún abierto
        
        pnl_pct = trade_result.get('pnl_pct', 0.0)
        
        # Reward basado en PnL con penalización por drawdown
        base_reward = pnl_pct / 10  # Normalizar
        
        # Bonificación por trades ganadores grandes
        if pnl_pct > 5.0:
            base_reward *= 1.5
        
        # Penalización por trades perdedores grandes
        elif pnl_pct < -3.0:
            base_reward *= 1.5
        
        # Bonificación por gestión de riesgo (usar stop loss)
        if trade_result.get('exit_reason') in ['Stop Loss', 'Trailing']:
            base_reward *= 1.1
        
        return base_reward
    
    def get_position_size(self, 
                         state: MarketState,
                         available_capital: float,
                         base_leverage: int,
                         training: bool = False) -> Tuple[float, int]:
        """
        Determina tamaño de posición y leverage usando RL.
        
        Args:
            state: Estado actual del mercado
            available_capital: Capital disponible
            base_leverage: Leverage base configurado
            training: Si está en modo entrenamiento
        
        Returns:
            (capital_to_use, adjusted_leverage)
        """
        action_idx, action = self.select_action(state, training=training)
        
        # Calcular tamaño basado en acción
        capital_to_use = available_capital * action.allocation_pct
        adjusted_leverage = int(base_leverage * action.leverage_multiplier)
        
        # Límites de seguridad
        adjusted_leverage = max(1, min(5, adjusted_leverage))
        
        # Registrar para posterior actualización
        self.history.append({
            'timestamp': datetime.now(),
            'state': state,
            'action_idx': action_idx,
            'action': action,
            'capital': capital_to_use,
            'leverage': adjusted_leverage
        })
        
        return capital_to_use, adjusted_leverage
    
    def save_state(self):
        """Guarda Q-table a archivo."""
        try:
            state_data = {
                'q_table': {k: dict(v) for k, v in self.q_table.items()},
                'metadata': {
                    'last_update': datetime.now().isoformat(),
                    'num_states': len(self.q_table),
                    'learning_rate': self.learning_rate,
                    'epsilon': self.epsilon
                }
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
            
            print(f"   💾 RL state saved: {len(self.q_table)} states")
            
        except Exception as e:
            print(f"   ⚠️ Error saving RL state: {e}")
    
    def load_state(self):
        """Carga Q-table desde archivo."""
        try:
            with open(self.state_file, 'r') as f:
                state_data = json.load(f)
            
            # Restaurar Q-table
            self.q_table = {
                k: {int(action): value for action, value in actions.items()}
                for k, actions in state_data['q_table'].items()
            }
            
            metadata = state_data.get('metadata', {})
            print(f"   📁 RL state loaded: {metadata.get('num_states', 0)} states")
            print(f"      Last update: {metadata.get('last_update', 'unknown')}")
            
        except FileNotFoundError:
            print(f"   ℹ️ No previous RL state found, starting fresh")
        except Exception as e:
            print(f"   ⚠️ Error loading RL state: {e}")


class PositionSizeCalculator:
    """Helper para calcular tamaño de posición con RL."""
    
    def __init__(self, rl_sizer: RLPositionSizer):
        self.rl_sizer = rl_sizer
        self.recent_trades = []
    
    def calculate_market_state(self,
                              data: pd.DataFrame,
                              signal_confidence: float,
                              open_positions: int,
                              recent_trades: List[Dict]) -> MarketState:
        """
        Calcula estado del mercado para RL.
        """
        # Volatilidad
        returns = data['Close'].pct_change().tail(20)
        volatility = returns.std()
        
        # Trend strength
        ma_fast = data['Close'].tail(10).mean()
        ma_slow = data['Close'].tail(50).mean()
        trend_strength = (ma_fast - ma_slow) / ma_slow if ma_slow > 0 else 0.0
        
        # Win rate recent
        if recent_trades:
            wins = sum(1 for t in recent_trades[-10:] if t.get('pnl_pct', 0) > 0)
            win_rate = wins / min(10, len(recent_trades))
        else:
            win_rate = 0.5  # Neutral
        
        # Drawdown
        equity_curve = [1000]  # Simular desde capital inicial
        for trade in recent_trades:
            pnl = trade.get('pnl_dollars', 0)
            equity_curve.append(equity_curve[-1] + pnl)
        
        peak = max(equity_curve)
        current = equity_curve[-1]
        drawdown = (peak - current) / peak if peak > 0 else 0.0
        
        return MarketState(
            volatility=volatility,
            trend_strength=trend_strength,
            win_rate_recent=win_rate,
            drawdown_current=drawdown,
            positions_open=open_positions,
            confidence_signal=signal_confidence
        )
    
    def get_optimal_size(self,
                        data: pd.DataFrame,
                        signal_confidence: float,
                        available_capital: float,
                        base_leverage: int,
                        open_positions: int,
                        recent_trades: List[Dict],
                        training: bool = False) -> Tuple[float, int]:
        """
        Obtiene tamaño óptimo de posición usando RL.
        
        Returns:
            (capital_to_use, leverage_to_use)
        """
        # Calcular estado
        state = self.calculate_market_state(
            data, signal_confidence, open_positions, recent_trades
        )
        
        # Obtener decisión RL
        capital, leverage = self.rl_sizer.get_position_size(
            state, available_capital, base_leverage, training
        )
        
        print(f"   🤖 RL Position Sizing:")
        print(f"      State: vol={state.volatility:.3f}, trend={state.trend_strength:.2f}, "
              f"wr={state.win_rate_recent:.2f}")
        print(f"      Decision: ${capital:.2f} @ {leverage}x")
        
        return capital, leverage
