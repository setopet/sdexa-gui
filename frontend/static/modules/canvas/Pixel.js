/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
/** Manages a pixel by wrapping access to the ImageData for better accessibility **/
export function Pixel(index, x, y, red, green, blue, alpha) {
    const originalValue = red;  // asserting the image is gray scale with identical color channels
    const uint8Max = 255;
    this.red = red;
    this.green = green;
    this.blue = blue;
    this.alpha = alpha;

    this.setImageData = imageData => {
        imageData[index]  = this.red;
        imageData[index+1] = this.green;
        imageData[index+2] = this.blue;
        imageData[index+3] = this.alpha;
        return imageData;
    }

    this.setYellow = (imageData, opacity) => {
        this.green = 150;
        this.red = 150;
        this.blue = 0;
        this.alpha = opacity * uint8Max;
        return this.setImageData(imageData);
    }

    this.setGrey = imageData => {
        const value = this.getValue();
        this.red = value;
        this.green = value;
        this.blue = value;
        this.alpha = uint8Max;
        return this.setImageData(imageData);
    }

    this.getValue = () => originalValue;

    this.getX = () => x;

    this.getY = () => y;

    return this;
}