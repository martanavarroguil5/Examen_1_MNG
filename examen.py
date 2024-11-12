import networkx as nx
import timeit
from memory_profiler import profile

localidades = { 
    "Madrid": [("Alcorcón", 13), ("Villaviciosa de Odón", 22), ("Alcalá de Henares", 35)], 
    "Villanueva de la Cañada": [("Villaviciosa de Odón", 11), ("Boadilla del Monte", 7)], 
    "Alcorcón": [("Madrid", 13), ("Móstoles", 5)], 
    "Móstoles": [("Alcorcón", 5), ("Fuenlabrada", 8)], 
    "Fuenlabrada": [("Móstoles", 8), ("Getafe", 10)], 
    "Getafe": [("Fuenlabrada", 10), ("Madrid", 16)], 
    "Villaviciosa de Odón": [("Madrid", 22), ("Villanueva de la Cañada", 11)], 
    "Boadilla del Monte": [("Villanueva de la Cañada", 7), ("Madrid", 15)], 
    "Alcalá de Henares": [("Madrid", 35), ("Torrejón de Ardoz", 15)], 
    "Torrejón de Ardoz": [("Alcalá de Henares", 15), ("Madrid", 20)] 
} 

# Creamos el grafo ponderado
G = nx.Graph()
# Añadir nodos y aristas con pesos al grafo
for localidad, conexiones in localidades.items():
    for destino, distancia in conexiones:
        G.add_edge(localidad, destino, weight=distancia)

#Función que encuentra la ruta mas corta entre dos localidades
# Dijkstra es la opción más adecuada porque ya existe una funcion en el modulo networkx
@profile
def encontrar_ruta_mas_corta(G, inicio, fin):
    ruta = nx.dijkstra_path(G, source=inicio, target=fin, weight='weight')
    
    # Mostrar la ruta encontrada
    print(f"La ruta más corta de {inicio} a {fin} es: {ruta}")
    
    # También se puede mostrar la distancia total de la ruta
    distancia = nx.dijkstra_path_length(G, source=inicio, target=fin, weight='weight')
    print(f"La distancia total es: {distancia} km")


# Función para ver las localidades con conexiones cortas dentro de un 
# umbral de 15 km
@profile   
def localidades_con_conexiones_cortas(G, umbral=15):
    localidades_cortas = []
    
    # Iteramos sobre todos los nodos del grafo
    for localidad in G.nodes():
        # Verificamos si todas las conexiones de la localidad tienen distancia 
        # menor al umbral = 15 km
        if all(G[localidad][destino]['weight'] < umbral for destino in G[localidad]):
            localidades_cortas.append(localidad)
    
    # Imprimir las localidades que cumplen la condición
    print(f"Localidades con todas sus rutas menores de {umbral} km:")
    for localidad in localidades_cortas:
        print(localidad)

# Comprobamos si el grafo es conexo utilizando una funcion de networx que lo
# evalua directamente
# Elegimos un nodo inicial arbitrario, en este caso, el primer nodo del grafo
@profile
@profile
def es_grafo_conexo(G):
    # Utilizamos la función is_connected para verificar la conectividad
    if nx.is_connected(G):
        print("El grafo es conexo.")
        return True
    else:
        print("El grafo NO es conexo.")
        return False
    
#Función que encuentra las rutas alternativas sin ciclos
# Se implementa una funcion de networkx para busqeda DFS
@profile
def encontrar_rutas_sin_ciclos(G, inicio, fin):
    # Lista para almacenar las rutas encontradas
    rutas = []
    
    # Función auxiliar DFS que busca todas las rutas sin ciclos
    def dfs_rutas(actual, destino, ruta_actual, visitados):
        # Si llegamos al destino, guardamos la ruta
        if actual == destino:
            rutas.append(ruta_actual)
            return
        
        # Recorremos los vecinos
        for vecino in G[actual]:
            # Si el vecino no está en la ruta actual (evitamos ciclos)
            if vecino not in visitados:
                # Marcamos el vecino como visitado y exploramos
                visitados.add(vecino)
                dfs_rutas(vecino, destino, ruta_actual + [vecino], visitados)
                # Desmarcamos el vecino para otras exploraciones
                visitados.remove(vecino)
    
    # Iniciamos DFS desde el nodo de inicio
    visitados = set([inicio])
    dfs_rutas(inicio, fin, [inicio], visitados)
    
    # Mostrar las rutas encontradas
    print(f"Rutas alternativas sin ciclos de {inicio} a {fin}:")
    for ruta in rutas:
        print(" -> ".join(ruta))
    
    # Si no se encontró ninguna ruta, indicar que no hay caminos alternativos
    if not rutas:
        print(f"No hay rutas alternativas sin ciclos entre {inicio} y {fin}.")
    



# Llamada a las funciones
# Llamar a las funciones para realizar el análisis de memoria
localidades_con_conexiones_cortas(G, 15)
encontrar_ruta_mas_corta(G, "Madrid", "Getafe")
es_grafo_conexo(G)
encontrar_rutas_sin_ciclos(G, "Madrid", "Getafe")





# Análisis de eficiencia con timeit 

# Medir el tiempo de ejecución de la función `localidades_con_conexiones_cortas`
tiempo_localidades = timeit.timeit(lambda: localidades_con_conexiones_cortas(G, 15), number=1)
print(f"Tiempo de ejecución de localidades_con_conexiones_cortas: {tiempo_localidades} segundos")

# Medir el tiempo de ejecución de la función `encontrar_ruta_mas_corta`
tiempo_ruta_corta = timeit.timeit(lambda: encontrar_ruta_mas_corta(G, "Madrid", "Getafe"), number=1)
print(f"Tiempo de ejecución de encontrar_ruta_mas_corta: {tiempo_ruta_corta} segundos")

# Medir el tiempo de ejecución de la función `es_grafo_conexo`
tiempo_grafo_conexo = timeit.timeit(lambda: es_grafo_conexo(G), number=1)
print(f"Tiempo de ejecución de es_grafo_conexo: {tiempo_grafo_conexo} segundos")

# Medir el tiempo de ejecución de la función `encontrar_rutas_sin_ciclos`
tiempo_rutas_sin_ciclos = timeit.timeit(lambda: encontrar_rutas_sin_ciclos(G, "Madrid", "Getafe"), number=1)
print(f"Tiempo de ejecución de encontrar_rutas_sin_ciclos: {tiempo_rutas_sin_ciclos} segundos")

# Análisis de Complejidad de las Funciones

# encontrar_ruta_mas_corta:
#   - O (Big-O): O(n log n) - Complejidad del algoritmo de Dijkstra
#   - Ω (Omega): Ω(n) - Caso mínimo recorriendo todos los nodos
#   - Θ (Theta): Θ(n log n) - Complejidad ajustada, similar a O

# localidades_con_conexiones_cortas:
#   - O (Big-O): O(n) - Recorre todos los nodos y sus conexiones
#   - Ω (Omega): Ω(n) - Caso mínimo con pocos nodos
#   - Θ (Theta): Θ(n) - Ajustada, similar a O

# es_grafo_conexo:
#   - O (Big-O): O(n) - Complejidad de DFS en grafos
#   - Ω (Omega): Ω(n) - Igual a O, DFS siempre recorre nodos y aristas
#   - Θ (Theta): Θ(n) - Ajustada, similar a O

# encontrar_rutas_sin_ciclos:
#   - O (Big-O): O(2^n) - Número de rutas sin ciclos puede crecer exponencialmente
#   - Ω (Omega): Ω(n) - Caso mínimo con pocos caminos
#   - Θ (Theta): Θ(2^n) - Complejidad ajustada, similar a O




# Bonus
