from tensorflow.keras.models import load_model
import cv2, dlib, os, time
import numpy as np
from django.conf import settings
front_top_model = load_model(os.path.join(settings.BASE_DIR), 'data/front_and_top_2021_06_21.h5')

res = front_top_model.predict()