# Realtime self driving car implementing DNN


## Install dependencies and create environment
First install the Anaconda distribution and install all the required dependencies.Create the virtual environment tf-gpu (for eg)

conda create --name tf-gpu

install supported verson of python by tensorflow and proceed to below steps

### Run the pretrained model(model-010.h5)
Turn on all the connections to esp32 and H-bridge driver and wait for five seconds while the servo returns to the centre

```python
python drive.py model-010.h5
```

### To train the model

You'll need the data folder which contains the training images.

The folder is created automatically when you run 

```python
python train.py
```
This creates a folder named training_data and run below code corresponding to the created folder!

```python
python model.py
```
if you run python train.py more than once the code automatically creates training_data1 and so on!

After running model.py it will generate a file `model-<epoch>.h5` whenever the performance in the epoch is better than the previous best.  For example, the first epoch will generate a file called `model-000.h5`.Models are saved after every epoch so run the latest model when you run the drive.py



