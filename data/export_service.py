import csv
import os
from datetime import datetime
from decimal import Decimal
from data.api_service import ApiService
class ExportService:

    def __init__(self):
        self.api_service = ApiService()
        self._rates = None

    def _get_rates(self):
        if self._rates is None:
            try:
                self._rates = self.api_service.get_all_latest_rate_eur()
            except Exception:
                self._rates = None
        return self._rates

    def _cotizacion_ars(self, currency):
        rates = self._get_rates()
        if rates is None or currency not in rates or "ARS" not in rates:
            return None
        return Decimal(str(rates["ARS"])) / Decimal(str(rates[currency]))

    def _build_rows(self, accounts, currency_filter=None):
        rows = []
        total_ars = Decimal("0")
        for moneda, saldo_str in sorted(accounts.items()):
            if currency_filter and currency_filter != "TODAS" and moneda != currency_filter:
                continue
            saldo = Decimal(saldo_str)
            cotizacion = self._cotizacion_ars(moneda) if moneda != "ARS" else Decimal("1")
            if cotizacion is not None:
                valor_ars = (saldo * cotizacion).quantize(Decimal("0.01"))
                total_ars += valor_ars
            else:
                valor_ars = None
            rows.append({
                "moneda": moneda,
                "saldo": saldo,
                "cotizacion": cotizacion,
                "valor_ars": valor_ars,
            })
        return rows, total_ars.quantize(Decimal("0.01"))

    def export_to_csv(self, accounts, username, filepath, currency_filter=None):
        rows, total_ars = self._build_rows(accounts, currency_filter)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Resumen de Cuentas -", username])
            writer.writerow(["Fecha:", datetime.now().strftime("%d/%m/%Y %H:%M")])
            writer.writerow([])
            writer.writerow(["Moneda", "Saldo", "Cotizacion ARS", "Valor en ARS"])
            for r in rows:
                cotiz = f"{r['cotizacion']:.4f}" if r["cotizacion"] is not None else "N/A"
                valor = f"{r['valor_ars']:.2f}" if r["valor_ars"] is not None else "N/A"
                writer.writerow([r["moneda"], f"{r['saldo']:.2f}", cotiz, valor])
            writer.writerow([])
            writer.writerow(["TOTAL EN ARS", "", "", f"{total_ars:.2f}"])
        return filepath

    def export_to_txt(self, accounts, username, filepath, currency_filter=None):
        rows, total_ars = self._build_rows(accounts, currency_filter)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
        sep = "=" * 50
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{sep}\n")
            f.write(f"  Resumen de Cuentas - {username}\n")
            f.write(f"  Fecha: {ahora}\n")
            f.write(f"{sep}\n")
            f.write(f"\n")
            f.write(f"  {'Moneda':<8} {'Saldo':>10}  {'Cotizacion':>12}  {'Valor ARS':>12}\n")
            f.write(f"  {'------':<8} {'-------':>10}  {'-----------':>12}  {'----------':>12}\n")
            for r in rows:
                cotiz = f"{r['cotizacion']:.4f}" if r["cotizacion"] is not None else "N/A"
                valor = f"{r['valor_ars']:.2f}" if r["valor_ars"] is not None else "N/A"
                f.write(f"  {r['moneda']:<8} {r['saldo']:>10.2f}  {cotiz:>12}  {valor:>12}\n")
            f.write(f"\n")
            f.write(f"{sep}\n")
            f.write(f"  TOTAL EN ARS: {total_ars:.2f}\n")
            f.write(f"{sep}\n")
        return filepath

    def export_to_pdf(self, accounts, username, filepath, currency_filter=None):
        from fpdf import FPDF

        rows, total_ars = self._build_rows(accounts, currency_filter)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Courier", size=10)

        ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
        sep = "=" * 56

        line_height = 5

        def writeln(text=""):
            pdf.cell(0, line_height, text, new_x="LMARGIN", new_y="NEXT")

        writeln(sep)
        writeln(f"  Resumen de Cuentas - {username}")
        writeln(f"  Fecha: {ahora}")
        writeln(sep)
        writeln()
        writeln(f"  {'Moneda':<8} {'Saldo':>10}  {'Cotizacion':>12}  {'Valor ARS':>12}")
        writeln(f"  {'------':<8} {'-------':>10}  {'-----------':>12}  {'----------':>12}")
        for r in rows:
            cotiz = f"{r['cotizacion']:.4f}" if r["cotizacion"] is not None else "N/A"
            valor = f"{r['valor_ars']:.2f}" if r["valor_ars"] is not None else "N/A"
            writeln(f"  {r['moneda']:<8} {r['saldo']:>10.2f}  {cotiz:>12}  {valor:>12}")
        writeln()
        writeln(sep)
        writeln(f"  TOTAL EN ARS: {total_ars:.2f}")
        writeln(sep)

        pdf.output(filepath)
        return filepath

    def export(self, accounts, username, formato, currency_filter=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = {"1": "csv", "2": "txt", "3": "pdf"}.get(formato, "txt")
        filename = f"{username}_resumen_{timestamp}.{ext}"
        filepath = os.path.join("data", "exports", filename)

        if formato == "1":
            return self.export_to_csv(accounts, username, filepath, currency_filter)
        elif formato == "2":
            return self.export_to_txt(accounts, username, filepath, currency_filter)
        elif formato == "3":
            return self.export_to_pdf(accounts, username, filepath, currency_filter)
        else:
            raise ValueError("Formato no valido. Use 1 (CSV), 2 (TXT) o 3 (PDF).")
