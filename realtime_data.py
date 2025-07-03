import requests
import json
from datetime import datetime
import pytz
import yfinance as yf
import feedparser
import wikipedia
from typing import Dict, Any, Optional

class RealTimeDataProvider:
    """Provides real-time information for the chatbot"""
    
    def __init__(self):
        self.news_sources = {
            'general': 'https://feeds.bbci.co.uk/news/rss.xml',
            'tech': 'https://feeds.feedburner.com/TechCrunch',
            'science': 'https://rss.cnn.com/rss/edition.rss'
        }
    
    def get_current_datetime(self, timezone='local'):
        """Get current date and time"""
        try:
            if timezone == 'local':
                # Get local timezone
                now = datetime.now()
                local_tz = now.astimezone().tzinfo
                now_local = datetime.now(local_tz)
                
                return {
                    'datetime': now_local.strftime('%Y-%m-%d %H:%M:%S %Z'),
                    'date': now_local.strftime('%Y-%m-%d'),
                    'time': now_local.strftime('%H:%M:%S'),
                    'timezone': str(local_tz),
                    'timestamp': now_local.timestamp(),
                    'day_name': now_local.strftime('%A'),
                    'month_name': now_local.strftime('%B')
                }
            elif timezone == 'UTC':
                tz = pytz.UTC
                now = datetime.now(tz)
            else:
                tz = pytz.timezone(timezone)
                now = datetime.now(tz)
            
            if timezone != 'local':
                return {
                    'datetime': now.strftime('%Y-%m-%d %H:%M:%S %Z'),
                    'date': now.strftime('%Y-%m-%d'),
                    'time': now.strftime('%H:%M:%S'),
                    'timezone': str(tz),
                    'timestamp': now.timestamp(),
                    'day_name': now.strftime('%A'),
                    'month_name': now.strftime('%B')
                }
        except Exception as e:
            return {'error': str(e)}
    
    def get_weather(self, city='London'):
        """Get current weather information"""
        try:
            # Using OpenWeatherMap API (you'll need to get a free API key)
            # For demo purposes, we'll use a mock response
            return {
                'city': city,
                'temperature': '22°C',
                'condition': 'Partly Cloudy',
                'humidity': '65%',
                'wind_speed': '15 km/h',
                'note': 'This is mock data. Get a free API key from OpenWeatherMap for real data.'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_stock_price(self, symbol='AAPL'):
        """Get current stock price"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            history = stock.history(period='1d')
            
            if not history.empty:
                current_price = history['Close'].iloc[-1]
                return {
                    'symbol': symbol,
                    'price': f"${current_price:.2f}",
                    'company': info.get('longName', symbol),
                    'change': f"{((current_price - history['Open'].iloc[0]) / history['Open'].iloc[0] * 100):.2f}%",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {'error': 'No data available'}
        except Exception as e:
            return {'error': str(e)}
    
    def get_news(self, category='general', limit=5):
        """Get latest news"""
        try:
            feed_url = self.news_sources.get(category, self.news_sources['general'])
            feed = feedparser.parse(feed_url)
            
            news_items = []
            for entry in feed.entries[:limit]:
                news_items.append({
                    'title': entry.title,
                    'summary': entry.summary[:200] + '...' if len(entry.summary) > 200 else entry.summary,
                    'link': entry.link,
                    'published': entry.published if hasattr(entry, 'published') else 'N/A'
                })
            
            return {
                'category': category,
                'count': len(news_items),
                'news': news_items,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_wikipedia_summary(self, query, sentences=3):
        """Get Wikipedia summary"""
        try:
            summary = wikipedia.summary(query, sentences=sentences)
            page = wikipedia.page(query)
            
            return {
                'query': query,
                'summary': summary,
                'url': page.url,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except wikipedia.exceptions.DisambiguationError as e:
            return {
                'query': query,
                'error': 'Multiple results found',
                'suggestions': e.options[:5]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_exchange_rate(self, from_currency='USD', to_currency='EUR'):
        """Get currency exchange rate"""
        try:
            # Using a free API like exchangerate-api.com
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                rate = data['rates'].get(to_currency)
                
                if rate:
                    return {
                        'from': from_currency,
                        'to': to_currency,
                        'rate': rate,
                        'timestamp': data['date']
                    }
                else:
                    return {'error': f'Currency {to_currency} not found'}
            else:
                return {'error': 'Unable to fetch exchange rate'}
        except Exception as e:
            return {'error': str(e)}
    
    def search_web(self, query, limit=3):
        """Search the web (mock implementation)"""
        try:
            # This is a mock implementation
            # In real usage, you'd use Google Custom Search API or similar
            return {
                'query': query,
                'results': [
                    {
                        'title': f'Search result for {query}',
                        'snippet': 'This is a mock search result. Implement with Google Custom Search API for real results.',
                        'url': 'https://example.com'
                    }
                ],
                'note': 'Mock search results. Implement with Google Custom Search API for real web search.'
            }
        except Exception as e:
            return {'error': str(e)}

# Function to process real-time queries
def process_realtime_query(user_message: str, data_provider: RealTimeDataProvider) -> Optional[Dict[str, Any]]:
    """Process user message and return real-time data if relevant"""
    
    message_lower = user_message.lower()
    
    # Time and date queries
    if any(keyword in message_lower for keyword in ['time', 'date', 'now', 'current']):
        # Check if user specified a timezone or city
        timezone = 'local'  # default to local time
        
        # Common timezone/city mappings
        timezone_mapping = {
            'utc': 'UTC',
            'london': 'Europe/London',
            'new york': 'America/New_York',
            'los angeles': 'America/Los_Angeles',
            'tokyo': 'Asia/Tokyo',
            'sydney': 'Australia/Sydney',
            'paris': 'Europe/Paris',
            'berlin': 'Europe/Berlin',
            'mumbai': 'Asia/Kolkata',
            'dubai': 'Asia/Dubai'
        }
        
        # Check if user mentioned a specific location
        for location, tz in timezone_mapping.items():
            if location in message_lower:
                timezone = tz
                break
        
        return {
            'type': 'datetime',
            'data': data_provider.get_current_datetime(timezone)
        }
    
    # Weather queries
    if any(keyword in message_lower for keyword in ['weather', 'temperature', 'climate']):
        # Try to extract city name (basic implementation)
        words = user_message.split()
        city = 'London'  # default
        for i, word in enumerate(words):
            if word.lower() in ['in', 'at', 'for'] and i + 1 < len(words):
                city = words[i + 1]
                break
        
        return {
            'type': 'weather',
            'data': data_provider.get_weather(city)
        }
    
    # Stock price queries
    if any(keyword in message_lower for keyword in ['stock', 'price', 'shares']):
        # Try to extract stock symbol
        words = user_message.upper().split()
        symbol = 'AAPL'  # default
        for word in words:
            if len(word) <= 5 and word.isalpha():
                symbol = word
                break
        
        return {
            'type': 'stock',
            'data': data_provider.get_stock_price(symbol)
        }
    
    # News queries
    if any(keyword in message_lower for keyword in ['news', 'latest', 'headlines']):
        category = 'general'
        if 'tech' in message_lower:
            category = 'tech'
        elif 'science' in message_lower:
            category = 'science'
        
        return {
            'type': 'news',
            'data': data_provider.get_news(category)
        }
    
    # Wikipedia queries
    if any(keyword in message_lower for keyword in ['wikipedia', 'wiki', 'what is', 'who is']):
        # Extract query after "what is" or "who is"
        query = user_message
        for phrase in ['what is', 'who is', 'tell me about']:
            if phrase in message_lower:
                query = user_message[message_lower.find(phrase) + len(phrase):].strip()
                break
        
        return {
            'type': 'wikipedia',
            'data': data_provider.get_wikipedia_summary(query)
        }
    
    # Exchange rate queries
    if any(keyword in message_lower for keyword in ['exchange', 'currency', 'convert']):
        return {
            'type': 'exchange',
            'data': data_provider.get_exchange_rate()
        }
    
    return None

# Function to format real-time data for display
def format_realtime_data(realtime_result: Dict[str, Any]) -> str:
    """Format real-time data for display in chat"""
    
    if not realtime_result:
        return ""
    
    data_type = realtime_result.get('type')
    data = realtime_result.get('data', {})
    
    if 'error' in data:
        return f"❌ Error getting {data_type}: {data['error']}"
    
    if data_type == 'datetime':
        # Create a more user-friendly time display
        time_str = f"🕐 **Current Time**: {data['time']}\n"
        time_str += f"📅 **Date**: {data['day_name']}, {data['date']} ({data['month_name']})"
        if 'timezone' in data and data['timezone']:
            time_str += f"\n🌍 **Timezone**: {data['timezone']}"
        return time_str
    
    elif data_type == 'weather':
        return f"🌤️ **Weather in {data['city']}**: {data['temperature']}, {data['condition']}\n💧 Humidity: {data['humidity']} | 💨 Wind: {data['wind_speed']}"
    
    elif data_type == 'stock':
        return f"📈 **{data['company']} ({data['symbol']})**: {data['price']} ({data['change']})"
    
    elif data_type == 'news':
        news_text = f"📰 **Latest {data['category'].title()} News**:\n"
        for i, item in enumerate(data['news'][:3], 1):
            news_text += f"{i}. **{item['title']}**\n   {item['summary']}\n\n"
        return news_text
    
    elif data_type == 'wikipedia':
        if 'suggestions' in data:
            return f"❓ **Multiple results for '{data['query']}'**. Did you mean: {', '.join(data['suggestions'][:3])}?"
        else:
            return f"📚 **Wikipedia**: {data['summary']}\n🔗 [Read more]({data['url']})"
    
    elif data_type == 'exchange':
        return f"💱 **Exchange Rate**: 1 {data['from']} = {data['rate']} {data['to']}"
    
    return ""
