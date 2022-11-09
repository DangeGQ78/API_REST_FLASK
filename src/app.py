from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

conexion = MySQL(app)


@app.route('/cursos', methods=['GET'])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * from estudiante"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []
        for fila in datos:
            curso = {'codigo': fila[0], 'nombre': fila[1], 'creditos': fila[2]}
            cursos.append(curso)
        return jsonify({'cursos': cursos, 'mensaje': "cursos_listados"})
    except:
        return jsonify({'mensaje': "Error"})


@app.route('/cursos/<codigo>', methods=['GET'])
def leerCurso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * from estudiante where codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {'codigo': datos[0],
                     'nombre': datos[1], 'creditos': datos[2]}
            return jsonify({'curso': curso, 'mensaje': "curso encontrado"})
    except:
        return jsonify({'mensaje': "curso no encontrado"})


@app.route('/cursos', methods=['POST'])
def registrar_curso():
    try:
        # print(request.json)
        repetido = curso_repetido(request.json['codigo'])

        if repetido == False:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO estudiante (codigo,nombre,creditos) 
                VALUES ('{0}','{1}','{2}')""".format(request.json['codigo'],
                                                     request.json['nombre'], request.json['creditos'])
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "curso registrado"})
        else:
            return jsonify({'mensaje': "el curso ya esta registrado"})
    except:
        return jsonify({'mensaje': "curso no registrado"})


@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar(codigo):
    try:
        # print(request.json)
        repetido = curso_repetido(codigo)

        if repetido == True:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM estudiante WHERE codigo = '{0}'".format(codigo)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "curso eliminado"})
        else:
            return jsonify({'mensaje': "no se encuentra el curso"})
    except:
        return jsonify({'mensaje': "error al intentar eliminar"})


@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = """UPDATE estudiante SET nombre = '{0}', creditos = '{1}' 
            WHERE codigo = '{2}'""".format(request.json['nombre'], request.json['creditos'], codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "curso actualizado"})
    except:
        return jsonify({'mensaje': "curso no encontrado"})


def curso_repetido(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * from estudiante where codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos[0] == codigo:
            return True
    except:
        return False


def pagina_no_encontrada(error):
    return "<h1>la pagina que intentas buscar no existe</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
