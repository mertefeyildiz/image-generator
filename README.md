# image-generator
A web-based image generator using Stable Diffusion and Flask.

# Image Generator with Diffusion Model

This project is a web-based application that allows users to generate custom images using a diffusion model. Users can upload images and logos, provide prompts, and customize the output with various text and color settings.

## Features

- **Image Upload**: Users can upload an image and a logo to generate a custom output.
- **Prompt-Based Generation**: The application uses a prompt provided by the user to generate or modify images.
- **Customization**: Users can set the punchline text, button text, and customize colors using hex codes.
- **Diffusion Model**: Utilizes the Stable Diffusion model from Stability AI to generate images.
- **Flask Backend**: The application is built using Flask, handling the image generation and serving the web interface.

## Technologies Used

- **Flask**: Web framework used to build the backend of the application.
- **Stable Diffusion Model**: Model used for generating and modifying images.
- **PIL (Pillow)**: For image processing and customization.
- **PyTorch**: For handling the diffusion pipeline.
- **HTML/CSS/JavaScript**: Frontend interface for user interaction.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Download the Stable Diffusion model:
    ```python
    # The required model is downloaded in the backend script automatically
    ```

## Usage

1. Run the Flask application:
    ```bash
    python case_api.py
    ```

2. Open your web browser and go to `http://localhost:80` to access the application.

3. Upload an image and a logo, enter the prompt and other details, and click on "Generate" to create your custom image.

## Project Structure

- `index3.html`: The HTML file that defines the frontend of the application.
- `case_api.py`: The backend Flask application that handles image generation and processing.
- `static/`: Folder containing any static files like CSS, JavaScript, or images.
- `templates/`: HTML templates used by Flask for rendering web pages.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your changes are well-tested and documented.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [your-email@example.com].

