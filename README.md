# Object-Detection-BDD100k

0./home/shared/setup.sh && source ~/.bashrc

1. Install docker. (https://docs.docker.com/install/)
2. Install nvidia-docker (https://github.com/NVIDIA/nvidia-docker)
3. Follow the steps of (https://github.com/facebookresearch/Detectron/blob/master/INSTALL.md)
3.1 Clone repo
3.2 Install docker image & run the test image
4. After that, start the container associated with the image: sudo nvidia-docker container run --rm -it detectron:c2-cuda9-cudnn7 bash
5. Now, inside the container you can run the demo:
python2 tools/infer_simple.py
--cfg configs/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml
--output-dir /tmp/detectron-visualizations
--image-ext jpg
--wts https://s3-us-west-2.amazonaws.com/detectron/35861858/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml.02_32_51.SgT4y1cO/output/train/coco_2014_train:coco_2014_valminusminival/generalized_rcnn/model_final.pkl
demo

6.
gcloud compute scp  /Users/weichen/Downloads/bdd100k_images.zip  macbook@cs231n:/home/shared/Detectron/detectron/datasets/data/
7.
cd /home/shared/Detectron/detectron/datasets/data
unzip bdd100k_images.zip

8. mkdir annotations
vi /home/shared/Detectron/detectron/datasets/dataset_catalog.py
add
'bdd100k_train': {
    _IM_DIR:
        _DATA_DIR + '/bdd100k/images/100k/train',
    _ANN_FN:
        _DATA_DIR + '/bdd100k/images/100k/annotations/origin_train.json'
},
'bdd100k_val': {
    _IM_DIR:
        _DATA_DIR + '/bdd100k/images/100k/val',
    _ANN_FN:
        _DATA_DIR + '/bdd100k/images/100k/annotations/origin_val.json'
},

9.
gcloud compute scp --recurse /Users/weichen/Downloads/annotations/origin_train.json  macbook@cs231n:/home/shared/Detectron/detectron/datasets/data/bdd100k/images/100k/annotations/origin_train.json

gcloud compute scp --recurse /Users/weichen/Downloads/annotations/origin_val.json  macbook@cs231n:/home/shared/Detectron/detectron/datasets/data/bdd100k/images/100k/annotations/origin_val.json

10.
vi /home/shared/Detectron/configs/getting_started/tutorial_8gpu_e2e_faster_rcnn_R-50-FPN.yaml
NUM_ClASS : 11
TEST:
  FORCE_JSON_DATASET_EVAL: True
update directory with bdd100k_train, bdd100k_val
11.
sudo nvidia-docker run -it --name bdd100k -v /home/shared/Detectron/configs:/detectron/configs -v /home/shared/Detectron/detectron/datasets/:/detectron/detectron/datasets/ detectron:c2-cuda9-cudnn7 bash

sudo nvidia-docker run -it --name bdd100k -v /home/shared/Detectron/configs:/detectron/configs -v /home/shared/Detectron/detectron/datasets/data:/detectron/detectron/datasets/data detectron:c2-cuda9-cudnn7 bash


12.
python2 tools/train_net.py \
    --multi-gpu-testing \
    --cfg configs/getting_started/tutorial_8gpu_e2e_faster_rcnn_R-50-FPN.yaml \
    OUTPUT_DIR /detectron/detectron/datasets/data/detectron-output USE_NCCL True

13. restart the docker daemen and let it running
sudo /user/bin/dockerd
 
