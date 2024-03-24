import os
import numpy
import uuid
import shutil
import random
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

WIDTH = 640
HEIGHT = 640
TEST_PERCENT = 0.2

# debug_dir = os.path.abspath('./data/debug')
# if os.path.exists(debug_dir):
#  shutil.rmtree(debug_dir)#
# os.mkdir(debug_dir)

# def save_features_debug(features):
#  image = PIL.Image.new(mode='RGB', size=(WIDTH, HEIGHT))
#  pixels = image.load()
#  for y in range(HEIGHT):
#    for x in range(WIDTH):
#      gray = int(features[y * WIDTH + x] * 255.0)
#      pixels[x,y] = (gray, gray, gray)
#  dst_path = os.path.join(debug_dir, f'{uuid.uuid4()}.png')
#  image.save(dst_path)

def create_entry(image, found, target_x, target_y):
  features = []
  pixels = image.load()
  for y in range(image.size[1]):
    for x in range(image.size[0]):
      pixel = pixels[x,y]
      features.append(max(0, pixel[0] - (pixel[1] + pixel[2]) / 2) / 255.0)
  labels = [1.0 if found else 0.0, target_x / WIDTH, target_y / HEIGHT]
  # save_features_debug(features)
  return numpy.asarray(features), numpy.asarray(labels)

def get_all_inputs():
  images = []
  input_dir = os.path.abspath('./data/input')
  cur = 0
  input_names = os.listdir(input_dir)
  for input_name in input_names:
    cur += 1
    print(f'LOAD IMAGE {cur}/{len(input_names)}')
    input_path = os.path.join(input_dir, input_name)
    image = PIL.Image.open(input_path)
    images.append(image)
  return images

def create_negative_entries(inputs):
  features_array = []
  labels_array = []
  cur = 0
  for input in inputs:
    cur += 1
    print(f'CREATE NEGATIVE ENTRY {cur}/{len(inputs)}')
    features, labels = create_entry(input, False, 0.0, 0.0)
    features_array.append(features)
    labels_array.append(labels)
  return features_array, labels_array

def create_random_name():
  name = ''
  for _ in range(random.randint(4, 12)):
    name += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
  return name

def create_positive_entries(inputs):
  features_array = []
  labels_array = []
  cur = 0
  for input in inputs:
    cur += 1
    print(f'CREATE POSITIVE ENTRY {cur}/{len(inputs)}')
    copy = input.copy()
    draw = PIL.ImageDraw.Draw(copy)
    text_height = random.randint(10, 16)
    font = PIL.ImageFont.truetype('./src/arialbd.ttf', size=text_height)
    text = create_random_name()
    text_width = int(draw.textlength(text, font=font))
    text_position = (random.randint(0, WIDTH - text_width), random.randint(0, HEIGHT - text_height))
    text_color = (random.randint(200, 255), random.randint(20, 70), random.randint(20, 70))
    draw.text(text_position, text, text_color, font)
    target_x = (text_position[0] + text_width / 2)
    target_y = (text_position[1] + text_height)
    features, labels = create_entry(copy, True, target_x, target_y)
    features_array.append(features)
    labels_array.append(labels)
  return features_array, labels_array

def create_entries(inputs):
  negative_features, negative_labels = create_negative_entries(inputs)
  positive_features, positive_labels = create_positive_entries(inputs)
  combined = list(zip(negative_features, negative_labels)) + list(zip(positive_features, positive_labels))
  random.shuffle(combined)
  test_count = int(len(combined) * TEST_PERCENT)
  test_combined = combined[:test_count]
  train_combined = combined[test_count:]
  test_features, test_labels = list(zip(*test_combined))
  train_features, train_labels = list(zip(*train_combined))
  return numpy.asarray(train_features), numpy.asarray(train_labels), numpy.asarray(test_features), numpy.asarray(test_labels)

def create_entries_and_save():
  inputs = get_all_inputs()
  train_features, train_labels, test_features, test_labels = create_entries(inputs)
  train_features_dst = os.path.abspath('./data/train_features.csv')
  train_labels_dst = os.path.abspath('./data/train_labels.csv')
  test_features_dst = os.path.abspath('./data/test_features.csv')
  test_labels_dst = os.path.abspath('./data/test_labels.csv')
  print(f'SAVE {train_features_dst}')
  numpy.savetxt(train_features_dst, train_features, delimiter=',')
  print(f'SAVE {train_labels_dst}')
  numpy.savetxt(train_labels_dst, train_labels, delimiter=',')
  print(f'SAVE {test_features_dst}')
  numpy.savetxt(test_features_dst, test_features, delimiter=',')
  print(f'SAVE {test_labels_dst}')
  numpy.savetxt(test_labels_dst, test_labels, delimiter=',')

def main():
  create_entries_and_save()

if __name__ == '__main__':
  main()
