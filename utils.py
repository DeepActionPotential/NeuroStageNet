import torch
from torchvision import transforms
from PIL import Image

class ModelWrapper:
    def __init__(self, model_path, device=None):
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Load full model (architecture + weights)
        self.model = torch.load(model_path, map_location=self.device, weights_only=False)
        self.model.eval()

        # Preprocessing: resize, to tensor, normalize (use ImageNet stats)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),  # EfficientNet-B3 default
            transforms.ToTensor(),
        ])

    def predict(self, image_path):
        """
        Args:
            image_path (str): path to input MRI image
        Returns:
            tuple: (predicted_class_index, confidence)
        """
        img = Image.open(image_path).convert("RGB")
        x = self.transform(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            outputs = self.model(x)
            probs = torch.softmax(outputs, dim=1)
            conf, pred = torch.max(probs, 1)
        return pred.item(), conf.item()



