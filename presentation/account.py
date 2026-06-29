from decimal import Decimal
from datetime import datetime
import os
from business.account_service import AccountService
from infrastructure.exporter_factory import ExporterFactory
import tabulate


class Account:

    def __init__(self, repository):
        self.account_service = AccountService(repository)
        self.exporter_factory = ExporterFactory()

    def abrir_cuenta(self, username):
        try:
            moneda = input("Ingrese el codigo de moneda (3 letras, ej: USD):\n")
            self.account_service.create_account(username, moneda)
            print(f"Cuenta en {moneda.upper()} creada con exito")
        except Exception as e:
            print(e)

    def listar_cuentas(self, username):
        try:
            accounts = self.account_service.get_accounts(username)
            if not accounts:
                print("No hay cuentas abiertas")
                return

            tabulate_data = [[moneda, str(Decimal(saldo).quantize(Decimal('0.01')))] for moneda, saldo in accounts.items()]
            print(tabulate.tabulate(tabulate_data, headers=["Moneda", "Saldo"], tablefmt="simple", floatfmt='.2f'))

            input("Presione ENTER para volver al menu de usuario...")
        except Exception as e:
            print(e)

    def cuenta_ars_registro(self, username):
        try:
            self.account_service.create_account(username, "ARS")
        except Exception as e:
            print(e)

    def ingresar_pesos_argentinos(self, username):
        try:
            if "ARS" not in self.account_service.get_accounts(username):
                print("No tienes una cuenta en ARS, creando una automaticamente para seguir operando...")
                self.cuenta_ars_registro(username)

            amount = input("Ingrese el monto en pesos argentinos:\n")
            amount = self.account_service.check_decimal(amount)

            accounts = self.account_service.get_accounts(username)
            current_balance = self.account_service.check_decimal(accounts["ARS"])
            new_balance = current_balance + amount

            str_balance = str(new_balance.quantize(Decimal('0.01')))
            accounts["ARS"] = str(new_balance)
            if self.account_service.save_accounts(username, accounts):
                print(f"Monto ingresado exitosamente. Nuevo saldo en ARS: {str_balance}")
            else:
                print("Error al guardar el nuevo saldo.")
        except Exception as e:
            print(e)

    def exportar_resumen(self, username):
        try:
            accounts = self.account_service.get_accounts(username)
            if not accounts:
                print("No hay cuentas para exportar.")
                return

            print("Seleccione formato:")
            print("1 - CSV (Excel)")
            print("2 - TXT (Texto plano)")
            print("3 - PDF")
            formato = input("Formato: ").strip()
            if formato not in ("1", "2", "3"):
                print("Formato no valido.")
                return

            print("Ingrese codigo de moneda (o 'TODAS' para todas las cuentas):")
            filtro = input().strip().upper()
            if filtro != "TODAS" and filtro not in accounts:
                print(f"No tenes una cuenta en {filtro}.")
                return

            exporter = self.exporter_factory.create(formato)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = {"1": "csv", "2": "txt", "3": "pdf"}[formato]
            filename = f"{username}_resumen_{timestamp}.{ext}"
            filepath = os.path.join("data", "exports", filename)
            exporter.export(accounts, username, filepath, filtro)
            print(f"Resumen exportado exitosamente a: {filepath}")
        except Exception as e:
            print(e)

    def ingresar_moneda_extranjera(self, username):
        try:
            accounts = self.account_service.get_accounts(username)

            print("Ingrese el codigo de moneda extranjera (3 letras, ej: USD):")
            moneda_extranjera = input().strip().upper()

            if not self.account_service.is_currency_valid(moneda_extranjera):
                print("Moneda no soportada. Por favor, intente nuevamente.")
                return

            if not self.account_service.has_account(username, moneda_extranjera):
                print(f"No tienes una cuenta en {moneda_extranjera}, Desea crearla? (s/n):")
                choice = input().strip().lower()
                if choice == 's':
                    self.account_service.create_account(username, moneda_extranjera)
                    accounts = self.account_service.get_accounts(username)
                else:
                    print("Operacion cancelada.")
                    return

            amount = input(f"Ingrese el monto en {moneda_extranjera}:\n")

            amount = self.account_service.check_decimal(amount)

            total_exchange = self.account_service.calc_exchange_rate(moneda_extranjera, amount)

            ars_decimal = Decimal(accounts.get("ARS", "0"))

            if ars_decimal < total_exchange:
                print(f"No tienes suficiente saldo en ARS para realizar esta operacion. Saldo actual en ARS: {ars_decimal}")
                return

            accounts["ARS"] = str(self.account_service.check_decimal(accounts["ARS"]) - total_exchange)
            accounts[moneda_extranjera] = str(self.account_service.check_decimal(accounts[moneda_extranjera]) + amount)

            if self.account_service.save_accounts(username, accounts):
                ars = Decimal(accounts["ARS"]).quantize(Decimal('0.01'))
                foreign = Decimal(accounts[moneda_extranjera]).quantize(Decimal('0.01'))
                print(f"Monto ingresado exitosamente. Nuevo saldo en ARS: {ars}, Nuevo saldo en {moneda_extranjera}: {foreign}")
            else:
                print("Error al guardar el nuevo saldo.")
        except Exception as e:
            print(e)
