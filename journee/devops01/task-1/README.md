## Task-1 Secret Enpoint
*Task-1 contains*
- app directory where the main API logic code is.
- logs directory where the log information is store
- Dockerfile file
- requirements.txt file
- secret.txt
| Note: The secret.txt file is for passing the values at built time
| It is also added to .gitignore to avoid exposing it to git repository
- result.csv file: the test result from testing main.py

| Dynamodb host unknown at the time of testing the built image. However, as it is expected result.csv should be created on the current working directory, i.e /journee.
| With the efs of task-2, the result.csv should be in /export/result.csv

### See the Dockerfile & .gitignore for secuirty practices on not exposing secrets

### The build command
`DOCKER_BUILDKIT=1 docker build -t minterview --no-cache --progress=plain --secret id=mysecret,src=secret.txt .`

Alternatively, 
`export DOCKER_BUILDKIT=1`

`docker build -t minterview --no-cache --progress=plain --secret id=mysecret,src=secret.txt .`

### Check the Built History
| The final built image does not contain secret

### Output 

:~/Documents/GitHub/journee/devops01/task-1|⇒  docker history minterview
IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
399ada9819b8   17 minutes ago   CMD ["uvicorn" "main:app" "--host" "127.0.0.…   0B        buildkit.dockerfile.v0
<missing>      17 minutes ago   HEALTHCHECK &{["CMD-SHELL" "wget --no-verbos…   0B        buildkit.dockerfile.v0
<missing>      17 minutes ago   RUN /bin/sh -c cat /run/secrets/mysecret # b…   0B        buildkit.dockerfile.v0
<missing>      17 minutes ago   COPY ./app /journee/app # buildkit              4.44kB    buildkit.dockerfile.v0
<missing>      17 minutes ago   RUN /bin/sh -c pip install --no-cache-dir --…   83.9MB    buildkit.dockerfile.v0
<missing>      18 minutes ago   COPY ./requirements.txt /journee/requirement…   106B      buildkit.dockerfile.v0
<missing>      2 hours ago      WORKDIR /journee                                0B        buildkit.dockerfile.v0
<missing>      15 months ago    /bin/sh -c #(nop)  CMD ["python3"]              0B        
<missing>      15 months ago    /bin/sh -c set -ex;   wget -O get-pip.py "$P…   8.31MB    
<missing>      15 months ago    /bin/sh -c #(nop)  ENV PYTHON_GET_PIP_SHA256…   0B        
<missing>      15 months ago    /bin/sh -c #(nop)  ENV PYTHON_GET_PIP_URL=ht…   0B        
<missing>      15 months ago    /bin/sh -c #(nop)  ENV PYTHON_PIP_VERSION=21…   0B        
<missing>      15 months ago    /bin/sh -c cd /usr/local/bin  && ln -s idle3…   32B       
<missing>      15 months ago    /bin/sh -c set -ex   && wget -O python.tar.x…   53.8MB    
<missing>      15 months ago    /bin/sh -c #(nop)  ENV PYTHON_VERSION=3.9.5     0B        
<missing>      15 months ago    /bin/sh -c #(nop)  ENV GPG_KEY=E3FF2839C048B…   0B        
<missing>      15 months ago    /bin/sh -c apt-get update && apt-get install…   18.1MB    
<missing>      15 months ago    /bin/sh -c #(nop)  ENV LANG=C.UTF-8             0B        
<missing>      15 months ago    /bin/sh -c #(nop)  ENV PATH=/usr/local/bin:/…   0B        
<missing>      15 months ago    /bin/sh -c set -ex;  apt-get update;  apt-ge…   466MB     
<missing>      15 months ago    /bin/sh -c apt-get update && apt-get install…   144MB     
<missing>      15 months ago    /bin/sh -c set -ex;  if ! command -v gpg > /…   17.3MB    
<missing>      15 months ago    /bin/sh -c set -eux;  apt-get update;  apt-g…   15.9MB    
<missing>      15 months ago    /bin/sh -c #(nop)  CMD ["bash"]                 0B        
<missing>      15 months ago    /bin/sh -c #(nop) ADD file:bc9eebfc439e3fbf9…   108MB