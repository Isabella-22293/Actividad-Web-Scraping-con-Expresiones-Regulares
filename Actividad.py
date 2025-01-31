import re
import csv
import html

# Lee un archivo utilizando un búfer con centinelas.
def leer_con_buffer(file_path, buffer_size=4096):
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            buffer = file.read(buffer_size)
            if not buffer:
                break
            yield buffer
            
# Extrae los nombres de los productos y las URLs de las imágenes del archivo HTML.
def extraer_productos_y_imagenes(file_path):
    nombre_producto_pattern = re.compile(r'<img.*?alt="(.*?)".*?src="(.*?)"')
    productos = []
    urls_vistas = set()  # Evitar duplicados
    buffer = ''
    
    for chunk in leer_con_buffer(file_path):
        buffer += chunk
        # Buscar nombres de productos y URLs de imágenes
        for match in nombre_producto_pattern.finditer(buffer):
            nombre_producto = match.group(1)
            url_imagen = match.group(2)
        
            # Decodificar las entidades HTML
            url_imagen = html.unescape(url_imagen)
            
            # Verificar si la URL ya ha sido vista
            if url_imagen not in urls_vistas:
                productos.append({'nombre': nombre_producto, 'imagen': url_imagen})
                urls_vistas.add(url_imagen)
        
        # Mantener el final del buffer para el siguiente chunk
        buffer = buffer[-len(chunk):]

    return productos

# Guarda la lista de productos en un archivo CSV.
def guardar_en_csv(productos, output_file='productos.csv'):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Nombre del Producto', 'URL de la Imagen']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for producto in productos:
            writer.writerow({'Nombre del Producto': producto['nombre'], 'URL de la Imagen': producto['imagen']})

if __name__ == "__main__":
    archivo_html = "D:\Descargas\EPIC.htm"    
    productos = extraer_productos_y_imagenes(archivo_html)    
    guardar_en_csv(productos)
    print(f"Se han guardado {len(productos)} productos en 'productos.csv'")
