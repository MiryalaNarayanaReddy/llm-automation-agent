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

# docker image

```
sudo docker build -t myapp .
sudo docker run -p 8000:8000 -e AIPROXY_TOKEN="your-secret-token" myapp
```


# push image to dockerhub
```
sudo docker login
sudo docker tag myapp <username>/myapp:latest
sudo docker push <username>/myapp:latest
``` 