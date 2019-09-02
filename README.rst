🐦 multi_class_pigeon - Quickly annotate data on Jupyter
========================

This repo is a simple multiclass image extenstion of the pigeon repo by
@agermanidis located [here](https://github.com/agermanidis/pigeon)

The base package does single class annotations for images, text, and regression. 
I frequently find myself working on problems which are multi-class or multi-label.
So I built an additional function to do multi-label image annotation.


Examples
-----

Code: 

.. code-block:: python

    from pigeon import multi_label_annotate
    from IPython.display import display, Image

    annotations = multi_label_annotate(
      ['assets/altera.jpg', 'assets/chibi_gil.jpg','assets/chibi_saber.jpg'],
      options={'cute':['yes','no'], 'saber':['yes','no'],'colors':['blue','gold','white','red']},
      display_fn=lambda filename: display(Image(filename))
    )

Preview:

.. image:: https://imgur.com/GNLyTCI
