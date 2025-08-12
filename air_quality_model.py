import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from data_processor import AirQualityDataProcessor

class AirQualityAI:
    """
    Hava kalitesi analizi ve AI destekli öneriler sunan sınıf
    """
    
    def __init__(self):
        self.data_processor = AirQualityDataProcessor()
        self.recommendations_db = self._load_recommendations()
        
    def _load_recommendations(self) -> Dict[str, List[Dict]]:
        """Öneriler veritabanını yükler"""
        return {
            'temperature': [
                {
                    'condition': 'low',
                    'threshold': 18,
                    'recommendations': [
                        "Ortam sıcaklığını 20-22°C arasına çıkarın",
                        "Isıtma sistemini kontrol edin",
                        "Pencere ve kapı yalıtımını iyileştirin",
                        "Sıcaklık sensörünü kalibre edin"
                    ],
                    'priority': 'high'
                },
                {
                    'condition': 'high',
                    'threshold': 26,
                    'recommendations': [
                        "Ortam sıcaklığını 22-24°C arasına düşürün",
                        "Klima sistemini çalıştırın",
                        "Havalandırmayı artırın",
                        "Güneş ışığını azaltın (perde kullanın)"
                    ],
                    'priority': 'high'
                }
            ],
            'humidity': [
                {
                    'condition': 'low',
                    'threshold': 30,
                    'recommendations': [
                        "Nem oranını %40-50 arasına çıkarın",
                        "Nemlendirici cihaz kullanın",
                        "Su kapları yerleştirin",
                        "Bitki sayısını artırın"
                    ],
                    'priority': 'medium'
                },
                {
                    'condition': 'high',
                    'threshold': 60,
                    'recommendations': [
                        "Nem oranını %45-55 arasına düşürün",
                        "Nem alma cihazı kullanın",
                        "Havalandırmayı artırın",
                        "Su sızıntılarını kontrol edin"
                    ],
                    'priority': 'medium'
                }
            ],
            'co2': [
                {
                    'condition': 'high',
                    'threshold': 1000,
                    'recommendations': [
                        "CO2 seviyesini 600-800 ppm arasına düşürün",
                        "Havalandırmayı artırın",
                        "Kişi sayısını azaltın",
                        "CO2 sensörü takın",
                        "Bitki sayısını artırın"
                    ],
                    'priority': 'critical'
                },
                {
                    'condition': 'very_high',
                    'threshold': 1500,
                    'recommendations': [
                        "ACİL: Ortamı hemen havalandırın",
                        "Kişileri başka odaya yönlendirin",
                        "CO2 seviyesini sürekli izleyin",
                        "Havalandırma sistemini maksimuma çıkarın"
                    ],
                    'priority': 'emergency'
                }
            ],
            'area_per_person': [
                {
                    'condition': 'low',
                    'threshold': 15,
                    'recommendations': [
                        "Kişi başına alanı artırın (en az 20m²)",
                        "Kişi sayısını azaltın",
                        "Daha büyük alan kullanın",
                        "Çalışma saatlerini ayırın"
                    ],
                    'priority': 'high'
                }
            ]
        }
    
    def analyze_air_quality(self, inputs: Dict[str, float]) -> Dict:
        """Hava kalitesi analizi yapar ve sonuçları döndürür"""
        # Veri doğrulama
        is_valid, errors = self.data_processor.validate_inputs(inputs)
        if not is_valid:
            return {
                'success': False,
                'errors': errors,
                'score': 0,
                'category': 'Geçersiz',
                'recommendations': []
            }
        
        # Veri normalizasyonu
        normalized_inputs = self.data_processor.normalize_inputs(inputs)
        
        # Hava kalitesi skoru hesaplama
        score = self.data_processor.calculate_air_quality_score(normalized_inputs)
        category, color = self.data_processor.get_air_quality_category(score)
        
        # Öneriler oluşturma
        recommendations = self._generate_recommendations(inputs, normalized_inputs, score)
        
        # Detaylı analiz
        detailed_analysis = self._create_detailed_analysis(inputs, normalized_inputs)
        
        return {
            'success': True,
            'score': score,
            'category': category,
            'color': color,
            'recommendations': recommendations,
            'detailed_analysis': detailed_analysis,
            'normalized_scores': normalized_inputs
        }
    
    def _generate_recommendations(self, inputs: Dict[str, float], 
                                normalized_inputs: Dict[str, float], 
                                overall_score: float) -> List[Dict]:
        """AI destekli öneriler oluşturur"""
        recommendations = []
        
        # Genel hava kalitesi önerileri
        if overall_score < 0.4:
            recommendations.append({
                'type': 'general',
                'priority': 'critical',
                'title': 'Genel Hava Kalitesi İyileştirme',
                'description': 'Hava kalitesi kritik seviyede. Acil önlem alınması gerekiyor.',
                'actions': [
                    'Tüm havalandırma sistemlerini maksimuma çıkarın',
                    'Kişi sayısını azaltın',
                    'CO2 seviyesini sürekli izleyin',
                    'Uzman desteği alın'
                ]
            })
        
        # Sıcaklık önerileri
        if inputs['temperature'] < 18:
            recommendations.extend(self._get_parameter_recommendations('temperature', 'low'))
        elif inputs['temperature'] > 26:
            recommendations.extend(self._get_parameter_recommendations('temperature', 'high'))
        
        # Nem önerileri
        if inputs['humidity'] < 30:
            recommendations.extend(self._get_parameter_recommendations('humidity', 'low'))
        elif inputs['humidity'] > 60:
            recommendations.extend(self._get_parameter_recommendations('humidity', 'high'))
        
        # CO2 önerileri
        if inputs['co2'] > 1500:
            recommendations.extend(self._get_parameter_recommendations('co2', 'very_high'))
        elif inputs['co2'] > 1000:
            recommendations.extend(self._get_parameter_recommendations('co2', 'high'))
        
        # Kişi başına alan önerileri
        area_per_person = self.data_processor.calculate_area_per_person(inputs['area'], inputs['occupancy'])
        if area_per_person < 15:
            recommendations.extend(self._get_parameter_recommendations('area_per_person', 'low'))
        
        # Önerileri öncelik sırasına göre sırala
        priority_order = {'emergency': 0, 'critical': 1, 'high': 2, 'medium': 3, 'low': 4}
        recommendations.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 4))
        
        return recommendations[:10]  # En önemli 10 öneriyi döndür
    
    def _get_parameter_recommendations(self, parameter: str, condition: str) -> List[Dict]:
        """Belirli parametre için önerileri döndürür"""
        recommendations = []
        
        if parameter in self.recommendations_db:
            for rec in self.recommendations_db[parameter]:
                if rec['condition'] == condition:
                    recommendations.append({
                        'type': parameter,
                        'priority': rec['priority'],
                        'title': f'{parameter.title()} İyileştirme',
                        'description': f'{parameter.title()} seviyesi optimal değerlerin dışında.',
                        'actions': rec['recommendations']
                    })
        
        return recommendations
    
    def _create_detailed_analysis(self, inputs: Dict[str, float], 
                                normalized_inputs: Dict[str, float]) -> Dict:
        """Detaylı analiz raporu oluşturur"""
        area_per_person = self.data_processor.calculate_area_per_person(inputs['area'], inputs['occupancy'])
        
        return {
            'temperature': {
                'value': inputs['temperature'],
                'unit': '°C',
                'score': normalized_inputs['temperature'],
                'status': 'Optimal' if 18 <= inputs['temperature'] <= 26 else 'İyileştirme Gerekli',
                'optimal_range': '18-26°C'
            },
            'humidity': {
                'value': inputs['humidity'],
                'unit': '%',
                'score': normalized_inputs['humidity'],
                'status': 'Optimal' if 30 <= inputs['humidity'] <= 60 else 'İyileştirme Gerekli',
                'optimal_range': '30-60%'
            },
            'co2': {
                'value': inputs['co2'],
                'unit': 'ppm',
                'score': normalized_inputs['co2'],
                'status': 'Optimal' if inputs['co2'] <= 1000 else 'İyileştirme Gerekli',
                'optimal_range': '< 1000 ppm'
            },
            'area_per_person': {
                'value': area_per_person,
                'unit': 'm²/kişi',
                'score': normalized_inputs['area_per_person'],
                'status': 'Optimal' if area_per_person >= 20 else 'İyileştirme Gerekli',
                'optimal_range': '≥ 20 m²/kişi'
            },
            'occupancy': {
                'value': inputs['occupancy'],
                'unit': 'kişi',
                'status': 'Normal' if inputs['occupancy'] <= 50 else 'Yüksek Yoğunluk',
                'optimal_range': '≤ 50 kişi'
            }
        }
    
    def get_improvement_predictions(self, current_inputs: Dict[str, float], 
                                  improvements: Dict[str, float]) -> Dict:
        """İyileştirme önerilerinin etkisini tahmin eder"""
        # Mevcut skoru hesapla
        current_normalized = self.data_processor.normalize_inputs(current_inputs)
        current_score = self.data_processor.calculate_air_quality_score(current_normalized)
        
        # İyileştirilmiş girdileri oluştur
        improved_inputs = current_inputs.copy()
        for param, improvement in improvements.items():
            # area_per_person için özel hesaplama
            if param == 'area_per_person':
                # Alan/Kişi iyileştirmesi için alanı artır veya kişi sayısını azalt
                current_area_per_person = self.data_processor.calculate_area_per_person(
                    improved_inputs['area'], improved_inputs['occupancy']
                )
                target_area_per_person = current_area_per_person + improvement
                
                # Kişi sayısını azaltarak hedefe ulaş
                if improved_inputs['occupancy'] > 1:
                    new_occupancy = max(1, improved_inputs['area'] / target_area_per_person)
                    improved_inputs['occupancy'] = int(new_occupancy)
            elif param in improved_inputs:
                improved_inputs[param] += improvement
        
        # İyileştirilmiş skoru hesapla
        improved_normalized = self.data_processor.normalize_inputs(improved_inputs)
        improved_score = self.data_processor.calculate_air_quality_score(improved_normalized)
        
        return {
            'current_score': current_score,
            'improved_score': improved_score,
            'improvement': improved_score - current_score,
            'improvement_percentage': ((improved_score - current_score) / current_score) * 100 if current_score > 0 else 0
        }
