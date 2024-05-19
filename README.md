# Snippets_19052024

## Инструкция по развертыванию проекта

1. Создать виртуальное окружение  
`python3 -m venv django_venv`

2. Активировать виртуальное окружение    
`source django_venv/bin/activate`

3. Установить пакеты в виртуальное окружение  
`pip install -r requirements.txt`

4. Применить миграции  
`python manange.py migrate`

5. Запустить проект  
`python manage.py runserver`


### Дополнение
Запустить `ipython` в контексте проекта  
`python manage.py shell_plus --ipython`