#!/usr/bin/env python

# Scale an image and then set its size so that is 1920 x 1080 in resolution.
#
# To invoke this Plugin from the command line, use a command which is similar to the following;
#
# gimp --no-interface \
#      --verbose \
#      --console-messages \
#      --batch-interpreter="plug-in-script-fu-eval" \
#      --batch '(python-fu-batch-scale-and-set-size-noninterctive RUN-NONINTERACTIVE 1920 1080 3 "/home/foo/fileList.txt")' \
#      --batch "(gimp-quit 1)"
#
# /home/foo/fileList.txt should be a file that contains a list of those files (one per line)
# which should be operated on by the Plugin.
#
# Exmples of locations within which Gimp Plugins can reside;
#
#   - /home/foo/.gimp-2.x/plug-ins
#   - /usr/lib/gimp/2.0/plug-ins


from os     import path
import time
from gimpfu import register, main, pdb, gimp, PF_IMAGE, PF_DRAWABLE, PF_INT, PF_STRING, PF_FILE, INTERPOLATION_NONE, INTERPOLATION_LINEAR, INTERPOLATION_CUBIC, INTERPOLATION_LANCZOS, PF_RADIO

import gtk


def simple_plugin(

  filename_background,
  filename_foreground,
  filename_result
) :

	nameProcedure = "simple_plugin"

	sleep_timer   = 0

	counter       = 1


	print("%s : Enter" % (nameProcedure))

	# ----------------------------------------------------------------------------------------------
	# Get the following from both the background and foreground image files;
	#
	#   - image
	#   - drawable
	# ----------------------------------------------------------------------------------------------

	image_background    = pdb.gimp_file_load(filename_background, filename_background)
	drawable_background = pdb.gimp_image_get_active_layer(image_background)

	image_foreground    = pdb.gimp_file_load(filename_foreground, filename_foreground)
	drawable_foreground = pdb.gimp_image_get_active_layer(image_foreground)

	display_diagnostics(

	  counter,
	  image_background,
	  image_foreground,
	  drawable_background,
	  drawable_foreground
	)

	counter = counter + 1

	gimp.progress_init("Have got image and drawable from both files")
	time.sleep(sleep_timer)

	# ----------------------------------------------------------------------------------------------
	# Start a GIMP Undo group, as this will allow the actions of this Plugin to be undone in one
	# step.
	# ----------------------------------------------------------------------------------------------

	pdb.gimp_image_undo_group_start(image_background)

	# ----------------------------------------------------------------------------------------------
	# Copy the foreground image.
	# ----------------------------------------------------------------------------------------------

	copy_result = pdb.gimp_edit_copy(drawable_foreground)

	print("%s : Copy result = %s" % (nameProcedure, str(copy_result)))

	gimp.progress_init("Have copied foreground image into Buffer")
	time.sleep(sleep_timer)

	# ----------------------------------------------------------------------------------------------
	# Paste the foreground image onto the background image.
	# ----------------------------------------------------------------------------------------------

	use_gimp_edit_paste_as_new = False

	if use_gimp_edit_paste_as_new :

		pdb.gimp_edit_paste(drawable_background, True)

	else :

		image_background_new = pdb.gimp_edit_paste_as_new(drawable_background, True)
	
		if (image_background_new == -1) :
	
			print("%s : Attempted to paste from the Edit buffer, but it appears to be empty." % (nameProcedure))

			exception_message = "\n\nAn Exception has been raised by the method;\n\n  " + \
			                    nameProcedure + \
			                    "\n\nThis method attempted to paste from the Edit buffer, but it appears to be empty.\n\nAs a result, this Plugin is about to terminate!"

			raise Exception(exception_message)

	gimp.progress_init("Have pasted foreground image from Buffer onto background image")
	time.sleep(sleep_timer)

	display_diagnostics(

	  counter,
	  image_background,
	  image_foreground,
	  drawable_background,
	  drawable_foreground
	)

	counter = counter + 1

	# ----------------------------------------------------------------------------------------------
	# Flatten the modified background image down into one layer.
	# ----------------------------------------------------------------------------------------------

	drawable_background = pdb.gimp_image_flatten(image_background)

	gimp.progress_init("Have flattened the background image")
	time.sleep(sleep_timer)

	display_diagnostics(

	  counter,
	  image_background,
	  image_foreground,
	  drawable_background,
	  drawable_foreground
	)

	# ----------------------------------------------------------------------------------------------
	# Save the background image into a specified file.
	# ----------------------------------------------------------------------------------------------

	if use_gimp_edit_paste_as_new :

		pdb.gimp_file_save(

		  image_background,
		  drawable_background,
		  filename_result,
		  filename_result
		)

	else :

		pdb.gimp_file_save(
	
		  image_background_new,
		  drawable_background,
		  filename_result,
		  filename_result
		)

	gimp.progress_init("Have saved the background image")
	time.sleep(sleep_timer)

	# ----------------------------------------------------------------------------------------------
	# End the GIMP Undo group which was started at the beginning of this Plugin.
	# ----------------------------------------------------------------------------------------------

	pdb.gimp_image_undo_group_end(image_background)

	# ----------------------------------------------------------------------------------------------
	# Close the GIMP images now that we have finished with them, otherwise they will use up memory 
	# nnecessarily.
	# ----------------------------------------------------------------------------------------------

	pdb.gimp_image_delete(image_foreground)
	pdb.gimp_image_delete(image_background)

	print("%s : Exit" % (nameProcedure))


def display_diagnostics(

  iteration,
  image_background,
  image_foreground,
  drawable_background,
  drawable_foreground
) :

	nameProcedure = "display_diagnostics"


	message = "Invocation number = " + \
	          str(iteration) + \
	          "\n\n" + \
	          "Filename background image :\n\n" + \
	          image_background.filename + \
	          "\n\n" + \
	          "Background image width = " + \
	          str(image_background.width) + \
	          "\n" + \
	          "Background image height = " + \
	          str(image_background.height) + \
	          "\n" + \
	          "Background drawable width = " + \
	          str(drawable_background.width) + \
	          "\n" + \
	          "Background drawable height = " + \
	          str(drawable_background.height) + \
	          "\n\n" + \
			  "Filename foreground image :\n\n" + \
	          image_foreground.filename + \
	          "\n\n" + \
	          "Foreground image width = " + \
	          str(image_foreground.width) + \
	          "\n" + \
	          "Foreground image height = " + \
	          str(image_foreground.height) + \
	          "\n" + \
	          "Foreground drawable width = " + \
	          str(drawable_foreground.width) + \
	          "\n" + \
	          "Foreground drawable height = " + \
	          str(drawable_foreground.height) + \
	          "\n"
			  
	message = ""

	dialog = gtk.MessageDialog(
	                           None,
	                           0,
	                           gtk.MESSAGE_INFO,
	                           gtk.BUTTONS_OK,
	                           None
	                          )
	dialog.set_title("GIMP Plugin Dialog")
	# dialog.set_size_request(800, 800)
	dialog.set_resizable(True)

	labelFilenameBackground = gtk.Label()
	labelFilenameBackground.set_text("Filename background image :")

	filenameBackground = gtk.Entry()
	filenameBackground.set_text(image_background.filename)

	labelFilenameForeground = gtk.Label()
	labelFilenameForeground.set_text("Filename foreground image :")

	filenameForeground = gtk.Entry()
	filenameForeground.set_text(image_foreground.filename)

	labelDimensionsImageBackground = gtk.Label()
	labelDimensionsImageBackground.set_text("Dimensions of Background Image :")

	dimensionsImageBackground = gtk.Entry()
	dimensionsImageBackground.set_text(str(image_background.width) + " x " + str(image_background.height))

	labelDimensionsDrawableBackground = gtk.Label()
	labelDimensionsDrawableBackground.set_text("Dimensions of Background Drawable :")

	dimensionsDrawableBackground = gtk.Entry()
	dimensionsDrawableBackground.set_text(str(drawable_background.width) + " x " + str(drawable_background.height))

	labelDimensionsImageForeground = gtk.Label()
	labelDimensionsImageForeground.set_text("Dimensions of Foreground Image :")

	dimensionsImageForeground = gtk.Entry()
	dimensionsImageForeground.set_text(str(image_foreground.width) + " x " + str(image_foreground.height))

	labelDimensionsDrawableForeground = gtk.Label()
	labelDimensionsDrawableForeground.set_text("Dimensions of Foreground Drawable :")

	dimensionsDrawableForeground = gtk.Entry()
	dimensionsDrawableForeground.set_text(str(drawable_foreground.width) + " x " + str(drawable_foreground.height))

	labelDimensionsDialog = gtk.Label()
	labelDimensionsDialog.set_text("Dimensions of this Dialog Window :")

	dimensionsDialog = gtk.Entry()

	dialog.vbox.add(labelFilenameBackground)
	dialog.vbox.add(filenameBackground)
	dialog.vbox.add(labelDimensionsImageBackground)
	dialog.vbox.add(dimensionsImageBackground)
	dialog.vbox.add(labelDimensionsDrawableBackground)
	dialog.vbox.add(dimensionsDrawableBackground)
	dialog.vbox.add(labelFilenameForeground)
	dialog.vbox.add(filenameForeground)
	dialog.vbox.add(labelDimensionsImageForeground)
	dialog.vbox.add(dimensionsImageForeground)
	dialog.vbox.add(labelDimensionsDrawableForeground)
	dialog.vbox.add(dimensionsDrawableForeground)
	dialog.vbox.add(labelDimensionsDialog)
	dialog.vbox.add(dimensionsDialog)

	dialog.show_all()
	
	textDimensionsDialog = str(dialog.allocation.width) + " x " + str(dialog.allocation.height)

	dimensionsDialog.set_text(textDimensionsDialog)

	print("Dimensions of this Dialog Window = %s" % (textDimensionsDialog))
	
	dialog.run()

	dialog.destroy()

	print("--------------------------------------------------------------------------------")
	print("(%d)" % (iteration))
	print("--------------------------------------------------------------------------------")

	print("Filename background image      = %s" % image_background.filename)
	print("Width    background image      = %s" % image_background.width)
	print("Height   background image      = %s" % image_background.height)
	print("Width    background drawable   = %s" % drawable_background.width)
	print("Height   background drawable   = %s" % drawable_background.height)

	print("Filename foreground image      = %s" % image_foreground.filename)
	print("Width    foreground image      = %s" % image_foreground.width)
	print("Height   foreground image      = %s" % image_foreground.height)
	print("Width    foreground drawable   = %s" % drawable_foreground.width)
	print("Height   foreground drawable   = %s" % drawable_foreground.height)

	print("Background image num of layers = %d" % len(pdb.gimp_image_get_layers(image_background)))
	print("Foreground image num of layers = %d" % len(pdb.gimp_image_get_layers(image_foreground)))


register(
	"simple_plugin",                                        # The name of the command.
	"Overlay a foreground image onto a background image.",  # A brief description of the command.
	"Overlay a foreground image onto a background image.",  # Help message.
	"Craig Sanders",                                        # Author.
	"Craig Sanders",                                        # Copyright holder.
	"2019",                                                 # Date.
	"Overlay one image onto another",                       # The way the script will be referred to in the menu.
	# "RGB*, GRAY*",                                        # Image mode
	"",                                                     # Create a new image, don't work on an existing one.
	[
		(PF_FILE,       "filename_background",        "Filename of background image",     "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png"),
		(PF_FILE,       "filename_foreground",        "Filename of foreground image",     "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/frames/png/animation_1/Eulers_formula_000100.png"),
		(PF_STRING,     "filename_result",            "Filename of resulting image",      "/home/craig/temp/image_result.png")
	],
	[],
	simple_plugin,
	menu="<Image>/Image/Craig's Utilities/")


class ImageOverlayAgent :

	#> Documentation for a class.
	#- ================================================================================
	#- Class : ImageOverlayAgent
	#-
	#- This class is responsible for overlaying a foreground image onto a background 
	#- image, with the resulting image being saved into the Foreground image file. This
	#- process can be repeated for as many foreground image files as are passed to an
	#- object of this class.
	#<
	

	nameClass               = "ImageOverlayAgent"

	# Lists of strings of filenames.

	filenameBackground      = None
	listFilenamesForeground = []

	imageBackground         = ""
	imageForeground         = ""
	imageNew                = ""

	drawableBackground      = ""
	drawableForeground      = ""
	drawableNew             = ""


	def __init__(

	  self,
	  filenameBackground,
	  filenamesForeground
	) :

		nameMethod = self.nameClass + "::__init__"


		print("%s : Enter" % (nameMethod))

		print("%s : filenameBackground  = %s" % (nameMethod, filenameBackground))
		print("%s : filenamesForeground = %s" % (nameMethod, filenamesForeground))

		self.filenameBackground = filenameBackground
		self.listFilenamesForeground = filenamesForeground

		print("%s : Exit" % (nameMethod))


	def run(

	  self
	) :

		nameMethod = self.nameClass + "::run"


		print("%s : Enter" % (nameMethod))

		print("%s : Number of foreground image files = %d" % (nameMethod, len(self.listFilenamesForeground)))

		self.checkLists()

		self.processList()

		print("%s : Exit" % (nameMethod))


	#> Documentation for a method.
	#- ================================================================================
	#- Method : ImageOverlayAgent::checkLists
	#-
	#- Check that;
	#-
	#-   - a Background image file has been specified, and
	#-
	#-   - one or more Foreground image files have been specified
	#<

	def checkLists(

	  self
	) :

		nameMethod = self.nameClass + "::checkLists"


		print("%s : Enter" % (nameMethod))



		print("%s : Number of elements in list = %d" % (nameMethod, len(self.listFilenamesForeground)))

		if self.filenameBackground == None :

			gimp.message("A) You must specify a background image file.")

		elif (
		      (len(self.listFilenamesForeground) == 0) or
		      (
		        (len(self.listFilenamesForeground) == 1) and
		        (self.listfilenamesForeground      == '')
		      )
		     ) :

			gimp.message("B) You must specify at least one foreground image file.")

			print("%s : Number of foreground image files = 0") % (nameMethod)

		else :

			self.checkFiles()

		print("%s : Exit" % (nameMethod))


	#> Documentation for a method.
	#- ================================================================================
	#- Method : ImageOverlayAgent::checkFiles
	#-
	#- Check that;
	#-
	#-   - 
	#<

	def checkFiles(

	  self
	) :

		nameMethod = self.nameClass + "::checkFiles"


		print("%s : Enter" % (nameMethod))

		if not path.isfile(self.filenameBackground) :

			print("%s : The following doesn't appear to be a file : %s"    % (nameMethod, self.filenameBackground))

			gimp.message("Hello!!!")

			raise Exception("Plugin is about to terminate!!!")

		for filenameForeground in self.listFilenamesForeground : 

			if (not path.isfile(filenameForeground)) :

				print("%s : The following doesn't appear to be a file : %s"    % (nameMethod, filenameForeground))

				raise Exception("Plugin is about to terminate!!!")			

		print("%s : Exit" % (nameMethod))


	def overlayImage(

	  self
	) :

		nameMethod = self.nameClass + "::overlayImage"

		imageBackground_new = None
		imageForeground_new = None

		drawableBackground_new = None
		drawableForeground_new = None

		print("%s : Enter" % (nameMethod))

		copyResult = pdb.gimp_edit_copy(self.drawableForeground)

		print("%s : Copy result = %s" % (nameMethod, str(copyResult)))

		# pdb.gimp_drawable_update(drawable, horizontalLocation, verticalLocation, 384, 216)

		# The following operation should paste the image which is in the buffer, into a new layer of the
		# background image.

		gimp.progress_init("Overlaying one image onto another")

		if (True) :

			pdb.gimp_edit_paste(self.drawableBackground, True)

			# imageBackground_new = self.imageBackground

		else :

			imageBackground_new = pdb.gimp_edit_paste_as_new(self.drawableBackground, True)

			if (imageBackground_new == -1) :

				print("%s : Attempted to paste from the Edit buffer, but it appears to be empty."    % (nameMethod))

				raise Exception("\n\nAn Exception has been raised by the method;\n\n  " + nameMethod + "\n\nThis method attempted to paste from the Edit buffer, but it appears to be empty.\n\nAs a result, this Plugin is about to terminate!")

		# self.drawableNew = pdb.gimp_image_get_active_layer(self.imageNew)
		
		# Flatten the modified background image down into one layer.
		
		drawableBackground_new = pdb.gimp_image_flatten(self.imageBackground)

		# self.drawableBackground = drawableBackground_new
		
		# Copy and paste the background image into the foreground image.
		
		copyResult = pdb.gimp_edit_copy(drawableBackground_new)

		pdb.gimp_edit_paste(self.drawableForeground, True)

		self.drawableForeground = pdb.gimp_image_flatten(self.imageForeground)

		# self.imageForeground = imageForeground_new 


	def processList(

	  self
	) :
	
		nameMethod = self.nameClass + "::run"


		print("%s : Enter" % (nameMethod))

		# Start a GIMP Undo group, as this will allow the actions of this Plugin to be undone in one step.

		# pdb.gimp_undo_push_group_start(image)

		indexList = 0

		for filenameForeground in self.listFilenamesForeground :

			indexList = indexList + 1

			# self.checkFiles(filename, filenameOverlay)

			self.imageBackground    = pdb.gimp_file_load(self.filenameBackground, self.filenameBackground)
			self.drawableBackground = pdb.gimp_image_get_active_layer(self.imageBackground)

			self.imageForeground    = pdb.gimp_file_load(filenameForeground, filenameForeground)
			self.drawableForeground = pdb.gimp_image_get_active_layer(self.imageForeground)

			print("%s : Processing ..."          % (nameMethod))
			print("%s :   Background image = %s" % (nameMethod, self.filenameBackground))
			print("%s :   Overlay    image = %s" % (nameMethod, filenameForeground))

			# Display information about both of the current images.

			self.displayImageData()

			# How many layers does the current image now contain?
			#
			# Use gimp-edit-copy and gimp-edit-paste?

			self.overlayImage()

			# Move the 

			# pdb.gimp_drawable_update()

			# self.drawableNew = pdb.gimp_image_flatten(self.imageNew)

			pdb.gimp_file_save(

			  self.imageForeground,
			  self.drawableForeground,
			  filenameForeground,
			  filenameForeground
			)

			# Close the images now that we have finished with it, otherwise they will use up memory unnecessarily.

			pdb.gimp_image_delete(self.imageForeground)
			pdb.gimp_image_delete(self.imageBackground)

			# End of for loop.

		# End the GIMP Undo group.

		# pdb.gimp_undo_push_group_end(image)

		print("%s : Enter" % (nameMethod))


	def displayImageData(

	  self
	) :

		nameMethod = self.nameClass + "::displayImageData"


		print("%s : Enter" % (nameMethod))

		print("Filename background image    = %s" % self.imageBackground.filename)
		print("Width    background image    = %s" % self.imageBackground.width)
		print("Height   background image    = %s" % self.imageBackground.height)
		print("Width    background drawable = %s" % self.drawableBackground.width)
		print("Height   background drawable = %s" % self.drawableBackground.height)

		print("Filename foreground image    = %s" % self.imageForeground.filename)
		print("Width    foreground image    = %s" % self.imageForeground.width)
		print("Height   foreground image    = %s" % self.imageForeground.height)
		print("Width    foreground drawable = %s" % self.drawableForeground.width)
		print("Height   foreground drawable = %s" % self.drawableForeground.height)

		print("%s : Exit" % (nameMethod))


main()
