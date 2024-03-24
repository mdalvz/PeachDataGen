import sys
import os
import time
import uuid
import shutil
import PIL.Image
import PIL.ImageGrab
import win32api
import win32con

def main():
  data_dir = os.path.abspath('./data')
  if not os.path.exists(data_dir):
    os.mkdir(data_dir)
  input_dir = os.path.join(data_dir, 'input')
  if os.path.exists(input_dir) and sys.argv[1] == 'reset':
    shutil.rmtree(input_dir)
  if not os.path.exists(input_dir):
    os.mkdir(input_dir)
  active = False
  taken = 0
  while True:
    time.sleep(0.1)
    if win32api.GetAsyncKeyState(win32con.VK_DELETE) & 1:
      active = not active
      print(f'ACTIVE {active}')
    if win32api.GetAsyncKeyState(win32con.VK_END) & 1:
      break
    if not active:
      continue
    # 1920 / 2 = 960
    # 1080 / 2 = 540
    # 960 - 320 = 640
    # 540 - 540 = 0
    # 960 + 320 = 1280
    # 540 + 100 = 640
    image = PIL.ImageGrab.grab(bbox=(640, 0, 1280, 640))
    #image = image.resize((128, 128))
    image_path = os.path.join(input_dir, f'{uuid.uuid4()}.png')
    image.save(image_path)
    taken += 1
    print(f'TAKEN {taken}')

if __name__ == '__main__':
  main()
