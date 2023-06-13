import time
from google.transit import gtfs_realtime_pb2 
tiempoActual = int(time.time()) 

def create_gtfs_realtime_feed(trip_updates):

    feed_message = gtfs_realtime_pb2.FeedMessage()
    feed_header = feed_message.header
    feed_header.gtfs_realtime_version = "1.0"
    feed_header.incrementality = gtfs_realtime_pb2.FeedHeader.FULL_DATASET
    feed_header.timestamp = int(time.time()) 

    for trip_update in trip_updates:
        entity = feed_message.entity.add()
        entity.id = str(tiempoActual)
        trip_update_proto = entity.trip_update 

        trip = trip_update_proto.trip
        trip.trip_id = trip_update['trip_id']
        trip.start_date = trip_update['start_date']
        trip.schedule_relationship = gtfs_realtime_pb2.TripDescriptor.SCHEDULED 

        for stop_time_update in trip_update['stop_time_updates']:

            stop_time_update_proto = trip_update_proto.stop_time_update.add()
            stop_time_update_proto.stop_sequence = stop_time_update['stop_sequence']

            arrival = stop_time_update_proto.arrival
            arrival.time = stop_time_update['arrival_time'] 

            departure = stop_time_update_proto.departure
            departure.time = stop_time_update['departure_time'] 

            stop_time_update_proto.stop_id = stop_time_update['stop_id']

    return feed_message

trip_updates = [
    {
        'trip_id': '22242ILB_24202_5',
        'start_date': '20230613',
        'stop_time_updates': [
            {
                'stop_sequence': 8,
                'arrival_time': (tiempoActual + 1200),
                'departure_time': (tiempoActual + 1200),
                'stop_id': '78081'
            }
        ],
    },
]
 
feed_message = create_gtfs_realtime_feed(trip_updates) 

with open('trip_up.pb', 'wb') as f:
    f.write(feed_message.SerializeToString())

print(f"Finalizado correctamente con un Timestamp de: {tiempoActual}")

