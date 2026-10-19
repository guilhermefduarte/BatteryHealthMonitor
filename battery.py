
import psutil
import subprocess
import tempfile
import re
from pathlib import Path
from bs4 import BeautifulSoup


def obter_dados_demo():
    return {
        "design_capacity": 50000,
        "full_charge_capacity": 43500,
        "cycle_count": 324,
        "charge": 75,
        "plugged": False,
        "mode": "DEMO"
    }


def extrair_valor(soup, nome):
    for linha in soup.find_all("tr"):
        colunas = linha.find_all(["td", "th"])

        if len(colunas) >= 2:
            campo = colunas[0].get_text(
                " ", strip=True
            )

            if campo.casefold() == nome.casefold():
                return colunas[1].get_text(
                    " ", strip=True
                )

    return None


def converter_numero(valor):
    if not valor:
        return None

    # Aceita separadores de milhares
    # como 50,000 ou 50.000
    texto = valor.split()[0]
    digitos = re.sub(r"[^\d]", "", texto)

    return int(digitos) if digitos else None


def obter_dados_reais():
    bateria = psutil.sensors_battery()

    if bateria is None:
        return None

    dados = {
        "design_capacity": None,
        "full_charge_capacity": None,
        "cycle_count": None,
        "charge": bateria.percent,
        "plugged": bateria.power_plugged,
        "mode": "REAL"
    }

    with tempfile.TemporaryDirectory() as pasta:
        relatorio = Path(pasta) / "battery-report.html"

        try:
            subprocess.run(
                [
                    "powercfg",
                    "/batteryreport",
                    "/output",
                    str(relatorio)
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            with open(
                relatorio,
                "r",
                encoding="utf-8-sig"
            ) as ficheiro:
                soup = BeautifulSoup(
                    ficheiro, "html.parser"
                )

            campos = {
                "design_capacity": "DESIGN CAPACITY",
                "full_charge_capacity": "FULL CHARGE CAPACITY",
                "cycle_count": "CYCLE COUNT"
            }

            for chave, nome in campos.items():
                valor = extrair_valor(soup, nome)
                dados[chave] = converter_numero(valor)

        except (
            subprocess.SubprocessError,
            OSError,
            UnicodeError
        ) as erro:
            print("Erro ao gerar relatório:", erro)

    return dados


def calcular_saude(dados):
    original = dados["design_capacity"]
    atual = dados["full_charge_capacity"]

    if not original or atual is None:
        return None

    return round((atual / original) * 100, 1)
