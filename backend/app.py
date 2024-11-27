import folium

# Crear mapa centrado en una ubicación
mapa = folium.Map(location=[-31.24735587063069, -61.51029371921464], zoom_start=16)  # Rafela, como ejemplo.

# Guardar el mapa
mapa.save("mapa.html")


# Agregar marcadores
def agregar_marcador(mapa, lat, lon, categoria, descripcion):
    folium.Marker(
        [lat, lon],
        popup=f"Categoría: {categoria}<br>{descripcion}",
        icon=folium.Icon(color="blue" if categoria == "Restaurante" else "green")
    ).add_to(mapa)

#Base datos para marcadores
import sqlite3

conn = sqlite3.connect("marcadores.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS marcadores (
        id INTEGER PRIMARY KEY,
        lat REAL,
        lon REAL,
        categoria TEXT,
        descripcion TEXT
    )
""")
conn.commit()


#interfaz marcadores
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/")
def home():
    # Cargar mapa con marcadores desde la base de datos
    mapa = folium.Map(location=[-34.6037, -58.3816], zoom_start=12)
    cursor.execute("SELECT lat, lon, categoria, descripcion FROM marcadores")
    for lat, lon, categoria, descripcion in cursor.fetchall():
        agregar_marcador(mapa, lat, lon, categoria, descripcion)
    mapa.save("templates/mapa.html")
    return render_template("index.html")

@app.route("/agregar", methods=["POST"])
def agregar():
    lat = request.form["lat"]
    lon = request.form["lon"]
    categoria = request.form["categoria"]
    descripcion = request.form["descripcion"]
    cursor.execute("INSERT INTO marcadores (lat, lon, categoria, descripcion) VALUES (?, ?, ?, ?)", (lat, lon, categoria, descripcion))
    conn.commit()
    return redirect("/")


#redireccionar a marcador
@app.route("/marcador/<lat>/<lon>")
def ir_a_marcador(lat, lon):
    mapa = folium.Map(location=[float(lat), float(lon)], zoom_start=15)
    mapa.save("templates/mapa.html")
    return render_template("mapa.html")
