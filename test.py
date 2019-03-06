from nsfw_detector import NSFWDetector
detector = NSFWDetector('./nsfw.299x299.h5')

# Predict single image
result = detector.predict('images/demo-card-1.jpg')
print('result:', result)

import os
base_dir = '../dataset/video2/images/'
filenames = os.listdir(base_dir)
fout = open('../dataset/video2/haha_video_keras_nsfw_score.csv', 'w')
fout.write('content_id,nsfw_score\n')
for i,filename in enumerate(filenames):
    if i % 1000 == 0:
        print(i, '/', len(filenames))
    result = detector.predict(base_dir+filename)
    for k, v in result.items():  # only one element
        nsfw_score = v['sexy']+v['porn']+v['hentai']
        fout.write(filename[:-4]+','+str(nsfw_score)+'\n')
fout.close()
