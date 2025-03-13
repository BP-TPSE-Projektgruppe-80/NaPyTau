# Marker Factory

## Overview

This module contains methods for generating error markers for `matplotlib`.

## Methods

### `generate_error_marker_path(error_amount: float) -> Path`

Generates error marker paths to be used by the Graph Component to represent error magnitudes

#### Parameters:
- `error_amount` *(float)*: The magnitude of the error, which determines the size of the marker.

#### Returns:
- `Path`: A matplotlib `Path` object that provides the general shape of the error marker.


