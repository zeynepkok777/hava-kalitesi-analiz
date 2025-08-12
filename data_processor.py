import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from typing import Dict, List, Tuple

class AirQualityDataProcessor:
    """
    Hava kalitesi verilerini işlemek için kullanılan sınıf
    """
    
    def __init__(self):
        # Hava kalitesi için referans değerler
        self.reference_values = {
            'temperature': {'min': 18, 'max': 26, 'optimal': 22},  # °C
            'humidity': {'min': 30, 'max': 60, 'optimal': 45},     # %
            'co2': {'min': 400, 'max': 1000, 'optimal': 600},     # ppm
            'area_per_person': {'min': 10, 'max': 50, 'optimal': 25},  # m²/kişi
            'occupancy': {'min': 1, 'max': 100, 'optimal': 10}     # kişi
        }
        
        self.scaler = StandardScaler()
        
    def calculate_area_per_person(self, area: float, occupancy: int) -> float:
        """Kişi başına düşen alanı hesaplar"""
        if occupancy <= 0:
            return area
        return area / occupancy
    
    def normalize_inputs(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """Girdi değerlerini normalize eder"""
        normalized = {}
        
        # Sıcaklık normalizasyonu (18-26°C arası optimal)
        temp_score = self._normalize_value(
            inputs['temperature'], 
            self.reference_values['temperature']['min'],
            self.reference_values['temperature']['max'],
            self.reference_values['temperature']['optimal']
        )
        normalized['temperature'] = temp_score
        
        # Nem normalizasyonu (30-60% arası optimal)
        humidity_score = self._normalize_value(
            inputs['humidity'],
            self.reference_values['humidity']['min'],
            self.reference_values['humidity']['max'],
            self.reference_values['humidity']['optimal']
        )
        normalized['humidity'] = humidity_score
        
        # CO2 normalizasyonu (400-1000 ppm arası optimal)
        co2_score = self._normalize_value(
            inputs['co2'],
            self.reference_values['co2']['min'],
            self.reference_values['co2']['max'],
            self.reference_values['co2']['optimal'],
            reverse=True  # CO2 için düşük değer daha iyi
        )
        normalized['co2'] = co2_score
        
        # Kişi başına alan normalizasyonu
        area_per_person = self.calculate_area_per_person(inputs['area'], inputs['occupancy'])
        area_score = self._normalize_value(
            area_per_person,
            self.reference_values['area_per_person']['min'],
            self.reference_values['area_per_person']['max'],
            self.reference_values['area_per_person']['optimal']
        )
        normalized['area_per_person'] = area_score
        
        return normalized
    
    def _normalize_value(self, value: float, min_val: float, max_val: float, 
                        optimal: float, reverse: bool = False) -> float:
        """Değeri 0-1 arasında normalize eder"""
        if value <= optimal:
            # Optimal değere kadar olan aralık
            if optimal - min_val == 0:
                score = 1.0
            else:
                score = (value - min_val) / (optimal - min_val)
        else:
            # Optimal değerden sonraki aralık
            if max_val - optimal == 0:
                score = 0.0
            else:
                score = 1.0 - ((value - optimal) / (max_val - optimal))
        
        # 0-1 arasında sınırla
        score = max(0.0, min(1.0, score))
        
        if reverse:
            score = 1.0 - score
            
        return score
    
    def calculate_air_quality_score(self, normalized_inputs: Dict[str, float]) -> float:
        """Normalize edilmiş girdilerden hava kalitesi skorunu hesaplar"""
        weights = {
            'temperature': 0.25,
            'humidity': 0.20,
            'co2': 0.35,
            'area_per_person': 0.20
        }
        
        total_score = 0
        total_weight = 0
        
        for param, weight in weights.items():
            if param in normalized_inputs:
                total_score += normalized_inputs[param] * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        return total_score / total_weight
    
    def get_air_quality_category(self, score: float) -> Tuple[str, str]:
        """Hava kalitesi skoruna göre kategori ve renk döndürür"""
        if score >= 0.8:
            return "Mükemmel", "green"
        elif score >= 0.6:
            return "İyi", "lightgreen"
        elif score >= 0.4:
            return "Orta", "orange"
        elif score >= 0.2:
            return "Kötü", "red"
        else:
            return "Çok Kötü", "darkred"
    
    def validate_inputs(self, inputs: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Girdi değerlerini doğrular"""
        errors = []
        
        # Sıcaklık kontrolü
        if inputs['temperature'] < -10 or inputs['temperature'] > 50:
            errors.append("Sıcaklık -10°C ile 50°C arasında olmalıdır")
        
        # Nem kontrolü
        if inputs['humidity'] < 0 or inputs['humidity'] > 100:
            errors.append("Nem 0% ile 100% arasında olmalıdır")
        
        # CO2 kontrolü
        if inputs['co2'] < 300 or inputs['co2'] > 5000:
            errors.append("CO2 seviyesi 300-5000 ppm arasında olmalıdır")
        
        # Alan kontrolü
        if inputs['area'] <= 0:
            errors.append("Alan pozitif bir değer olmalıdır")
        
        # Kişi sayısı kontrolü
        if inputs['occupancy'] < 0:
            errors.append("Kişi sayısı negatif olamaz")
        
        return len(errors) == 0, errors
