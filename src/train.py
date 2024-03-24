import keras
import numpy

WIDTH = 640
HEIGHT = 640
SIZE = WIDTH * HEIGHT

def main():
  train_features = numpy.loadtxt('./data/train_features.csv', delimiter=',')
  train_labels = numpy.loadtxt('./data/train_labels.csv', delimiter=',')
  test_features = numpy.loadtxt('./data/test_features.csv', delimiter=',')
  test_labels = numpy.loadtxt('./data/test_labels.csv', delimiter=',')
  print(f'TRAIN FEATURES {train_features.shape}')
  print(f'TRAIN LABELS {len(train_labels)}')
  print(f'TEST FEATURES {len(test_features)}')
  print(f'TEST LABELS {len(test_labels)}')
  model = keras.Sequential()
  model.add(keras.layers.Dense(SIZE, input_shape=(SIZE,), activation='relu'))
  model.add(keras.layers.Dense(SIZE // 2, activation='relu'))
  model.add(keras.layers.Dense(SIZE // 4, activation='relu'))
  model.add(keras.layers.Dense(SIZE // 8, activation='relu'))
  model.add(keras.layers.Dense(SIZE // 16, activation='relu'))
  model.add(keras.layers.Dense(3, activation='sigmoid'))
  model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
  model.fit(train_features, train_labels, validation_split=0.2, epochs=20, batch_size=10, verbose=2)

if __name__ == '__main__':
  main()
