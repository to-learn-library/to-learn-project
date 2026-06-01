from flask import Flask, render_template, request
import random

app = Flask(__name__, template_folder='templates')

# بنك الأسئلة الكامل (يتم اختيار 3 منها عشوائياً في كل مرة يدخل بها الطالب)
ALL_QUESTIONS = [
    {"id": 1, "question": "Choose the correct word: She ____ to school every day.", "options": ["go", "goes", "going"], "correct": "goes"},
    {"id": 2, "question": "If it rains tomorrow, we ____ the football match.", "options": ["will cancel", "canceled", "would cancel"], "correct": "will cancel"},
    {"id": 3, "question": "By the time the police arrived, the thief ____.", "options": ["escaped", "has escaped", "had escaped"], "correct": "had escaped"},
    {"id": 4, "question": "I haven't seen him ____ last year.", "options": ["for", "since", "ago"], "correct": "since"},
    {"id": 5, "question": "This is the hospital ____ I was born.", "options": ["where", "which", "who"], "correct": "where"},
    {"id": 6, "question": "He speaks English ____ than his brother.", "options": ["good", "better", "best"], "correct": "better"}
]

# قاعدة بيانات الـ 3 كتب لكل مستوى مع الروابط المباشرة للـ PDF
BOOKS_DATABASE = {
    "Beginner (A1)": [
        {
            "title": "The Little Prince 👑✨", 
            "author": "Antoine de Saint-Exupéry", 
            "desc": "رواية 'الأمير الصغير' العالمية - لغتها مبسطة وجملها قصيرة، وهي الخيار الأول عالمياً لكل من يبدأ بتعلم القراءة بالإنجليزية.",
            "pdf_url": "https://www.gutenberg.org/files/65238/65238-h/65238-h.htm"
        },
        {
            "title": "Alice's Adventures in Wonderland 🐰🎩", 
            "author": "Lewis Carroll", 
            "desc": "مغامرات أليس في بلاد العجائب - قصة ممتعة ومليئة بالخيال، كلماتها واضحة وتتكرر كثيراً لتسهيل حفظ المفردات الجديدة.",
            "pdf_url": "https://www.gutenberg.org/files/11/11-h/11-h.htm"
        },
        {
            "title": "Peter Pan ✨🧚", 
            "author": "J.M. Barrie", 
            "desc": "قصة بيتر بان الشهيرة - كلاسيكية ومكتوبة بأسلوب قصصي ممتع وسهل الاستيعاب للمبتدئين بدون تعقيد تراكيب الجمل.",
            "pdf_url": "https://www.gutenberg.org/files/16/16-h/16-h.htm"
        }
    ],
    "Intermediate (B1)": [
        {
            "title": "The Secret Garden 🌿🗝️", 
            "author": "Frances Hodgson Burnett", 
            "desc": "رواية 'الحديقة السرية' - قصة رائعة عن الأمل والصداقة، ممتازة جداً لتطوير لغة الحوار والمفردات العامة للمستوى المتوسط.",
            "pdf_url": "https://www.gutenberg.org/files/16f/16f-h/16f-h.htm"
        },
        {
            "title": "The Adventures of Tom Sawyer 🛶🏹", 
            "author": "Mark Twain", 
            "desc": "مغامرات توم سوير - أحداث كوميدية ومشوقة تجبر القارئ على الاستمرار بالقراءة، وتطور مهارة فهم القصص الطويلة.",
            "pdf_url": "https://www.gutenberg.org/files/74/74-h/74-h.htm"
        },
        {
            "title": "Sherlock Holmes Short Stories 🕵️‍♂️🔍", 
            "author": "Arthur Conan Doyle", 
            "desc": "قصص شرلوك هولمز القصيرة - لعشاق الغموض والذكاء والقضايا، تطور مصطلحات التحقيق والربط المنطقي للجمل.",
            "pdf_url": "https://www.gutenberg.org/files/1661/1661-h/1661-h.htm"
        }
    ],
    "Advanced (C1)": [
        {
            "title": "Think and Grow Rich ⚡🎯", 
            "author": "Napoleon Hill", 
            "desc": "كتاب 'فكر وازدد ثراءً' - من أشهر كتب تطوير الذات وبناء النجاح المالي عالمياً، لغته قوية وعميقة لرفع مستوى التعبير الأدبي والمتقدم.",
            "pdf_url": "https://archive.org/details/think-and-grow-rich-pdf"
        },
        {
            "title": "The Time Machine ⏳🛸", 
            "author": "H.G. Wells", 
            "desc": "رواية 'آلة الزمن' الكلاسيكية - خيال علمي فخم ومتقدم، يحتوي على مصطلحات علمية وتراكيب لغوية عميقة وممتازة للمستويات العالية.",
            "pdf_url": "https://www.gutenberg.org/files/35/35-h/35-h.htm"
        },
        {
            "title": "Great Expectations 🎩🏛️", 
            "author": "Charles Dickens", 
            "desc": "رواية 'آمال عظيمة' لتشارلز ديكنز - واحدة من روائع الأدب الإنجليزي، ممتازة جداً لمن يريد إتقان اللغة الإنجليزية الرسمية والفخمة.",
            "pdf_url": "https://www.gutenberg.org/files/1400/1400-h/1400-h.htm"
        }
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    # اختيار 3 أسئلة عشوائية بالكامل في كل مرة يدخل بها الطالب للاختبار
    selected_questions = random.sample(ALL_QUESTIONS, k=3)
    # خلط ترتيب الاختيارات عشوائياً لكل سؤال
    for q in selected_questions:
        random.shuffle(q['options'])
    return render_template('quiz.html', questions=selected_questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    # حساب الإجابات الصحيحة بناءً على الأسئلة التي أجاب عليها المستخدم
    for q in ALL_QUESTIONS:
        user_answer = request.form.get(f"question_{q['id']}")
        if user_answer and user_answer == q['correct']:
            score += 1
            
    # تحديد المستوى حسب عدد الإجابات الصحيحة من الـ 3 أسئلة العشوائية
    if score == 1:
        level = "Beginner (A1)"
    elif score == 2:
        level = "Intermediate (B1)"
    elif score == 3:
        level = "Advanced (C1)"
    else:
        level = "Beginner (A1)"
        
    # جلب الكتب الـ 3 المحددة للمستوى من قاعدة البيانات
    books = BOOKS_DATABASE.get(level, [])
    return render_template('results.html', level=level, books=books, score=score)

if __name__== '__main__':
    app.run(debug=True)