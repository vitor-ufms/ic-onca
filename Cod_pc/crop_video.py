import  os, glob
import mmcv

cwd = os.getcwd()

path_oncas = os.path.join(cwd, 'oncas')
#path_c_onca = os.path.join(cwd, 's_oncas')
form = ['.MP4', '.AVI','.mp4', '.avi', '.ASF']

##
#end_video = os.path.join(cwd,"modelo","video.MP4") 
#video = mmcv.VideoReader(end_video)

list_direct = glob.glob(path_oncas + "/*" ) #lista com end
print(cwd)
for path_onca in list_direct: # percorre list_direct tem end de pastas
  print(path_onca)
  path_videos = os.path.join(path_onca, 'videos')

  if not os.path.exists(path_videos): # se o diretório video não exitir pula para a próxima pasta
     continue

  videos = glob.glob(path_videos + "/*") # lista com vídeos
  
  nova_pasta = os.path.join(path_onca, "img_vid")

  if not os.path.exists(nova_pasta):
    os.mkdir(nova_pasta) #criar pasta seg_ll

  id_video = 0
  for end_video in videos: 
    video = mmcv.VideoReader(end_video)
    if end_video[-4:] in form: # tem formato de vídeo?
      if not video.opened:
        print("Erro ao abrir o vídeo")
        continue
      print("###",end_video)
      
      i = 0
      for frame in video:
        if (i % 20) != 0 :
          continue
        #mmcv.imwrite(img, nova_img) # salvar
        mmcv.imwrite(frame, nova_pasta + os.sep + f"vid{id_video}im{i}out.jpg") # salvar
        #cv2.imwrite(path_c_onca, frame)
        i += 1
        
    id_video +=1

