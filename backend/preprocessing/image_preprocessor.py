from pathlib import Path

from PIL import Image


class ImagePreprocessor:
    """
    Handles image preprocessing before AI enhancement.
    """

    VALID_FORMATS = {".png", ".jpg", ".jpeg"}

    @staticmethod
    def is_valid_image(path: Path) -> bool:
        return (
            path.exists()
            and path.is_file()
            and path.suffix.lower() in ImagePreprocessor.VALID_FORMATS
        )

    @staticmethod
    def process_image(
        input_image: Path,
        output_image: Path,
        scale: float = 0.25,
        quality: int = 90,
    ) -> None:

        if not ImagePreprocessor.is_valid_image(input_image):
            raise ValueError(f"Invalid image: {input_image}")

        output_image.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with Image.open(input_image) as image:

            image = image.convert("RGB")

            if scale != 1.0:

                width = int(image.width * scale)
                height = int(image.height * scale)

                image = image.resize(
                    (width, height),
                    Image.Resampling.LANCZOS,
                )

            image.save(
                output_image,
                quality=quality,
                optimize=True,
            )

    def process_directory(
        self,
        input_directory: Path,
        output_directory: Path,
        scale: float = 0.25,
        quality: int = 90,
    ) -> int:

        for file in output_directory.iterdir():
            if file.is_file():
                file.unlink()

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        count = 0

        for image in sorted(input_directory.iterdir()):

            if not self.is_valid_image(image):
                continue

            destination = output_directory / image.name

            self.process_image(
                image,
                destination,
                scale,
                quality,
            )

            count += 1

        return count
