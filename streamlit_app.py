import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cv2
from collections import Counter
import streamlit as st


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def get_colors(image, mc):
    length = int(600 * float(image.shape[0] / image.shape[1]))
    image = cv2.resize(image, (600, length), interpolation=cv2.INTER_AREA)
    # st.image(image)
    modified_image = image.reshape(image.shape[0] * image.shape[1], 3)
    clf = KMeans(n_clusters=mc, random_state=42)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)

    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    # plt.figure(figsize=(12, 8))
    fig1, ax1 = plt.subplots()

    def make_autopct():
        def my_autopct(pct):
            return '{p:.2f}%'.format(p=pct)

        return my_autopct

    ax1.pie(counts.values(), labels=hex_colors, colors=hex_colors, autopct=make_autopct(),
            rotatelabels=True, wedgeprops={'animated': True, "edgecolor": "black", 'linewidth': "0.05",
                                           'antialiased': True}, textprops={'size': 5, 'color': "black"})
    fig1.patch.set_facecolor(color="None")
    st.header("\n")
    st.subheader("Colours:")
    st.pyplot(fig1)

    return rgb_colors


if __name__ == "__main__":
    menu_items = {
        'About': '''
    	 ### Colour Identification in Images
    	 Made by - Rohan Karan
    	'''
    }
    st.set_page_config(page_title="Colour Identification in Images", page_icon="❤️", menu_items=menu_items)
    st.title("Colour Identification in Images")
    st.markdown(""" <style>
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        up_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
        st.subheader("Uploaded image:")
        st.image(up_image)
        max_unique_colors = len(np.unique(up_image, axis=0, return_counts=True)[0])
        max_value = min(10, max_unique_colors)
        st.sidebar.subheader("Maximum colours:")
        if max_unique_colors <= 1:
            max_colors = 1
            st.sidebar.warning("Only one colour!")
        else:
            max_colors = st.sidebar.slider(f'Choose between 1-{max_value}', min_value=1, max_value=max_value,
                                           value=min(5, max_unique_colors))

        with st.spinner("Analyzing..."):
            get_colors(up_image, max_colors)
            st.success("Done!")
