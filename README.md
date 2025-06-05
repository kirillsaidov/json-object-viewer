# json-object-viewer
View JSON objects as blocks on canvas. 

<img src="imgs/img.svg" width="720">

## Install
```sh
$ git clone --recurse-submodules git@github.com:kirillsaidov/json-object-viewer.git
```

### Run
Run directly in developer mode:
```sh
# install python dependencies
python3 -m venv venv && source ./venv/bin/activate
pip install -r requirements.txt

# run app
uvicorn src.main:app --reload --port 8505
```

Run using Docker:
```sh
# build container
docker buildx build -f Dockerfile -t json-object-viewer:latest .

# run app
docker run -d --network=host --name=json-object-viewer \
    json-object-viewer:latest -b 0.0.0.0:8505 -w 1
```

## LICENSE
Unlicense.
