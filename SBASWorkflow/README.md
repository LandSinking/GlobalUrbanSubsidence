# SBASWorkflow: steps for InSAR time series analysis
# 
This is an example from Houston that demonstrates SBAS InSAR processing for monitoring global urban subsidence, utilizing [ASF's HYP3 cloud computing platform](https://search.asf.alaska.edu/) and [MintPy package](https://github.com/insarlab/MintPy).

The Houston configuration file at `config/USA_357_Houston.py` records key parameters for data preprocessing and InSAR time-series analysis, including 

- Base image, date and frame ranges for searching SBAS stacks
- ASF account and password for submitting InSAR jobs to ASF's HYP3 cloud computing platform
- Study area extent for image clipping
- Reference point coordinates and the coherence threshold for MintPy analysis.

**For detailed information on the InSAR processing parameters used for 465 global major cities, see Table S1 (Supplementary Materials) of our manuscript.**

**Our monitoring results, including the land subsidence velocities, InSAR coherence, the standard deviation of velocities, and geographic locations of reference points for all 465 cities in this study can be visualized at [GUS portal](https://ee-pkurelab.projects.earthengine.app/view/gus).**

The entire procedure of InSAR time series analysis can be executed following the workflow below:

1. edit the ASFUsr and ASFPwd in `config/USA_357_Houston.py`, and run `procSearchAndModifyPairs.py` to search Sentinel-1 stack (according to the base image and date ranges in config file), filter the searched image pairs (according to the frame ranges in config file) and edit the SBAS network via a simple GUI：
```
cd ./code
python procSearchAndModifyPairs.py -c ../config/USA_357_Houston.py
```

  The code provides `-t` option to set the temporal baseline, and its default value is set to 36 days. 

  In the editing GUI, the X and Y axes represent date and spatial baseline, respectively. Images are displayed as nodes, and pairs as lines connecting them.
  - To Add a Pair: Click the "Add pairs" button, then select two nodes. A line will be drawn between them, creating a new pair.

  - To Remove a Pair: Click the "Remove pairs" button, select a line, and press the "Delete" key on your keyboard. The line will be removed, deleting that pair.

  *Note: Basic navigation tools (Reset, Pan, Zoom, etc.) in the lower-left corner are only accessible when the "Remove pairs" mode is active.*

2. run `procHYP3.py` with `-s` option to submit jobs to ASF. Details for available options can be found in the source code.
<pre><code>python procHYP3.py -c ../config/USA_357_Houston.py -s</code></pre>
3. After the jobs are finished, run `procHYP3.py` with `-d` option to get the links for downloading the interferogram products. 
<pre><code>python procHYP3.py -c ../config/USA_357_Houston.py -d</code></pre>
4. Download the interferogram products to the folder `S1AAdata/USA_357_Houston`, and then run `procPrepData.py` to unzip, clip and prepare the datasets
<pre><code>python procPrepData.py -c ../config/USA_357_Houston.py</code></pre> 
5. As advised by the ASF's HyP3 platform — ***Always doubt your interferogram first!*** — users must carefully inspect the quality of each interferogram to ensure the reliability of InSAR-derived results. 
6. run `procSBAS.py` to start the first round of MintPy time series analysis
<pre><code>python procSBAS.py -c ../config/USA_357_Houston.py</code></pre> 
7. Result files can be found in folder `./workplace_USA_357_Houston/Mintpy`
8. Identify a new reference point where the subsiding velocity is close to the mode, typically on a man-made structure; and then update the `reference_yx` variable in the config file with the new reference point's Y and X coordinates in the result file. Afterwards, run second round of Mintpy time series analysis with the new reference point:
<pre><code>python procSBAS.py -c ../config/USA_357_Houston.py</code></pre> 
9. Result files can be found in folder `./workplace_USA_357_Houston/Mintpy`
