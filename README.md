<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>LifeLine</h1>

<p><strong>LifeLine</strong> is a web application that predicts the likelihood of a message being suicidal. The application uses a machine learning model to analyze the content of the message and provides a probability score indicating how likely the message is to contain suicidal thoughts.</p>

<h2>Features</h2>
<ul>
    <li><strong>Message Analysis</strong>: Users can input a message, and the application will predict the likelihood of the message being suicidal.</li>
    <li><strong>Simple Interface</strong>: A user-friendly interface to input messages and view predictions.</li>
    <li><strong>Machine Learning Model</strong>: Uses a trained machine learning model to analyze the text.</li>
</ul>

<h2>Technologies Used</h2>
<ul>
    <li><strong>Backend</strong>: Flask, Python</li>
    <li><strong>Frontend</strong>: HTML, CSS, Bootstrap</li>
    <li><strong>Machine Learning</strong>: Scikit-learn, TensorFlow (or other relevant libraries)</li>
    <li><strong>Database</strong>: SQLite (or any other database)</li>
</ul>

<h2>Installation</h2>
<ol>
    <li>Clone the repository:
        <pre><code>git clone https://github.com/Amar-Nath9/LifeLine.git
cd LifeLine
        </code></pre>
    </li>
    <li>Create a virtual environment and activate it:
        <pre><code>python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
        </code></pre>
    </li>
    <li>Install the dependencies:
        <pre><code>pip install -r requirements.txt
        </code></pre>
    </li>
    <li>Run the Flask application:
        <pre><code>python app.py
        </code></pre>
    </li>
    <li>Access the application: Open your web browser and go to <code>http://127.0.0.1:5000/</code>.</li>
</ol>

<h2>Usage</h2>
<ol>
    <li>Navigate to the homepage.</li>
    <li>Input a message in the provided text box.</li>
    <li>Submit the form to receive a prediction score.</li>
    <li>The application will display the probability that the message is suicidal.</li>
</ol>

<h3>Example</h3>
<pre><code>Message: "I can't take this anymore. I feel like giving up."
Prediction: 85% likelihood of being suicidal.
</code></pre>



</body>
</html>
