# docker-compose-swarm-overlay
Utilizando o Docker Compose em várias engines do Docker através da rede overlay do Swarm.

As pastas swarm-manager, swarm-worker1 e swarm-worker2 representam a pasta cluster-hadoop de cada máquina virtual fixa.

# Passo a passo para fazer o segundo desafio do lab 8

* Este tutorial utiliza 3 máquinas virtuais chamadas swarm-manager, swarm-worker1 e swarm-worker2. As 3 máquinas devem conseguir se comunicar entre si.

* Adicionar spark-worker-3 e spark-worker-4 ao arquivo workers da máquina que irá executar o spark-master

* Criar um cluster do docker swarm através dos comandos:

    - Criar swarm (na máquina master):

            docker swarm init --advertise-addr <MANAGER-IP>

    - Ingressar no swarm com os workers (executar comando dentro de cada worker - o comando exato é mostrado pelo manager ao criar o swarm):

            docker swarm join --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c 192.168.99.100:2377

* Criar a rede overlay que permite a comunicação entre os containers em diferentes hosts do docker:

        docker network create -d overlay --attachable --subnet=10.0.1.0/24 cluster-net30

* Neste momento, a rede overlay só existe na máquina master. Rode um container qualquer dentro de cada worker
para que o swarm envie a rede overlay criada para os workers:

        docker run -dit --name alpine3 --network cluster-net alpine

* Prepare o arquivo docker-compose.yml de cada máquina. Cada container deve possuir um IP estático dentro da faixa de rede
definida pela rede overlay que foi criada (verificar faixa com o comando "docker network inspect <rede>").
A máquina master irá executar apenas o container spark-master. spark-worker-1 e spark-worker-2 serão executados na segunda
máquina, enquanto spark-worker-3 e spark-worker-4 serão executados na terceira.

* Configuração de rede dentro do container:

        networks:
          cluster-net:
            ipv4_address: 10.0.1.2
        environment:
          - "SPARK_LOCAL_IP=10.0.1.2"

* Configuração de rede do arquivo inteiro (aplicada a todos os containers do arquivo / fora do escopo services):

        networks:
          cluster-net:
            driver: overlay
            external: true

* Suba os ambientes com o comando:

        docker compose up

Suba primeiro o ambiente nas duas máquinas workers antes de subir na máquina master.

