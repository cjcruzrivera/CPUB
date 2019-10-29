from flask import Flask, abort, request, render_template, redirect

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return render_template("inicio.html")

@app.route('/registro',methods=['GET', 'POST'])
def registro():
    if request.method == "POST":
        return render_template("registro.html", registrado=True)
    elif request.method == "GET":
        return render_template("registro.html")

@app.route('/consulta',methods=['GET'])
def consulta():
    return render_template("consulta.html")


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')