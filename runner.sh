#!/bin/bash
for i in $(seq 1 8)
do 
	./utils/get_circles.py -i Images/Simulated\ sputum\ images\ \(for\ assessment\)/Image\ 1.${i}.JPG  -o Images/task1-circles/Image_1.${i}.JPG
	./utils/get_circles.py -i Images/Simulated\ sputum\ images\ \(for\ assessment\)/Image\ 2.${i}.JPG  -o Images/task1-circles/Image_2.${i}.JPG

	./utils/get_squares.py -i Images/Simulated\ sputum\ images\ \(for\ assessment\)/Image\ 1.${i}.JPG  -o Images/task2-squares/Image_1.${i}.JPG
	./utils/get_squares.py -i Images/Simulated\ sputum\ images\ \(for\ assessment\)/Image\ 2.${i}.JPG  -o Images/task2-squares/Image_2.${i}.JPG
	
	./utils/get_sample_boundaries.py -i Images/Simulated\ sputum\ images\ \(for\ assessment\)/Image\ 1.${i}.JPG  -o Images/task3-boundary/Image_1.${i}.JPG
	./utils/get_sample_boundaries.py -i Images/Simulated\ sputum\ images\ \(for\ assessment\)/Image\ 2.${i}.JPG  -o Images/task3-boundary/Image_2.${i}.JPG
done
