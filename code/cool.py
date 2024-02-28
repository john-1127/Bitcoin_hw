import json

with open('./source.json', 'r') as file:
    data = json.load(file)

final_data = {}

for item in data:
    annotations = item["annotations"]
    video_file = item["file_upload"]
    video_file = video_file.split("-")[-1]  
    final_data[video_file] = []

    for annotation in annotations:
        for result in annotation["result"]:
            values = result["value"]
            sequence = values["sequence"]
            frames = []
            x = []
            y = []
            for se in sequence:
                width = se["width"] / 2
                height = se["height"] / 2
                x_instance = se["x"] + width
                y_instance = se["y"] - height
                frames.append(se["frame"])
                x.append(x_instance)
                y.append(y_instance)
            
            labels = values["labels"]
            action_type = labels[0]
            start_frame = frames[0]
            end_frame = frames[-1]
            down_coordinate = [x[0], y[0]]
            up_coordinate = [x[-1], y[-1]] if len(x) > 1 and len(y) > 1 else down_coordinate

            current_annotation = {
                "start_frame": str(start_frame),
                "end_frame": str(end_frame),
                "action_type": action_type,
                "down_coordinate": down_coordinate,
                "up_coordinate": up_coordinate,
                "type_word": None  
            }

            final_data[video_file].append(current_annotation)

with open('new.json', 'w') as f:
    json.dump(final_data, f, indent=4)
