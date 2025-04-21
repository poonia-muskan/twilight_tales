from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_stories():
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute('SELECT id, title FROM stories')
    stories = c.fetchall()
    conn.close()

    image_map = {
        'School Love 💌': 'school.jpg',
        'Forest Adventure 🌳': 'forest_background.jpg',
        'Haunted Mansion 🦇': 'mansion_background.jpg',
        'Mystery Key 🔐': 'key_background.jpg',
        'Lost Island 🏝️': 'island_background.jpg',
        'A Journey Together 🌍': 'journey_background.jpg',
        'A Second Chance ❤️': 'second_chance_background.jpg',
        'Enchanted Garden 🌸': 'garden_background.jpg',
        'A New Beginning 💑': 'new_beginnings_background.jpg',
        'Child Rights 🧒': 'child_rights.jpg',
        'The Start of Us 💖': 'first_kiss_background.jpg',
        'Twisted Love 💕': 'twisted_love.jpg',
        'Twisted Games 🖤': 'twisted_games.jpg',
        'Twisted Hate 🔥': 'twisted_hate.jpg',
        'Twisted Lies 🕸️': 'twisted_lies.jpg',
        'Transfer Student 🔪': 'transfer_student.jpg'
    }

    story_data = []
    for s in stories:
        story_data.append({
            'id': s[0],
            'title': s[1],
            'image': image_map.get(s[1], 'default.jpg')  
        })
    return story_data

@app.route('/')
def index():
    stories = get_stories()
    return render_template('webindex.html', stories=stories)

@app.route('/story/<int:story_id>/step/<int:step_number>')
def story_step(story_id, step_number):
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()

    c.execute(''' 
        SELECT content, option1, option2, next1, next2 
        FROM steps 
        WHERE story_id = ? AND step_number = ?
    ''', (story_id, step_number))
    step = c.fetchone()

    c.execute('SELECT title FROM stories WHERE id = ?', (story_id,))
    title_result = c.fetchone()
    story_title = title_result[0] if title_result else 'Story'

    conn.close()

    if step:
        content, option1, option2, next1, next2 = step
        return render_template(
            'story.html',
            story_id=story_id,
            step_number=step_number,
            content=content,
            option1=option1,
            option2=option2,
            next1=next1,
            next2=next2,
            title=story_title
        )
    else:
        return "Story step not found", 404

if __name__ == '__main__':
    app.run(debug=True)