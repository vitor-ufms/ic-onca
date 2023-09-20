echo "Criando imagem..."
#docker build -t img-read-vitor . 

echo "Pegando o diretório atual"
dir="$PWD"

echo "Criando container com volume no diretório atual"
#cont="winpty docker run --name cont-read-vitor -v "$dir"/:/mmdetection/vitor.duarte -it img-read-vitor"

#se der erro use o outro
cont="docker run --name cont-read-vitor --gpus all -v "$dir":/mmdetection/vitor.duarte -it img-read-vitor"

#echo "$cont"
#$cont

# Acorda o container
docker container restart cont-read-vitor 

# Entrar no container
winpty docker exec -it cont-read-vitor /bin/bash

read


#ls
#echo "aquiiiiiiiiiiiii"
#dir="$PWD"
#echo "aquiiiiiiiiiiiii"
#ex="python "$dir"/test.py"

# executa $ex 
# imprime o conteudo echo "$ex" 
