## Linear Regression Using Gradient Descent
<p>This program demonstrates how the <b>Gradient Descent</b> algorithm works in linear regression.</p>

### Linear Regression
<p>Given a set of points, linear regression is finding the best-fit line for predicting similar points.</p> 

### Gradient Descent
<p>Gradient Descent algorithm recursively changes parameters of the line equation to obtain the minimum error.</p>
<p>Problem is summarized in the following formulas.</p>
<img width="568" alt="Screen Shot 2021-07-16 at 14 54 38" src="https://user-images.githubusercontent.com/76282148/125943599-39b9dd56-bf9c-4da2-b4b2-eee78be2b56c.png">
<p>The algorithm decreases thetas by alpha times partial derivatives of the error function with respect to individual thetas, where alpha is the learning rate.</p>
<img width="360" alt="Screen Shot 2021-07-16 at 14 58 10" src="https://user-images.githubusercontent.com/76282148/125943974-189e1419-f588-4d98-9790-7847cdcc9b8f.png">
<p>In this program, alpha is decaying rather than fixed.</p>
<img width="450" alt="Screen Shot 2021-07-16 at 15 09 31" src="https://user-images.githubusercontent.com/76282148/125945173-6191b6ea-f7c6-49de-a3cf-35b13cf502f7.png">
<p>Initially, gradient descent has a lot of errors and error function parabola roots are far away from thetas.</p>
<img width="320" alt="Screen Shot 2021-07-16 at 15 14 14" src="https://user-images.githubusercontent.com/76282148/125945718-4292a206-ece9-408d-9ab7-1f576a09be94.png">
<img width="640" alt="Screen Shot 2021-07-16 at 15 15 46" src="https://user-images.githubusercontent.com/76282148/125945882-f9ed2e95-0e57-4f6a-b340-3fe9658fb73b.png">
<p>As the algorithm proceeds, the error gets minimized and optimal thetas are found.</p>
<img width="320" alt="Screen Shot 2021-07-16 at 15 19 28" src="https://user-images.githubusercontent.com/76282148/125946298-248d383d-9d31-4cf2-b723-72ee137ed566.png">
<img width="640" alt="Screen Shot 2021-07-16 at 15 19 49" src="https://user-images.githubusercontent.com/76282148/125946334-3fd05fb5-e314-4f4c-97e2-e585a7cf5317.png">

### How to Use
<p>In <code>settings.py</code>, generate a 50-digit key for <code>SECRET_KEY</code> using key generators. If the host is not allowed, add the local host IP address to <code>ALLOWED_HOSTS</code> or set <code>DEBUG = True.</code></p>
<p>Open a terminal in the project root. Start the server with the following command:</p>
<code>python manage.py runserver</code>
<p>After making attribute changes in the model, run the following commands:</p>
<code>python manage.py makemigrations</code><br>
<code>python manage.py migrate</code><br>

<b>Slides are taken from Andrew Ng, Machine Learning by Stanford University, Coursera.</b>