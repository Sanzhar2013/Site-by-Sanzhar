from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime
import os

app = Flask(__name__)

RESULT_FILE = "results.txt"

# ============================================================
# 15 СҰРАҚ
# ============================================================

QUESTIONS = [

    {
        "question": "Шалкиіз Тіленшіұлы кім болған?",
        "answers": [
            "Хан",
            "Жырау, ақын, ойшыл әрі жауынгер",
            "Саудагер",
            "Дәрігер"
        ],
        "correct": 1
    },

    {
        "question": "Шалкиіз қай ғасырларда өмір сүрген?",
        "answers": [
            "X–XI ғасырларда",
            "XII–XIII ғасырларда",
            "XV–XVI ғасырларда",
            "XVIII–XIX ғасырларда"
        ],
        "correct": 2
    },

    {
        "question": "Шалкиіздің өмір сүрген жылдары шамамен қайсысы?",
        "answers": [
            "1200–1250",
            "1465–1560",
            "1600–1650",
            "1750–1800"
        ],
        "correct": 1
    },

    {
        "question": "Шалкиіздің жастық шағы қай ордамен тығыз байланысты болды?",
        "answers": [
            "Алтын Ордамен",
            "Қазақ хандығымен",
            "Ноғай Ордасымен",
            "Қырым хандығымен"
        ],
        "correct": 2
    },

    {
        "question": "Шалкиіз кімдердің айналасында жүрген?",
        "answers": [
            "Темір би мен Жүсіп бидің",
            "Абылай хан мен Кенесарының",
            "Абай мен Шоқанның",
            "Қасым хан мен Есім ханның"
        ],
        "correct": 0
    },

    {
        "question": "Шалкиіздің кейінгі өмірінде кімнің маңында болғаны туралы дерек бар?",
        "answers": [
            "Тәуке ханның",
            "Хақназар ханның",
            "Абылай ханның",
            "Керей ханның"
        ],
        "correct": 1
    },

    {
        "question": "Шалкиіз ерте жастан кімнің қолында тәрбиеленген?",
        "answers": [
            "Ханның",
            "Нағашы жұртының",
            "Жауынгерлердің",
            "Достарының"
        ],
        "correct": 1
    },

    {
        "question": "Шалкиіздің анасы кімнің қызы болған деген дерек бар?",
        "answers": [
            "Темір бидің",
            "Жүсіп бидің",
            "Мұса бидің",
            "Хақназар ханның"
        ],
        "correct": 2
    },

    {
        "question": "Шалкиіз өміріндегі маңызды тұлғалардың бірі кім?",
        "answers": [
            "Би Темір",
            "Абай",
            "Қорқыт",
            "Шоқан"
        ],
        "correct": 0
    },

    {
        "question": "Шалкиіз Би Темірдің маңында қандай рөл атқарған?",
        "answers": [
            "Саудагер болған",
            "Кеңесшісі әрі жақын серігі болған",
            "Әскері болған",
            "Елші болған"
        ],
        "correct": 1
    },

    {
        "question": "Шалкиіз Темір биге өз ойын қалай жеткізе алған?",
        "answers": [
            "Ашық жеткізген",
            "Мүлде айтпаған",
            "Тек хат арқылы жеткізген",
            "Басқа адамдар арқылы айтқан"
        ],
        "correct": 0
    },

    {
        "question": "«Ер Шобан» қандай тақырыптағы шығарма?",
        "answers": [
            "Махаббат тақырыбындағы",
            "Ерлік тақырыбындағы",
            "Табиғат туралы",
            "Сауда туралы"
        ],
        "correct": 1
    },

    {
        "question": "«Ер Шобан» жырында кімнің ерлігі суреттеледі?",
        "answers": [
            "Би Темірдің",
            "Хақназар ханның",
            "Ер Шобанның",
            "Мұса бидің"
        ],
        "correct": 2
    },

    {
        "question": "«Ер Шобан» жырындағы батыр қандай адам ретінде бейнеленеді?",
        "answers": [
            "Қиындыққа мойымайтын, ел намысын қорғайтын",
            "Қорқақ әрі әлсіз",
            "Саудамен айналысатын",
            "Биліктен қашатын"
        ],
        "correct": 0
    },

    {
        "question": "Шалкиіз поэзиясында қандай тақырыптар маңызды орын алады?",
        "answers": [
            "Ерлік пен патриотизм",
            "Тек сауда",
            "Тек табиғат",
            "Тек ғылым"
        ],
        "correct": 0
    }
]


# ============================================================
# БАСҚЫ БЕТ
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# ОҚУШЫҒА 10 КЕЗДЕЙСОҚ СҰРАҚ БЕРУ
# ============================================================

@app.route("/questions")
def get_questions():

    # 15 сұрақтың ішінен 10 сұрақ таңдаймыз
    selected_ids = random.sample(
        range(len(QUESTIONS)),
        10
    )

    result = []

    for question_id in selected_ids:

        q = QUESTIONS[question_id]

        # Әр жауапқа өзінің ID-сін береміз
        answers = []

        for answer_id, answer_text in enumerate(q["answers"]):

            answers.append({
                "id": answer_id,
                "text": answer_text
            })

        # Жауаптардың орнын араластыру
        random.shuffle(answers)

        result.append({
            "id": question_id,
            "question": q["question"],
            "answers": answers
        })

    return jsonify(result)


# ============================================================
# НӘТИЖЕНІ ҚАБЫЛДАУ
# ============================================================

@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json()

    name = str(data.get("name", "")).strip()
    student_class = str(
        data.get("studentClass", "")
    ).strip()

    answers = data.get("answers", [])

    # Аты тексеріледі
    if not name:

        return jsonify({
            "success": False,
            "message": "Аты-жөнің енгізілмеген."
        }), 400

    # Сынып тексеріледі
    if not student_class:

        return jsonify({
            "success": False,
            "message": "Сынып таңдалмаған."
        }), 400

    # ========================================================
    # ЖАУАПТАРДЫ ТЕКСЕРУ
    # ========================================================

    correct_count = 0

    for user_answer in answers:

        try:

            question_id = int(
                user_answer["questionId"]
            )

            answer_id = int(
                user_answer["answerId"]
            )

        except (KeyError, ValueError, TypeError):

            continue

        # Question ID дұрыс па?
        if not (
            0 <= question_id < len(QUESTIONS)
        ):
            continue

        correct_answer_id = QUESTIONS[
            question_id
        ]["correct"]

        # Дұрыс жауап па?
        if answer_id == correct_answer_id:

            correct_count += 1

    total_questions = 10

    score = correct_count * 10

    # ========================================================
    # УАҚЫТ
    # ========================================================

    current_time = datetime.now().strftime(
        "%d.%m.%Y %H:%M:%S"
    )

    # ========================================================
    # TXT ФАЙЛҒА САҚТАУ
    # ========================================================

    result_line = (
        f"{name} | "
        f"{student_class} | "
        f"{correct_count}/{total_questions} | "
        f"{score}/100 | "
        f"{current_time}\n"
    )

    with open(
        RESULT_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(result_line)

    # ========================================================
    # БРАУЗЕРГЕ НӘТИЖЕ ЖІБЕРУ
    # ========================================================

    return jsonify({

        "success": True,

        "name": name,

        "studentClass": student_class,

        "correct": correct_count,

        "total": total_questions,

        "score": score

    })


# ============================================================
# НӘТИЖЕЛЕРДІ КӨРУ
# ============================================================

@app.route("/results")
def results():

    if not os.path.exists(RESULT_FILE):

        return "<h2>Әзірге нәтиже жоқ.</h2>"

    with open(
        RESULT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    html = """
    <!DOCTYPE html>

    <html lang="kk">

    <head>

    <meta charset="UTF-8">

    <title>Нәтижелер</title>

    <style>

    body {
        font-family: Arial;
        background: #111;
        color: white;
        padding: 30px;
    }

    h1 {
        color: #f5c542;
    }

    table {
        border-collapse: collapse;
        width: 100%;
        max-width: 1000px;
    }

    th, td {
        border: 1px solid #555;
        padding: 12px;
        text-align: center;
    }

    th {
        background: #f5c542;
        color: black;
    }

    tr:nth-child(even) {
        background: #222;
    }

    </style>

    </head>

    <body>

    <h1>📊 Шалкиіз жырау — нәтижелер</h1>

    <table>

    <tr>
        <th>№</th>
        <th>Оқушы</th>
        <th>Сынып</th>
        <th>Дұрыс</th>
        <th>Ұпай</th>
        <th>Уақыт</th>
    </tr>
    """

    for number, line in enumerate(lines, 1):

        parts = line.strip().split(" | ")

        if len(parts) == 5:

            name = parts[0]
            student_class = parts[1]
            correct = parts[2]
            score = parts[3]
            time = parts[4]

            html += f"""
            <tr>

            <td>{number}</td>

            <td>{name}</td>

            <td>{student_class}</td>

            <td>{correct}</td>

            <td><b>{score}</b></td>

            <td>{time}</td>

            </tr>
            """

    html += """
    </table>

    </body>

    </html>
    """

    return html


# ============================================================
# СЕРВЕРДІ ІСКЕ ҚОСУ
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 50)
    print("       ШАЛКИІЗ ЖЫРАУ QUIZ")
    print("=" * 50)
    print()
    print("Компьютерде:")
    print("http://127.0.0.1:5000")
    print()
    print("Нәтижелер:")
    print("http://127.0.0.1:5000/results")
    print()
    print("Сервер іске қосылды!")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )