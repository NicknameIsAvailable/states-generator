import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

count = input("Сколько статей нужно сгенерировать?  ")
mainTopic = input("Какая общая тематика? (Нажми Enter, если нет общей тематики) ")
folder_path = input('Введите путь к папке, в которую нужно загрузить статьи (E:\\Название папки\\): ') or 'E:\\Статьи\\'

content = f'Придумай {count} тем для статей'
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


def state_generation():
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

    if topics[i].endswith('.'):
        topics[i] = topics[i].rstrip('.')

    filename = f'{topics[i].replace(",", "").replace(":", "")}.txt'
    file_path = f'{folder_path}{filename}'

    file = open(file_path, "w+")
    file.write(image_url + "\n" + response)
    file.close()
    print(f'Добавлен файл {topics[i]}.txt')


for i in range(len(topics)):
    content = f'Я хочу, чтобы вы выступили в качестве профессионального писателя. Вам нужно будет исследовать ' \
              f'заданную тему, сформулировать тезис и создать убедительное произведение, которое будет информативным' \
              f' и захватывающим. Мой первый запрос на помощь звучит так: "Мне нужна помощь в написании статьи' \
              f' по теме "{topics[i]}".'

    try:
        state_generation()

    except:
        state_generation()
