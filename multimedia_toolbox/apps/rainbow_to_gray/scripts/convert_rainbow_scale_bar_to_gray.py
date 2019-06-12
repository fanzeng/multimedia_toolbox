# This version does not require opencv

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--in_image_file', help='path to input image file', required=True)
	parser.add_argument('--out_path', help='output path', required=True)
	parser.add_argument('--rainbow_position', help='position of the scale bar', required=True)
	parser.add_argument('--dark_end', help='position of the leftmost pixel of the scale bar', required=True)
	parser.add_argument('--bright_end', help='position of the leftmost pixel of the scale bar', required=True)
	parser.add_argument('-is_vertical', help='whether the rainbow color bar is vertical', action='store_true')

	args = parser.parse_args()
	in_image_file = args.in_image_file
	out_path = args.out_path
	dark_end = int(args.dark_end)
	bright_end = int(args.bright_end)
	rainbow_position = int(args.rainbow_position)
	
	is_vertical = False
	if args.is_vertical:
		is_vertical = True

	original = plt.imread(in_image_file)
	converted = np.ndarray(original.shape[:2])

	hsv = matplotlib.colors.rgb_to_hsv(original[:,:,:3])
	hsv = (hsv*255).astype(int)

	gray_value = 0 
	gray_value_increment = 255.0 / (bright_end - dark_end + 1)
	d_colour_to_gray = {}

	for colour_position in range(dark_end, bright_end):
		if is_vertical:
			colour = hsv[colour_position, rainbow_position]
		else:
			colour = hsv[rainbow_position, colour_position]
		# print colour
		if sum(colour) == 0:
			continue
		colour_hash_str = '{:03d}'.format(colour[0]) + '{:03d}'.format(colour[1]) + '{:03d}'.format(colour[2])
		d_colour_to_gray[colour_hash_str] = gray_value
		gray_value += gray_value_increment


	for y in range(hsv.shape[0]):
		for x in range(hsv.shape[1]):
			colour = hsv[y, x]
			colour[1] = 255
			original_color = original[y, x]
			if sum(original_color) == 255*3: # or sum(original_color) == 0:
				continue

			if sum(original_color) == 0:
				colour = np.array([60, 255, 255])
			# print y, x, colour
			found = False
			step = 0

			while(found is False and step < 2):
				# for component_id, component in enumerate(colour):
				component_id = 0
				component = colour[component_id]
				adj_colour = colour.copy()
				if component + step >= 0 and component + step <= 255:
					adj_colour[component_id] = component + step
				colour_hash_str = '{:03d}'.format(adj_colour[0]) + '{:03d}'.format(adj_colour[1]) + '{:03d}'.format(adj_colour[2])
				gray_value = d_colour_to_gray.get(colour_hash_str)

				if gray_value is not None:
					converted[y, x] = int(gray_value)
					found = True
					# print gray_value
				if not found:
					if step == 0:
						step = 1
					else:
						step *= -1
						if step > 0:
							step += 1

	out_image_file = out_path + '/converted.png'
	plt.imsave(out_image_file, converted, cmap='binary_r')
