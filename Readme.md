Поднять проект:
    1)docker-compose up --build
    
    2)Если будет ошибка про 5432ой порт сдлеать docker-compose restart web
    
    3)Это из за того что Проект поднялся быстрее бд (ну я так думаю)

Автоматичесикй создаются модели провайдеров, они прописаны в миграций "0006_alter_provider_branch_code.py"

GET http://0.0.0.0:9000/api/airflow/search/ для получения search_id пойска

GET http://0.0.0.0:9000/api/airflow/results/<search_id>/<currency>/ для получения результатов от провайдеров
