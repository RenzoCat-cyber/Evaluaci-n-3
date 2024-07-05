import os
import time
import csv
import json
import random
from datetime import datetime

def menu():
    os.system('cls')
    print('Seleccione una de las siguientes opciones: ')
    print('1. Precargar ventas y guardar en ventas.json')
    print('2. Crear nuevas ventas')
    print('3. Reporte de sueldos')
    print('4. Ver Estadísticas por tienda')
    print('5. Salir')

def error():
    os.system('cls')
    print('La opción ingresada no es válida')
    time.sleep(2)

def guardar_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def leer_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def id_venta_mayor(ventas):
    id_mayor = 0
    for venta in ventas["ventas"]:
        if int(venta["id_venta"]) > id_mayor:
            id_mayor = int(venta["id_venta"])
    return id_mayor

def cargar_ventas(vendedores, ventas, path_ventas):
    id_mayor = id_venta_mayor(ventas)
    for i in range(500):
        vendedor = random.choice(vendedores)
        id_mayor += 1
        nueva_venta = {
            "id_venta": id_mayor,
            "id_vendedor": vendedor["id_vendedor"],
            "id_tienda": vendedor["id_tienda"],
            "fecha": datetime.now().strftime("%d-%m-%Y"),
            "total_venta": round(random.randint(100000, 300000), -2)
        }
        ventas["ventas"].append(nueva_venta)
    guardar_json(path_ventas, ventas)
    os.system('cls')
    print('Ventas agregadas de manera exitosa')
    time.sleep(2)

def crear_venta(vendedores, ventas, tiendas, path_ventas):
    id_mayor = id_venta_mayor(ventas)
    while True:
        os.system('cls')
        print('Seleccione su tienda para iniciar venta o "6" para salir: ')
        for tienda in tiendas:
            print(f'{tienda["id_tienda"]} - {tienda["nombre"]}')
        
        try:
            opctienda = int(input('Ingrese el ID de la tienda: '))
        except ValueError:
            error()
            continue

        if opctienda < 1 or opctienda > 6:
            error()
        else:
            if 1 <= opctienda <= 5:
                os.system('cls')
                print('Seleccione Vendedor: ')
                for vendedor in vendedores:
                    if opctienda == vendedor["id_tienda"]:
                        print(f'ID: {vendedor["id_vendedor"]} -->> {vendedor["nombre"]} {vendedor["apellido"]}')
                print('------------------------------------')
                try:
                    opcvendedor = input('Ingrese el ID del vendedor: ')
                except ValueError:
                    error()
                    continue

                id_mayor += 1
                total_venta = int(input('Ingrese el monto de la venta: '))
                nueva_venta = {
                    "id_venta": id_mayor,
                    "id_vendedor": opcvendedor,
                    "id_tienda": opctienda,
                    "fecha": datetime.now().strftime("%d-%m-%Y"),
                    "total_venta": total_venta,
                }
                ventas["ventas"].append(nueva_venta)
                guardar_json(path_ventas, ventas)
                os.system('cls')
                print('Venta agregada de manera exitosa')
                time.sleep(2)
                break
            else:
                break

def reporte_sueldos(vendedores, ventas, tiendas):
    for vendedor in vendedores:
        total_ventas = 0
        bono = 0
        salud = int(vendedor["sueldo_base"] * 0.07)
        afp = int(vendedor["sueldo_base"] * 0.12)
        for venta in ventas["ventas"]:
            if vendedor["id_vendedor"] == venta["id_vendedor"]:
                total_ventas += venta["total_venta"]
        
        if total_ventas >= 5000000:
            bono = 0.15 * total_ventas
        elif total_ventas >= 3000000:
            bono = 0.12 * total_ventas
        elif total_ventas >= 1000000:
            bono = 0.10 * total_ventas

        sueldo_liquido = (vendedor["sueldo_base"] - salud - afp) + bono
        nombre_tienda = next(tienda["nombre"] for tienda in tiendas if tienda["id_tienda"] == vendedor["id_tienda"])

        print(f'Nombre: {vendedor["nombre"]} {vendedor["apellido"]} | Tienda: {nombre_tienda} | Sueldo Bruto: {vendedor["sueldo_base"]} | Bono: {bono} | Desc. Salud: {salud} | Desc. AFP: {afp} | Sueldo Líquido: {sueldo_liquido}')

def generar_estadisticas(vendedores, ventas, tiendas, path_estadisticas):
    estadisticas = [["Tienda", "Sueldo más alto", "Sueldo más bajo", "Promedio de sueldos", "Número de ventas", "Promedio de ventas"]]
    
    for tienda in tiendas:
        tienda_id = tienda["id_tienda"]
        sueldos_tienda = []
        for v in vendedores:
            if v["id_tienda"] == tienda_id:
                sueldos_tienda.append(v["sueldo_base"])

        ventas_tienda = []
        for v in ventas["ventas"]:
            if v["id_tienda"] == tienda_id:
                ventas_tienda.append(v["total_venta"])

        max_sueldo = max(sueldos_tienda) if sueldos_tienda else 0
        min_sueldo = min(sueldos_tienda) if sueldos_tienda else 0
        promedio_sueldo = sum(sueldos_tienda) / len(sueldos_tienda) if sueldos_tienda else 0

        num_ventas = len(ventas_tienda)
        promedio_venta = sum(ventas_tienda) / num_ventas if ventas_tienda else 0

        estadisticas.append([tienda["nombre"], max_sueldo, min_sueldo, promedio_sueldo, num_ventas, promedio_venta])

    guardar_csv(path_estadisticas, estadisticas)
    print("Estadísticas guardadas en estadisticas.csv")

def guardar_csv(file_path, data):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def main():
    while True:
        path_vendedores = 'vendedores.json'
        path_tiendas = 'tiendas.json'
        path_ventas = 'ventas.json'
        path_estadisticas = 'estadisticas.csv'
        vendedores = leer_json(path_vendedores)
        tiendas = leer_json(path_tiendas)
        ventas = leer_json(path_ventas)
        menu()
        try:
            opcion = int(input('Ingrese la opción: '))
        except ValueError:
            error()
            continue

        if opcion < 1 or opcion > 5:
            error()
        else:
            if opcion == 1:
                print('Precargar ventas')
                cargar_ventas(vendedores, ventas, path_ventas)
            elif opcion == 2:
                print('Crear venta')
                crear_venta(vendedores, ventas, tiendas, path_ventas)
            elif opcion == 3:
                print('Reporte de sueldos')
                reporte_sueldos(vendedores, ventas, tiendas)
                input("Presione Enter para continuar...")
            elif opcion == 4:
                print('Ver Estadísticas')
                generar_estadisticas(vendedores, ventas, tiendas, path_estadisticas)
                input("Presione Enter para continuar...")
            elif opcion == 5:
                os.system('cls')
                print('Saliendo de la app')
                time.sleep(2)
                break

if __name__ == '__main__':
    main()
