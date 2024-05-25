FROM python:3.11.7-alpine AS build

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk update && apk add --no-cache tzdata && \
    pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple && \
    pip install --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN pip install --timeout 30 --user --no-cache-dir --no-warn-script-location -r requirements.txt

FROM python:3.11.7-alpine

ENV LOCAL_PKG="/root/.local"
COPY --from=build ${LOCAL_PKG} ${LOCAL_PKG}
COPY --from=build /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN ln -sf ${LOCAL_PKG}/bin/* /usr/local/bin/ && echo "Asia/Shanghai" > /etc/timezone

WORKDIR /app

COPY . /app

EXPOSE 8000

CMD ["python", "app.py"]
