FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

RUN useradd -ms /bin/bash flaskuser

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y procps net-tools iputils-ping telnet

COPY . .

RUN chown -R flaskuser:flaskuser /app

USER flaskuser

ENV FLASK_APP=app.proxy
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
