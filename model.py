import tensorflow as tf
# Data hosted from: http://yann.lecun.com/exdb/mnist/
from tensorflow.examples.tutorials.mnist import input_data


# The following implements a multilayer convolutional neural network showcased and adapted from a tutorial on the tensorflow website.
# https://www.tensorflow.org/get_started/mnist/pros
def setup(x):
    # Set up variables - variables are values that live in a TensorFlow computation graph.
    # Weight initialization
    # We will be doing this a few times - so methods are handy models
    # According to tensorflow it is also good practice to initialize them with a slightly positive initial bias to avoid "dead neurons".
    # Since we are using ReLu neurons
    def weight_variable(shape):
      initial = tf.truncated_normal(shape, stddev=0.1)
      return tf.Variable(initial)
    def bias_variable(shape):
      initial = tf.constant(0.1, shape=shape)
      return tf.Variable(initial)
    # Convolution and Pooling
    # We also be abstracting these into 
    def conv2d(x, W):
      return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2x2(x):
      return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                            strides=[1, 2, 2, 1], padding='SAME')
    # First Convolutional Layer.
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    # To apply the layer, we first reshape x to a 4d tensor, with the second and third dimensions corresponding to image width and height, and the final dimension corresponding to the number of color channels.
    x_image = tf.reshape(x, [-1, 28, 28, 1])
    # convolve x_image with the weight tensor, add the bias, apply the ReLU function, and finally max pool. The max_pool_2x2 method will reduce the image size to 14x14.
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)
    # Second Convolutional Layer.
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)
    # Densely Connected Layer.
    # The image size has been reduced to 7x7, we add a fully-connected layer with 1024 neurons to allow processing on the entire image.
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])
    # Reshape the tensor from the pooling layer into a batch of vectors, multiply by a weight matrix, add a bias, and apply a ReLU.
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
    # Dropout Layer.
    # To reduce overfitting, we will apply dropout before the readout layer. 
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
    # Finally, the Readout Layer.
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    # Predicted class.
    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    
    return y_conv, keep_prob

def create(FILEPATH):
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    # MNIST is are two data sets - one of handwritten images mnist.test.images/mnist.train.images/mnist.validation.images
    # and one of their corresponding labels (being their digit) used for classification mnist.test.labels/mnist.train.labels/mnist.validation.labels
    
    # First layer - placeholders for the inputs
    # x lets you feed the graph any number of 784 length lists (a 28*28 vector flattened)
    # x lets you feed the graph any number of 10 list length (one hot encoded digits from 0-9)
    x = tf.placeholder(tf.float32, shape=[None, 784])
    y_ = tf.placeholder(tf.float32, shape=[None, 10])

    # Call set up to set up tensorflow variables.
    y_conv, keep_prob = setup(x)

    # Loss function.
    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    saver = tf.train.Saver()

    # Time to train the model! 
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        # large iteration - you're going to be here a while!
        for i in range(20000):
            # feeding it in batches of 50
            batch = mnist.train.next_batch(50)
            if i % 100 == 0:
                train_accuracy = accuracy.eval(feed_dict={
                    x: batch[0], y_: batch[1], keep_prob: 1.0})
                print('step %d, training accuracy %g' % (i, train_accuracy))
            train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
        saver.save(sess, FILEPATH)

        # Train the model
        # We will also use tf.Session rather than tf.InteractiveSession. This better separates model specification and model fitting.
        print('test accuracy %g' % accuracy.eval(feed_dict={
            x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
        saver.save(sess, FILEPATH)