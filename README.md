# Price Converter (OCR-Based)


## Overview

Price Converter is a Python application that detects prices from images or a live webcam feed using Optical Character Recognition (OCR), identifies the associated currency, and converts detected prices into a target currency.

This project was developed to explore computer vision, text processing, and API-based currency conversion in a practical context. The goal was to create a practical tool that could help travelers quickly understand foreign prices without manually converting each one.


## Features

- OCR-based text detection using EasyOCR

- Automatic price extraction with currency recognition

- Support for symbols and codes (€, $, £, ¥, EUR, USD, GBP, JPY, 円)

- Optional default currency and manual currency override

- Real-time webcam mode

- Static image processing mode

- Noise filtering (confidence threshold, minimum price value)

- Basic OCR error correction for common currency misreads


## How It Works

1. The application captures an image (from a file or webcam).

2. EasyOCR detects text regions and returns bounding boxes with confidence scores.

3. A custom price parser extracts numeric values using regular expressions and associates them with detected currencies.

4. Prices are converted using live exchange rates via **forex-python**.

5. The converted values are displayed on the image alongside the original price.


## Project Structure

- webcam.py – Real-time webcam-based price detection

- static_image.py – Image-based price detection

- ocr.py – OCR handling using EasyOCR

- price_parser.py – Price extraction and currency association

- currency.py – Currency conversion logic

- text_normalizer.py – Fixes common OCR currency symbol errors

- images/ – Sample images for testing


## Installation

Clone the repository and install dependencies:

```
bash
  
pip install -r requirements.txt
```


## Usage

Run static image mode:

```
bash
  
python static_image.py
```


Run webcam mode:

```
bash
  
python webcam.py
```


In webcam mode:

- Press **t** to trigger OCR and conversion

- Press **c** to clear results

- Press **q** to quit



## Expected Outputs

- Below is an example of the webcam mode detecting a price in JPY and converting it to EUR in real time.

![Webcam price detection example](assets/webcam-conversion-demo.jpg)



- Example output from static_image.py converting JPY prices to EUR using a sample image.

![Static image price detection example](assets/static-image-conversion-demo.jpg)


## Learning Goals

This project was developed to:

- Understand how OCR systems work in practice

- Implement pattern-based text parsing using regular expressions

- Handle noisy input data

- Integrate third-party APIs

- Structure a small but complete Python application


## Known Limitations

- OCR accuracy depends heavily on lighting, camera quality, and text clarity.

- Exchange rates are retrieved at runtime and require an internet connection.

- Complex price formats (e.g., thousands separators in different locales) may not always be parsed correctly.

- Real-time processing is not continuous by default in webcam mode (manual trigger required).

- The application is optimized for learning purposes, not production deployment.


## License

This project is licensed under the MIT License.
