
import customtkinter as ctk
from tkinter import messagebox

from battery import (
    obter_dados_demo,
    obter_dados_reais,
    calcular_saude
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BatteryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Battery Health Monitor")
        self.geometry("780x580")
        self.minsize(650, 520)
        self.configure(fg_color="#101827")

        self.modo_demo = True

        self.criar_interface()
        self.atualizar_dados()

    def criar_interface(self):
        # Cabeçalho
        header = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        header.pack(
            fill="x", padx=30, pady=(25, 15)
        )

        ctk.CTkLabel(
            header,
            text="Battery Health Monitor",
            font=("Segoe UI", 26, "bold")
        ).pack(side="left")

        self.modo_label = ctk.CTkLabel(
            header,
            text="DEMO",
            text_color="#f5bd65",
            font=("Segoe UI", 14, "bold")
        )
        self.modo_label.pack(side="right")

        # Cartao principal
        principal = ctk.CTkFrame(
            self,
            fg_color="#1c293a",
            corner_radius=15
        )
        principal.pack(
            fill="x", padx=30, pady=12
        )

        ctk.CTkLabel(
            principal,
            text="BATTERY HEALTH",
            text_color="#aab9cc",
            font=("Segoe UI", 14)
        ).pack(pady=(22, 5))

        self.saude_label = ctk.CTkLabel(
            principal,
            text="--%",
            text_color="#48dba0",
            font=("Segoe UI", 58, "bold")
        )
        self.saude_label.pack()

        self.estado_label = ctk.CTkLabel(
            principal,
            text="A analisar...",
            font=("Segoe UI", 14)
        )
        self.estado_label.pack(pady=(0, 20))

        # Grelha de indicadores
        grelha = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        grelha.pack(
            fill="x", padx=30, pady=10
        )

        grelha.grid_columnconfigure(
            (0, 1), weight=1
        )

        self.valores = {}

        indicadores = [
            ("Design Capacity", "design_capacity"),
            ("Full Charge Capacity", "full_charge_capacity"),
            ("Cycle Count", "cycle_count"),
            ("Current Charge", "charge")
        ]

        for i, (titulo, chave) in enumerate(indicadores):
            cartao = ctk.CTkFrame(
                grelha,
                fg_color="#1c293a",
                corner_radius=12
            )
            cartao.grid(
                row=i // 2,
                column=i % 2,
                sticky="nsew",
                padx=6,
                pady=6
            )

            ctk.CTkLabel(
                cartao,
                text=titulo,
                text_color="#aab9cc",
                font=("Segoe UI", 13)
            ).pack(pady=(15, 3))

            valor = ctk.CTkLabel(
                cartao,
                text="--",
                font=("Segoe UI", 23, "bold")
            )
            valor.pack(pady=(0, 15))

            self.valores[chave] = valor

        # Botoes
        botoes = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        botoes.pack(
            fill="x", padx=35, pady=20
        )

        ctk.CTkButton(
            botoes,
            text="Atualizar diagnóstico",
            command=self.atualizar_dados,
            height=42
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        self.botao_modo = ctk.CTkButton(
            botoes,
            text="Mudar para Modo Real",
            command=self.alternar_modo,
            fg_color="#34465c",
            hover_color="#455c77",
            height=42
        )
        self.botao_modo.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

    def alternar_modo(self):
        self.modo_demo = not self.modo_demo

        self.botao_modo.configure(
            text=(
                "Mudar para Modo Real"
                if self.modo_demo
                else "Mudar para Modo Demo"
            )
        )

        self.atualizar_dados()

    def atualizar_dados(self):
        if self.modo_demo:
            dados = obter_dados_demo()
        else:
            dados = obter_dados_reais()

        if dados is None:
            self.mostrar_indisponivel()
            return

        self.modo_label.configure(
            text=dados["mode"],
            text_color=(
                "#f5bd65" if self.modo_demo
                else "#48dba0"
            )
        )

        saude = calcular_saude(dados)

        if saude is None:
            self.saude_label.configure(text="N/D")
            self.estado_label.configure(
                text="Capacidade não disponível"
            )
        else:
            self.saude_label.configure(
                text=f"{saude:.1f}%"
            )

            if saude >= 80:
                estado = "Boa condição"
                cor = "#48dba0"
            elif saude >= 60:
                estado = "Desgaste moderado"
                cor = "#f5bd65"
            else:
                estado = "Desgaste elevado"
                cor = "#f87171"

            self.saude_label.configure(
                text_color=cor
            )
            self.estado_label.configure(
                text=estado
            )

        for chave, label in self.valores.items():
            valor = dados[chave]

            if valor is None:
                texto = "N/D"
            elif chave in (
                "design_capacity",
                "full_charge_capacity"
            ):
                texto = f"{valor:,} mWh"
            elif chave == "charge":
                texto = f"{valor}%"
            else:
                texto = str(valor)

            label.configure(text=texto)

    def mostrar_indisponivel(self):
        self.modo_label.configure(
            text="SEM BATERIA",
            text_color="#f87171"
        )

        self.saude_label.configure(
            text="N/D",
            text_color="#aab9cc"
        )

        self.estado_label.configure(
            text="Nenhuma bateria detetada"
        )

        for label in self.valores.values():
            label.configure(text="N/D")

        messagebox.showinfo(
            "Bateria não detetada",
            "Este computador não possui uma "
            "bateria detetável pelo Windows.\n\n"
            "Podes utilizar o Modo Demo."
        )


if __name__ == "__main__":
    app = BatteryApp()
    app.mainloop()
