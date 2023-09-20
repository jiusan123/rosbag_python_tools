import rosbag
def extract_topic_data(bag_file, topic_name, file_object):
    bag = rosbag.Bag(bag_file)

    for topic, msg, t in bag.read_messages(topics=[topic_name]):
	
	for event in msg.events:
	    Ostr = ''
            x = str(event.x)
	    y = str(event.y)
            secs = str(event.ts.secs)
	    nsecs = str(event.ts.nsecs)
	    polarity = str(event.polarity)
            time = str(t.to_sec())
            Ostr = Ostr + time + ' ' + secs + ' ' + nsecs + ' ' + x + ' ' + y + ' ' + polarity + '\n'
	    file_object.writelines(Ostr)

    file_object.close()
    bag.close()


bag_file = "/home/helena/Data/rpg/rpg_boxes_edited.bag"
topic_name = "/davis/left/events"
file_object = open('events_timestamp1.txt','w')
extract_topic_data(bag_file, topic_name, file_object)
