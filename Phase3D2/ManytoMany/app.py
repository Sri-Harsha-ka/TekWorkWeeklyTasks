import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, RepeatVector, TimeDistributed, Dense
from tensorflow.keras.optimizers import Adam
import streamlit as st
import matplotlib.pyplot as plt


def generate_sequences(num_sequences=250, input_len=10, output_len=5, n_sensors=3, noise_std=0.1, seed=42):
    """
    Generate synthetic multi-sensor temperature sequences.

    Each sequence is a sum of sine waves with different frequencies/phases per sensor,
    plus Gaussian noise.
    """
    rng = np.random.RandomState(seed)
    total_len = input_len + output_len
    data = np.zeros((num_sequences, total_len, n_sensors), dtype=np.float32)

    # Base temperatures to make sensors operate around different means
    base_temps = rng.uniform(low=15.0, high=25.0, size=(n_sensors,))

    for i in range(num_sequences):
        t = np.arange(total_len)
        for s in range(n_sensors):
            freq = rng.uniform(0.05, 0.25) * (1.0 + 0.2 * rng.randn())
            phase = rng.uniform(0, 2 * np.pi)
            amplitude = rng.uniform(0.5, 2.0)
            seasonal = amplitude * np.sin(2 * np.pi * freq * t + phase)
            trend = 0.01 * (t - total_len / 2)  # small linear trend
            noise = rng.normal(scale=noise_std, size=total_len)
            data[i, :, s] = base_temps[s] + seasonal + trend + noise

    return data


def fit_min_max_scaler(data):
    mins = data.min(axis=(0, 1))
    maxs = data.max(axis=(0, 1))

    return mins, maxs


def scale_sequences(data, mins, maxs):

    def scale(x):
        return (x - mins) / (maxs - mins + 1e-8)

    return scale(data)


def train_test_split(X, y, test_frac=0.2, shuffle=True, seed=123):
    n = X.shape[0]
    idx = np.arange(n)
    if shuffle:
        rng = np.random.RandomState(seed)
        rng.shuffle(idx)
    split = int(n * (1 - test_frac))
    train_idx = idx[:split]
    test_idx = idx[split:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def make_residual_targets(y, last_observed_step):
    return y - last_observed_step[:, None, :]


@st.cache_resource
def build_and_train_model(X_train, y_train, X_val, y_val, input_len, output_len, n_sensors,
                          epochs=15, batch_size=16, verbose=0):
    tf.keras.backend.clear_session()
    model = Sequential([
        LSTM(64, activation='tanh', input_shape=(input_len, n_sensors)),
        RepeatVector(output_len),
        LSTM(64, activation='tanh', return_sequences=True),
        TimeDistributed(Dense(n_sensors))
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        verbose=verbose
    )
    return model, history


def inverse_scale(scaled, mins, maxs):
    return scaled * (maxs - mins + 1e-8) + mins


def plot_sequence(input_seq, actual_future, pred_future, sensor_idx, input_len, output_len):
    # input_seq, actual_future, pred_future are 1D arrays for the chosen sensor
    total_x = np.arange(input_len + output_len)
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(total_x[:input_len], input_seq, label='Input (past)', marker='o')
    ax.plot(total_x[input_len:], actual_future, label='Actual future', marker='o')
    ax.plot(total_x[input_len:], pred_future, label='Predicted future', marker='x')
    ax.set_xlabel('Time step (hours)')
    ax.set_ylabel('Temperature')
    ax.set_title(f'Sensor {sensor_idx} — Past {input_len} -> Next {output_len} hours')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig


def main():
    st.set_page_config(page_title='Multi-sensor Many-to-Many RNN Demo', layout='wide')
    st.title('Multi-sensor Temperature Forecasting (Many-to-Many RNN)')

    # --- Generate synthetic data ---
    input_len = 10
    output_len = 5
    n_sensors = 3
    num_sequences = 260

    st.sidebar.header('Data / Training settings')
    num_sequences = st.sidebar.slider('Number of sequences', 100, 500, num_sequences, step=20)
    epochs = st.sidebar.slider('Epochs', 5, 50, 15)
    batch_size = st.sidebar.selectbox('Batch size', [8, 16, 32], index=1)

    sequences = generate_sequences(num_sequences=num_sequences,
                                   input_len=input_len,
                                   output_len=output_len,
                                   n_sensors=n_sensors)

    train_sequences, test_sequences, _, _ = train_test_split(sequences, sequences, test_frac=0.2)

    mins, maxs = fit_min_max_scaler(train_sequences)
    train_scaled = scale_sequences(train_sequences, mins, maxs)
    test_scaled = scale_sequences(test_sequences, mins, maxs)

    X_train = train_scaled[:, :input_len, :]
    y_train = train_scaled[:, input_len:, :]
    X_test = test_scaled[:, :input_len, :]
    y_test = test_scaled[:, input_len:, :]

    y_train_residual = make_residual_targets(y_train, X_train[:, -1, :])
    y_test_residual = make_residual_targets(y_test, X_test[:, -1, :])

    st.sidebar.markdown(f'Training samples: {X_train.shape[0]}')
    st.sidebar.markdown(f'Test samples: {X_test.shape[0]}')

    # --- Build / train model ---
    with st.spinner('Training model — this may take a short moment'):
        model, history = build_and_train_model(
            X_train, y_train_residual, X_test, y_test_residual,
            input_len=input_len, output_len=output_len, n_sensors=n_sensors,
            epochs=epochs, batch_size=batch_size, verbose=0
        )

    st.success('Model trained')

    # Show training curve
    st.subheader('Training Loss')
    loss_vals = history.history['loss']
    val_loss_vals = history.history.get('val_loss')
    fig1, ax1 = plt.subplots()
    ax1.plot(loss_vals, label='train')
    if val_loss_vals:
        ax1.plot(val_loss_vals, label='val')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('MSE loss')
    ax1.legend()
    st.pyplot(fig1)

    # --- Interactive inspection ---
    st.sidebar.header('Inspect predictions')
    sensor_idx = st.sidebar.selectbox('Choose sensor', list(range(n_sensors)))
    sample_idx = st.sidebar.slider('Test sample index', 0, X_test.shape[0] - 1, 0)

    X_sample = X_test[sample_idx:sample_idx + 1]
    y_sample = y_test[sample_idx:sample_idx + 1]

    y_pred_residual = model.predict(X_sample)

    # Inverse scale to original temperature units
    input_orig = inverse_scale(X_sample[0], mins, maxs)  # shape (input_len, n_sensors)
    actual_orig = inverse_scale(y_sample[0], mins, maxs)  # shape (output_len, n_sensors)
    pred_scaled = y_pred_residual + X_sample[:, -1:, :]
    pred_orig = inverse_scale(pred_scaled[0], mins, maxs)

    st.subheader('Selected sequence prediction')
    st.write(f'Sample index (test set): {sample_idx}')

    fig2 = plot_sequence(input_orig[:, sensor_idx], actual_orig[:, sensor_idx], pred_orig[:, sensor_idx],
                         sensor_idx, input_len, output_len)
    st.pyplot(fig2)

    # Show numeric comparison for all sensors
    st.subheader('Numeric comparison (next 5 hours)')
    hours = [f'+{i+1}h' for i in range(output_len)]
    # Build a simple display
    for s in range(n_sensors):
        actual_s = actual_orig[:, s]
        pred_s = pred_orig[:, s]
        last_input_value = float(input_orig[-1, s])
        rows = []
        for h in range(output_len):
            rows.append({'Hour': hours[h], 'Last observed': last_input_value, 'Actual': float(actual_s[h]), 'Predicted': float(pred_s[h]), 'Delta vs last': float(pred_s[h] - last_input_value)})
        st.write(f'Sensor {s}')
        st.table(rows)

    st.markdown('---')
    st.subheader('Model summary')
    st.text(model.summary())


if __name__ == '__main__':
    main()
