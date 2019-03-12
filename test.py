from nsfw_detector import NSFWDetector
detector = NSFWDetector('./nsfw.299x299.h5')

# Predict single image
result = detector.predict('images/demo-card-1.jpg')
print('result:', result)

import os
base_dir = '../dataset/video2/images/'
filenames = os.listdir(base_dir)
for i in range(len(filenames)):
    filenames[i] = base_dir+filenames[i]
print('filenames:', len(filenames))

try:
    fin = open('../dataset/video2/haha_video_keras_nsfw_score.csv', 'r')
    lines = fin.readlines()
    exist_content_ids = dict()
    for line in lines:
        params = line.split(',')
        content_id = params[1]
        exist_content_ids[content_id] = 1
    fin.close()
    print('exist_content_ids:', len(exist_content_ids), list(exist_content_ids.keys())[0])
    new_filenames = []
    for i in range(len(filenames)):
        content_id = filenames[i].replace(base_dir, '')[:-4]
        print('content_id:', content_id)
        if content_id not in exist_content_ids:
            new_filenames.append(filenames[i])
    filenames = new_filenames
    print('new_filenames:', len(filenames))
except Exception as e:
    print(e)
    pass

exit(-1)

fout = open('../dataset/video2/haha_video_keras_nsfw_score.csv', 'w')
fout.write('content_id,nsfw_score\n')
batch_size = 64
for i in range(int(len(filenames)/batch_size+1)):
    print(i*batch_size, '/', len(filenames))
    result = detector.predict(filenames[i*batch_size:(i+1)*batch_size], batch_size=batch_size)
    for k, v in result.items():
        content_id = k.replace(base_dir, '')[:-4]
        nsfw_score = v['sexy']+v['porn']+v['hentai']
        fout.write(content_id+','+str(nsfw_score)+'\n')
fout.close()
