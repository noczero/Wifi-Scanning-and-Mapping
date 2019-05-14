from time import sleep
import datetime
import csv
from access_point_lib import *
from dronekit import connect, VehicleMode, LocationGlobalRelative,LocationGlobal


dt = datetime.datetime.now()
logfile = 'res_csv/result-%s-%s-%s-%s-%s.csv' % (dt.day, dt.month, dt.year, dt.hour, dt.minute)
# csvwrite


def write_tocsv(data) :
    with open(logfile, "a") as output_file:
        writer = csv.writer(output_file, delimiter=',', lineterminator='\r')
        writer.writerow(data)

# reorder data and save it to csv
def data_process(AP_list, latitude, longitude, altitude):
    result = []
    for x in AP_list:
        result.append(x.bssid)
        result.append(x.ssid)
        result.append(x.quality)
        result.append(x.rssi)
        result.append(latitude)
        result.append(longitude)
        result.append(altitude)
        write_tocsv(result)
        result = []

latitude  = None
longitude = None
altitude = None
def location_callback(self, attr_name, value):
    # print "Location (Relative): ", value
    global latitude, longitude, altitude
    latitude = value.lat
    longitude = value.lon
    altitude = value.alt
    print("Vehicle status = lat : %s - lon : %s - alt : %s " % (latitude,longitude,altitude))


def main():
    global latitude,longitude,altitude
    # wifi
    wifi_scanner = get_scanner()
    access_point = wifi_scanner.get_access_points()
    data_process(access_point , latitude, longitude, altitude)
    sleep(1)


# drone
connection = "udp:127.0.0.1:14551" # SITL
#connection = "/dev/ttyCOM1"
print("Connecting to the drone via MAVLINK at %s" % connection)
vehicle = connect(connection, wait_ready=True)
vehicle.wait_ready('autopilot_version')

print("Connection established")
vehicle.add_attribute_listener('location.global_relative_frame', location_callback)

if __name__ == '__main__':
    while True:
        try:
            main()  # start the leap and mqtt
        except KeyboardInterrupt:
            print "Bye"
            sys.exit()

