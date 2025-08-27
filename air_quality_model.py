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
                        "Fabrika ısıtma sistemini kontrol edin ve ayarlayın",
                        "Üretim alanlarındaki sıcaklık sensörlerini kalibre edin",
                        "Pencere ve kapı yalıtımını iyileştirin",
                        "Çalışma alanlarında ek ısıtıcılar yerleştirin",
                        "Sıcaklık dağılımını optimize etmek için fan sistemlerini ayarlayın"
                    ],
                    'priority': 'high'
                },
                {
                    'condition': 'high',
                    'threshold': 26,
                    'recommendations': [
                        "Fabrika klima sistemini çalıştırın ve ayarlayın",
                        "Endüstriyel fan sistemlerini maksimuma çıkarın",
                        "Üretim makinelerinin ısı çıkışını azaltın",
                        "Çalışma saatlerini sıcaklığa göre ayarlayın",
                        "Soğutma sistemlerinin bakımını yapın"
                    ],
                    'priority': 'high'
                }
            ],
            'humidity': [
                {
                    'condition': 'low',
                    'threshold': 30,
                    'recommendations': [
                        "Fabrika nemlendirme sistemini çalıştırın",
                        "Üretim alanlarında endüstriyel nemlendiriciler yerleştirin",
                        "Su püskürtme sistemlerini aktif edin",
                        "Nem sensörlerini kalibre edin",
                        "Havalandırma sistemlerini nem kontrolü için ayarlayın"
                    ],
                    'priority': 'medium'
                },
                {
                    'condition': 'high',
                    'threshold': 60,
                    'recommendations': [
                        "Fabrika nem alma sistemlerini çalıştırın",
                        "Endüstriyel nem alma cihazları yerleştirin",
                        "Havalandırmayı artırın ve nem kontrolü yapın",
                        "Su sızıntılarını ve yoğuşma noktalarını kontrol edin",
                        "Üretim süreçlerindeki nem kaynaklarını azaltın"
                    ],
                    'priority': 'medium'
                }
            ],
            'co2': [
                {
                    'condition': 'high',
                    'threshold': 1000,
                    'recommendations': [
                        "Fabrika havalandırma sistemlerini maksimuma çıkarın",
                        "CO2 sensörlerini tüm üretim alanlarına yerleştirin",
                        "Çalışan sayısını azaltın veya vardiya sistemini uygulayın",
                        "Endüstriyel hava temizleme sistemleri kurun",
                        "Üretim süreçlerindeki CO2 emisyonlarını azaltın",
                        "Acil havalandırma sistemlerini aktif edin"
                    ],
                    'priority': 'critical'
                },
                {
                    'condition': 'very_high',
                    'threshold': 1500,
                    'recommendations': [
                        "ACİL: Tüm üretimi durdurun ve ortamı tahliye edin",
                        "Acil havalandırma sistemlerini maksimuma çıkarın",
                        "CO2 seviyesini sürekli izleyin ve alarm sistemini aktif edin",
                        "Çalışanları güvenli alanlara yönlendirin",
                        "Uzman ekipleri çağırın ve güvenlik protokollerini uygulayın",
                        "Üretim süreçlerindeki CO2 kaynaklarını tespit edin"
                    ],
                    'priority': 'emergency'
                }
            ],
            'area_per_person': [
                {
                    'condition': 'low',
                    'threshold': 15,
                    'recommendations': [
                        "Üretim alanlarını genişletin veya çalışan sayısını azaltın",
                        "Vardiya sistemini uygulayarak yoğunluğu azaltın",
                        "Çalışma alanlarını yeniden düzenleyin",
                        "Uzaktan çalışma seçeneklerini değerlendirin",
                        "Üretim kapasitesini optimize edin"
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
                'title': 'Fabrika Hava Kalitesi Acil İyileştirme',
                'description': 'Fabrika hava kalitesi kritik seviyede. Acil önlem alınması gerekiyor.',
                'actions': [
                    'Tüm endüstriyel havalandırma sistemlerini maksimuma çıkarın',
                    'Üretim süreçlerini geçici olarak durdurun',
                    'CO2 ve diğer sensörleri sürekli izleyin',
                    'Güvenlik ekiplerini çağırın ve protokolleri uygulayın',
                    'Çalışanları güvenli alanlara yönlendirin'
                ]
            })
        
        # Sıcaklık önerileri
        if inputs['temperature'] < 18:
            temp_recs = self._get_parameter_recommendations('temperature', 'low')
            if temp_recs:
                recommendations.extend(temp_recs)
        elif inputs['temperature'] > 26:
            temp_recs = self._get_parameter_recommendations('temperature', 'high')
            if temp_recs:
                recommendations.extend(temp_recs)
        
        # Nem önerileri
        if inputs['humidity'] < 30:
            humidity_recs = self._get_parameter_recommendations('humidity', 'low')
            if humidity_recs:
                recommendations.extend(humidity_recs)
        elif inputs['humidity'] > 60:
            humidity_recs = self._get_parameter_recommendations('humidity', 'high')
            if humidity_recs:
                recommendations.extend(humidity_recs)
        
        # CO2 önerileri
        if inputs['co2'] > 1500:
            co2_recs = self._get_parameter_recommendations('co2', 'very_high')
            if co2_recs:
                recommendations.extend(co2_recs)
        elif inputs['co2'] > 1000:
            co2_recs = self._get_parameter_recommendations('co2', 'high')
            if co2_recs:
                recommendations.extend(co2_recs)
        
        # Kişi başına alan önerileri
        area_per_person = self.data_processor.calculate_area_per_person(inputs['area'], inputs['occupancy'])
        if area_per_person < 15:
            area_recs = self._get_parameter_recommendations('area_per_person', 'low')
            if area_recs:
                recommendations.extend(area_recs)
        
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
                    # Parametre adlarını Türkçe'ye çevir
                    param_names = {
                        'temperature': 'Sıcaklık',
                        'humidity': 'Nem',
                        'co2': 'CO2',
                        'area_per_person': 'Kişi Başına Alan'
                    }
                    
                    param_name = param_names.get(parameter, parameter.title())
                    
                    recommendations.append({
                        'type': parameter,
                        'priority': rec['priority'],
                        'title': f'Fabrika {param_name} İyileştirme',
                        'description': f'Fabrika {param_name.lower()} seviyesi optimal değerlerin dışında. Endüstriyel önlemler alınması gerekiyor.',
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
