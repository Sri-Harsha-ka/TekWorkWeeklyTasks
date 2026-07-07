import numpy as np
import streamlit as st
import tensorflow as tf


CLASS_NAMES = ["Normal", "Elevated", "Critical"]


def generate_synthetic_dataset(total_samples=240, random_state=42):
	rng = np.random.default_rng(random_state)
	bpm_values = rng.uniform(35.0, 185.0, size=total_samples).astype(np.float32)
	labels = np.array([label_bpm(value) for value in bpm_values], dtype=np.int32)
	shuffle_indices = rng.permutation(total_samples)
	return bpm_values[shuffle_indices], labels[shuffle_indices]


def label_bpm(bpm_value):
	if 60.0 <= bpm_value <= 100.0:
		return 0
	if 40.0 <= bpm_value < 60.0 or 100.0 < bpm_value <= 140.0:
		return 1
	return 2


def preprocess_data(bpm_values, labels, test_ratio=0.2, random_state=42):
	rng = np.random.default_rng(random_state)
	indices = rng.permutation(len(bpm_values))

	split_index = int(len(bpm_values) * (1.0 - test_ratio))
	train_indices = indices[:split_index]
	test_indices = indices[split_index:]

	x_train = bpm_values[train_indices].astype(np.float32)
	y_train = labels[train_indices].astype(np.int32)
	x_test = bpm_values[test_indices].astype(np.float32)
	y_test = labels[test_indices].astype(np.int32)

	mean_value = float(x_train.mean())
	std_value = float(x_train.std())
	if std_value == 0.0:
		std_value = 1.0

	x_train_scaled = ((x_train - mean_value) / std_value).reshape(-1, 1, 1)
	x_test_scaled = ((x_test - mean_value) / std_value).reshape(-1, 1, 1)

	return x_train_scaled, x_test_scaled, y_train, y_test, mean_value, std_value


def build_model():
	model = tf.keras.Sequential(
		[
			tf.keras.layers.SimpleRNN(16, input_shape=(1, 1), activation="tanh", return_sequences=False),
			tf.keras.layers.Dense(16, activation="relu"),
			tf.keras.layers.Dense(3, activation="softmax"),
		]
	)
	model.compile(
		optimizer="adam",
		loss="sparse_categorical_crossentropy",
		metrics=["accuracy"],
	)
	return model


@st.cache_resource(show_spinner=False)
def train_model():
	bpm_values, labels = generate_synthetic_dataset()
	x_train, x_test, y_train, y_test, mean_value, std_value = preprocess_data(bpm_values, labels)

	model = build_model()
	history = model.fit(
		x_train,
		y_train,
		validation_data=(x_test, y_test),
		epochs=14,
		batch_size=16,
		verbose=0,
	)

	test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

	return {
		"model": model,
		"mean_value": mean_value,
		"std_value": std_value,
		"history": history,
		"test_loss": float(test_loss),
		"test_accuracy": float(test_accuracy),
	}


def predict_bpm(model, bpm_value, mean_value, std_value):
	scaled_value = (np.array([[bpm_value]], dtype=np.float32) - mean_value) / std_value
	model_input = scaled_value.reshape(1, 1, 1)
	probabilities = model.predict(model_input, verbose=0)[0]
	predicted_index = int(np.argmax(probabilities))
	predicted_class = CLASS_NAMES[predicted_index]
	confidence = float(probabilities[predicted_index])
	return predicted_class, probabilities, confidence


def main():
	st.set_page_config(page_title="Heart Rate Anomaly Detector", page_icon="❤️", layout="centered")

	trained = train_model()
	model = trained["model"]
	mean_value = trained["mean_value"]
	std_value = trained["std_value"]

	st.title("Heart Rate Anomaly Detector")
	st.write(
		"Enter a single heart rate reading in BPM. The model classifies it as Normal, Elevated, or Critical using a one-to-one RNN."
	)

	# col1, col2 = st.columns(2)
	# col1.metric("Test Accuracy", f"{trained['test_accuracy'] * 100:.1f}%")
	# col2.metric("Test Loss", f"{trained['test_loss']:.3f}")

	bpm_value = st.number_input("Heart rate (BPM)", min_value=0.0, max_value=220.0, value=72.0, step=1.0)

	if st.button("Predict"):
		predicted_class, probabilities, confidence = predict_bpm(model, bpm_value, mean_value, std_value)

		if predicted_class == "Critical":
			st.error(f"Prediction: {predicted_class}")
		elif predicted_class == "Elevated":
			st.warning(f"Prediction: {predicted_class}")
		else:
			st.success(f"Prediction: {predicted_class}")

		st.write(f"Confidence: **{confidence * 100:.2f}%**")
		st.write("Class probabilities:")
		st.write({name: f"{prob * 100:.2f}%" for name, prob in zip(CLASS_NAMES, probabilities)})

	st.caption(
		"Synthetic data uses simple threshold rules: 60-100 BPM = Normal, 40-59 or 101-140 BPM = Elevated, and values outside those ranges = Critical."
	)


if __name__ == "__main__":
	main()
