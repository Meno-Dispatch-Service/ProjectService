FROM python3.12

COPY requirementrs.txt requirements.txt

RUN pip install -r requirements.txt

COPY . . 

CMD ["run.sh"]

