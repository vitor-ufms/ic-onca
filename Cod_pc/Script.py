import os

print("--Criando imagem...")

img = "docker build -t img-read-vitor ."
os.system(img) 

cwd = os.getcwd()

print("---Criando container com volume no diretório atual")
print("-- "+cwd)
#cont=" docker run --name cont-read-vitor -v "+ cwd + "/:/mmdetection/vitor.duarte -it img-read-vitor"
cont=" docker run --name cont-read-vitor -d -v "+ cwd + "/:/mmdetection/vitor.duarte -it img-read-vitor"

os.system(cont) 
print("passou do cont")

# Acorda o container
acord = "docker container restart cont-read-vitor"
os.system(acord)

# Entrar no container
ent_cont = "docker exec -it cont-read-vitor /bin/bash"
#os.system(ent_cont)

c_img = "docker exec -it -w /mmdetection/vitor.duarte cont-read-vitor python crop_img.py"
c_video = "docker exec -it -w /mmdetection/vitor.duarte cont-read-vitor python crop_video.py"
c_img_vid = "docker exec -it -w /mmdetection/vitor.duarte cont-read-vitor python crop_img_vid.py"
#os.system(c_video)
os.system(c_img_vid)
#os.system(c_img)
#os.system("docker container stop cont-read-vitor")