# SDEXA GUI

### Description
This web application is a software for calculating the <b>areal bone mineral density (aBMD)</b> from a CT surview scan (SDEXA). It therefore uses a provided neural network for segmentation of the vertebral bodies.
It is also usable for other kinds of tasks related to medical image processing, like <b>image registration</b>.


### Getting started:
- Install Python 3.9


- It is recommended to create a new virtual environment (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


- Install the required dependencies:
    ```
    $ pip install -r requirements.txt
    ```

- Place a `pytorch checkpoint file (.ckpt)` for example in `/backend/segmentation/checkpoints/` and update the `CHECKPOINT_PATH` entry in the `config.yaml` accordingly


- Make sure everything is working by executing the tests
    ```
    $ python test.py
    ```


- Start the app
     ```
    $ python app.py
    ```
  

- If you want to use the software locally, visit `http://localhost:5000` in your browser. If that does not work, take the <u>url</u> from the console output:
    ```
    * Running on <url should show up here> (Press CTRL+C to quit)
    ```
