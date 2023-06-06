FROM python:3.11-slim

RUN mkdir /organic-accretion
WORKDIR "/organic-accretion"

ADD requirements.txt /organic-accretion/
ADD src/__main__.py /organic-accretion/

CMD ["python", "__main__.py"]