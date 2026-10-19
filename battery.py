
import psutil


def obter_dados_demo():
    return {
        "design_capacity": 50000,
        "full_charge_capacity": 43500,
        "cycle_count": 324,
        "charge": 75,
        "plugged": False,
        "mode": "DEMO"
    }


def obter_dados_reais():
    bateria = psutil.sensors_battery()

    if bateria is None:
        return None

    return {
        "design_capacity": None,
        "full_charge_capacity": None,
        "cycle_count": None,
        "charge": bateria.percent,
        "plugged": bateria.power_plugged,
        "mode": "REAL"
    }


def calcular_saude(dados):
    original = dados["design_capacity"]
    atual = dados["full_charge_capacity"]

    if not original or atual is None:
        return None

    return round((atual / original) * 100, 1)
