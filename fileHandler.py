import os
import shutil

class FileHandler:
    def __init__(self):
        # working directory
        self.working_dir = None
        # directory where valid images will be placed, invalid images remain in working directory
        self.output_dir = None
        # black image path
        self.empty_path = 'blank.png'
        # current file being worked on
        self.current_file = self.empty_path
        # stream containing all images in working directory
        self.instream = []
        # stream containing updated path for each file
        self.outstream = []
        # flag
        self.ready = False
    def reset(self, working_dir, output_dir):
        self.working_dir = working_dir
        self.output_dir = output_dir
        # stream containing all images in working directory
        self.instream = [working_dir + f for f in os.listdir(working_dir) if not f.startswith('.')]
        # stream containing updated path for each file
        self.outstream = []
        # current file being worked on
        self.current_file = self.get_next_file()
        self.ready = True
    def get_next_file(self):
        if len(self.instream) > 0:
            self.current_file = self.instream.pop()
            return self.current_file
        else:
            self.current_file = self.empty_path
            return None
    def update(self, key_pressed):
        if self.ready:
            # invalid image            
            if key_pressed == '0' and self.current_file != None and self.current_file != 'blank.png':
                self.outstream.append(self.current_file)
                # do somthign with next file
                next_file = self.get_next_file()
            # valid image
            elif key_pressed == '1' and self.current_file != None and self.current_file != 'blank.png':
                output_file_path = self.output_dir + self.current_file.split("/")[-1]
                # move file from working dir to output dir
                shutil.move(self.current_file, output_file_path)
                self.outstream.append(output_file_path)
                self.get_next_file()
            # left arrow key pressed
            elif ord(key_pressed) == 63234 and len(self.outstream) > 0:
                # add previous file to instream
                if self.current_file != None:
                    self.instream.append(self.current_file)
                prev_file = self.outstream.pop()
                prev_file_parent_dir = prev_file.split("/")[-2]
                if prev_file_parent_dir != self.working_dir.split("/")[-1]:
                    updated_path = self.working_dir + prev_file.split("/")[-1]
                    shutil.move(prev_file, updated_path)
                    self.current_file = updated_path
