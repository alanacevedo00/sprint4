import csv
import sys
from datetime import datetime

def filtrar_cheques(cheques, dni, tipo_cheque, estado=None, fecha_inicio=None, fecha_fin=None):
    resultados = []
    for cheque in cheques:
        if cheque["DNI"] == dni and cheque["Estado"] == estado:
            if tipo_cheque == "EMITIDO" and "FechaOrigen" in cheque:
                fecha_cheque = datetime.fromtimestamp(int(cheque["FechaOrigen"])).strftime('%Y-%m-%d %H:%M:%S')
            elif tipo_cheque == "DEPOSITADO" and "FechaPago" in cheque:
                fecha_cheque = datetime.fromtimestamp(int(cheque["FechaPago"])).strftime('%Y-%m-%d %H:%M:%S')
            else:
                continue

            if (not fecha_inicio or fecha_inicio <= fecha_cheque) and (not fecha_fin or fecha_cheque <= fecha_fin):
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
    timestamp_actual = datetime.now().strftime("%Y%m%d%H%M%S")
    if len(sys.argv) < 6:
        print("Uso: python listado_cheques.py <nombre_archivo_csv> <dni_cliente> <PANTALLA o CSV> <EMITIDO o DEPOSITADO> [--estado <estado_cheque>] [--fecha_inicio <fecha>] [--fecha_fin <fecha>]")
        sys.exit(1)

    nombre_archivo = sys.argv[1]
    dni_cliente = sys.argv[2]
    tipo_salida = sys.argv[3]
    tipo_cheque = sys.argv[4]
    estado_cheque = None
    fecha_inicio = None
    fecha_fin = None

    if tipo_salida not in ["PANTALLA", "CSV"] or tipo_cheque not in ["EMITIDO", "DEPOSITADO"]:
        print("Parámetros no válidos.")
        sys.exit(1)

    if tipo_cheque == "EMITIDO":
        estado_index = 5
        fecha_inicio_index = 7
        fecha_fin_index = 9
    else:
        estado_index = 7
        fecha_inicio_index = 5
        fecha_fin_index = 8

    if len(sys.argv) > estado_index and sys.argv[estado_index] == "--estado":
        estado_cheque = sys.argv[estado_index + 1]

    if len(sys.argv) > fecha_inicio_index and sys.argv[fecha_inicio_index] == "--fecha_inicio":
        fecha_inicio = datetime.strptime(sys.argv[fecha_inicio_index + 1], "%Y-%m-%d %H:%M:%S")

    if len(sys.argv) > fecha_fin_index and sys.argv[fecha_fin_index] == "--fecha_fin":
        fecha_fin = datetime.strptime(sys.argv[fecha_fin_index + 1], "%Y-%m-%d %H:%M:%S")

    with open(nombre_archivo, mode='r') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        cheques = list(lector_csv)

    try:
        cheques_filtrados = filtrar_cheques(cheques, dni_cliente, tipo_cheque, estado_cheque, fecha_inicio, fecha_fin)
        if tipo_salida == "PANTALLA":
            for cheque in cheques_filtrados:
                print(cheque)
        elif tipo_salida == "CSV":
            exportar_csv(cheques_filtrados, dni_cliente)
            print(f"Resultados exportados a CSV: {dni_cliente}_{timestamp_actual}.csv")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
