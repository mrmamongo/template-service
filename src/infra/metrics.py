from fastapi import FastAPI

from src.config import ApiConfig


def setup_metrics(app: FastAPI, config: ApiConfig) -> None:
    """Установка метрик для приложения."""
    # Докуменатция по експортеру и дополнительным метрикам
    # "https://github.com/stephenhillier/starlette_exporter?tab=readme-ov-file#custom-metrics"
    # может быть полезно для просчитывания прокси или аккаунтов (парсер менеджер)

    from starlette_exporter import PrometheusMiddleware
    from starlette_exporter import handle_metrics
    from starlette_exporter.optional_metrics import request_body_size
    from starlette_exporter.optional_metrics import response_body_size

    app.add_middleware(
        PrometheusMiddleware,
        # https://github.com/stephenhillier/starlette_exporter?tab=readme-ov-file#options
        app_name=config.project_name,
        prefix='fast_api',
        skip_paths=['/health', '/openapi.json', '/docs', '/metrics'],
        skip_methods=['OPTIONS'],
        # Ведра гистограммы
        # buckets=[
        #     0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5,
        #     10.0
        # ],
        optional_metrics=[response_body_size, request_body_size],  # можно вырубить
    )
    app.add_route('/metrics', handle_metrics)
