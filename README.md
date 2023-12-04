# NotSoHumanBenchmark

## Overview
NotSoHumanBenchmark is a Python project that automates various games from the Human Benchmark website. It includes a variety of games designed to test different cognitive abilities, such as reaction time, memory, and typing speed.

## Games Included
- **Aim Trainer**: Tests your speed and accuracy in hitting targets.
- **Chimp Test**: Measures your short-term memory capacity.
- **Number Memory Test**: Evaluates how many numbers you can remember in sequence.
- **Reaction Time Test**: Assesses how quickly you can respond to a visual stimulus.
- **Sequence Memory Test**: Challenges your ability to remember and replicate a sequence of lights.
- **Typing Test**: Measures your typing speed and accuracy.
- **Verbal Memory Test**: Tests your ability to remember which words have been shown.
- **Visual Memory Test**: Evaluates your spatial memory and ability to remember patterns.

## Installation
To run NotSoHumanBenchmark, you need to install the required Python packages. You can install them using the following command:

```bash
pip install -r requirements.txt
```

## Usage
To start the application, run the `main.py` script:

```bash
python main.py
```

Once the script is running, it will automatically detect the Human Benchmark game window and start playing the selected game.

## Dependencies
- PyGetWindow
- Pillow
- NumPy
- OpenCV-Python
- Keyboard
- PyAutoGUI
- pytesseract

## Extra Dependencies
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (for the Typing Test game you have to install Tesseract OCR to your system)

## Contributing
Contributions to the NotSoHumanBenchmark project are welcome. If you have an idea for improving the code or adding new features, feel free to create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Note: This project is for educational purposes only and is not intended to be used for cheating or violating the terms of service of the Human Benchmark website.*

