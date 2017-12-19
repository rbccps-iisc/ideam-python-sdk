import contextlib
import requests
import warnings
import json
import asyncio
import aiohttp
from time import time
import threading
requests.packages.urllib3.disable_warnings()
from sys import platform


class Entity(object):
    """ The entity object represents any of the IoT entities registered with the RBCCPS IoT Data Exchange & Analytics
    Middleware (IDEAM). It can do publish, subscribe, historical data, bind and unbind operations.
    Details of these operations are specified in the https://rbccps.org/smartcity.

    """
    def __init__(self, entity_id, entity_api_key):
        self.entity_id = entity_id
        self.owner_api_key = entity_api_key
        self.entity_api_key = ""
        self.base_url = "https://smartcity.rbccps.org/"
        self.subscribe_data = {}
        self.event_loop = asyncio.get_event_loop()

    def __del__(self):
        self.stop_subscribe()

    def set_base_url(self, value):
        self.base_url = value
        return self.base_url

    def set_entity_api_key(self, value):
        self.entity_api_key = value
        return self.entity_api_key

    def entity_api_key(self):
        return self.entity_api_key

    def subscribe_data(self):
        return self.subscribe_data

    def register(self):
        """ Registers a new device with the name entity_id. This device has permissions for services like subscribe,
        publish and access historical data.

        """
        register_url = self.base_url + "api/0.1.0/register"
        register_headers = {
            "apikey": str(self.owner_api_key),
            "resourceID": str(self.entity_id),
            "serviceType": "publish,subscribe,historicData"
        }
        with self.no_ssl_verification():
            r = requests.get(register_url, {}, headers=register_headers)
        response = r.content.decode("utf-8")
        if "APIKey" in str(r.content.decode("utf-8")):
            response = json.loads(response[:-331] + "}")  # Temporary fix to a middleware bug, should be removed in future
            response["Registration"] = "success"
        else:
            response = json.loads(response)
            response["Registration"] = "failure"
        return response

    @contextlib.contextmanager
    def no_ssl_verification(self):
        """ Requests module fails due to lets encrypt ssl encryption. Will be fixed in the future release."""
        try:
            from functools import partialmethod
        except ImportError:
            # Python 2 fallback: https://gist.github.com/carymrobbins/8940382
            from functools import partial

            class partialmethod(partial):
                def __get__(self, instance, owner):
                    if instance is None:
                        return self

                    return partial(self.func, instance, *(self.args or ()), **(self.keywords or {}))

        old_request = requests.Session.request
        requests.Session.request = partialmethod(old_request, verify=False)
        warnings.filterwarnings('ignore', 'Unverified HTTPS request')
        yield
        warnings.resetwarnings()
        requests.Session.request = old_request

    def publish(self, data):
        """ This function allows an entity to publish data to the middleware.

        Args:
            data    (string): contents to be published by this entity.
        """
        if self.entity_api_key == "":
            return {'status': 'failure', 'response': 'No API key found in request'}
        publish_url = self.base_url + "api/0.1.0/publish"
        publish_headers = {"apikey": self.entity_api_key}
        publish_data = {
            "exchange": "amq.topic",
            "key": str(self.entity_id),
            "body": str(data)
        }
        with self.no_ssl_verification():
            r = requests.post(publish_url, json.dumps(publish_data), headers=publish_headers)
        response = dict()
        if "No API key" in str(r.content.decode("utf-8")):
            response["status"] = "failure"
            r = json.loads(r.content.decode("utf-8"))['message']
        elif 'publish message ok' in str(r.content.decode("utf-8")):
            response["status"] = "success"
            r = r.content.decode("utf-8")
        else:
            response["status"] = "failure"
            r = r.content.decode("utf-8")
        response["response"] = str(r)
        return response

    def db(self, entity, query_filters="size=10"):
        """ This function allows an entity to access the historic data.

        Args:
            entity        (string): Name of the device to listen to
            query_filters (string): Elastic search response format string
                                    example, "pretty=true&size=10"
        """
        if self.entity_api_key == "":
            return {'status': 'failure', 'response': 'No API key found in request'}

        historic_url = self.base_url + "api/0.1.0/historicData?" + query_filters
        historic_headers = {
            "apikey": self.entity_api_key,
            "Content-Type": "application/json"
        }

        historic_query_data = json.dumps({
            "query": {
                "match": {
                    "key": entity
                }
            }
        })

        with self.no_ssl_verification():
            r = requests.get(historic_url, data=historic_query_data, headers=historic_headers)
        response = dict()
        if "No API key" in str(r.content.decode("utf-8")):
            response["status"] = "failure"
        else:
            r = r.content.decode("utf-8")
            response = r
        return response

    def bind(self, devices_to_bind):
        """ This function allows an entity to list the devices to subscribe for data. This function must be called
        at least once, before doing a subscribe. Subscribe function will listen to devices that are bound here.

        Args:
            devices_to_bind  (list): an array of devices to listen to.
                                     Example bind(["test100","testDemo"])

        """
        if self.entity_api_key == "":
            return {'status': 'failure', 'response': 'No API key found in request'}
        url = self.base_url + "api/0.1.0/subscribe/bind"
        headers = {"apikey": self.entity_api_key}
        data = {
            "exchange": "amq.topic",
            "keys": devices_to_bind,
            "queue": self.entity_id
        }

        with self.no_ssl_verification():
            r = requests.post(url, json=data, headers=headers)
        response = dict()
        if "No API key" in str(r.content.decode("utf-8")):
            response["status"] = "failure"
            r = json.loads(r.content.decode("utf-8"))['message']
        elif 'bind queue ok' in str(r.content.decode("utf-8")):
            response["status"] = "success"
            r = r.content.decode("utf-8")
        else:
            response["status"] = "failure"
            r = r.content.decode("utf-8")
        response["response"] = str(r)
        return response

    def unbind(self, devices_to_unbind):
        """ This function allows an entity to unbound devices that are already bound.

        Args:
            devices_to_unbind (list): an array of devices that are to be unbound ( stop listening)
                                     Example unbind(["test10","testDemo105"])
        """
        if self.entity_api_key == "":
            return {'status': 'failure', 'response': 'No API key found in request'}
        url = self.base_url + "api/0.1.0/subscribe/unbind"
        headers = {"apikey": self.entity_api_key}
        data = {
            "exchange": "amq.topic",
            "keys": devices_to_unbind,
            "queue": self.entity_id
        }

        with self.no_ssl_verification():
            r = requests.delete(url, json=data, headers=headers)
            print(r)
        response = dict()
        if "No API key" in str(r.content.decode("utf-8")):
            response["status"] = "failure"
            r = json.loads(r.content.decode("utf-8"))['message']
        elif 'unbind' in str(r.content.decode("utf-8")):
            response["status"] = "success"
            r = r.content.decode("utf-8")
        else:
            response["status"] = "failure"
            r = r.content.decode("utf-8")
        response["response"] = str(r)
        return response

    def subscribe(self, devices_to_bind=[]):
        """ This function allows an entity to subscribe for data from the devices specified in the bind operation. It
        creates a thread with an event loop to manager the tasks created in start_subscribe_worker.

        Args:
            devices_to_bind (list): an array of devices to listen to
        """
        if self.entity_api_key == "":
            return {'status': 'failure', 'response': 'No API key found in request'}
        self.bind(devices_to_bind)
        loop = asyncio.new_event_loop()
        t1 = threading.Thread(target=self.start_subscribe_worker, args=(loop,))
        t1.daemon = True
        t1.start()


    def start_subscribe_worker(self, loop):
        """ Switch to new event loop as a thread and run until complete. """
        url = self.base_url + "api/0.1.0/subscribe"
        task = loop.create_task(self.asynchronously_get_data(url + "?name={0}".format(self.entity_id)))
        asyncio.set_event_loop(loop)
        loop.run_until_complete(task)
        self.event_loop = loop


    async def asynchronously_get_data(self, url):
        """ Asynchronously get data from Chunked transfer encoding of https://smartcity.rbccps.org/api/0.1.0/subscribe.
        (Only this function requires Python 3. Rest of the functions can be run in python2.

        Args:
             url (string): url to subscribe
        """
        headers = {"apikey": self.entity_api_key}
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                async with session.get(url, headers=headers, timeout=3000) as response:
                    while True:  # loop over for each chunk of data
                        chunk = await response.content.readchunk()
                        if not chunk:
                            break
                        if platform == "linux" or platform == "linux2": # In linux systems, readchunk() returns a tuple
                            chunk = chunk[0]
                        resp = dict()
                        resp["data"] = chunk.decode()
                        current_milli_time = lambda: int(round(time() * 1000))
                        resp["timestamp"] = str(current_milli_time())
                        self.subscribe_data = resp
        except Exception as e:
            print("\n*********    Oops: " + url + " " + str(type(e)) + str(e) + "     *********\n")
        print('\n*********    Closing TCP: {}     *********\n'.format(url))

    def stop_subscribe(self):
        """ This function is used to stop the event loop created when subscribe is called. But this function doesn't
        stop the thread and should be avoided until its completely developed.

        """
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        self.event_loop.stop()
        self.event_loop.close()
