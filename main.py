from flask import Flask, render_template, request,redirect,url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app =  Flask(__name__, template_folder= template_dir)


@app.route('/')
def index():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM books")
    result_books = cursor.fetchall()
    insertObject= []
    columnNames = [column[0] for column in cursor.description ]
    for record in result_books:
        insertObject.append(dict(zip(columnNames,record)))
    
    cursor.execute("SELECT * FROM book")
    result_book = cursor.fetchall()
    insertObject1= []
    columnNames1 = [column[0] for column in cursor.description ]
    for record in result_book:
        insertObject1.append(dict(zip(columnNames1,record)))

    cursor.close()

    return render_template('index.html',data=[insertObject,insertObject1])


@app.route("/addCollection", methods=['POST'])
def addCollection():
    name_collection = request.form["nombre_library"]
    quality = request.form["quality_library"]
    cursor = db.database.cursor()
    sql1= "INSERT INTO books (name,quality) VALUES(%s,%s)"
    data = (name_collection,quality)
    cursor.execute(sql1,data)
    db.database.commit()
    return redirect(url_for('index'))

@app.route('/deleteCollection/<string:id>')
def deleteCollection(id):
    cursor = db.database.cursor()
    sql1= "DELETE FROM books WHERE id=%s"
    data = (id,)
    cursor.execute(sql1,data)
    db.database.commit()
    return redirect(url_for('index'))

@app.route("/editCollection/<string:id>", methods=["POST"])
def editCollection(id):
    name_collection = request.form["nombre_library"]
    quality = request.form["quality_library"]
    cursor = db.database.cursor()
    sql1= "UPDATE books set name_collection = %s, quality_library = %s WHERE id =  %d  "
    data = (name_collection,quality,id)
    cursor.execute(sql1,data)
    db.database.commit()
    return redirect(url_for('index'))

 


@app.route("/addBook", methods=['POST'])
def addBook():
    nombre_book = request.form["nombre_book"]
    collection_book = request.form["collection_book"]
    location_book = request.form["location_book"]
    cursor = db.database.cursor()
    sql1= "INSERT INTO book (name,collection,location) VALUES(%s,%d,%s)"
    data = (nombre_book,collection_book,location_book)
    cursor.execute(sql1,data)
    db.database.commit()
    return redirect(url_for('index'))




@app.route('/deleteBook/<string:id>')
def deleteBook(id):
    cursor = db.database.cursor()
    sql1= "DELETE FROM book WHERE id=%s"
    data = (id,)
    cursor.execute(sql1,data)
    db.database.commit()
    return redirect(url_for('index'))

@app.route("/editBook/<string:id>", methods=["POST"])
def editBook(id):
    nombre_book = request.form["nombre_book"]
    collection_book = request.form["collection_book"]
    location_book = request.form["location_book"]
    cursor = db.database.cursor()
    sql1= "UPDATE books set nombre_book = %s, collection_book = %d, location_book = %s WHERE id =  %d  "
    data = (nombre_book,collection_book,location_book)
    cursor.execute(sql1,data)
    db.database.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)