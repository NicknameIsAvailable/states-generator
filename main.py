import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

print("Сколько статей нужно сгенерировать?")
count = input()
print("Какая общая тематика? (Нажми Enter, если нет общей тематики)")
mainTopic = input()
content = f'Придумай {count} тем для статей на яндекс дзен'
if mainTopic:
    content += f'с общей тематикой "{mainTopic}"'
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": content
        }
    ]
)
topics = completion.choices[0].message.content.split('\n')
for i in range(len(topics)):
    topics[i] = topics[i].replace(str(i + 1) + '. ', '')
for i in range(len(topics)):
    content = f'Я хочу, чтобы вы выступили в качестве профессионального писателя. Вам нужно будет исследовать ' \
              f'заданную тему, сформулировать тезис и создать убедительное произведение, которое будет информативным' \
              f' и захватывающим. Мой первый запрос на помощь звучит так: "Мне нужна помощь в написании статьи' \
              f' по теме "{topics[i]}".'
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    image = openai.Image.create(
        prompt=topics[i],
        n=1,
        size="512x512"
    )
    image_url = image['data'][0]['url']
    response = completion.choices[0].message.content
    filename = f'{topics[i]}.txt'
    file = open(f'./States/{filename}', "w+")
    file.write(image_url + "\n" + response)
    file.close()
    print(f'Добавлен файл {topics[i]}.txt')
