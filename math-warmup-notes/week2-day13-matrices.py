import numpy as np

print("=" * 60)
print("MATRIX BASICS FOR ML")
print("=" * 60)

# 1. Create matrices 
print("\n1. CREATING MATRICES:")
A = np.array([[1, 2], 
              [3, 4]])
B = np.array([[5, 6], 
              [7, 8]])

print("Matrix A:")
print(A)
print("\nMatrix B:")
print(B)

# 2. Matrix addition (element-wise)
print("\n2. MATRIX ADDITION:")
C = A + B
print("A + B =")
print(C)

# 3. Matrix multiplication 
print("\n3. MATRIX MULTIPLICATION (DOT PRODUCT):")
D = np.dot(A, B)  # or A @ B
print("A × B =")
print(D)
print("\nWhy this matters: Every neural network layer does this!")

# 4. Transpose (flip rows and columns)
print("\n4. TRANSPOSE:")
print("A transposed:")
print(A.T)

# 5. Element-wise multiplication (Hadamard product)
print("\n5. ELEMENT-WISE MULTIPLICATION:")
E = A * B  # Different from dot product!
print("A ⊙ B =")
print(E)

# 6. Real ML example: A simple neural network layer
print("\n\n6. REAL ML EXAMPLE:")
print("=" * 60)
print("Simple Neural Network Layer")
print("=" * 60)

# Input: 2 features (like age=25, salary=50000)
input_data = np.array([[25, 50000]])  # 1 row, 2 columns

# Weights: learned by the model
weights = np.array([[0.1, 0.2],    # 2 rows, 2 columns
                   [0.3, 0.4]])

# Forward pass (matrix multiplication!)
output = np.dot(input_data, weights)

print(f"\nInput (1x2): {input_data}")
print(f"\nWeights (2x2):\n{weights}")
print(f"\nOutput (1x2): {output}")
print("\nThis is how neural networks process data!")

print("\n" + "=" * 60)
print("Key takeaway: ML is just matrix math at scale!")
print("=" * 60)