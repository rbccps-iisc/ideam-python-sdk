=======================================================
Python SDK for IoT Data Exchange & Analytics Middleware
=======================================================

Key Features
============

- Supports IoT entities to register, publish, subscribe, access historical data.
- Supports asynchronous access of data from the entity.

Installation
============
    ``$ python3 -m pip install ideam``

**NOTE**: Python2 is not supported.

Getting started
===============
Using this FORM_, you can register yourself with the middleware.

After registering yourself as a provider of the devices/applications with the middleware, you will receive a ``OWNER API KEY``.


Register
--------
To **register** a new entity with the (IDEAM) Middleware, you need a ``UNIQUE device name`` and the ``OWNER API KEY``:

.. code-block:: python

  >>> from ideam.entity import Entity
  >>> deviceHandler = Entity("new-device-name", "OWNER-API-KEY")
  >>> deviceHandler.register()
  {'APIKey': 'DEVICE-API-KEY', 'Subscription Queue Name': 'new-device-name', 'ResourceID': 'new-device-name', 'Registration': 'success'}
  >>> deviceHandler.set_entity_api_key("DEVICE-API-KEY")
  DEVICE-API-KEY

**NOTE**: Store the ``DEVICE-API-KEY`` obtained in the response, in a safe place. This ``DEVICE-API-KEY`` will be required for doing operations like publish, subscribe and accessing historical data.

For an Already Registered Device
--------------------------------
Here, we can skip the registration of the entity with the middleware.

.. code-block:: python

  >>> from ideam.entity import Entity
  >>> deviceHandler = Entity("device-name", "OWNER-API-KEY")
  >>> deviceHandler.set_entity_api_key("DEVICE-API-KEY")


Publish
-------
To **publish** to the (IDEAM) Middleware as an IoT device/entity:



 Args:
            *data*    (string): contents to be published by this entity.

.. code-block:: python

  >>> from ideam.entity import Entity
  >>> deviceHandler = Entity("publishing-device-name", "OWNER-API-KEY")
  >>> deviceHandler.set_entity_api_key("PUBLISHING-DEVICE-API-KEY")
  >>> deviceHandler.publish("demo data")
  {'status': 'success', 'response': 'publish message ok'}


Subscribe
---------

To **listen (subscribe)** to the data from a device/entity registered with the (IDEAM) Middleware, do the following steps:

 **Subscribe**. This method will start listening for the data from middleware. This method will automatically bind or listen to any devices provided in the argument list. When a new data from the device arrives, it is stored in an internal variable called ``subscribe_data``.  The ``subscribe_data`` is a dictionary with ``data`` and ``timestamp`` field. ``timestamp`` denotes the epoch time (in milliseconds) at which data arrived.

 Args:
           *devices_to_bind*  (list of strings): an array of devices to listen to.
                                                 Ex: subscribe(["test100", "testDemo"])

.. code-block:: python

  >>> from ideam.entity import Entity
  >>> applicationHandler = Entity("listening-device-name", "OWNER-API-KEY")
  >>> applicationHandler.set_entity_api_key("LISTENING-DEVICE-API-KEY")
  >>>
  >>> applicationHandler.subscribe(["publishing-device-name", "publishing-device-2"])
  >>> applicationHandler.subscribe_data
  {'data': 'demo data', 'timestamp': '1513526954674'}


Unbind
------
To unbind any entity that is already bound to, use the **unbind** method:

  Args:
      *devices_to_unbind* (list of strings): an array of devices that are to be unbound ( stop listening). Ex. unbind(["test10","testDemo105"])

.. code-block:: python

  >>> from ideam.entity import Entity
  >>> applicationHandler = Entity("listening-device-name", "OWNER-API-KEY")
  >>> applicationHandler.set_entity_api_key("LISTENING-DEVICE-API-KEY")
  >>> applicationHandler.unbind(["publishing-device-name"])
  {'status': 'success', 'response': 'unbind queue ok'}

Access historical data
----------------------
The db function allows an entity to access the historical data.

   Args:
        entity        (string): Name of the device to listen
        query_filters (string): Elastic search response format string. Ex. query_filters="pretty=true&size=10"

.. code-block:: python

  >>> from ideam.entity import Entity
  >>> applicationHandler = Entity("listening-device-name", "OWNER-API-KEY")
  >>> applicationHandler.set_entity_api_key("LISTENING-DEVICE-API-KEY")
  >>> applicationHandler.db("rbccpsEnergy.EM_D0025860")
  '{"took":5,"timed_out":false,"_shards":{"total":5,"successful":5,"failed":0},"hits":{"total":92292,"max_score":1.0487294,"hits":[{"_index":"sensor_data","_type":"logs","_id":"AV6AVeOG7sVBkWsIECvP","_score":1.0487294,"_source":{"@timestamp":"2017-09-14T12:21:06.047Z","data":"{\\"YPhaseReactivePower\\": 2407.9000949859619, \\"BPhaseVoltage\\": 239.428466796875, \\"YPhaseApparentPower\\": 3263.2999420166016, \\"YPhaseActivePower\\": 2202.8000354766846, \\"RPhasePowerFactor\\": 0.78799998760223389, \\"BPhaseActivePower\\": 2222.1999168395996, \\"EnergyReactive\\": 18639.000782012939, \\"BPhaseCurrent\\": 14.46090030670166, \\"RPhaseApparentPower\\": 5156.0001373291016, \\"RPhaseReactivePower\\": 3173.30002784729, \\"YPhasePowerFactor\\": 0.67400002479553223, \\"RPhaseVoltage\\": 234.58619689941406, \\"BPhaseReactivePower\\": 2654.9999713897705, \\"BPhasePowerFactor\\": 0.64099997282028198, \\"RPhaseActivePower\\": 4066.8997764587402, \\"YPhaseCurrent\\": 13.757100105285645, \\"YPhaseVoltage\\": 237.21040344238281, \\"RPhaseCurrent\\": 21.979299545288086, \\"BPhaseApparentPower\\": 3462.3000621795654, \\"dataSamplingInstant\\": 1505138556.0, \\"EnergyActive\\": 20038.0}","@version":"1","routing-key":"rbccpsEnergy.EM_D0025860","key":"rbccpsEnergy.EM_D0025860"}},{"_index":"sensor_data","_type":"logs","_id":"AV6AQ3-E7sVBkWsIECuo","_score":1.0487294,"_source":{"@timestamp":"2017-09-14T12:01:00.796Z","data":"{\\"YPhaseReactivePower\\": 2367.5999641418457, \\"BPhaseVoltage\\": 238.37925720214844, \\"YPhaseApparentPower\\": 3248.5001087188721, \\"YPhaseActivePower\\": 2224.600076675415, \\"RPhasePowerFactor\\": 0.79400002956390381, \\"BPhaseActivePower\\": 2253.4999847412109, \\"EnergyReactive\\": 18635.600391387939, \\"BPhaseCurrent\\": 14.405300140380859, \\"RPhaseApparentPower\\": 5144.4997787475586, \\"RPhaseReactivePower\\": 3123.1000423431396, \\"YPhasePowerFactor\\": 0.68400001525878906, \\"RPhaseVoltage\\": 233.84330749511719, \\"BPhaseReactivePower\\": 2590.8999443054199, \\"BPhasePowerFactor\\": 0.65600001811981201, \\"RPhaseActivePower\\": 4091.1998748779297, \\"YPhaseCurrent\\": 13.756699562072754, \\"YPhaseVoltage\\": 236.14106750488281, \\"RPhaseCurrent\\": 22.0, \\"BPhaseApparentPower\\": 3433.9001178741455, \\"dataSamplingInstant\\": 1505137324.0, \\"EnergyActive\\": 20034.201171875}","@version":"1","routing-key":"rbccpsEnergy.EM_D0025860","key":"rbccpsEnergy.EM_D0025860"}},{"_index":"sensor_data","_type":"logs","_id":"AV6AVBB27sVBkWsIECvK","_score":1.0487294,"_source":{"@timestamp":"2017-09-14T12:19:06.479Z","data":"{\\"YPhaseReactivePower\\": 0.0, \\"BPhaseVoltage\\": 0.0, \\"YPhaseApparentPower\\": 0.0, \\"YPhaseActivePower\\": 0.0, \\"RPhasePowerFactor\\": 0.0, \\"BPhaseActivePower\\": 0.0, \\"EnergyReactive\\": 0.0, \\"BPhaseCurrent\\": 0.0, \\"RPhaseApparentPower\\": 0.0, \\"RPhaseReactivePower\\": 0.0, \\"YPhasePowerFactor\\": 0.0, \\"RPhaseVoltage\\": 0.0, \\"BPhaseReactivePower\\": 0.0, \\"BPhasePowerFactor\\": 0.0, \\"RPhaseActivePower\\": 0.0, \\"YPhaseCurrent\\": 0.0, \\"YPhaseVoltage\\": 0.0, \\"RPhaseCurrent\\": 0.0, \\"BPhaseApparentPower\\": 0.0, \\"dataSamplingInstant\\": 1505138437.0, \\"EnergyActive\\": 0.0}","@version":"1","routing-key":"rbccpsEnergy.EM_D0025860","key":"rbccpsEnergy.EM_D0025860"}}]}}'


.. _FORM: https://docs.google.com/forms/d/e/1FAIpQLSc-L_kMayQjpXsIZ5BU_UCBFI_v6dNPrBcmQIHp0J3kBkfyFQ/viewform?c=0&w=1
