import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt

class NegativeSelectionAlgorithm:
    def __init__(self, self_set_size, non_self_set_size, threshold, dimensions):
        self.self_set_size = self_set_size
        self.non_self_set_size = non_self_set_size
        self.dimensions = dimensions
        self.threshold = threshold
        self.total_samples = np.random.rand(self.self_set_size + self.non_self_set_size, dimensions)
        np.random.shuffle(self.total_samples)
        self.self_set = self.total_samples[:self.self_set_size]
        self.non_self_set = self.total_samples[self.self_set_size:self.self_set_size + self.non_self_set_size]

    def train(self):
        self.detectors = np.zeros(self.non_self_set_size)
        for i in range(self.non_self_set_size):
            self.detectors[i] = self.calculate_detection_threshold(self.non_self_set[i])
        
    def detect_anomalies(self, input):
        for i in range(self.non_self_set_size):
            distance = np.linalg.norm(input - self.non_self_set[i])
            if distance <= self.detectors[i]:
                return 'Anomaly'
        return 'Normal'
    
    def calculate_detection_threshold(self, self_pattern):
        distances = np.linalg.norm(self.non_self_set - self_pattern, axis=1)
        threshold = np.percentile(distances, 2)
        return threshold
    

def plot_regions(NSA, input=None):
    plt.figure(figsize=(8, 8))
    plt.scatter(NSA.non_self_set[:, 0], NSA.non_self_set[:, 1], color='green', label='Self-Patterns')
    for i in range(NSA.non_self_set_size):
        circle = plt.Circle((NSA.non_self_set[i, 0], NSA.non_self_set[i, 1]), 
                            NSA.detectors[i], 
                            color='red', 
                            fill=False)
        plt.gca().add_patch(circle)
    plt.plot(input[0], input[1], 'bo', label=f'{result}')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Detection Regions')
    plt.legend()
    plt.axis('equal')
    plt.show()

# Example usage:
self_set_size = 10000
non_self_set_size = 50
dimensions = 2
threshold = 0.01

nsa = NegativeSelectionAlgorithm(self_set_size, non_self_set_size, threshold, dimensions)
nsa.train()


# # Detect anomalies
new_input = np.random.rand(dimensions)
result = nsa.detect_anomalies(new_input)
plot_regions(nsa, new_input)