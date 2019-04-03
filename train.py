import argparse
import numpy as np
from keras.datasets import mnist
from keras.utils import to_categorical
from cvae import CVAE



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='quickdraw_data',
                        help="The input data directory for the program")
    parser.add_argument('--logs_dir', type=str, default='logs',
                        help="The logs directory for the tensorboard")
    parser.add_argument('--save_model', type=str, default='models',
                        help="The directory to store the ml5js model")
    parser.add_argument('--save_checkpoints', type=str, default='checkpoints',
                        help="The directory to store checkpointed models")
    parser.add_argument('--n_dim', type=int, default=16,
                        help="The dimension of latent z")
    parser.add_argument('--image_size', type=int, default=28,
                        help="The input image size, which should be a square image")
    parser.add_argument('--num_layers', type=int, default=2,
                        help="The number of CNN layers in the encoder and decoder model")
    parser.add_argument('--filters', type=int, default=8,
                        help="The number of the filters in the first CNN layer")
    parser.add_argument('--learning_rate', type=int, default=0.0005,
                        help="The learning rate of the Adam optimizer")
    parser.add_argument('--decay_rate', type=int, default=0.0,
                        help="The decay rate of the Adam optimizer")
    parser.add_argument('--epochs', type=int, default=30,
                        help="The number of epochs when training")
    parser.add_argument('--batch_size', type=int, default=100,
                        help="The number of batch_size when training")
    parser.add_argument('--image_depth', type=int, default=1,
                        help="The number of channels in image")
    
    args = parser.parse_args()

    (X_train, Y_train), (X_test, Y_test) = mnist.load_data()

    X_train = np.reshape(X_train, [-1, args.image_size, args.image_size, args.image_depth])
    X_test = np.reshape(X_test, [-1, args.image_size, args.image_size, args.image_depth])
    X_train = X_train.astype('float32') / 255.
    X_test = X_test.astype('float32') / 255.

    y_train = to_categorical(Y_train)
    y_test = to_categorical(Y_test)

    X_shape = X_train.shape[1]
    y_shape = y_train.shape[1]


    cvae = CVAE(args)
    cvae.forward(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    main()
