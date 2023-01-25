import os

if __name__ == "__main__":
    root_dir = "./docs/System"
    for file in os.listdir(root_dir):
        if ".md" not in file or "index" in file:
            continue
        path = os.path.join(root_dir, file)
        f = open(path, 'r')
        new_file_path = os.path.join(root_dir, file.replace('：', '-'))
        new_file = open(new_file_path, 'w')
        lines = f.readlines()
        for line in lines:
            if "<img src" in line:
                img_path = line.split('alt=')[1].split(' ')[0].replace('\"', '')
                new_file.write("![{}](./static/{}.png)".format(img_path, img_path))
            else:
                new_file.write(line)
        new_file.close()