import glob

import os
import mmdet.apis
import mmcv
import cv2
import numpy as np
import torch, torchvision
from PIL import Image


from mmdet.apis import inference_detector, show_result_pyplot, init_detector
from mmdet.core.visualization.palette import get_palette, palette_val

##########################################################################
def draw_masks(img, masks, color=None, with_edge=True, alpha=0.8):
    img_orig = img.copy()
    taken_colors = set([0, 0, 0])
    if color is None:
        random_colors = np.random.randint(0, 255, (masks.size(0), 3))
        color = [tuple(c) for c in random_colors]
        color = np.array(color, dtype=np.uint8)
    polygons = []
    mask = None
    for i, mask in enumerate(masks):
        
        color_mask = color[i]
        mask = mask.astype(bool)
        #img[mask] = img[mask] * (1 - alpha) + color_mask * alpha
        img[mask] = img[mask] * 0
    
    img_aux = img.copy()
    mask_aux = img_aux.astype(bool)
    img_orig[mask_aux] = img_orig[mask_aux] * 0
    
    return img_orig
########################################################################3
# Lendo o modelo
config_file = f"modelo{os.sep}my_config.py" # IA
checkpoint_file = f"modelo{os.sep}epoch_12.pth"
model = init_detector(config_file, checkpoint_file, device='cpu')
#####################################################################

cwd = os.getcwd()
path_oncas = os.path.join(cwd, 'oncas')
form = ['.jpg', '.JPG','JPEG', 'jpeg', '.png', '.PNG', '.RAW','.raw']
list_direct = glob.glob(path_oncas + "/*" ) #lista com end da pasta de cada onca

score_thr = 0.75
mask_color=None

for path_onca in list_direct: # percorre list_direct tem end de pastas
  print(path_onca)
  oncas = glob.glob(path_onca + "/*") # lista com endereços de fotos de uma pasta
  nova_pasta = path_onca + "/seg_all"

  if not os.path.exists(nova_pasta):
    os.mkdir(nova_pasta) #criar pasta seg_ll

  id_onca = 0
  for path_img in oncas : # percorre imagens de uma pasta
    #print(path_img[-4:])
    if path_img[-4:] in form: # tem formato de imagem?
      img = mmcv.imread(path_img)
      result = inference_detector(model, img)
      bbox, seg = result
      #show_result_pyplot(model, path_img, result, score_thr=0.90) # score_thr define o score para aceitar 


      if len(seg[0]) < 1: # pular se a imagem não tiver onça
        continue
      #######################
      #img = mmcv.imread(img_file)
      #img = img.copy()
      if isinstance(result, tuple):
          bbox_result, segm_result = result ### delete
          if isinstance(segm_result, tuple):
              segm_result = segm_result[0]  # ms rcnn
      else:
          bbox_result, segm_result = result, None
      bboxes = np.vstack(bbox_result)
      labels = [
          np.full(bbox.shape[0], i, dtype=np.int32)
          for i, bbox in enumerate(bbox_result)
      ]
      labels = np.concatenate(labels)
      # draw segmentation masks
      segms = None
      if segm_result is not None and len(labels) > 0:  # non empty
          segms = mmcv.concat_list(segm_result)
          if isinstance(segms[0], torch.Tensor):
              segms = torch.stack(segms, dim=0).detach().cpu().numpy()
          else:
              segms = np.stack(segms, axis=0)
      #############
      if score_thr > 0:
        assert bboxes is not None and bboxes.shape[1] == 5
        scores = bboxes[:, -1]
        inds = scores > score_thr
        bboxes = bboxes[inds, :]
        labels = labels[inds]
        if segms is not None:
            segms = segms[inds, ...]

      max_label = int(max(labels) if len(labels) > 0 else 0)

      mask_palette = get_palette(mask_color, max_label + 1)
      colors = [mask_palette[label] for label in labels]
      colors = np.array(colors, dtype=np.uint8)
      img = draw_masks(img, segms, colors, with_edge=True)
      ##########################################33

      print("salvando imagem")
      nova_img = nova_pasta + "/out" + str(id_onca) + ".jpeg"
      id_onca += 1 
      mmcv.imwrite(img, nova_img) # salvar

      #print("printando abaixo img")
      #immg = img.copy()
      #immg = Image.fromarray(immg.astype(np.uint8)) # passa esse não salva, mas imprime
      #plt.imshow(immg)
      #plt.show()
      #############
      np_poly_array = []
      for i, bbox in enumerate(bboxes):
        bbox_int = bbox.astype(np.int32)
        poly = [[bbox_int[0], bbox_int[1]], [bbox_int[0], bbox_int[3]],
                [bbox_int[2], bbox_int[3]], [bbox_int[2], bbox_int[1]]]
        np_poly = np.array(poly).reshape((4, 2))
        np_poly_array.append(np_poly)
              
      # print(np_poly_array[0])
      #########################
      #print("## Iniciando loop do crop")
      nova_img = nova_pasta + "/out.jpeg"

      for i in range(len(np_poly_array)):# o crop corta para imagem ficar só o pedaço de seleção
        image_crop = img[int(np_poly_array[i][0][1]):int(np_poly_array[i][1][1]), int(np_poly_array[i][0][0]):int(np_poly_array[i][2][0])]
        image_crop = Image.fromarray(image_crop) # converte imagem np em PIL.image
      # display(image_crop)
      #mmcv.imwrite(image_crop, nova_img) # salvar
      #show_result_pyplot(model, path_img, result, score_thr=0.90) # score_thr define o score para aceitar 
      
      #print("Fim do for do crop")
    else:
      print(path_img + "\n" + "formato incopativel" )

  #print("Mudou de pasta ####################" +"\n")
print("FIMMM")


