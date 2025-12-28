"""
ON-CHAIN METRICS ANALYZER
Analiza métricas blockchain para señales de trading

Métricas incluidas:
- Exchange flows (deposits/withdrawals)
- Active addresses
- Transaction volume
- Network hash rate (BTC)
- Whale activity
"""

import requests
import time
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class OnChainSignal:
    """Señal derivada de métricas on-chain."""
    signal_type: str  # 'BULLISH', 'BEARISH', 'NEUTRAL'
    strength: float  # 0.0 a 1.0
    metrics: Dict[str, float]
    timestamp: datetime
    
    def is_strong_signal(self, threshold: float = 0.6) -> bool:
        return self.strength >= threshold


class OnChainAnalyzer:
    """
    Analiza métricas on-chain para generar señales.
    
    Fuentes de datos:
    - CryptoCompare API (blockchain stats)
    - Datos públicos de exchanges vía APIs
    """
    
    def __init__(self, cryptocompare_api_key: str):
        self.api_key = cryptocompare_api_key
        self.base_url = "https://min-api.cryptocompare.com"
        self.session = requests.Session()
        self.cache = {}
        self.cache_duration = 600  # 10 minutos
    
    def get_onchain_signal(self, symbol: str) -> Optional[OnChainSignal]:
        """
        Analiza métricas on-chain y genera señal.
        
        Args:
            symbol: Símbolo crypto (BTC, ETH, etc.)
        
        Returns:
            OnChainSignal o None
        """
        clean_symbol = symbol.split('-')[0].upper()
        
        # Check cache
        cache_key = f"{clean_symbol}_{int(time.time() / self.cache_duration)}"
        if cache_key in self.cache:
            print(f"   🔗 OnChain cache hit: {clean_symbol}")
            return self.cache[cache_key]
        
        try:
            metrics = {}
            
            # 1. Blockchain stats
            blockchain_data = self._get_blockchain_stats(clean_symbol)
            if blockchain_data:
                metrics.update(blockchain_data)
            
            # 2. Exchange flows (si disponible)
            exchange_flow = self._analyze_exchange_flows(clean_symbol)
            if exchange_flow:
                metrics['exchange_flow_signal'] = exchange_flow
            
            # 3. Active addresses trend
            address_trend = self._get_active_addresses_trend(clean_symbol)
            if address_trend:
                metrics['address_trend'] = address_trend
            
            if not metrics:
                return None
            
            # Calcular señal agregada
            signal_type, strength = self._calculate_signal(metrics)
            
            onchain_signal = OnChainSignal(
                signal_type=signal_type,
                strength=strength,
                metrics=metrics,
                timestamp=datetime.now()
            )
            
            # Cache
            self.cache[cache_key] = onchain_signal
            
            print(f"   🔗 OnChain {clean_symbol}: {signal_type} (strength: {strength:.2f})")
            print(f"      Metrics: {metrics}")
            
            return onchain_signal
            
        except Exception as e:
            print(f"   ⚠️ Error en onchain analysis: {e}")
            return None
    
    def _get_blockchain_stats(self, symbol: str) -> Optional[Dict]:
        """Obtiene estadísticas de blockchain."""
        try:
            url = f"{self.base_url}/data/blockchain/latest"
            params = {
                'fsym': symbol,
                'tsym': 'USD'
            }
            headers = {'authorization': f'Apikey {self.api_key}'}
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Response') != 'Success':
                return None
            
            blockchain_data = data.get('Data', {})
            
            # Extraer métricas relevantes
            metrics = {}
            
            # Transaction count trend
            if 'transaction_count_24h' in blockchain_data:
                metrics['tx_count_24h'] = blockchain_data['transaction_count_24h']
            
            # Average transaction value
            if 'average_transaction_value' in blockchain_data:
                metrics['avg_tx_value'] = blockchain_data['average_transaction_value']
            
            # Hash rate (BTC specific)
            if symbol == 'BTC' and 'hashrate' in blockchain_data:
                metrics['hashrate'] = blockchain_data['hashrate']
            
            return metrics if metrics else None
            
        except Exception as e:
            print(f"   ⚠️ Error en blockchain stats: {e}")
            return None
    
    def _analyze_exchange_flows(self, symbol: str) -> Optional[float]:
        """
        Analiza flujos de exchanges.
        
        Returns:
            Score: +1 (salida masiva, bullish) a -1 (entrada masiva, bearish)
        """
        # Esta es una implementación simplificada
        # En producción, usarías APIs como Glassnode, CryptoQuant, etc.
        
        try:
            # Usar datos de CryptoCompare como proxy
            url = f"{self.base_url}/data/exchange/histoday"
            params = {
                'fsym': symbol,
                'tsym': 'USD',
                'limit': 7,  # Última semana
                'aggregate': 1
            }
            headers = {'authorization': f'Apikey {self.api_key}'}
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Response') != 'Success':
                return None
            
            exchange_data = data.get('Data', [])
            
            if len(exchange_data) < 2:
                return None
            
            # Comparar volumen recent vs histórico
            recent_volume = sum(d.get('volumeto', 0) for d in exchange_data[-3:])
            historical_volume = sum(d.get('volumeto', 0) for d in exchange_data[:-3])
            
            if historical_volume == 0:
                return 0.0
            
            volume_ratio = recent_volume / historical_volume
            
            # Normalizar a -1 to +1
            # Ratio > 1.5 = mucho volumen (podría ser distribución) = bearish
            # Ratio < 0.7 = poco volumen (acumulación fuera de exchanges) = bullish
            
            if volume_ratio > 1.5:
                return -0.3  # Bearish leve
            elif volume_ratio < 0.7:
                return 0.3   # Bullish leve
            else:
                return 0.0
            
        except Exception as e:
            print(f"   ⚠️ Error en exchange flows: {e}")
            return None
    
    def _get_active_addresses_trend(self, symbol: str) -> Optional[float]:
        """
        Analiza tendencia de direcciones activas.
        
        Returns:
            Score: -1 (decreciente) a +1 (creciente)
        """
        try:
            # CryptoCompare no tiene este endpoint directamente
            # En producción usarías APIs especializadas
            # Aquí usamos un proxy basado en actividad general
            
            url = f"{self.base_url}/data/blockchain/histo/day"
            params = {
                'fsym': symbol,
                'limit': 30,
                'aggregate': 1
            }
            headers = {'authorization': f'Apikey {self.api_key}'}
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Response') != 'Success':
                return None
            
            hist_data = data.get('Data', {}).get('Data', [])
            
            if len(hist_data) < 15:
                return None
            
            # Comparar actividad reciente vs pasada
            recent = hist_data[-7:]
            past = hist_data[-14:-7]
            
            recent_avg = sum(d.get('transaction_count', 0) for d in recent) / len(recent)
            past_avg = sum(d.get('transaction_count', 0) for d in past) / len(past)
            
            if past_avg == 0:
                return 0.0
            
            change = (recent_avg - past_avg) / past_avg
            
            # Normalizar a -1 to +1
            normalized = max(-1.0, min(1.0, change * 2))  # *2 para amplificar
            
            return normalized
            
        except Exception as e:
            print(f"   ⚠️ Error en active addresses: {e}")
            return None
    
    def _calculate_signal(self, metrics: Dict) -> tuple:
        """
        Calcula señal agregada de múltiples métricas.
        
        Returns:
            (signal_type, strength)
        """
        signals = []
        weights = []
        
        # Exchange flow signal
        if 'exchange_flow_signal' in metrics:
            signals.append(metrics['exchange_flow_signal'])
            weights.append(0.4)
        
        # Active addresses trend
        if 'address_trend' in metrics:
            signals.append(metrics['address_trend'])
            weights.append(0.6)
        
        if not signals:
            return 'NEUTRAL', 0.0
        
        # Weighted average
        weighted_score = sum(s * w for s, w in zip(signals, weights)) / sum(weights)
        
        # Classify
        if weighted_score > 0.2:
            signal_type = 'BULLISH'
            strength = min(1.0, abs(weighted_score))
        elif weighted_score < -0.2:
            signal_type = 'BEARISH'
            strength = min(1.0, abs(weighted_score))
        else:
            signal_type = 'NEUTRAL'
            strength = 0.5
        
        return signal_type, strength


def should_trade_based_on_onchain(onchain_signal: Optional[OnChainSignal],
                                  trade_signal: str,
                                  min_strength: float = 0.5) -> bool:
    """
    Decide si operar basado en métricas on-chain.
    
    Args:
        onchain_signal: OnChainSignal del asset
        trade_signal: 'BUY' o 'SELL'
        min_strength: Fuerza mínima de señal
    
    Returns:
        True si on-chain confirma la operación
    """
    if onchain_signal is None:
        return True  # No bloquear si no hay datos
    
    if not onchain_signal.is_strong_signal(min_strength):
        return True  # No bloquear si señal débil
    
    # Verificar alineación
    if trade_signal == 'BUY':
        return onchain_signal.signal_type != 'BEARISH'
    else:  # SELL
        return onchain_signal.signal_type != 'BULLISH'
