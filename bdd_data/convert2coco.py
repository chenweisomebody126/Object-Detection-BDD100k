from label import labels
import json
import os
from os import path as osp


class BDD_100K():
    def __init__(self, datapath):
        self.info = {"year" : 2018,
                     "version" : "1.0",
                     "description" : "BDD_100K",
                     "contributor" : "somebody",
                     "url" : "http://bdd-data.berkeley.edu/",
                     "date_created" : "2018"
                    }
        self.licenses = [{"id": 1,
                          "name": "Attribution-NonCommercial",
                          "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
                         }]
        self.type = "instances"
        self.datapath = datapath
        # self.seqs = yaml.load(open(os.path.join(self.datapath, "Annotations", "db_info.yml"),
        #                            "r")
        #                      )["sequences"]

        # self.categories = [{"id": seqId+1, "name": seq["name"], "supercategory": seq["name"]}
        #                       for seqId, seq in enumerate(self.seqs)]
        # self.cat2id = {cat["name"]: catId+1 for catId, cat in enumerate(self.categories)}
        self.categories = [{"id": l.trainId, "name": l.name, "supercategory": l.category} for l in labels]
        self.cat2id = dict([(l.name, l.trainId) for l in labels])
        self.image_id = 0
        self.ann_id = 0
        for s in ["train", "val"]:
            #imlist = np.genfromtxt( os.path.join(self.datapath, "ImageSets", imageres, s + ".txt"), dtype=str)
            images, annotations = self.__get_annotation__(s)
            json_data = {"info" : self.info,
                         "images" : images,
                         "licenses" : self.licenses,
                         "type" : self.type,
                         "annotations" : annotations,
                         "categories" : self.categories}

            with open(os.path.join(self.datapath, "annotations", "origin_" +
                                   s+".json"), "w") as jsonfile:
                json.dump(json_data, jsonfile, sort_keys=True, indent=4)


    def __get_image_annotation_pairs__(self, label):
        images, annotations = [], []
        for frame in label['frames']:
            self.image_id +=1
            images.append({"date_captured" : "2018",
                           "file_name" : label['name'] + '.jpg',
                           "id" : self.image_id,
                           "license" : 1,
                           "url" : "",
                           "height" : 720,
                           "width" : 1280})

            for obj in frame['objects']:
                if 'box2d' not in obj:
                    continue
                xy = obj['box2d']
                if xy['x1'] >= xy['x2'] and xy['y1'] >= xy['y2']:
                    continue
                if obj['category'] not in self.cat2id:
                    continue
                x1, x2 = min(xy['x1'], xy['x2']), max(xy['x1'], xy['x2'])
                y1, y2 = min(xy['y1'], xy['y2']), max(xy['y1'], xy['y2'])
                w, h = (x2-x1)+1, (y2-y1)+1
                self.ann_id += 1
                annotations.append({"segmentation" : [[x1,y1,x1,y2,x2,y2,x2,y1]],#[[x1,y1,x1,x2,y2,y2,x2,y1]],
                                    "area" : w*h,
                                    "iscrowd" : 0,
                                    "image_id" : self.image_id,
                                    "bbox" : [x1, y1, w, h],
                                    'score': 1.0,
                                    "category_id" : self.cat2id[obj['category']],
                                    "id": self.ann_id})
        return images, annotations

    # def __get_image_annotation_pairs__(self, image_set):
    #     images = []
    #     annotations = []
    #     if not osp.exists(label_dir):
    #         print('Can not find', label_dir)
    #         return
    #     print('Processing', label_dir)
    #     input_names = [n for n in os.listdir(label_dir)
    #                            if osp.splitext(n)[1] == '.json']
    #     count = 0
    #     for name in input_names:
    #         in_path = osp.join(label_dir, name)
    #         out = self.label2det(json.load(open(in_path, 'r')))
    #         boxes.extend(out)
    #         count += 1
    #         if count % 1000 == 0:
    #             print('Finished', count)
    #
    #
    #     for imId, paths in enumerate(image_set):
    #         impath, annotpath = paths[0], paths[1]
    #         print (impath)
    #         name = impath.split("/")[3]
    #         img = np.array(Image.open(os.path.join(self.datapath + impath)).convert('RGB'))
    #         mask = np.array(Image.open(os.path.join(self.datapath + annotpath)).convert('L'))
    #         if np.all(mask == 0):
    #             continue
    #
    #         segmentation, bbox, area = self.__get_annotation__(mask, img)
    #         images.append({"date_captured" : "2016",
    #                        "file_name" : impath[1:], # remove "/"
    #                        "id" : imId+1,
    #                        "license" : 1,
    #                        "url" : "",
    #                        "height" : mask.shape[0],
    #                        "width" : mask.shape[1]})
    #         annotations.append({"segmentation" : segmentation,
    #                             "area" : np.float(area),
    #                             "iscrowd" : 0,
    #                             "image_id" : imId+1,
    #                             "bbox" : bbox,
    #                             "category_id" : self.cat2id[name],
    #                             "id": imId+1})
    #     return images, annotations


    def __get_annotation__(self, folder):
        # if not osp.exists(label_dir):
        #     print('Can not find', label_dir)
        #     return
        # print('Processing', label_dir)
        label_dir = self.datapath+folder
        input_names = [n for n in os.listdir(label_dir) if osp.splitext(n)[1] == '.json']
        images, annotations = [], []
        for name in input_names:
            in_path = osp.join(label_dir, name)
            images_out, annotations_out = self.__get_image_annotation_pairs__(json.load(open(in_path, 'r')))
            images.extend(images_out)
            annotations.extend(annotations_out)
            if self.image_id % 1000 == 0:
                print('Finished ', self.image_id)

        return images, annotations

if __name__ == "__main__":
    datapath = "bdd100k/labels/100k/"
    BDD_100K(datapath)
