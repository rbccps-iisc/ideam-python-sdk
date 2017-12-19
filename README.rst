===================================
Python SDK for Smart City framework
===================================

Key Features
============

- Supports IoT entities to do publish, subscribe, access historical data.
- Supports asynchronously get data from the entity.

Getting started
===============

Publish
-------
To **publish** to the RBCCPS smart-city middleware as an IoT device/entity:


.. code-block:: python

  >>> from smartcity_middleware import Entity
  >>> DeviceA = Entity("publishing-device-name", "publishing-device-api-key")
  >>> DeviceA.publish("demo data")
  {'status': 'success', 'response': 'publish message ok'}
  >>>

Subscribe
---------

To **listen (subscribe)** to the data from a device/entity registered with RBCCPS smart-city middleware, do the following steps:

1. **Bind**. This method will tell middleware which devices to listen to.
    For more details on bind method, go to http://rbccps.org/smartcity/doku.php#subscriber-bind_api

.. code-block:: python

  >>> from smartcity_middleware import Entity
  >>> DeviceB = Entity("listening-device-name", "listening-device-api-key")
  >>> DeviceB.bind(["publishing-device-name","testDemo"])
  {'status': 'success', 'response': 'bind queue ok'}

2. **Subscribe**. This method will start listening for the data from middleware. When a new data arrives, it is stored in an internal variable called "subscribe_data". The subscribe_data is a dictionary with "*data*" field and "*timestamp*". *Timestamp* denotes the epoch time (in milliseconds) at which data arrived.

.. code-block:: python

  >>> from smartcity_middleware import Entity
  >>> DeviceC = Entity("listening-device-name", "listening-device-api-key")
  >>> DeviceC.subscribe()
  >>> DeviceC.subscribe_data
  {'data': 'demo data', 'timestamp': '1513526954674'}

Unbind
------
To unbind any entity that is already bound to, use the **unbind** method:

.. code-block:: python

  >>> from smartcity_middleware import Entity
  >>> DeviceB = Entity("listening-device-name", "listening-device-api-key")
  >>> DeviceB.unbind(["testDemo"])
  {'status': 'success', 'response': 'unbind queue ok'}

Access historical data
----------------------

.. code-block:: python

  >>> from smartcity_middleware import Entity
  >>> DeviceB = Entity("listening-device-name", "listening-device-api-key")
  >>> DeviceB.historic_data()
