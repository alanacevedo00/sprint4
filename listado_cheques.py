import csv
import sys
from datetime import datetime
def validar_parametros(tipo_salida, tipo_cheque):
    if tipo_salida not in ["PANTALLA", "CSV"] or tipo_cheque not in ["EMITIDO", "DEPOSITADO"]:
        print("Parámetros no válidos.")
        sys.exit(1)
def filtrar_cheques(cheques, dni, tipo_cheque, estado=None):
    resultados = []
    for cheque in cheques:
        if cheque["DNI"] == dni and cheque["Tipo"] == tipo_cheque:
            if estado is None or cheque["Estado"] == estado:
                resultados.append(cheque)
    return resultados
def exportar_csv(cheques, dni):
    timestamp_actual = datetime.now().strftime('%Y%m%d%H%M%S')
    nombre_archivo = f"{dni}_{timestamp_actual}.csv"
    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        campos = ["NroCheque", "CodigoBanco", "CodigoScurusal", "NumeroCuentaOrigen", "NumeroCuentaDestino",
                  "Valor", "FechaOrigen", "FechaPago", "DNI", "Estado", "Tipo"]
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)
        escritor_csv.writeheader()
        escritor_csv.writerows(cheques)
def main():
    if len(sys.argv) != 5:
        print("Uso: python listado_cheques.py <nombre_archivo_csv> <dni_cliente> <PANTALLA o CSV> <EMITIDO o DEPOSITADO>")
        sys.exit(1)
    nombre_archivo = sys.argv[1]
    dni_cliente = sys.argv[2]
    tipo_salida = sys.argv[3]
    tipo_cheque = sys.argv[4]
    validar_parametros(tipo_salida, tipo_cheque)
    with open(nombre_archivo, mode='r') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        cheques = list(lector_csv)
    try:
        cheques_filtrados = filtrar_cheques(cheques, dni_cliente, tipo_cheque)
        print(f"Cheques filtrados: {len(cheques_filtrados)}")
        if tipo_salida == "PANTALLA":
            for cheque in cheques_filtrados:
                print(cheque)
        elif tipo_salida == "CSV":
            exportar_csv(cheques_filtrados, dni_cliente)
            print(f"Resultados exportados a CSV: {dni_cliente}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
    except Exception as e:
        print(f"Error: {str(e)}")
if __name__ == "__main__":
    main()
