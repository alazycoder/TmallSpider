from torchvision.transforms import ToTensor


class MyTransform:
    """Resize a PIL Image and convert it to tensor.
    Converts a PIL Image (H x W x C) in the range
    [0, 255] to a torch.FloatTensor of shape (C x H x W) in the range [0.0, 1.0].
    """
    def __init__(self):
        self.to_tensor = ToTensor()
        self.height = 224
        self.width = 224

    def __call__(self, pic):
        """
        Args:
            pic (PIL): Image to be transformed.

        Returns:
            Tensor: Converted image.
        """

        pic = pic.resize((self.height, self.width))
        return self.to_tensor(pic)

    def __repr__(self):
        return self.__class__.__name__ + '()'