import pandas as pd
import numpy as np
import xml.etree.ElementTree as et
from pathlib import Path
import os

class DataParsing:

    Data_df = pd.DataFrame()

    def __init__(self):

        fileName = []
        path = []
        source = []
        width = []
        height = []
        depth = []
        segmented = []

        objectName = []
        objectPose = []
        objectTruncated = []
        difficult = []
        # the value here would be a point of (xmin,ymin) (xmax, ymax)

        bndbox = []

        path_of_the_directory = '../Data/annotated-images/'
        # paths = Path(path_of_the_directory).glob('img-*/*.xml')
        # print(paths)
        ext = ('.xml')
        for files in os.scandir(path_of_the_directory):
            if files.path.endswith(ext):

                print(files)
                print(files.path)
                root = self.parse_XML(files.path)
                self.render_node_columns_by_name(root, "folder", fileName)
                self.render_node_columns_by_name(root, "path", path)
                self.render_node_columns_by_name(root, "source", source)

                size_node = self.render_node_by_elment(root, "size")

                self.render_node_columns_by_name(size_node, "width", width)
                self.render_node_columns_by_name(size_node, "height", height)
                self.render_node_columns_by_name(size_node, "depth", depth)

                self.render_node_columns_by_name(root, "segmented",segmented)

                object_node = self.render_node_by_elment(root, "object")

                self.render_node_columns_by_name(object_node, "name", objectName)
                self.render_node_columns_by_name(object_node, "pose", objectPose)
                self.render_node_columns_by_name(object_node, "truncated", objectTruncated)
                self.render_node_columns_by_name(object_node, "difficult", difficult)

                self.render_node_columns_by_name(root, "bndbox", bndbox)


        df = pd.DataFrame(list(
            zip(fileName, path, source, width, height, depth, segmented,
                objectName, objectPose, objectTruncated, difficult, bndbox)),
            columns=['FILE_NAME', 'PATH', 'SOURCE', 'WIDTH', 'HEIGHT', 'DEPTH', 'SEGMENTED', 'OBJECT_NAME',
                     'OBJECT_POSE', 'OBJECT_TRUNCATED', 'DIFFICULT', 'BND_BOX']
        )
        self.set_df(df)
        self.create_csv(df)

    def parse_XML(self, path):
        # '../Data/annotated-images/img-1.xml'
        tree = et.parse(path)
        root = tree.getroot()
        return root



    def get_df(self):
        return self.Data_df

    def set_df(self, Data_df):
        self.Data_df = Data_df

    def create_csv(self, Data_df):
        Data_df.to_csv("Data.csv")


    def render_node_columns_by_name(self, root, node, column):
        for elm in root.iter(node):
            # print(elm.text)
            # print("name")
            column.append(elm.text)

    def render_node_by_elment(self, parent, node):
        return parent.find(node, "")

    def render_bndbox(self, parent, node, column):
        for elm in parent.iter(node):

            xmin = elm.find("xmin","").text
            ymin = elm.find("ymin", "").text
            xmax = elm.find("xmax", "").text
            ymax = elm.find("ymax", "").text
            column.append(xmin + ',' + ymin + "," + xmax + "," + ymax)


def main():
    parse = DataParsing()


if __name__== "__main__":
    main()
