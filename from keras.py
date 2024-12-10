from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Define the CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),  # First conv layer
    MaxPooling2D(pool_size=(2, 2)),  # First pooling layer

    Conv2D(64, (3, 3), activation='relu'),  # Second conv layer
    MaxPooling2D(pool_size=(2, 2)),  # Second pooling layer

    Flatten(),  # Flatten for fully connected layer
    Dense(128, activation='relu'),  # Fully connected layer
    Dense(10, activation='softmax')  # Output layer for 10 classes
])

# Summarize the model to view trainable parameters
model.summary()
