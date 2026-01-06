import torch

def test_gpu():
    # Check if CUDA (GPU) is available
    if torch.cuda.is_available():
        print("GPU is available!")
        print(f"Device name: {torch.cuda.get_device_name(0)}")
        
        # Create a test tensor and move it to GPU
        test_tensor = torch.tensor([1., 2., 3.]).cuda()
        print(f"Test tensor on GPU: {test_tensor}")
        print(f"Tensor device: {test_tensor.device}")
    else:
        print("GPU is not available. Using CPU instead.")
        print(f"Current device: {torch.device('cpu')}")

if __name__ == "__main__":
    test_gpu()



