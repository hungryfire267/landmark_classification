class ModelFitter(): 
    def __init__(self, method_type, dropout_rate, learning_rate): 
        self.method_type = method_type
        self.dropout_rate = dropout_rate
        self.learning_rate = learning_rate
        
    def functional_model(self): 
        model_subclassed = None
        if (self.method_type == "VGG16"): 
            model_subclassed = VGG16Model(dropout_rate=self.dropout_rate)
        inputs = Input(shape=(64, 64, 3))
        model = Model(inputs, model_subclassed.call(inputs))
        return model
    
    def compile(self, model): 
        model.compile(
            optimizer=Adam(learning_rate=self.learning_rate), 
            loss=SparseCategoricalCrossentropy(from_logits=True),
            metrics=["accuracy"]
        )
        return model
    
    def fit(self, model, X_train, y_train, X_val, y_val, epochs, callbacks, verbose): 
        model_history = model.fit(
            X_train, y_train, batch_size=32, callbacks=callbacks,
            validation_data=(X_val, y_val), verbose=verbose, epochs=epochs
        )
        return model_history
    
class VGG16Model(tf.keras.Model): 
    def __init__(self, dropout_rate): 
        super(VGG16Model, self).__init__()
        self.conv_base = VGG16(weights="imagenet", include_top=False, input_shape=(64, 64, 3))
        self.conv_base.trainable = False
        self.flatten = tf.keras.layers.Flatten()
        self.hidden1 = tf.keras.layers.Dense(3200, activation="relu")
        self.dropout1 = tf.keras.layers.Dropout(dropout_rate)
        self.hidden2 = tf.keras.layers.Dense(1200, activation="relu")
        self.dropout2 = tf.keras.layers.Dropout(dropout_rate)
        self.hidden3 = tf.keras.layers.Dense(128, activation="relu")
        self.main_output = tf.keras.layers.Dense(10, activation="softmax")
    
    def call(self, input): 
        x = self.conv_base(input)
        x = self.flatten(x)
        x = self.hidden1(x)
        x = self.dropout1(x)
        x = self.hidden2(x)
        x = self.dropout2(x)
        x = self.hidden3(x)
        return self.main_output(x)