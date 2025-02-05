FROM langchain/langgraph-api:3.11



ADD requirements.txt /deps/__outer_deployment/src/requirements.txt
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -r /deps/__outer_deployment/src/requirements.txt

ADD . /deps/__outer_deployment/src
RUN set -ex && \
    for line in '[project]' \
                'name = "deployment"' \
                'version = "0.1"' \
                '[tool.setuptools.package-data]' \
                '"*" = ["**/*"]'; do \
        echo "$line" >> /deps/__outer_deployment/pyproject.toml; \
    done

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

ENV LANGSERVE_GRAPHS='{"task_maistro": "/deps/__outer_deployment/src/task_maistro.py:graph"}'

WORKDIR /deps/__outer_deployment/src