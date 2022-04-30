#Analyze the best tuned model
#Let's compare the real labels with the classified labels.


_, _, test_data, test_labels = get_iris_data()
plot_data(test_data, test_labels.argmax(1))


# Obtain the directory where the best model is saved.
print("You can use any of the following columns to get the best model: \n{}.".format(
    [k for k in analysis.dataframe() if k.startswith("keras_info")]))
print("=" * 10)
logdir = analysis.get_best_logdir("keras_info/val_loss", mode="min")
# We saved the model as `model.h5` in the logdir of the trial.
from tensorflow.keras.models import load_model
tuned_model = load_model(logdir + "/model.h5")

tuned_loss, tuned_accuracy = tuned_model.evaluate(test_data, test_labels, verbose=0)
print("Loss is {:0.4f}".format(tuned_loss))
print("Tuned accuracy is {:0.4f}".format(tuned_accuracy))
print("The original un-tuned model had an accuracy of {:0.4f}".format(original_accuracy))
predicted_label = tuned_model.predict(test_data)
plot_data(test_data, predicted_label.argmax(1))


def plot_comparison(X, y):
    # Visualize the data sets
    plt.figure(figsize=(16, 6))
    plt.subplot(1, 2, 1)
    for target, target_name in enumerate(["Incorrect", "Correct"]):
        X_plot = X[y == target]
        plt.plot(X_plot[:, 0], X_plot[:, 1], linestyle='none', marker='o', label=target_name)
    plt.xlabel(feature_names[0])
    plt.ylabel(feature_names[1])
    plt.axis('equal')
    plt.legend();

    plt.subplot(1, 2, 2)
    for target, target_name in enumerate(["Incorrect", "Correct"]):
        X_plot = X[y == target]
        plt.plot(X_plot[:, 2], X_plot[:, 3], linestyle='none', marker='o', label=target_name)
    plt.xlabel(feature_names[2])
    plt.ylabel(feature_names[3])
    plt.axis('equal')
    plt.legend();
    
plot_comparison(test_data, test_labels.argmax(1) == predicted_label.argmax(1))