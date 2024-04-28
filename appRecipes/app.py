from flask import Flask, render_template, request, redirect, url_for, session
from utils.dbHelper import add_comment_to_post, add_recipe_to_db, get_comments_by_post_id, get_recipe_by_id, get_recipes

app = Flask(__name__)
#Тестовый ключ. Обязательно поменять на продакшене 
app.secret_key = b'kd8d#$1!_r5dc@s28d=3'

@app.route('/')
def index():
    recipes = get_recipes()
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    recipes = get_recipes()
    if(recipe_id <= len(recipes) and recipe_id > 0):
        comments = get_comments_by_post_id(recipe_id)
        return render_template('recipe.html', recipe=recipes[recipe_id - 1], comments=comments)
    else:
        return redirect(url_for('index'))
    
@app.route('/recipe/<int:recipe_id>/add_comment', methods=['POST'])
def add_comment(recipe_id):
    user = request.form.get('user')
    text = request.form.get('text')
    add_comment_to_post(recipe_id, user, text)
    return redirect(url_for('recipe', recipe_id=recipe_id))

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'role' not in session:
        return "Forbidden"
    if (session['role'] != 'admin'):
        return "Forbidden"
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        add_recipe_to_db(name, description)

        return redirect(url_for('index'))

    return render_template('add_recipe.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #пока админ захардкожен, потом добавим возможность брать его из БД
        if username == 'admin' and password == 'password':
            session['role'] = 'admin'
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

if (__name__ == '__main__'):
    app.run(port = 5002)