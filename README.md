# llm-automation-agent

# setup

```bash
    pip install -r requirements.txt
    python datagen.py email="<email>" --root="<data-dir>"
```

# run
```bash
    python app.py
```
- use uv run app.py

# docker image
sudo docker image remove -f $(sudo docker images -a -q)

```
sudo docker build -t myapp .
sudo docker run -p 8000:8000 -e AIPROXY_TOKEN="your-secret-token" myapp
```

```
sudo docker exec -it <container-id> bash
```
# push image to dockerhub
```
sudo docker login
sudo docker tag myapp <username>/myapp:latest
sudo docker push <username>/myapp:latest
``` 

# final docker image commands
```
sudo docker build -t narayanareddy123/llmagent .

```
# testing


```bash
pip install pytest
pytest