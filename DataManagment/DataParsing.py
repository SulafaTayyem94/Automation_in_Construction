import pandas as pd
import xml.etree.ElementTree as et
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
        bndbox = []

        path_of_the_directory = '../Data/annotated-images/'

        extension = ('.xml')

        self.rename_files(path_of_the_directory, extension)

        for subdir, dirs, files in os.walk(path_of_the_directory):
            for name in files:

                if name.endswith(extension):
                    root = self.parse_XML(subdir+name)

                    fileName.append(name)
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

                    self.render_bndbox(root, "bndbox", bndbox)


        df = pd.DataFrame(list(
            zip(fileName, path, source, width, height, depth, segmented,
                objectName, objectPose, objectTruncated, difficult, bndbox)),
            columns=['FILE_NAME', 'PATH', 'SOURCE', 'WIDTH', 'HEIGHT', 'DEPTH', 'SEGMENTED', 'OBJECT_NAME',
                     'OBJECT_POSE', 'OBJECT_TRUNCATED', 'DIFFICULT', 'BND_BOX']
        )

        df.sort_values(by=['FILE_NAME'], inplace=True)
        self.set_df(df)
        self.create_csv(df)

    def parse_XML(self, path):
        # '../Data/annotated-images/img-1.xml'
        tree = et.parse(path)
        root = tree.getroot()
        return root

    def rename_files(self, path_of_the_directory, extension):
        for subdir, dirs, files in os.walk(path_of_the_directory):
            for name in files:
                if name.endswith(extension):
                    file_x = name.split('img-')[1].split('.')[0]
                    new_format = "{:03d}".format(int(file_x))
                    old_file = os.path.join(subdir, name)
                    new_file = os.path.join(subdir, "img-"+ new_format + ".xml")
                    os.rename(old_file, new_file)

    def get_df(self):
        return self.Data_df

    def set_df(self, Data_df):
        self.Data_df = Data_df

    def create_csv(self, Data_df):
        Data_df.to_csv("Data.csv")


    def render_node_columns_by_name(self, root, node, column):
        for elm in root.iter(node):
            column.append(elm.text)

    def render_node_by_elment(self, parent, node):
        return parent.find(node, "")

    def render_bndbox(self, parent, node, column):
        for elm in parent.iter(node):
            xmin = elm.find("xmin","").text
            ymin = elm.find("ymin", "").text
            xmax = elm.find("xmax", "").text
            ymax = elm.find("ymax", "").text
            column.append("("+xmin + ',' + ymin + "),(" + xmax + "," + ymax+")")


def main():
    parse = DataParsing()


if __name__== "__main__":
    main()
