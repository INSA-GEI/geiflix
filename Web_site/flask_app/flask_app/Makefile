start_process:
	rm ../GPS_parser/cutecom.log
	rm ../GPS_parser/fire_coord.txt
	rm ../GPS_parser/path_coord.txt
	rm ../GPS_parser/degrees_coord.txt
	lxterminal -e "cat /dev/ttyACM0 > ../GPS_parser/cutecom.log"
	python3 parser_gps.py &
	python3 map_for_path.py &
	python3 global.py &
	

