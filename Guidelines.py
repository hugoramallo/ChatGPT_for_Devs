import os
import openai
openai.api_key  = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

##########################################################
#PRINCIPIO 1 - ESCRIBIR INSTRUCCIONES CLARAS Y ESPECÍFICAS
##########################################################

#TACTICA 1: USAR DELIMITADORES QUE INDIQUEN DIFERENTES PARTES DEL TEXTO DE ENTRADA
#Tripe Quotes: """, Triple backticks ```, Triple dashes ---, Angle brackets <>, XML tagas: <tag> </tag>

#Texto para resumir
text = f"""
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
"""
#Petición
prompt = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
"""
#respuesta, llamamos al método get_completion()
response = get_completion(prompt)
#sacamos el resultado
#print(response)



#TACTICA 2: REQUIERE UNA ESTRUCTURA DE SALIDA, HTML, JSON
prompt = f"""
Generate a list of three made-up book titles along \ 
with their authors and genres. 
Provide them in JSON format with the following keys: 
book_id, title, author, genre.
"""
response = get_completion(prompt)
#print(response)



#TACTICA 3: PREGUNTA AL MODELO SI SE CUMPLES LAS CONDICIONES
#Texto con instrucciones a organizar y texto sin instrucciones

text_1 = f"""
Making a cup of tea is easy! First, you need to get some \ 
water boiling. While that's happening, \ 
grab a cup and put a tea bag in it. Once the water is \ 
hot enough, just pour it over the tea bag. \ 
Let it sit for a bit so the tea can steep. After a \ 
few minutes, take out the tea bag. If you \ 
like, you can add some sugar or milk to taste. \ 
And that's it! You've got yourself a delicious \ 
cup of tea to enjoy.
"""
#aquí el prompt le dirá que detecte si hay instrucciones a seguir y si las hay las organizará
prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_1}\"\"\"
"""
response = get_completion(prompt)
print("Completion for Text 1:")
#print(response)

#prompt sin instrucciones
text_2 = f"""
The sun is shining brightly today, and the birds are \
singing. It's a beautiful day to go for a \ 
walk in the park. The flowers are blooming, and the \ 
trees are swaying gently in the breeze. People \ 
are out and about, enjoying the lovely weather. \ 
Some are having picnics, while others are playing \ 
games or simply relaxing on the grass. It's a \ 
perfect day to spend time outdoors and appreciate the \ 
beauty of nature.
"""
#este prompt le pide que detecte si hay instrucciones y si no las hay lo indicará (no las hay)
prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_2}\"\"\"
"""
response = get_completion(prompt)
#print("Completion for Text 2:")
#print(response)



#TACTICA 4: FEW SHOT PROMPTING (DANDO EJEMPLOS DE LA SALIDA QUE ESPERAMOS)
#Dar un ejemplo a la IA ayuda a entender el resultado que buscamos en la salida
prompt = f"""
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest \ 
valley flows from a modest spring; the \ 
grandest symphony originates from a single note; \ 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
"""
response = get_completion(prompt)
#print(response)



#############################################
#PRINCIPIO 2: DAR AL MODELO TIEMPO PARA PENSAR
#############################################

#TÁCTICA 1: ESPECIFICAR LOS PASOS PARA COMPLETAR UNA TAREA
#Step 1, Step 2, Step 3...

#texto sobre e lque vamos a trabajar
text = f"""
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
"""
# Ejemplos de lo que queremos que haga
prompt_1 = f"""
Perform the following actions: 
1 - Summarize the following text delimited by triple \
backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following \
keys: french_summary, num_names.

Separate your answers with line breaks.

Text:
```{text}```
"""
response = get_completion(prompt_1)
#print("Completion for prompt 1:")
#print(response)

#PIDE UNA SALIDA EN UN FORMATO ESPECÍFICO

prompt_2 = f"""
Your task is to perform the following actions: 
1 - Summarize the following text delimited by 
  <> with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the 
  following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Italian summary>
Output JSON: <json with summary and num_names>

Text: <{text}>
"""
response = get_completion(prompt_2)
#print("\nCompletion for prompt 2:")
#print(response)

#TACTICA 2: PIDE MODELO QUE COMPRUEBE SI SU SOLUCIÓN COINCIDE LA INDICADA
#En el primer caso la solución no es correcta
#Al solo preguntarle si es correcta o no sin darle mas detalles puede fallar
prompt = f"""
Determine if the student's solution is correct or not.

Question:
I'm building a solar power installation and I need \
 help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \ 
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations 
as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
"""
response = get_completion(prompt)
#El modelo determina que es correcta pero no lo es
#print(response)

#En el segundo caso le pedimos que creé su solución y la compare con el del alumno
#Resultado, el modelo determina que la solución del alumno no es correcta
prompt = f"""
Your task is to determine if the student's solution \
is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem. 
- Then compare your solution to the student's solution \ 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
```
question here
```
Student's solution:
```
student's solution here
```
Actual solution:
```
steps to work out the solution and your solution here
```
Is the student's solution the same as actual solution \
just calculated:
```
yes or no
```
Student grade:
```
correct or incorrect
```

Question:
```
I'm building a solar power installation and I need help \
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations \
as a function of the number of square feet.
``` 
Student's solution:
```
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
```
Actual solution:
"""
response = get_completion(prompt)
#print(response)


#LIMITACIONES DEL MODELO(MODEL LIMITATIONS)
# HALLUCINATION (ALUCINACIONES)
#* Hacer afirmaciones que parecen admisibles pero no son ciertas
prompt = f"""
Tell me about AeroGlide UltraSlim Smart Toothbrush by Boie
"""
response = get_completion(prompt)
#print(response)

#GUÍA DEL PROMPT
#Ser claro y específico
#Analizar el porqué el resultado no da la salida deseada
#Refinar la idea y el prompt

