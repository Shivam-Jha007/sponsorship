import gradio as gr
import sqlite3

# SQLite database setup (it will create the file if it doesn't exist)
def init_db():
    conn = sqlite3.connect('students.db')  # Creates a file students.db
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            score REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert student data into the database
def register_student(name, category, description, score):
    try:
        score = float(score)
    except ValueError:
        return "❌ Score must be a number."
    
    # Insert data into database
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, category, description, score)
        VALUES (?, ?, ?, ?)
    ''', (name, category, description, score))
    conn.commit()
    conn.close()
    return f"✅ {name} registered under {category}."

# Fetch eligible students from the database based on category
def find_students(category):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, category, description, score FROM students WHERE category = ?
    ''', (category,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize the database (run once when app starts)
init_db()

# Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# 🎓 Sponsorship Platform")

    with gr.Tab("🎓 Student Registration"):
        with gr.Row():
            name = gr.Textbox(label="Name")
            category = gr.Dropdown(choices=["Academics", "Sports", "Awards"], label="Category")
        description = gr.Textbox(label="Achievement Description")
        score = gr.Textbox(label="Score / Level / Rank")
        submit_btn = gr.Button("Submit")
        output = gr.Textbox(label="Status")
        submit_btn.click(register_student, [name, category, description, score], output)

    with gr.Tab("💼 Sponsor View"):
        sponsor_cat = gr.Dropdown(choices=["Academics", "Sports", "Awards"], label="Choose Category")
        show_btn = gr.Button("Show Eligible Students")
        results = gr.Dataframe(headers=["Name", "Category", "Description", "Score"], interactive=False)
        show_btn.click(find_students, inputs=sponsor_cat, outputs=results)

app.launch()
