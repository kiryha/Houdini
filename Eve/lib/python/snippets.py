data ={
	"0":{
		"floor_coordinate":12,
		"floor_height":1,
		"floor_index":0,
		"floor_scale":1,
		"level_index":"0"
	},
	"1":{
		"floor_coordinate":13,
		"floor_height":3,
		"floor_index":1,
		"floor_scale":1,
		"level_index":"1"
	},
	"2":{
		"floor_coordinate":16,
		"floor_height":3,
		"floor_index":2,
		"floor_scale":1,
		"level_index":"1"
	},
	"3":{
		"floor_coordinate":19,
		"floor_height":1,
		"floor_index":3,
		"floor_scale":1,
		"level_index":"2"
	}
}


# sort dictionary by keys
data = dict(sorted(data.items(), key=lambda item: item[0]))  # sort by floor number
floor_coordinates = [data[key]["floor_coordinate"] for key in data]

print(floor_coordinates)

