from flask import Flask, render_template, request, jsonify
from html import escape
from datetime import datetime
import random
import os

# template_folder="." — index.html лежит в корне репозитория,
# поэтому папка templates/ не нужна.
app = Flask(__name__, template_folder=".")

RESULT_FILE = os.environ.get("RESULT_FILE", "results.txt")
TOTAL_QUESTIONS = 10

# ============================================================
# 15 СҰРАҚ
# ============================================================

QUESTIONS = [
    {
        "question": "Шалкиіз Тіленшіұлы кім болған?",
        "answers": ["Хан", "Жырау, ақын, ойшыл әрі жауынгер", "Саудагер", "Дәрігер"],
        "correct": 1,
    },
    {
        "question": "Шалкиіз қай ғасырларда өмір сүрген?",
        "answers": ["X–XI ғасырларда", "XII–XIII ғасырларда", "XV–XVI ғасырларда", "XVIII–XIX ғасырларда"],
        "correct": 2,
    },
    {
        "question": "Шалкиіздің өмір сүрген жылдары шамамен қайсысы?",
        "answers": ["1200–1250", "1465–1560", "1600–1650", "1750–1800"],
        "correct": 1,
    },
    {
        "question": "Шалкиіздің жастық шағы қай ордамен тығыз байланысты болды?",
        "answers": ["Алтын Ордамен", "Қазақ хандығымен", "Ноғай Ордасымен", "Қырым хандығымен"],
        "correct": 2,
    },
    {
        "question": "Шалкиіз кімдердің айналасында жүрген?",
        "answers": ["Темір би мен Жүсіп бидің", "Абылай хан мен Кенесарының", "Абай мен Шоқанның", "Қасым хан мен Есім ханның"],
        "correct": 0,
    },
    {
        "question": "Шалкиіздің кейінгі өмірінде кімнің маңында болғаны туралы дерек бар?",
        "answers": ["Тәуке ханның", "Хақназар ханның", "Абылай ханның", "Керей ханның"],
        "correct": 1,
    },
    {
        "question": "Шалкиіз ерте жастан кімнің қолында тәрбиеленген?",
        "answers": ["Ханның", "Нағашы жұртының", "Жауынгерлердің", "Достарының"],
        "correct": 1,
    },
    {
        "question": "Шалкиіздің анасы кімнің қызы болған деген дерек бар?",
        "answers": ["Темір бидің", "Жүсіп бидің", "Мұса бидің", "Хақназар ханның"],
        "correct": 2,
    },
    {
        "question": "Шалкиіз өміріндегі маңызды тұлғалардың бірі кім?",
        "answers": ["Би Темір", "Абай", "Қорқыт", "Шоқан"],
        "correct": 0,
    },
    {
        "question": "Шалкиіз Би Темірдің маңында қандай рөл атқарған?",
        "answers": ["Саудагер болған", "Кеңесшісі әрі жақын серігі болған", "Әскері болған", "Елші болған"],
        "correct": 1,
    },
    {
        "question": "Шалкиіз Темір биге өз ойын қалай жеткізе алған?",
        "answers": ["Ашық жеткізген", "Мүлде айтпаған", "Тек хат арқылы жеткізген", "Басқа адамдар арқылы айтқан"],
        "correct": 0,
    },
    {
        "question": "«Ер Шобан» қандай тақырыптағы шығарма?",
        "answers": ["Махаббат тақырыбындағы", "Ерлік тақырыбындағы", "Табиғат туралы", "Сауда туралы"],
        "correct": 1,
    },
    {
        "question": "«Ер Шобан» жырында кімнің ерлігі суреттеледі?",
        "answers": ["Би Темірдің", "Хақназар ханның", "Ер Шобанның", "Мұса бидің"],
        "correct": 2,
    },
    {
        "question": "«Ер Шобан» жырындағы батыр қандай адам ретінде бейнеленеді?",
        "answers": [
            "Қиындыққа мойымайтын, ел намысын қорғайтын",
            "Қорқақ әрі әлсіз",
            "Саудамен айналысатын",
            "Биліктен қашатын",
        ],
        "correct": 0,
    },
    {
        "question": "Шалкиіз поэзиясында қандай тақырыптар маңызды орын алады?",
        "answers": ["Ерлік пен патриотизм", "Тек сауда", "Тек табиғат", "Тек ғылым"],
        "correct": 0,
    },
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
    selected_ids = random.sample(range(len(QUESTIONS)), TOTAL_QUESTIONS)

    result = []
    for question_id in selected_ids:
        q = QUESTIONS[question_id]

        answers = [
            {"id": answer_id, "text": answer_text}
            for answer_id, answer_text in enumerate(q["answers"])
        ]
        random.shuffle(answers)

        result.append({
            "id": question_id,
            "question": q["question"],
            "answers": answers,
        })

    return jsonify(result)

# ============================================================
# НӘТИЖЕНІ ҚАБЫЛДАУ
# ============================================================

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()[:100]
    student_class = str(data.get("studentClass", "")).strip()[:20]
    answers = data.get("answers", [])

    if not name:
        return jsonify({"success": False, "message": "Аты-жөнің енгізілмеген."}), 400

    if not student_class:
        return jsonify({"success": False, "message": "Сынып таңдалмаған."}), 400

    if not isinstance(answers, list):
        answers = []

    # Жауаптарды тексеру. Әр сұраққа тек бір рет есептеледі,
    # сонда ұпайды жасанды түрде көбейту мүмкін емес.
    correct_count = 0
    seen_questions = set()

    for user_answer in answers:
        try:
            question_id = int(user_answer["questionId"])
            answer_id = int(user_answer["answerId"])
        except (KeyError, ValueError, TypeError):
            continue

        if not (0 <= question_id < len(QUESTIONS)):
            continue

        if question_id in seen_questions:
            continue
        seen_questions.add(question_id)

        if answer_id == QUESTIONS[question_id]["correct"]:
            correct_count += 1

    correct_count = min(correct_count, TOTAL_QUESTIONS)
    score = correct_count * 10

    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    # "|" таңбасы мен жаңа жолды алып тастаймыз, әйтпесе файл форматы бұзылады
    safe_name = name.replace("|", "/").replace("\n", " ").replace("\r", " ")
    safe_class = student_class.replace("|", "/").replace("\n", " ").replace("\r", " ")

    result_line = (
        f"{safe_name} | "
        f"{safe_class} | "
        f"{correct_count}/{TOTAL_QUESTIONS} | "
        f"{score}/100 | "
        f"{current_time}\n"
    )

    with open(RESULT_FILE, "a", encoding="utf-8") as file:
        file.write(result_line)

    return jsonify({
        "success": True,
        "name": name,
        "studentClass": student_class,
        "correct": correct_count,
        "total": TOTAL_QUESTIONS,
        "score": score,
    })

# ============================================================
# НӘТИЖЕЛЕРДІ КӨРУ
# ============================================================

RESULTS_HEAD = """
<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Нәтижелер</title>
<style>
body { font-family: Arial; background: #111; color: white; padding: 30px; }
h1 { color: #f5c542; }
table { border-collapse: collapse; width: 100%; max-width: 1000px; }
th, td { border: 1px solid #555; padding: 12px; text-align: center; }
th { background: #f5c542; color: black; }
tr:nth-child(even) { background: #222; }
</style>
</head>
<body>
<h1>📊 Шалкиіз жырау — нәтижелер</h1>
<table>
<tr>
<th>№</th><th>Оқушы</th><th>Сынып</th><th>Дұрыс</th><th>Ұпай</th><th>Уақыт</th>
</tr>
"""

@app.route("/results")
def results():
    if not os.path.exists(RESULT_FILE):
        return "<h2>Әзірге нәтиже жоқ.</h2>"

    with open(RESULT_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    rows = []
    for number, line in enumerate(lines, 1):
        parts = line.strip().split(" | ")
        if len(parts) != 5:
            continue

        # escape() — оқушы аты арқылы HTML/JS кодын енгізуден қорғайды
        name, student_class, correct, score, time = (escape(p) for p in parts)

        rows.append(
            f"<tr><td>{number}</td><td>{name}</td><td>{student_class}</td>"
            f"<td>{correct}</td><td><b>{score}</b></td><td>{time}</td></tr>"
        )

    return RESULTS_HEAD + "\n".join(rows) + "\n</table>\n</body>\n</html>"

# ============================================================
# ЖЕРГІЛІКТІ ІСКЕ ҚОСУ (Render-де gunicorn қолданылады)
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Сервер: http://127.0.0.1:{port}")
    print(f"Нәтижелер: http://127.0.0.1:{port}/results")
    app.run(host="0.0.0.0", port=port, debug=False)
