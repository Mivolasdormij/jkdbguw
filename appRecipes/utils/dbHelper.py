import sqlite3
import json

def add_comment_to_post(recipe_id, author, text):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()

    c.execute("INSERT INTO comments (author, text) VALUES (?, ?)", (author, text))
    comment_id = c.lastrowid  

    c.execute("SELECT comments FROM posts WHERE id=?", (recipe_id,))
    row = c.fetchone()

    if row:
        current_comments = json.loads(row[0])  
        current_comments.append(comment_id)
        updated_comments = json.dumps(current_comments)
        
        c.execute("UPDATE posts SET comments=? WHERE id=?", (updated_comments, recipe_id))
        conn.commit()

        print("Комментарий успешно добавлен и обновлен для рецепта")
    else:
        print("Рецепт с указанным идентификатором не найден")

    conn.close()

def add_recipe_to_db(name, description):
    empty_comments = json.dumps([])
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()

    query = "INSERT INTO posts (name, description, comments) VALUES (?, ?, ?)"
    c.execute(query, (name, description, empty_comments))

    conn.commit()
    conn.close()


def get_recipe_by_id(recipe_id):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()

    c.execute("SELECT * FROM posts WHERE id=?", (recipe_id,))
    row = c.fetchone()

    if row:
        recipe_data = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'comments': json.loads(row[3])
        }
        print("Данные по рецепту успешно получены")
        return recipe_data
    else:
        print("Рецепт с указанным идентификатором не найден")
        return None

def get_recipe_by_id(recipe_id):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id=?", (recipe_id,))
    row = c.fetchone()

    if row:
        recipe_data = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'comments': json.loads(row[3])  # Преобразование JSON в Python объект
        }
        print("Данные по рецепту успешно получены")
        return recipe_data
    else:
        print("Рецепт с указанным идентификатором не найден")
        return None

def get_comments_by_post_id(post_id):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()

    c.execute("SELECT author, text FROM comments WHERE id IN (SELECT json_each.value FROM posts, json_each(posts.comments) as json_each WHERE posts.id=?);", (post_id,)) #нужно додумать последнюю часть запроса

    comments_list = [{'name': row[0], 'text': row[1]} for row in c.fetchall()]

    conn.close()
    return comments_list

def get_recipes():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()

    c.execute("SELECT * FROM posts")
    
    recipes_list = []
    
    for row in c.fetchall():
        recipe = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'comments': json.loads(row[3]) if row[3] else [] 
        }
        recipes_list.append(recipe)

    conn.close()

    return recipes_list