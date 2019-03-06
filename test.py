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
fout = open('../dataset/video2/haha_video_keras_nsfw_score.csv', 'w')
fout.write('content_id,nsfw_score\n')
batch_size = 1024
for i in range(len(filenames)/batch_size+1):
    print(i*batch_size, '/', len(filenames))
    result = detector.predict(filenames[i*batch_size:(i+1)*batch_size], batch_size=batch_size)
    for k, v in result.items():
        content_id = k.replace(base_dir, '')[:-4]
        nsfw_score = v['sexy']+v['porn']+v['hentai']
        fout.write(content_id+','+str(nsfw_score)+'\n')
fout.close()
