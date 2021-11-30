# SDEXA GUI

### Description
This web application is a software primarily for calculating the <b>areal bone mineral density (aBMD)</b> from a CT surview scan (SDEXA). It therefore uses a provided neural network for segmentation of the vertebral bodies.
It is also usable for other kinds of tasks related to medical image processing, like <b>image registration</b>.


### Getting started: 
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