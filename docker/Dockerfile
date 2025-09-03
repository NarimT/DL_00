# Use OSGeo GDAL ubuntu-full as base - most comprehensive geospatial image available
FROM ghcr.io/osgeo/gdal:ubuntu-full-latest

# Maintainer info
LABEL maintainer="pyGILE Team"
LABEL description="pygile comprehensive geospatial analysis environment with working matplotlib plotting"

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CONDA_DIR=/opt/conda
ENV PATH=/opt/conda/bin:$PATH
ENV MAMBA_NO_BANNER=1
ENV CONDA_ALWAYS_YES=1
ENV CONDA_SOLVER=libmamba

# Install system dependencies and miniforge in one layer with cleanup
RUN apt-get update && \
    apt-get install -y wget curl git vim build-essential && \
    wget -O miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh && \
    bash miniforge.sh -b -p /opt/conda && \
    rm miniforge.sh && \
    /opt/conda/bin/conda clean -afy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Configure conda channels globally
RUN conda config --set channel_priority strict && \
    conda config --add channels conda-forge

# Create pygile environment (matching batch file)
RUN mamba create -n pygile --override-channels -c conda-forge python=3.10 -y && \
    mamba clean -all -y

# Configure channels for pygile environment
RUN mamba run -n pygile conda config --env --add channels conda-forge && \
    mamba run -n pygile conda config --env --set channel_priority strict

# BATCH 1: Foundation Stack - NumPy + Core Scientific Libraries
RUN mamba install -n pygile --override-channels -c conda-forge -y \
    numpy pandas scipy matplotlib scikit-learn \
    && mamba clean -all -y

# BATCH 2: System Geospatial Libraries + Core Bindings  
RUN mamba install -n pygile --override-channels -c conda-forge -y \
    gdal proj geos libspatialindex fiona shapely pyproj geopandas \
    && mamba clean -all -y

# BATCH 3: Raster Processing + Data Formats + Parallel Computing
RUN mamba install -n pygile --override-channels -c conda-forge -y \
    rasterio xarray rioxarray dask dask-geopandas netcdf4 h5py zarr tifffile \
    && mamba clean -all -y

# BATCH 4: Jupyter + Visualization + Interactive Tools + Node.js + matplotlib integration
RUN mamba install -n pygile --override-channels -c conda-forge -y \
    jupyter jupyterlab ipywidgets plotly folium contextily mapclassify ipympl nodejs \
    && mamba clean -all -y

# Build Jupyter Lab extensions for matplotlib plotting
RUN mamba run -n pygile jupyter lab build --dev-build=False --minimize=False && \
    mamba clean -all -y

# BATCH 5: Specialized Geospatial Analysis + Network Tools
RUN mamba install -n pygile --override-channels -c conda-forge -y \
    osmnx rasterstats xarray-spatial \
    && mamba clean -all -y

# Install cloud access tools (fallback to pip if conda fails)
RUN mamba install -n pygile --override-channels -c conda-forge -y \
    pystac stackstac planetary-computer || \
    mamba run -n pygile pip install --no-cache-dir pystac stackstac planetary-computer

# Install advanced mapping tools  
RUN mamba install -n pygile --override-channels -c conda-forge -y \
    geemap palettable \
    && mamba clean -all -y

# BATCH 6: Additional Tools + Development + Documentation (via pip like batch file)
RUN mamba run -n pygile pip install --no-cache-dir \
    earthengine-api census us sklearn-xarray pygis \
    black flake8 jupyter-book nbconvert \
    pykrige geojson \
    && pip cache purge

# Additional tools present in original docker but not in batch (keeping for compatibility)
RUN mamba run -n pygile pip install --no-cache-dir \
    earthpy streamlit-folium geoplot localtileserver rio-cogeo \
    && pip cache purge

# Verify installation (matching batch file verification)
RUN mamba run -n pygile python -c "import numpy, pandas, geopandas, rasterio, xarray, matplotlib; print('Core geospatial stack verification: SUCCESS'); print(f'NumPy: {numpy.__version__}'); print(f'GeoPandas: {geopandas.__version__}'); print(f'Rasterio: {rasterio.__version__}')"

# Test matplotlib plotting capability
RUN mamba run -n pygile python -c "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; plt.plot([1,2,3], [1,4,2]); plt.savefig('/tmp/test_plot.png'); print('Matplotlib plotting: SUCCESS')" && \
    rm -f /tmp/test_plot.png

# Activate pygile environment by default
RUN echo "conda activate pygile" >> ~/.bashrc
ENV CONDA_DEFAULT_ENV=pygile

# Copy entrypoint script and fix line endings
COPY entrypoint.sh /usr/local/bin/
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

# Create working directory
WORKDIR /workspace

# Expose Jupyter port
EXPOSE 8888

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]