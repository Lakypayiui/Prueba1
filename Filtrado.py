import pdfplumber
import re
from collections import deque

def es_texto_relevante(linea):
    patrones_excluidos = [r'\.com', r'www\.', r'\.org', r'\.pdf']
    for patron in patrones_excluidos:
        if re.search(patron, linea):
            return False
    if len(linea.strip()) < 30:
        return False
    if linea.isupper():
        return False
    if re.match(r'^\d+$', linea.strip()):
        return False
    return True

def procesar_texto_con_pilas_y_cola(texto):
    pila_principal = []
    pila_temporal = []
    cola_final = deque()

    lineas = texto.split('\n')

    for linea in lineas:
        pila_principal.append(linea)

        if es_texto_relevante(linea):
            cola_final.append(linea)
        else:
            pila_temporal.append(linea)

    texto_filtrado = "\n".join(cola_final)
    return texto_filtrado

def extraer_texto_de_pdf(pdf_path):
    texto_completo = ""
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + '\n'
    return texto_completo

def guardar_en_txt(texto, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(texto)
    print(f"Texto guardado en {nombre_archivo}")

def main(pdf_path, nombre_archivo_txt):
    texto = extraer_texto_de_pdf(pdf_path)
    texto_limpio = procesar_texto_con_pilas_y_cola(texto)
    guardar_en_txt(texto_limpio, nombre_archivo_txt)

pdf_path = "sistemas_conscientes.pdf"
nombre_archivo_txt = "texto_filtrado.txt"
main(pdf_path, nombre_archivo_txt)