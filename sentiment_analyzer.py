"""
SENTIMENT ANALYZER - CryptoCompare API Integration
Analiza el sentiment de redes sociales y noticias para crypto
"""

import os
import requests
import time
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SentimentScore:
    overall_score: float  # -1 (muy negativo) a +1 (muy positivo)
    news_score: float
    social_score: float
    confidence: float
    timestamp: datetime
    
    def is_bullish(self, threshold: float = 0.2) -> bool:
        return self.overall_score > threshold
    
    def is_bearish(self, threshold: float = -0.2) -> bool:
        return self.overall_score < threshold


class SentimentAnalyzer:
    """
    Integra datos de sentiment de CryptoCompare API
    
    Endpoints utilizados:
    - /data/v2/news/ - Últimas noticias
    - /data/social/coin/latest - Stats sociales
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://min-api.cryptocompare.com"
        self.session = requests.Session()
        self.cache = {}
        self.cache_duration = 300  # 5 minutos
    
    def get_sentiment(self, symbol: str) -> Optional[SentimentScore]:
        """
        Obtiene sentiment score para un símbolo.
        
        Args:
            symbol: Símbolo crypto (BTC, ETH, etc.)
        
        Returns:
            SentimentScore o None si hay error
        """
        # Normalizar símbolo (BTC-USD -> BTC)
        clean_symbol = symbol.split('-')[0].upper()
        
        # Check cache
        cache_key = f"{clean_symbol}_{int(time.time() / self.cache_duration)}"
        if cache_key in self.cache:
            print(f"   📋 Sentiment cache hit: {clean_symbol}")
            return self.cache[cache_key]
        
        try:
            # 1. News sentiment
            news_score = self._get_news_sentiment(clean_symbol)
            
            # 2. Social sentiment
            social_score = self._get_social_sentiment(clean_symbol)
            
            # 3. Calculate overall score
            if news_score is None and social_score is None:
                return None
            
            # Weighted average (60% social, 40% news)
            scores = []
            weights = []
            
            if social_score is not None:
                scores.append(social_score)
                weights.append(0.6)
            
            if news_score is not None:
                scores.append(news_score)
                weights.append(0.4)
            
            overall = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
            
            # Confidence based on data availability
            confidence = 1.0 if (social_score is not None and news_score is not None) else 0.5
            
            sentiment = SentimentScore(
                overall_score=overall,
                news_score=news_score or 0.0,
                social_score=social_score or 0.0,
                confidence=confidence,
                timestamp=datetime.now()
            )
            
            # Cache result
            self.cache[cache_key] = sentiment
            
            print(f"   💭 Sentiment {clean_symbol}: Overall={overall:.2f}, News={news_score}, Social={social_score}")
            
            return sentiment
            
        except Exception as e:
            print(f"   ⚠️ Error obteniendo sentiment para {clean_symbol}: {e}")
            return None
    
    def _get_news_sentiment(self, symbol: str) -> Optional[float]:
        """
        Analiza sentiment de noticias recientes.
        
        Returns:
            Score de -1 a +1, o None si error
        """
        try:
            url = f"{self.base_url}/data/v2/news/"
            params = {
                'categories': symbol,
                'lang': 'EN'
            }
            
            headers = {
                'authorization': f'Apikey {self.api_key}'
            }
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Response') != 'Success':
                return None
            
            news_items = data.get('Data', [])
            
            if not news_items:
                return None
            
            # Analizar sentiment basado en categorías y keywords
            positive_keywords = ['bullish', 'surge', 'rally', 'gain', 'pump', 'moon', 'adoption']
            negative_keywords = ['bearish', 'crash', 'dump', 'drop', 'fall', 'decline', 'regulation']
            
            sentiment_scores = []
            
            for item in news_items[:20]:  # Últimas 20 noticias
                title = item.get('title', '').lower()
                body = item.get('body', '').lower()
                text = title + ' ' + body
                
                pos_count = sum(1 for word in positive_keywords if word in text)
                neg_count = sum(1 for word in negative_keywords if word in text)
                
                if pos_count + neg_count > 0:
                    score = (pos_count - neg_count) / (pos_count + neg_count)
                    sentiment_scores.append(score)
            
            if not sentiment_scores:
                return 0.0
            
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            
            return avg_sentiment
            
        except Exception as e:
            print(f"   ⚠️ Error en news sentiment: {e}")
            return None
    
    def _get_social_sentiment(self, symbol: str) -> Optional[float]:
        """
        Obtiene métricas sociales (Twitter, Reddit, etc.).
        
        Returns:
            Score de -1 a +1, o None si error
        """
        try:
            url = f"{self.base_url}/data/social/coin/latest"
            params = {
                'coinId': self._get_coin_id(symbol)
            }
            
            headers = {
                'authorization': f'Apikey {self.api_key}'
            }
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Response') != 'Success':
                return None
            
            social_data = data.get('Data', {})
            
            # Extraer métricas clave
            twitter_followers = social_data.get('Twitter', {}).get('followers', 0)
            reddit_subscribers = social_data.get('Reddit', {}).get('subscribers', 0)
            twitter_points = social_data.get('Twitter', {}).get('Points', 0)
            reddit_points = social_data.get('Reddit', {}).get('Points', 0)
            
            # Normalizar a score -1 to +1
            # Más followers/subscribers/points = más positivo
            # Esto es simplificado - idealmente compararíamos con histórico
            
            if twitter_followers == 0 and reddit_subscribers == 0:
                return None
            
            # Score basado en engagement points (normalizado)
            total_points = twitter_points + reddit_points
            
            # Normalizar aproximadamente (ajustar según experiencia)
            if total_points > 10000:
                score = 0.5
            elif total_points > 5000:
                score = 0.3
            elif total_points > 1000:
                score = 0.1
            elif total_points < 100:
                score = -0.2
            else:
                score = 0.0
            
            return score
            
        except Exception as e:
            print(f"   ⚠️ Error en social sentiment: {e}")
            return None
    
    def _get_coin_id(self, symbol: str) -> int:
        """
        Mapea símbolos a CryptoCompare coin IDs.
        """
        # Mapeo básico - expandir según necesidad
        coin_map = {
            'BTC': 1182,
            'ETH': 7605,
            'ADA': 5038,
            'SOL': 151340,
            'MATIC': 202330,
            'AVAX': 166503,
            'LINK': 3808,
            'DOT': 165542
        }
        
        return coin_map.get(symbol, 1182)  # Default BTC
    
    def get_market_sentiment_summary(self, symbols: list) -> Dict[str, str]:
        """
        Obtiene resumen de sentiment del mercado para múltiples símbolos.
        
        Returns:
            Dict con símbolo -> clasificación (BULLISH/NEUTRAL/BEARISH)
        """
        summary = {}
        
        for symbol in symbols:
            sentiment = self.get_sentiment(symbol)
            
            if sentiment is None:
                summary[symbol] = 'UNKNOWN'
            elif sentiment.is_bullish():
                summary[symbol] = 'BULLISH'
            elif sentiment.is_bearish():
                summary[symbol] = 'BEARISH'
            else:
                summary[symbol] = 'NEUTRAL'
        
        return summary


# Función helper para usar en el bot
def should_trade_based_on_sentiment(sentiment: Optional[SentimentScore],
                                   signal: str,
                                   min_confidence: float = 0.5) -> bool:
    """
    Decide si operar basado en sentiment y señal técnica.
    
    Args:
        sentiment: SentimentScore del asset
        signal: 'BUY' o 'SELL'
        min_confidence: Confianza mínima requerida
    
    Returns:
        True si sentiment confirma la señal
    """
    if sentiment is None:
        return True  # No bloquear si no hay datos
    
    if sentiment.confidence < min_confidence:
        return True  # No bloquear si confianza baja
    
    # Confirmar señal con sentiment
    if signal == 'BUY':
        return sentiment.overall_score >= 0.0  # Sentiment neutral o positivo
    else:  # SELL
        return sentiment.overall_score <= 0.0  # Sentiment neutral o negativo
