FROM python:3.7


# Project files
ARG PROJECT_DIR=/srv/api
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY requirements.txt ./
COPY entrypoint.sh /entrypoint.sh

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /entrypoint.sh



EXPOSE 5000

CMD [ "/entrypoint.sh" ]