from flask import Flask, render_template, request, session, redirect, url_for, flash
import random
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# ========================= QUIZ DATA =========================
QUIZ_DATA = {
    'python': [
        {
            'question': 'What is the output of print(2 ** 3)?',
            'options': ['6', '8', '9', '23'],
            'correct': 1,
            'explanation': '2 ** 3 means 2 to the power of 3, which equals 8.'
        },
        {
            'question': 'Which of the following is used to define a function in Python?',
            'options': ['def', 'function', 'define', 'func'],
            'correct': 0,
            'explanation': 'The "def" keyword is used to define functions in Python.'
        },
        {
            'question': 'What data type is the object below? L = [1, 23, "hello", 1]',
            'options': ['Dictionary', 'Tuple', 'List', 'Array'],
            'correct': 2,
            'explanation': 'Square brackets [] define a list in Python.'
        },
        {
            'question': 'Which method is used to add an element to the end of a list?',
            'options': ['add()', 'append()', 'insert()', 'extend()'],
            'correct': 1,
            'explanation': 'The append() method adds a single element to the end of a list.'
        },
        {
            'question': 'What is the correct way to create a comment in Python?',
            'options': ['// This is a comment', '/* This is a comment */', '# This is a comment', '-- This is a comment'],
            'correct': 2,
            'explanation': 'Python uses # for single-line comments.'
        },
        {
            'question': 'Which of the following is the correct syntax for a for loop in Python?',
            'options': ['for i in range(10):', 'for i = 0; i < 10; i++:', 'for (i = 0; i < 10; i++):', 'foreach i in range(10):'],
            'correct': 0,
            'explanation': 'Python uses "for variable in iterable:" syntax for loops.'
        },
        {
            'question': 'What does the len() function do in Python?',
            'options': ['Returns the length of an object', 'Returns the type of an object', 'Returns the memory size', 'Returns the maximum value'],
            'correct': 0,
            'explanation': 'The len() function returns the number of items in an object.'
        },
        {
            'question': 'Which operator is used for floor division in Python?',
            'options': ['/', '//', '%', '**'],
            'correct': 1,
            'explanation': 'The // operator performs floor division, returning the largest integer less than or equal to the result.'
        },
        {
            'question': 'What is the output of print("Hello" + "World")?',
            'options': ['Hello World', 'HelloWorld', 'Hello+World', 'Error'],
            'correct': 1,
            'explanation': 'String concatenation with + joins strings without spaces.'
        },
        {
            'question': 'Which method converts a string to lowercase in Python?',
            'options': ['toLowerCase()', 'lower()', 'toLower()', 'downcase()'],
            'correct': 1,
            'explanation': 'The lower() method returns a lowercase version of the string.'
        },
        {
            'question': 'What is the correct way to create a dictionary in Python?',
            'options': ['dict = {key: value}', 'dict = [key: value]', 'dict = (key: value)', 'dict = <key: value>'],
            'correct': 0,
            'explanation': 'Dictionaries are created using curly braces {} with key:value pairs.'
        },
        {
            'question': 'Which of these is NOT a valid variable name in Python?',
            'options': ['_variable', 'variable2', '2variable', 'variable_name'],
            'correct': 2,
            'explanation': 'Variable names cannot start with a number in Python.'
        },
        {
            'question': 'What does the range(5) function generate?',
            'options': ['1, 2, 3, 4, 5', '0, 1, 2, 3, 4', '0, 1, 2, 3, 4, 5', '1, 2, 3, 4'],
            'correct': 1,
            'explanation': 'range(5) generates numbers from 0 to 4 (5 is excluded).'
        },
        {
            'question': 'Which statement is used to exit from a loop in Python?',
            'options': ['exit', 'break', 'stop', 'end'],
            'correct': 1,
            'explanation': 'The break statement is used to exit from a loop prematurely.'
        },
        {
            'question': 'What is the output of print(bool(0))?',
            'options': ['True', 'False', '0', 'Error'],
            'correct': 1,
            'explanation': 'In Python, 0 is considered False when converted to boolean.'
        },
        {
            'question': 'Which method is used to remove whitespace from both ends of a string?',
            'options': ['trim()', 'strip()', 'clean()', 'remove()'],
            'correct': 1,
            'explanation': 'The strip() method removes whitespace from the beginning and end of a string.'
        },
        {
            'question': 'What is the correct syntax for exception handling in Python?',
            'options': ['try-catch', 'try-except', 'catch-try', 'handle-error'],
            'correct': 1,
            'explanation': 'Python uses try-except blocks for exception handling.'
        },
        {
            'question': 'Which of the following creates a tuple in Python?',
            'options': ['(1, 2, 3)', '[1, 2, 3]', '{1, 2, 3}', '<1, 2, 3>'],
            'correct': 0,
            'explanation': 'Tuples are created using parentheses () in Python.'
        },
        {
            'question': 'What does the continue statement do in a loop?',
            'options': ['Exits the loop', 'Skips the current iteration', 'Restarts the loop', 'Pauses the loop'],
            'correct': 1,
            'explanation': 'The continue statement skips the rest of the current iteration and moves to the next one.'
        },
        {
            'question': 'Which function is used to get input from the user in Python 3?',
            'options': ['get()', 'input()', 'read()', 'scan()'],
            'correct': 1,
            'explanation': 'The input() function is used to get user input in Python 3.'
        }
    ],
    'general': [
        {
            'question': 'What is the capital of France?',
            'options': ['London', 'Berlin', 'Paris', 'Madrid'],
            'correct': 2,
            'explanation': 'Paris is the capital and largest city of France.'
        },
        {
            'question': 'Which planet is known as the Red Planet?',
            'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
            'correct': 1,
            'explanation': 'Mars is called the Red Planet due to its reddish appearance from iron oxide.'
        },
        {
            'question': 'What is the largest ocean on Earth?',
            'options': ['Atlantic', 'Indian', 'Arctic', 'Pacific'],
            'correct': 3,
            'explanation': 'The Pacific Ocean is the largest and deepest ocean on Earth.'
        },
        {
            'question': 'Who painted the Mona Lisa?',
            'options': ['Vincent van Gogh', 'Pablo Picasso', 'Leonardo da Vinci', 'Michelangelo'],
            'correct': 2,
            'explanation': 'Leonardo da Vinci painted the famous Mona Lisa during the Renaissance.'
        },
        {
            'question': 'What is the smallest country in the world?',
            'options': ['Monaco', 'Vatican City', 'San Marino', 'Liechtenstein'],
            'correct': 1,
            'explanation': 'Vatican City is the smallest sovereign state in the world by both area and population.'
        },
        {
            'question': 'Which element has the chemical symbol "O"?',
            'options': ['Gold', 'Oxygen', 'Silver', 'Iron'],
            'correct': 1,
            'explanation': 'Oxygen is represented by the chemical symbol "O" on the periodic table.'
        },
        {
            'question': 'How many continents are there?',
            'options': ['5', '6', '7', '8'],
            'correct': 2,
            'explanation': 'There are seven continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia.'
        },
        {
            'question': 'What is the longest river in the world?',
            'options': ['Amazon River', 'Nile River', 'Mississippi River', 'Yangtze River'],
            'correct': 1,
            'explanation': 'The Nile River in Africa is generally considered the longest river in the world at about 6,650 km.'
        },
        {
            'question': 'Which gas makes up about 78% of Earth\'s atmosphere?',
            'options': ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Hydrogen'],
            'correct': 2,
            'explanation': 'Nitrogen makes up approximately 78% of Earth\'s atmosphere by volume.'
        },
        {
            'question': 'In which year did World War II end?',
            'options': ['1944', '1945', '1946', '1947'],
            'correct': 1,
            'explanation': 'World War II ended in 1945 with the surrender of Japan in September.'
        }
    ]
}

# ========================= CHART GENERATOR =========================
def create_charts(correct_answers, wrong_answers, total_questions, category):
    """Create pie chart and bar chart for quiz results"""
    try:
        # Set up the matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor('white')
        
        # Pie Chart
        labels = ['Correct', 'Wrong']
        sizes = [correct_answers, wrong_answers]
        colors = ['#2E8B57', '#DC143C']  # SeaGreen and Crimson
        explode = (0.1, 0)  # explode the correct answers slice
        
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops={'fontsize': 12})
        ax1.set_title(f'{category.title()} Quiz Results - Distribution', fontsize=14, fontweight='bold')
        
        # Bar Chart
        categories = ['Correct\nAnswers', 'Wrong\nAnswers', 'Total\nQuestions']
        values = [correct_answers, wrong_answers, total_questions]
        bar_colors = ['#2E8B57', '#DC143C', '#4682B4']  # SeaGreen, Crimson, SteelBlue
        
        bars = ax2.bar(categories, values, color=bar_colors, alpha=0.8)
        ax2.set_title(f'{category.title()} Quiz Results - Summary', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Number of Questions', fontsize=12)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{value}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Set y-axis limit to accommodate labels
        ax2.set_ylim(0, max(values) * 1.2)
        
        # Tight layout
        plt.tight_layout()
        
        # Save plot to a BytesIO object
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        
        # Encode to base64 for embedding in HTML
        plot_data = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()  # Close the figure to free memory
        
        return plot_data
    
    except Exception as e:
        print(f"Error generating charts: {e}")
        # If seaborn style is not available, try without it
        try:
            plt.style.use('default')
            # Repeat the chart creation without seaborn style
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            fig.patch.set_facecolor('white')
            
            # Pie Chart
            labels = ['Correct', 'Wrong']
            sizes = [correct_answers, wrong_answers]
            colors = ['#2E8B57', '#DC143C']
            explode = (0.1, 0)
            
            ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                    shadow=True, startangle=90, textprops={'fontsize': 12})
            ax1.set_title(f'{category.title()} Quiz Results - Distribution', fontsize=14, fontweight='bold')
            
            # Bar Chart
            categories = ['Correct\nAnswers', 'Wrong\nAnswers', 'Total\nQuestions']
            values = [correct_answers, wrong_answers, total_questions]
            bar_colors = ['#2E8B57', '#DC143C', '#4682B4']
            
            bars = ax2.bar(categories, values, color=bar_colors, alpha=0.8)
            ax2.set_title(f'{category.title()} Quiz Results - Summary', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Number of Questions', fontsize=12)
            
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                        f'{value}', ha='center', va='bottom', fontsize=11, fontweight='bold')
            
            ax2.set_ylim(0, max(values) * 1.2)
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            
            plot_data = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
            return plot_data
        except Exception as e2:
            print(f"Error generating charts with default style: {e2}")
            return None

# ========================= FLASK ROUTES =========================
@app.route('/')
def home():
    print("Home route accessed!")  # This will show in terminal
    return render_template('home.html')

@app.route('/quiz/<category>')
def start_quiz(category):
    if category not in QUIZ_DATA:
        flash('Invalid quiz category!')
        return redirect(url_for('home'))
    
    # Initialize quiz session
    questions = QUIZ_DATA[category].copy()
    random.shuffle(questions)  # Randomize question order
    
    session['quiz_category'] = category
    session['questions'] = questions
    session['current_question'] = 0
    session['user_answers'] = []
    session['start_time'] = datetime.now().timestamp()
    
    return redirect(url_for('quiz_question'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_question():
    if 'questions' not in session:
        return redirect(url_for('home'))
    
    current_q = session['current_question']
    questions = session['questions']
    
    if current_q >= len(questions):
        return redirect(url_for('quiz_results'))
    
    if request.method == 'POST':
        # Process answer
        try:
            answer = int(request.form.get('answer'))
            session['user_answers'].append(answer)
            session['current_question'] += 1
            session.modified = True
            
            if session['current_question'] >= len(questions):
                return redirect(url_for('quiz_results'))
            else:
                return redirect(url_for('quiz_question'))
                
        except (ValueError, TypeError):
            flash('Please select an answer!')
    
    # Display current question
    question = questions[current_q]
    return render_template('quiz.html',
                         question=question,
                         current_question=current_q,
                         total_questions=len(questions),
                         category=session['quiz_category'])

@app.route('/results')
def quiz_results():
    if 'questions' not in session or 'user_answers' not in session:
        return redirect(url_for('home'))
    
    questions = session['questions']
    user_answers = session['user_answers']
    category = session['quiz_category']
    
    # Calculate results
    correct_answers = 0
    review_data = []
    
    for i, question in enumerate(questions):
        user_answer = user_answers[i] if i < len(user_answers) else None
        correct_answer = question['correct']
        
        if user_answer == correct_answer:
            correct_answers += 1
            
        review_data.append((question, user_answer, correct_answer))
    
    wrong_answers = len(questions) - correct_answers
    score = round((correct_answers / len(questions)) * 100, 1)
    
    # Generate charts
    chart_data = create_charts(correct_answers, wrong_answers, len(questions), category)
    
    # Store results in session for home page
    session['last_score'] = score
    session['last_correct'] = correct_answers
    session['last_total'] = len(questions)
    
    # Clear quiz data
    session.pop('questions', None)
    session.pop('user_answers', None)
    session.pop('current_question', None)
    session.pop('quiz_category', None)
    
    return render_template('results.html',
                         score=score,
                         correct_answers=correct_answers,
                         wrong_answers=wrong_answers,
                         total_questions=len(questions),
                         review_data=review_data,
                         category=category,
                         chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True, port=3000)