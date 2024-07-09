# -*- coding: utf-8 -*-
"""mnist-digit-classification-with-a-fully-connected-neural-network.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uOXo1Sw4RpWfG2701SyRE3gtRIOVAUDH

This notebook presents an MNIST digit classifier built with a fully-connected neural network in TensorFlow and Keras.

## 1. Import Statements

---
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# %tensorflow_version 2.x
import tensorflow as tf

"""## 2. Data Preprocessing

---

The first step is to preprocess our data. Here, we load the MNIST digit dataset from the Keras datasets library, split it into training and test sets, reshape the matrices, and encode the labels categorically.
"""

# Load the MNIST dataset.
mnist = tf.keras.datasets.mnist
train_data, test_data = mnist.load_data()

# Divide the data into features and labels.
train_images, train_labels = train_data
train_images, validation_images , train_labels , validation_labels = train_test_split(train_images, train_labels, test_size= 10000, random_state=42)
test_images, test_labels = test_data
print(test_images.shape)
print(validation_images.shape)
print(train_labels.shape)

# Reshape and normalize the images.
X_train = train_images.reshape((50000, 784))
X_train = X_train.astype('float32') / 255
X_validation = validation_images.reshape((10000, 784))
X_validation = X_validation.astype('float32') / 255
X_test = test_images.reshape((10000, 784))
X_test = X_test.astype('float32') / 255

# Reshape the labels and encode them categorically.
y_train = tf.keras.utils.to_categorical(train_labels)
y_validation = tf.keras.utils.to_categorical(validation_labels)
y_test = tf.keras.utils.to_categorical(test_labels)
print(y_train.shape)

"""Further, the following are the shapes of each matrix, as well as a visualization of a random MNIST digit."""

# Show the shapes of the data.
print("Training Images:", X_train.shape)
print("Validation Images:", X_validation.shape)
print("Testing Images:", X_test.shape)
print("Training Labels:", y_train.shape)
print("Validation Labels:", y_validation.shape)
print("Test Labels:", y_test.shape)

# Show a sample MNIST digit.
plt.imshow(train_images[10])
plt.show()

"""## 3. Neural Network

---

### 3.1. Define the Model

We then have to define our neural network. Here, we define a sequential model with two fully-connected layers.
"""

# Define the sequential model.
model = tf.keras.models.Sequential()

# Add two fully-connected layers to the network
model.add(tf.keras.layers.Dense(1024, activation='relu', input_shape=(28 * 28,)))
model.add(tf.keras.layers.Dropout(0.4))
# model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dense(10, activation='softmax'))

# Show the model.
model.summary()

"""Once our model is defined, we can compile it using the Adam optimizer and the categorical cross-entropy loss function."""

# # Compile the model.
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

"""### 3.2. Train the Model

We then train the model on 10 epochs, using a batch size of 256.
"""

# Define the parameters.
num_epochs = 10
batch_size = 256

# Train the model.
history = model.fit(X_train,
                      y_train,
                      epochs=num_epochs,
                      batch_size=batch_size,
                      validation_data=(X_validation, y_validation))

"""### 3.3. Display the Metrics

Finally, we display the metrics. We begin by displaying the model's accuracy and loss based on the test set.
"""

test_loss, test_accuracy = model.evaluate(X_test, y_test)
print('Test Accuracy:', test_accuracy)
print('Test Loss:', test_loss)

val_loss, val_accuracy = model.evaluate(X_validation, y_validation)
print('Validation Accuracy:', val_accuracy)
print('Validation Loss:', val_loss)

val_loss, val_accuracy = model.evaluate(X_train, y_train)
print('Train Accuracy:', val_accuracy)
print('Train Loss:', val_loss)

"""Then, we save the metric values for each epoch to plot the loss and accuracy curves for our model."""

# Save the metrics.
metrics = history.history

"""Finally, once we have our metric history, we can plot the curves."""

# Save the loss values.
training_loss_list = metrics['loss']
val_loss_list = metrics['val_loss']

# Plot the training and test loss.
x = np.arange(0, num_epochs, 1)
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.plot(x, training_loss_list, label='Training Loss')
plt.plot(x, val_loss_list, label='Validation Loss')
plt.legend()
plt.show()

train_accuracy_list = metrics['accuracy']
val_accuracy_list = metrics['val_accuracy']

plt.title('Training and Test Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.plot(x, train_accuracy_list, label='Training Accuracy')
plt.plot(x, val_accuracy_list, label='Validation Accuracy')
plt.legend()
plt.show()

"""## 4. Make a Prediction

---

Once our model is trained, we can use it to make predictions. To do this, we first use our test set to predict the classes.
"""

# Make predictions with the trained model.
predictions = model.predict(X_test)

"""Finally, we can show a random test image with its corresponding prediction."""

# Choose an index.
index = 40

# Show an image from the test set.
plt.imshow(test_images[index])
plt.show()

print("Prediction:", np.argmax(predictions[index]))