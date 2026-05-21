from flask import Flask, render_template

# Inicializa la aplicación
app = Flask(__name__)

# Define la ruta principal (página de inicio)
@app.route('/')
def home():
    username = "Marta"
    return render_template('index.html', username=username)

# Ejecuta el servidor de desarrollo
if __name__ == '__main__':
    app.run(debug=True)
