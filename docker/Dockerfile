# Use OSGeo GDAL ubuntu-full as base - most comprehensive geospatial image available
FROM ghcr.io/osgeo/gdal:ubuntu-full-latest

# Maintainer info
LABEL maintainer="pyGILE Team"
LABEL description="pygile comprehensive geospatial analysis environment"

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CONDA_DIR=/opt/conda
ENV PATH=/opt/conda/bin:$PATH

# Install system dependencies and miniforge in one layer with cleanup
RUN apt-get update && \
    apt-get install -y wget curl git vim build-essential && \
    wget -O miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh && \
    bash miniforge.sh -b -p /opt/conda && \
    rm miniforge.sh && \
    /opt/conda/bin/conda clean -afy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Configure conda
RUN conda config --set channel_priority strict

# Install core Python and scientific stack
RUN mamba install -n base -c conda-forge -y \
    python=3.10 numpy pandas scipy matplotlib \
    && mamba clean -all -y

# Install core geospatial libraries
RUN mamba install -n base -c conda-forge -y \
    gdal geopandas rasterio shapely pyproj fiona \
    && mamba clean -all -y

# Install data format libraries
RUN mamba install -n base -c conda-forge -y \
    xarray netcdf4 h5py zarr \
    && mamba clean -all -y

# Install visualization packages
RUN mamba install -n base -c conda-forge -y \
    plotly bokeh folium contextily \
    && mamba clean -all -y

# Install Jupyter ecosystem
RUN mamba install -n base -c conda-forge -y \
    jupyter jupyterlab ipywidgets \
    && mamba clean -all -y

# Install geospatial analysis tools
RUN mamba install -n base -c conda-forge -y \
    osmnx earthpy \
    && mamba clean -all -y

# Install machine learning
RUN mamba install -n base -c conda-forge -y \
    scikit-learn \
    && mamba clean -all -y

# Install additional packages via pip (your original list without geowombat)
RUN pip install --no-cache-dir \
    earthengine-api streamlit-folium nbconvert black flake8 \
    && pip cache purge

RUN pip install --no-cache-dir \
    sympy jupyter-book geojson pykrige \
    && pip cache purge

RUN pip install --no-cache-dir \
    geoplot sklearn-xarray census \
    && pip cache purge

RUN mamba install -n pygile -c conda-forge -y \
    localtileserver rio-cogeo rioxarray \
    && mamba clean -all -y

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