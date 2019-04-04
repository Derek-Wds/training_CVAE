import os
import tensorflow as tf
import numpy as np

# get all the files and its label
def get_files(path):
    dirs = [x[0] for x in os.walk(path)][1:]
    
    training_features = None
    validation_features = None
    training_labels = None
    validation_labels = None
    labels_value = None
    count = 1

    #TODO: Load Img
    for d in dirs:
        files = [f for f in os.listdir(d)] #load np
        for f in files:
            data = np.load(d+'/'+f)                
            data = data.reshape([-1, 28, 28, 1])
            length = data.shape[0]
            # concatenate arrays to get the training data
            if training_features is None:
                training_features = np.copy(data[:length-(length//10),:,:,:])
            else:
                training_features = np.concatenate([training_features, data[:length-(length//10),:,:,:]], axis=0)
            
            # get validation data
            if training_labels is None:
                training_labels = count * np.ones((length-(length//10),1))
            else:
                new_labels = count * np.ones((length-(length//10),1))
                training_labels = np.concatenate([training_labels, new_labels], axis=0)

            # concatenate arrays to get the validation data
            if validataion_features is None:
                validataion_features = np.copy(data[length-(length//10):,:,:,:])
            else:
                validataion_features = np.concatenate([validataion_features ,data[length-(length//10):,:,:,:]), axis=0)

            # get validation data
            if validation_labels is None:
                validation_labels = count * np.ones(((length//10),1))
            else:
                new_labels = count * np.ones(((length//10),1))
                validation_labels = np.concatenate([validation_labels, new_labels], axis=0)
        
        labels_value.append(d)
        count += 1
    
    
    return (training_features.astype('uint8'), training_labels.astype('uint8')), \
        (validation_features.astype('uint8'), validation_labels.astype('uint8'))

# create training data
def get_data(training_features, training_labels, validation_features, validation_labels):
    # get training data
    train_imgs = tf.constant(training_features)
    train_labels = tf.constant(training_labels)

    # get validation data
    validation_imgs = tf.constant(validation_features)
    validation_labels = tf.constant(validation_labels)

    training_data = tf.data.Dataset.from_tensor_slices((train_imgs, train_labels))
    validation_data = tf.data.Dataset.from_tensor_slices((validation_imgs, validation_labels))

    return training_data, validation_data

(train_features, train_labels), (validataion_features, validataion_labels) = get_files('quickdraw_data')
image_label_ds = get_data(train_features, train_labels, validataion_features, validataion_labels)


print('image shape: ', image_label_ds.output_shapes[0])
print('label shape: ', image_label_ds.output_shapes[1])
print('types: ', image_label_ds.output_types)
print()
print(image_label_ds)
