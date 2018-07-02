import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        #print(percent)
        ##print(color)
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

def detect_color(img_path):
    img = cv2.imread(img_path)
    im = Image.open(img_path)
    size = im.size
    pix = np.array(im)
    f,s,t, ft = pix[0,0,:],pix[0,size[0]-1,:],pix[size[1]-1,0,:],pix[size[1]-1,size[0]-1,:]

    print(f)
    print(s)
    print(t)
    print(ft)

    background_color = []



    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(img)

    hist = find_histogram(clt)
    #bar = plot_colors2(hist, clt.cluster_centers_)

    final_color=[]
    final_hist = []
    for color in clt.cluster_centers_:
        print(color)
    if (f[0] == s[0] and f[1] == s[1] and f[2]==s[2]) or (t[0] == ft[0] and t[1] == ft[1] and t[2]==ft[2]):
        print("background color detected")
        min_distance = 9999
        min_index = 0
        for index, color in enumerate(clt.cluster_centers_):
            temp = abs(color[0] - f[0]) + abs(color[1] - f[1]) + abs(color[2] - f[2])
            if temp <= min_distance:
                min_index = index 
                min_distance = temp

        for index, color in enumerate(clt.cluster_centers_):
            if index == min_index:
                pass
            else:
                #print(color)
                final_color.append(color)
                final_hist.append(hist[index])

                #print(hist[index])
    else:
        for index, color in enumerate(clt.cluster_centers_):
            final_color.append(color)
            final_hist.append(hist[index])
    max_value = max(final_hist)
    max_index = final_hist.index(max_value)    
    return final_color[max_index]
